import argparse
import importlib
import importlib.metadata
import os
import sys
from dataclasses import dataclass

from pyquantumkit import Framework_Namespace, PyQuantumKitError, Supported_Frameworks
from pyquantumkit.procedure.circuit_io import CircuitIO
from pyquantumkit.procedure.generic import new_circuit, new_mixed_circuit, run_and_get_counts
from pyquantumkit.translate.framework_map import framework_interpret_protocol


class RunError(PyQuantumKitError):
    pass


@dataclass
class RunResult:
    counts: dict[str, int]
    provider: str
    backend: str
    task_id: str = None
    protocol: str = 'r'
    interpreted: list = None


def _argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='PyQuantumKit quantum circuit execution options.',
        allow_abbrev=False,
    )
    parser.add_argument('-provider', '--provider', default='qiskit',
                        help='execution provider: qiskit, originq, or quafu (default: qiskit)')
    parser.add_argument('-backend', '--backend', default=None,
                        help='local simulator or cloud device name; cloud names are validated by the provider API')
    parser.add_argument('-shots', '--shots', type=int, default=1024,
                        help='number of measurement repetitions (default: 1024)')
    parser.add_argument('-api-key-file', '--api-key-file', default=None,
                        help='read the cloud API key from this file when PK_API_KEY is not set')
    return parser


def _cli_options() -> argparse.Namespace:
    args, _ = _argument_parser().parse_known_args(sys.argv[1:])
    return args


def _load_framework(framework: str) -> None:
    for module_name in Supported_Frameworks[framework]:
        if module_name not in Framework_Namespace[framework]:
            try:
                Framework_Namespace[framework][module_name] = importlib.import_module(module_name)
            except ImportError as exc:
                raise RunError(
                    f"Provider requires Python module '{module_name}'. "
                    f"Install the corresponding PyQuantumKit optional dependency."
                ) from exc


def _convert_circuit(circuit: CircuitIO, framework: str, subsdict: dict = None):
    if not circuit.check_nqbits():
        raise RunError('The circuit uses more qubits than declared.')
    if not circuit.check_ncbits():
        raise RunError('The circuit uses more classical bits than declared.')
    _load_framework(framework)
    if circuit.get_ncbits() > 0:
        converted = new_mixed_circuit(framework, circuit.get_nqbits(), circuit.get_ncbits())
    else:
        converted = new_circuit(framework, circuit.get_nqbits())
    circuit.append_into_actual_circuit(converted, subsdict)
    return converted


def _normalize_counts(values: dict, ncbits: int, probabilities: bool = False,
                      shots: int = None) -> dict[str, int]:
    counts = {}
    for raw_bit, raw_count in values.items():
        if isinstance(raw_bit, int):
            bit = format(raw_bit, f'0{ncbits}b')
        else:
            bit = str(raw_bit).strip().replace(' ', '')
            if bit.lower().startswith('0x'):
                bit = format(int(bit, 16), f'0{ncbits}b')
        if not bit or set(bit) - {'0', '1'}:
            raise RunError(f'Invalid measurement result: {raw_bit!r}')
        count = round(raw_count * shots) if probabilities else int(raw_count)
        if count < 0:
            raise RunError(f'Invalid measurement count: {raw_count!r}')
        if count:
            counts[bit] = counts.get(bit, 0) + count
    return counts


def _api_key(provider: str, api_key: str = None, api_key_file: str = None) -> str:
    key = api_key if api_key is not None else os.environ.get('PK_API_KEY')
    if key is None and api_key_file is not None:
        try:
            with open(api_key_file, 'r', encoding='utf-8') as stream:
                key = stream.read()
        except OSError as exc:
            raise RunError(f'Cannot read API key file: {api_key_file}') from exc
    if key is None or not key.strip():
        raise RunError(
            f"Provider '{provider}' requires an API key. Set PK_API_KEY, "
            "pass api_key, or use --api-key-file."
        )
    return key.strip()


