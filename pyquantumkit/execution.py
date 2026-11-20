import argparse
import importlib
import importlib.metadata
import json
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
                        help='execution provider: qiskit, originq, quafu, or tianyan (default: qiskit)')
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


def _print_run_info(provider: str, backend: str, available: str = None,
                    qpus: str = None, simulators: str = None) -> None:
    lines = [f'provider: {provider}']
    if qpus is not None or simulators is not None:
        lines.append(f'available QPU backends: {qpus or "(none)"}')
        lines.append(f'available remote simulator backends: {simulators or "(none)"}')
    else:
        lines.append(f'available backends: {available}')
    lines.append(f'running on backend: {backend}')
    rows = [f'  {line}' for line in lines[:-1]]
    rows.append(f'▶ {lines[-1]}')
    title = ' PyQuantumKit '
    width = max(max(len(row) for row in rows), len(title) + 2)
    print('┌' + title + '─' * (width - len(title)) + '┐')
    for row in rows:
        print('│' + row.ljust(width) + '│')
    print('└' + '─' * width + '┘')


class _ProviderBackend:
    provider: str
    framework: str
    api_key_hint = 'Check the API key.'
    _API_KEY_MARKERS = ('unauthorized',)
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
            _print_run_info(self.provider, self.backend, available='local')
            return self._run_local(circuit, shots, subsdict)
        return self._run_cloud(circuit, shots, subsdict)

    def _run_local(self, circuit: CircuitIO, shots: int, subsdict: dict = None) -> RunResult:
        raise NotImplementedError

    def _run_cloud(self, circuit: CircuitIO, shots: int, subsdict: dict = None) -> RunResult:
        raise NotImplementedError

    @classmethod
    def _api_key_failure(cls, exc: BaseException) -> bool:
        text = str(exc).lower()
        return any(marker in text for marker in cls._API_KEY_MARKERS)

    def _api_key_error(self, action: str, exc: BaseException) -> RunError:
        return RunError(f'{self.provider} could not {action}: {exc}. {self.api_key_hint}')

    def _invalid_backend(self, qpus: str, simulators: str) -> RunError:
        return RunError(
            f"Invalid {self.provider} backend '{self.backend}'. "
            f"Available QPU backends: {qpus}. "
            f"Available remote simulator backends: {simulators}."
        )

    def _announce_cloud(self, qpus: str, simulators: str) -> None:
        _print_run_info(self.provider, self.backend, qpus=qpus, simulators=simulators)

    @staticmethod
    def _listed(names) -> str:
        names = sorted(names)
        return ', '.join(names) if names else '(none)'


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
    api_key_hint = 'Check that the API key is an OriginQ QCloud key.'

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
            if self._api_key_failure(exc):
                raise self._api_key_error('list backends', exc) from exc
            raise RunError(
                f'{self.provider} could not list backends: {exc}. {self.api_key_hint}'
            ) from exc
        return dict(catalog)

    def _available_names(self, catalog: dict, simulator: bool) -> str:
        names = (
            name for name, available in catalog.items()
            if available and self._is_simulator(name) == simulator
        )
        return self._listed(names)

    def _run_cloud(self, circuit: CircuitIO, shots: int, subsdict: dict = None) -> RunResult:
        from pyqpanda3.qcloud import QCloudService
        converted = _convert_circuit(circuit, self.framework, subsdict)
        service = QCloudService(self.api_key)
        catalog = self._catalog(service)
        qpus = self._available_names(catalog, False)
        simulators = self._available_names(catalog, True)
        if self.backend not in catalog:
            raise self._invalid_backend(qpus, simulators)
        try:
            cloud_backend = service.backend(self.backend)
        except RuntimeError as exc:
            if self._api_key_failure(exc):
                raise self._api_key_error(f"open backend '{self.backend}'", exc) from exc
            raise self._invalid_backend(qpus, simulators) from exc
        self._announce_cloud(qpus, simulators)
        try:
            job = cloud_backend.run(converted, shots)
        except RuntimeError as exc:
            if self._api_key_failure(exc):
                raise self._api_key_error(
                    f"run backend '{self.backend}'", exc
                ) from exc
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

    def _available_groups(self, devices) -> tuple[str, str]:
        qpus = []
        simulators = []
        for device in devices:
            if not isinstance(device, dict) or not device.get('name') or not self._is_available(device):
                continue
            (simulators if self._is_simulator(device) else qpus).append(device['name'])
        return self._listed(qpus), self._listed(simulators)

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
        qpus, simulators = self._available_groups(devices)
        if self.backend not in available_backends:
            raise self._invalid_backend(qpus, simulators)
        self._announce_cloud(qpus, simulators)
        compiler = self.options.get('compiler', 'qiskit')
        qasm = circuit.export_standalone_code('OpenQASM2.0', 'qs', subsdict=subsdict)
        job = client.submit(qasm, target=self.backend, shots=shots, compiler=compiler)
        result = job.result()
        if result.counts is None:
            raise RunError(f'Quafu job {job.id} returned no measurement results.')
        counts = _normalize_counts(result.counts, circuit.get_ncbits())
        protocol = framework_interpret_protocol(compiler) if compiler in Supported_Frameworks else 'r'
        return self._result(counts, str(job.id), protocol)


