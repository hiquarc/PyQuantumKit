# translate/translate_scripts/qiskit.py
#    Create: 2025/6/10
#    Update: 2026/11/6
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from ..common import get_standard_gatename, get_standard_subroutine_name, FrameworkMapError
import packaging.version

# The interpret protocol
INTERPRET_PROTOCOL = 'r'
# Set of supported quantum subroutines
SUPPORT_SUBROUTINES = {
    'QFT' : 'qiskit.circuit.library',       # qsub name : corresponding package name
    'QFT_NS' : 'qiskit.circuit.library',
    'IQFT' : 'qiskit.circuit.library',
    'IQFT_NS' : 'qiskit.circuit.library',
}

EXPORT_CONSTANTS = {
    'comment' : "# Qiskit code exported from PyQuantumKit",
    'prefix' : "",
    'suffix' : "",
    'stdlib_name' : 'qiskit',
}

def IMPORT(module_name : str) -> str:
    return f"from {module_name} import *"

def DECLARE(cir_name : str, module_name : str,
            mixed : bool, nqbits : int, ncbits : int) -> str:
    circuit_type = "QuantumCircuit"
    declare_str = "" if cir_name is None else cir_name + " = "
    module_str = "" if module_name is None else module_name + "."
    if mixed:
        return f"{declare_str}{module_str}{circuit_type}({nqbits}, {ncbits})"
    else:
        return f"{declare_str}{module_str}{circuit_type}({nqbits})"

def APPLY(cir_name : str, module_name : str,
          op_name : str, qbits : list[int], paras : list,
          is_qsub : bool = False) -> str:
    if is_qsub:
        # Translation for quantum subroutines
        s = get_standard_subroutine_name(op_name).upper()
        if s not in SUPPORT_SUBROUTINES:
            raise FrameworkMapError(f"Unsupported quantum subroutine: {s}")

        slibname = SUPPORT_SUBROUTINES.get(s, None)
        slib = "" if slibname is None else f"framework_modules('qiskit', {slibname})."
        execstr = cir_name + ".append(" + slib

        # Qautnum Fourier Transform Series
        if s == 'QFT':
            execstr += f"QFT({len(qbits)}), {qbits})"
        elif s == 'QFT_NS':
            execstr += f"QFT({len(qbits)}, do_swaps=False), {qbits})"
        elif s == 'IQFT':
            execstr += f"QFT({len(qbits)}, inverse=True), {qbits})"
        elif s == 'IQFT_NS':
            execstr += f"QFT({len(qbits)}, do_swaps=False, inverse=True), {qbits})"

        return execstr

    else:
        # Translation for quantum gates
        g = get_standard_gatename(op_name).lower()
        execstr = cir_name
        #glib = '' if gate_lib_name is None else gate_lib_name + "."

        if g == 'm':
            execstr += f".measure({qbits}, {paras})"
            return execstr

        if g == 'i':
            g = 'id'
        elif g == 'sw':
            g = 'swap'
        elif g == 'isw':
            g = 'iswap'
        elif g == 'csw':
            g = 'cswap'
        elif g == 'u3':
            g = 'u'
        elif g == 'u1':
            g = 'p'
        elif g == 'cu1':
            g = 'cp'
        elif g == 'sd':
            g = 'sdg'
        elif g == 'td':
            g = 'tdg'
        elif g == 'csd':
            g = 'csdg'
        elif g == 'sxd':
            g = 'sxdg'

        execstr += "." + g + "("
        if not paras:
            execstr += str(qbits)[1:-1] + ")"
        else:
            execstr += str(paras)[1:-1] + ", " + str(qbits)[1:-1] + ")"
        return execstr

def GATE(gate_name : str, qbits : list[int], paras : list) -> str:
    return APPLY("qc", None, gate_name, qbits, paras)

def SUBROUTINE(qsub_name : str, qbits : list[int], paras : list) -> str:
    return APPLY("qc", None, qsub_name, qbits, paras, True)

def NEW(mixed_circuit : bool, nqbits : int, ncbits : int) -> str:
    std = EXPORT_CONSTANTS['stdlib_name']
    return DECLARE(None, f"framework_modules('qiskit', '{std}')", mixed_circuit, nqbits, ncbits)

def BITS(ret_cbit : bool, ret_list : bool) -> str:
    if ret_list:
        return "list(range(qc.num_clbits))" if ret_cbit else "list(range(qc.num_qubits))"
    else:
        return "qc.num_clbits" if ret_cbit else "qc.num_qubits"


def RUN(options : dict) -> str:
    return """
compiled_qc = framework_modules('qiskit', 'qiskit').transpile(qc, qvm)
job = qvm.run(compiled_qc, shots=run_shots)
try:
    RESULT = job.result().get_counts()
except Exception as e:
    if 'No counts' in str(e):
        RESULT = {}
    else:
        raise
    """


# ---------- Actions just for internal usage ----------
def CIRCUIT(is_remap : bool, is_inv : bool) -> str:
    execstr = "qc_dest.compose(qc_src"
    if is_inv:
        execstr += ".inverse()"
    if is_remap:
        execstr += ",rmlist"
    execstr += ",inplace=True)"
    return execstr

def MIXED_CIRCUIT(remap_q : bool, remap_c : bool) -> str:
    execstr = "qp_dest.compose(qp_src"
    if remap_q:
        execstr += ",qbits_remap"
    if remap_c:
        execstr += ",cbits_remap"
    execstr += ",inplace=True)"
    return execstr
