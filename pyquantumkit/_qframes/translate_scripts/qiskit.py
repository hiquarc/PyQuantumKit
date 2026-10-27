# _qframes/translate_scripts/qiskit.py
#    2025/6/10
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from ..code_translate import get_standard_gatename, get_standard_subroutine_name, FrameworkMapError
import packaging.version

# The interpret protocol
INTERPRET_PROTOCOL = 'r'
# Wether support inverse circuit
SUPPORT_INVERSE = True
# Wether support remap the index of bits
SUPPORT_REMAP = True
# Set of supported quantum subroutines
SUPPORT_SUBROUTINES = {'QFT', 'QFT_NS', 'IQFT', 'IQFT_NS'}


def CODE(cir_name : str, module_name : str,
          op_name : str, qbits : list[int], paras : list,
          is_qsub : bool = False) -> str:
    if is_qsub:
        # Translation for quantum subroutines
        s = get_standard_subroutine_name(op_name).upper()
        if s not in SUPPORT_SUBROUTINES:
            raise FrameworkMapError(f"Unsupported quantum subroutine: {s}")

        slib = '' if module_name is None else module_name + "."
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

        if g == 'i':
            g = 'id'
        if g == 'm':
            execstr += f".measure({qbits}, {paras})"
            return execstr

        if g == 'sw':
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
    return CODE("qc", None, gate_name, qbits, paras)


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


def NEW(contains_cbits : bool) -> str:
    if contains_cbits:
        return "framework_modules('qiskit', 0).QuantumCircuit(nqbits, ncbits)"
    return "framework_modules('qiskit', 0).QuantumCircuit(nqbits)"


def BITS(ret_cbit : bool, ret_list : bool) -> str:
    if ret_list:
        return "list(range(qc.num_clbits))" if ret_cbit else "list(range(qc.num_qubits))"
    else:
        return "qc.num_clbits" if ret_cbit else "qc.num_qubits"


def RUN(options : dict) -> str:
    return """
compiled_qc = framework_modules('qiskit', 0).transpile(qc, qvm)
job = qvm.run(compiled_qc, shots=run_shots)
try:
    RESULT = job.result().get_counts()
except Exception as e:
    if 'No counts' in str(e):
        RESULT = {}
    else:
        raise
    """


def SUBROUTINE(qsub_name : str, qbits : list[int], paras : list) -> str:
    return CODE("qc", "framework_modules('qiskit', 1)", qsub_name, qbits, paras, True)
    