class _ProviderBackend:
    provider: str
    framework: str
    default_backend = 'local'
    local_only = False

    def __init__(self, backend: str = None, api_key: str = None, options: dict = None):
        self.backend = backend or self.default_backend
        self.options = options or {}
        self.api_key = None
        if self.backend == 'local':
            return
        if self.local_only:
            raise RunError(
                f"Provider '{self.provider}' currently supports only backend 'local'."
            )
        self.api_key = _api_key(self.provider, api_key, self.options.get('api_key_file'))

    def _result(self, counts: dict[str, int], task_id: str = None,
                protocol: str = None) -> RunResult:
        if protocol is None:
            protocol = framework_interpret_protocol(self.framework)
        return RunResult(counts, self.provider, self.backend, task_id, protocol)

    def _simulator_result(self, qvm, circuit: CircuitIO, shots: int,
                          subsdict: dict = None) -> RunResult:
        converted = _convert_circuit(circuit, self.framework, subsdict)
        counts = run_and_get_counts(qvm, converted, shots)
        return self._result(_normalize_counts(counts, circuit.get_ncbits()))

    def run(self, circuit: CircuitIO, shots: int, subsdict: dict = None) -> RunResult:
        if self.backend == 'local':
            return self._run_local(circuit, shots, subsdict)
        return self._run_cloud(circuit, shots, subsdict)

    def _run_local(self, circuit: CircuitIO, shots: int, subsdict: dict = None) -> RunResult:
        raise NotImplementedError

    def _run_cloud(self, circuit: CircuitIO, shots: int, subsdict: dict = None) -> RunResult:
        raise NotImplementedError


class QiskitBackend(_ProviderBackend):
    provider = 'qiskit'
    framework = 'qiskit'
    local_only = True

    def _run_local(self, circuit: CircuitIO, shots: int, subsdict: dict = None) -> RunResult:
        try:
            from qiskit_aer import AerSimulator
        except ImportError as exc:
            raise RunError("Provider 'qiskit' requires qiskit-aer. Install 'pyquantumkit[qiskit]'.") from exc
        return self._simulator_result(AerSimulator(), circuit, shots, subsdict)


class OriginQBackend(_ProviderBackend):
    provider = 'originq'
    framework = 'pyqpanda3'

    def _run_local(self, circuit: CircuitIO, shots: int, subsdict: dict = None) -> RunResult:
        from pyqpanda3.core import CPUQVM
        return self._simulator_result(CPUQVM(), circuit, shots, subsdict)

    @staticmethod
    def _is_simulator(name: str) -> bool:
        return name.endswith('amplitude')

    def _catalog(self, service) -> dict:
        try:
            catalog = service.backends()
        except RuntimeError as exc:
            raise RunError(
                'OriginQ could not list backends. The cloud response was not a backend list. '
                'Check that the API key is an OriginQ QCloud key.'
            ) from exc
        return dict(catalog)

    def _available_names(self, catalog: dict, simulator: bool) -> str:
        names = sorted(
            name for name, available in catalog.items()
            if available and self._is_simulator(name) == simulator
        )
        return ', '.join(names) if names else '(none)'

    def _unknown_backend(self, catalog: dict) -> RunError:
        return RunError(
            f"Invalid OriginQ backend '{self.backend}'. "
            f"Available QPU backends: {self._available_names(catalog, False)}. "
            f"Available remote simulator backends: {self._available_names(catalog, True)}."
        )

    def _run_cloud(self, circuit: CircuitIO, shots: int, subsdict: dict = None) -> RunResult:
        from pyqpanda3.qcloud import QCloudService
        converted = _convert_circuit(circuit, self.framework, subsdict)
        service = QCloudService(self.api_key)
        try:
            catalog = self._catalog(service)
        except RunError:
            catalog = None
        if catalog is not None and self.backend not in catalog:
            raise self._unknown_backend(catalog)
        try:
            cloud_backend = service.backend(self.backend)
        except RuntimeError as exc:
            if catalog is not None:
                raise self._unknown_backend(catalog) from exc
            raise RunError(
                f"OriginQ could not open backend '{self.backend}': {exc}. "
                'Check that the API key is an OriginQ QCloud key.'
            ) from exc
        try:
            job = cloud_backend.run(converted, shots)
        except RuntimeError as exc:
            raise RunError(
                f"OriginQ backend '{self.backend}' rejected the circuit: {exc}"
            ) from exc
        task_id = str(job.job_id())
        probabilities = job.result().get_probs()
        if not probabilities:
            raise RunError(f'OriginQ job {task_id} returned no probabilities.')
        counts = _normalize_counts(probabilities, circuit.get_ncbits(), True, shots)
        return self._result(counts, task_id)


