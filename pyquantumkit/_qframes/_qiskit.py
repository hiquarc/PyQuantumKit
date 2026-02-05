# _qframes/_qiskit.py
#    2025/6/10
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from .code_translate import get_standard_gatename

# Whether the reverse of output 0/1 string is required to let the index of characters match corresponding cbits
REVERSE_OUTPUT_STRING = True
# Wether support inverse circuit
SUPPORT_INVERSE = True
# Wether support remap the index of bits
SUPPORT_REMAP = True
# List of supported algorithms
SUPPORT_ALGORITHMS = []


def CODE(cir_name : str, gate_lib_name : str, linebreak : str,
          gate_name : str, qbits : list[int], paras : list) -> str:
    g = get_standard_gatename(gate_name).lower()
    execstr = cir_name
    #glib = '' if gate_lib_name is None else gate_lib_name + "."

    if g == 'i':
        g = 'id'
    if g == 'm':
        execstr += ".measure(" + str(qbits) + ", " + str(paras) + ")"
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
    return CODE("qc", "FN('qiskit')", ";", gate_name, qbits, paras)


def CIRCUIT(is_remap : bool, is_inv : bool) -> str:
    execstr = "qc_dest.compose(qc_src"
    if is_inv:
        execstr += ".inverse()"
    if is_remap:
        execstr += ",rmlist"
    execstr += ",inplace=True)"
    return execstr


def PROGRAM(remap_q : bool, remap_c : bool) -> str:
    execstr = "qp_dest.compose(qp_src"
    if remap_q:
        execstr += ",qbits_remap"
    if remap_c:
        execstr += ",cbits_remap"
    execstr += ",inplace=True)"
    return execstr


def NEW(is_qprog : bool) -> str:
    if is_qprog:
        return "FN('qiskit').QuantumCircuit(nqbits, ncbits)"
    return "FN('qiskit').QuantumCircuit(nqbits)"


def BITS(ret_cbit : bool, ret_list : bool) -> str:
    if ret_list:
        return "list(range(qc.num_clbits))" if ret_cbit else "list(range(qc.num_qubits))"
    else:
        return "qc.num_clbits" if ret_cbit else "qc.num_qubits"


def RUN(line : int, **kwargs) -> str:
    if line == 1:
        return "qvm.run(qc,shots=run_shots)"
    if line == 2:
        return "qvm.run(qc,shots=run_shots).result().get_counts()"
    return ""
