# _qframes/_pyquafu.py
#    2025/7/4
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from .code_translate import get_standard_gatename
from pyquantumkit import PyQuantumKitError

# Whether the reverse of output 0/1 string is required to let the index of characters match corresponding cbits
REVERSE_OUTPUT_STRING = False
# Wether support inverse circuit
SUPPORT_INVERSE = False
# Wether support remap the index of bits
SUPPORT_REMAP = False
# List of supported algorithms
SUPPORT_ALGORITHMS = []


def CODE(cir_name : str, gate_lib_name : str, linebreak : str,
          gate_name : str, qbits : list[int], paras : list) -> str:
    g = get_standard_gatename(gate_name).lower()
    execstr = cir_name
    glib = '' if gate_lib_name is None else gate_lib_name + "."

    if g == 'i':
        g = 'id'
    if g == 'm':
        execstr += ".measure(" + str(qbits) + ", " + str(paras) + ")"
        return execstr
    
    if g == 'ccz':
        execstr += ".mcx(" + str(qbits[0:2]) + ", " + str(qbits[2]) + ")"
        return execstr
    if g == 'ch':
        execstr += " << " + glib + "HGate(" + str(qbits[1]) + ").ctrl_by(" + str(qbits[0]) + ")"
        return execstr
    if g == 'csd':
        execstr += " << " + glib + "SdgGate(" + str(qbits[1]) + ").ctrl_by(" + str(qbits[0]) + ")"
        return execstr

    if g == 'u3':
        execstr += " << " + glib + "U3Gate"
    elif g == 'crx':
        execstr += " << " + glib + "CRXGate"
    elif g == 'cry':
        execstr += " << " + glib + "CRYGate"
    elif g == 'crz':
        execstr += " << " + glib + "CRZGate"
    elif g == 'sw':
        execstr += '.swap'
    elif g == 'isw':
        execstr += '.iswap'
    elif g == 'csw':
        execstr += '.fredkin'
    elif g == 'u1':
        execstr += ".p"
    elif g == 'cu1':
        execstr += '.cp'
    elif g == 'sd':
        execstr += '.sdg'
    elif g == 'td':
        execstr += '.tdg'
    elif g == 'ccx':
        execstr += '.toffoli'
    elif g == 'sxd':
        execstr += '.sxdg'
    else:
        execstr += '.' + g

    if not paras:
        execstr += "(" + str(qbits)[1:-1] + ")"
    else:
        execstr += "(" + str(qbits)[1:-1] + ", " + str(paras)[1:-1] + ")"
    return execstr


def GATE(gate_name : str, qbits : list[int], paras : list) -> str:
    return CODE("qc", "FN('quafu',1)", ";", gate_name, qbits, paras)


def CIRCUIT(is_remap : bool, is_inv : bool) -> str:
    # unsupport
    raise PyQuantumKitError('Quantum circuit operations are not supported by quafu.')


def PROGRAM(remap_q : bool, remap_c : bool) -> str:
    # unsupport
    raise PyQuantumKitError('Quantum program operations are not supported by quafu.')


def NEW(is_qprog : bool) -> str:
    if is_qprog:
        return "FN('quafu').QuantumCircuit(nqbits, ncbits)"
    return "FN('quafu').QuantumCircuit(nqbits)"


def BITS(ret_cbit : bool, ret_list : bool) -> str:
    if ret_list:
        return "list(range(qc.cbits_num))" if ret_cbit else "qc.used_qubits"
    else:
        return "qc.cbits_num" if ret_cbit else "len(qc.used_qubits)"


def RUN(line : int, **kwargs) -> str:
    if line == 1:
        return "res = qvm(qc,shots=run_shots) if qvm == FN('quafu').simulate else None"
    if line == 2:
        return "res.counts"
    return ""