class QuafuBackend(_ProviderBackend):
    provider = 'quafu'
    framework = 'pyquafu'
    _AVAILABLE_STATUS = {'online', 'starting'}

    @staticmethod
    def _is_simulator(device: dict) -> bool:
        kind = device.get('kind')
        if kind == 'sim':
            return True
        if kind == 'real':
            return False
        name = str(device.get('name', ''))
        return name == 'sim' or name.endswith('-sim') or '-sim-' in name

    @classmethod
    def _is_available(cls, device: dict) -> bool:
        status = device.get('status')
        return status is None or str(status).lower() in cls._AVAILABLE_STATUS

    def _unknown_backend(self, devices) -> RunError:
        qpus = []
        simulators = []
        for device in devices:
            if not isinstance(device, dict) or not device.get('name') or not self._is_available(device):
                continue
            (simulators if self._is_simulator(device) else qpus).append(device['name'])

        def listed(names: list[str]) -> str:
            return ', '.join(sorted(names)) if names else '(none)'

        return RunError(
            f"Invalid Quafu backend '{self.backend}'. "
            f"Available QPU backends: {listed(qpus)}. "
            f"Available remote simulator backends: {listed(simulators)}."
        )

    def _run_local(self, circuit: CircuitIO, shots: int, subsdict: dict = None) -> RunResult:
        import quafu
        if not hasattr(quafu, 'simulate'):
            raise RunError("Quafu local execution requires pyquafu. Install 'pyquantumkit[quafu]'.")
        converted = _convert_circuit(circuit, self.framework, subsdict)
        result = quafu.simulate(converted, shots=shots)
        return self._result(_normalize_counts(result.counts, circuit.get_ncbits()))

    def _run_cloud(self, circuit: CircuitIO, shots: int, subsdict: dict = None) -> RunResult:
        try:
            import quafu
        except ImportError as exc:
            raise RunError("Provider 'quafu' requires pyquafu. Install 'pyquantumkit[quafu]'.") from exc
        client_class = getattr(quafu, 'Client', None)
        if client_class is None:
            try:
                from quafu.client import Client as client_class
                quafu.__version__ = importlib.metadata.version('quafu-sdk')
            except (ImportError, importlib.metadata.PackageNotFoundError) as exc:
                raise RunError(
                    "Quafu cloud execution requires quafu-sdk. Install 'pyquantumkit[quafu-sdk]'."
                ) from exc
        client = client_class(api_key=self.api_key, base_url=self.options.get('base_url'))
        devices = list(client.devices())
        available_backends = {
            device['name'] for device in devices
            if isinstance(device, dict) and device.get('name') and self._is_available(device)
        }
        if self.backend not in available_backends:
            raise self._unknown_backend(devices)
        compiler = self.options.get('compiler', 'qiskit')
        qasm = circuit.export_standalone_code('OpenQASM2.0', 'qs', subsdict=subsdict)
        job = client.submit(qasm, target=self.backend, shots=shots, compiler=compiler)
        result = job.result()
        if result.counts is None:
            raise RunError(f'Quafu job {job.id} returned no measurement results.')
        counts = _normalize_counts(result.counts, circuit.get_ncbits())
        protocol = framework_interpret_protocol(compiler) if compiler in Supported_Frameworks else 'r'
        return self._result(counts, str(job.id), protocol)


_BACKEND_CLASSES = {
    'qiskit': QiskitBackend,
    'originq': OriginQBackend,
    'quafu': QuafuBackend,
}
_PROVIDER_ALIASES = {
    'origin': 'originq',
    'pyqpanda3': 'originq',
    'pyquafu': 'quafu',
}


def run(circuit, provider: str = None, backend: str = None, shots: int = None,
        api_key: str = None, api_key_file: str = None, subsdict: dict = None,
        options: dict = None) -> RunResult:
    """Run a CircuitIO or QProgramBuilder on the selected local or cloud backend."""
    from pyquantumkit.program_build.builder import QProgramBuilder
    if isinstance(circuit, QProgramBuilder):
        return circuit.run(provider, backend, shots, api_key, api_key_file, subsdict, options)
    if not isinstance(circuit, CircuitIO):
        raise TypeError('run() expects a CircuitIO or QProgramBuilder object.')

    args = _cli_options()
    provider = provider or args.provider
    provider = _PROVIDER_ALIASES.get(provider.lower(), provider.lower())
    if provider not in _BACKEND_CLASSES:
        supported = ', '.join(_BACKEND_CLASSES)
        raise RunError(f"Unsupported provider '{provider}'. Available providers: {supported}.")
    backend = backend if backend is not None else args.backend
    shots = shots if shots is not None else args.shots
    if isinstance(shots, bool) or not isinstance(shots, int) or shots <= 0:
        raise RunError('shots must be a positive integer.')
    api_key_file = api_key_file or args.api_key_file
    if api_key_file is not None:
        options = dict(options or {})
        options['api_key_file'] = api_key_file
    backend_impl = _BACKEND_CLASSES[provider](backend, api_key, options)
    return backend_impl.run(circuit, shots, subsdict)