class TianYanBackend(_ProviderBackend):
    provider = 'tianyan'
    framework = 'cqlib'
    api_key_hint = 'Check that the API key is a TianYan login key.'
    _API_KEY_MARKERS = ('unauthorized', 'login failed')
    _AVAILABLE_STATUS = {'running'}
    _SIMULATOR_NAMES = {
        'tianyan_sw', 'tianyan_sa', 'tianyan_s', 'tianyan_tn', 'tianyan_tnn', 'tianyan_swn',
    }
    _ROW_STATUS = _AVAILABLE_STATUS | {'calibration', 'under maintenance', 'off-line', 'unknown'}
    _ROW_IGNORE = _ROW_STATUS | {'free', 'paid', '未知状态'}

    @classmethod
    def _is_simulator(cls, name: str) -> bool:
        lowered = name.lower()
        prefix, separator, suffix = lowered.rpartition('_')
        return lowered in cls._SIMULATOR_NAMES or 'sim' in lowered or (
            separator == '_' and prefix.startswith('tianyan') and suffix.isalpha()
        )

    @classmethod
    def _computer(cls, row) -> tuple[str, str]:
        if isinstance(row, dict):
            name = row.get('machineName') or row.get('code') or row.get('name') or ''
            status = str(row.get('status', '')).lower()
            return str(name), status
        values = [str(item) for item in row]
        status = next((item.lower() for item in values if item.lower() in cls._ROW_STATUS), '')
        names = [item for item in values if item.lower() not in cls._ROW_IGNORE and not item.isdigit()]
        return (names[-1] if names else ''), status

    @staticmethod
    def _measure_cbits(circuit: CircuitIO) -> list[int]:
        cbits = []
        for name, _qubits, targets in circuit.get_gate_list():
            if name == 'M':
                cbits.extend(targets)
        return cbits

    @classmethod
    def _counts_from_shots(cls, shots, cbits: list[int], ncbits: int) -> dict[str, int]:
        counts = {}
        for shot in shots:
            outcomes = [str(bit) for bit in shot]
            if len(outcomes) != len(cbits):
                raise RunError('TianYan returned a measurement whose width does not match the circuit.')
            chars = ['0'] * ncbits
            for outcome, cbit in zip(outcomes, cbits):
                if outcome not in {'0', '1'}:
                    raise RunError(f'Invalid TianYan measurement bit: {outcome!r}')
                chars[cbit] = outcome
            bit = ''.join(chars)
            counts[bit] = counts.get(bit, 0) + 1
        return counts

    @classmethod
    def _counts_from_bitstrings(cls, values: dict, cbits: list[int], ncbits: int,
                                shots: int, probabilities: bool) -> dict[str, int]:
        """Place little-endian measurement strings onto classical-bit positions."""
        expanded = {}
        for raw_bit, raw_count in values.items():
            text = str(raw_bit).strip().replace(' ', '')
            if text.lower().startswith('0b'):
                text = text[2:]
            if len(text) != len(cbits) or set(text) - {'0', '1'}:
                raise RunError(f'Invalid TianYan measurement result: {raw_bit!r}')
            chars = ['0'] * ncbits
            for outcome, cbit in zip(reversed(text), cbits):
                chars[cbit] = outcome
            bit = ''.join(chars)
            count = round(raw_count * shots) if probabilities else int(raw_count)
            if count:
                expanded[bit] = expanded.get(bit, 0) + count
        return expanded

    def _counts(self, result: dict, circuit: CircuitIO, shots: int) -> dict[str, int]:
        cbits = self._measure_cbits(circuit)
        if not cbits:
            raise RunError('The circuit has no measurements to submit to TianYan.')
        status = result.get('resultStatus')
        if isinstance(status, str):
            status = json.loads(status)
        if status:
            return self._counts_from_shots(status[1:], cbits, circuit.get_ncbits())
        probability = result.get('probability')
        if isinstance(probability, str):
            probability = json.loads(probability)
        if isinstance(probability, dict) and probability:
            return self._counts_from_bitstrings(
                probability, cbits, circuit.get_ncbits(), shots, True
            )
        raise RunError(f"TianYan job {result.get('experimentTaskId', '')} returned no measurement results.")

    @staticmethod
    def _error_text(exc: BaseException):
        message = getattr(exc, 'message', None)
        return message if isinstance(message, str) and message else exc

    def _guard(self, action: str, exc: BaseException, hint: bool = False) -> RunError:
        text = self._error_text(exc)
        if self._api_key_failure(exc):
            return self._api_key_error(action, text)
        if hint:
            return RunError(f'{self.provider} could not {action}: {text}. {self.api_key_hint}')
        return RunError(f'{self.provider} could not {action}: {text}')

    def _platform(self):
        try:
            from cqlib import TianYanPlatform
        except ImportError as exc:
            raise RunError("Provider 'tianyan' requires cqlib. Install 'pyquantumkit[cqlib]'.") from exc
        try:
            return TianYanPlatform(login_key=self.api_key)
        except Exception as exc:
            raise self._guard('log in', exc, hint=True) from exc

    def _machines(self, platform) -> list[tuple[str, str]]:
        try:
            rows = platform.query_quantum_computer_list()
        except Exception as exc:
            raise self._guard('list backends', exc, hint=True) from exc
        return [self._computer(row) for row in rows]

    def _run_local(self, circuit: CircuitIO, shots: int, subsdict: dict = None) -> RunResult:
        try:
            from cqlib.simulator import StatevectorSimulator
        except ImportError as exc:
            raise RunError("Provider 'tianyan' requires cqlib. Install 'pyquantumkit[cqlib]'.") from exc
        converted = _convert_circuit(circuit, self.framework, subsdict)
        cbits = self._measure_cbits(circuit)
        if not cbits:
            raise RunError('The circuit has no measurements.')
        try:
            raw = StatevectorSimulator(converted).sample(shots=shots)
        except Exception as exc:
            raise RunError(f'tianyan local simulator failed: {exc}') from exc
        counts = self._counts_from_bitstrings(raw, cbits, circuit.get_ncbits(), shots, False)
        return self._result(counts)

    def _run_cloud(self, circuit: CircuitIO, shots: int, subsdict: dict = None) -> RunResult:
        from cqlib import QuantumLanguage
        platform = self._platform()
        machines = self._machines(platform)
        available = [(name, status) for name, status in machines if name and status in self._AVAILABLE_STATUS]
        qpus = self._listed(name for name, _status in available if not self._is_simulator(name))
        simulators = self._listed(name for name, _status in available if self._is_simulator(name))
        if self.backend not in {name for name, _status in available}:
            raise self._invalid_backend(qpus, simulators)
        self._announce_cloud(qpus, simulators)
        converted = _convert_circuit(circuit, self.framework, subsdict)
        platform.set_machine(self.backend)
        try:
            query_ids = platform.submit_experiment(
                circuit=converted.qcis,
                language=QuantumLanguage.QCIS,
                num_shots=shots,
                machine_name=self.backend,
                name='pyquantumkit',
            )
        except Exception as exc:
            raise self._guard(f"submit backend '{self.backend}'", exc) from exc
        if not query_ids:
            raise RunError(f"TianYan backend '{self.backend}' did not return a task id.")
        task_id = str(query_ids[0] if isinstance(query_ids, (list, tuple)) else query_ids)
        try:
            results = platform.query_experiment(
                task_id,
                max_wait_time=self.options.get('max_wait_time', 3600),
                sleep_time=self.options.get('sleep_time', 5),
            )
        except Exception as exc:
            raise self._guard(f"query job '{task_id}'", exc) from exc
        if not results:
            raise RunError(f'TianYan job {task_id} returned no measurement results.')
        counts = self._counts(results[0], circuit, shots)
        reported_id = results[0].get('experimentTaskId')
        return self._result(counts, str(reported_id or task_id))


_BACKEND_CLASSES = {
    'qiskit': QiskitBackend,
    'originq': OriginQBackend,
    'quafu': QuafuBackend,
    'tianyan': TianYanBackend,
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
    provider = (provider or args.provider).lower()
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
