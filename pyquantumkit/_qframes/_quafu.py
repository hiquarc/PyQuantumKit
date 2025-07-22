# _qframes/_pyquafu.py
#    2025/7/4
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from .code_translate import get_args_assign_str, get_standard_gatename
from pyquantumkit import PyQuantumKitError

# Whether the reverse of output 0/1 string is required to let the index of characters match corresponding cbits
REVERSE_OUTPUT_STRING = False
# Wether support inverse circuit
SUPPORT_INVERSE = False
# Wether support remap the index of bits
SUPPORT_REMAP = False

# Translate the gate applying into the code of calling in qiskit
def GATE(gate_name : str, nqs : int, nps : int) -> str:
    g = get_standard_gatename(gate_name).lower()
    if g == 'i':
        return ''
    if g == 'm':
        execstr = "qc.measure([" + get_args_assign_str('qbits', nqs) + "],[" + get_args_assign_str('paras', nps) + "])"
        return execstr
    
    if g == 'ccz':
        execstr = "qc.mcx([qbits[0],qbits[1]],qbits[2])"
        return execstr
    if g == 'ch':
        execstr = "qc<<FN('quafu',1).HGate(qbits[1]).ctrl_by(qbits[0])"
        return execstr
    
    execstr = "qc"

    if g == 'u3':
        execstr += "<<FN('quafu',1).U3Gate"
    elif g == 'crx':
        execstr += "<<FN('quafu',1).CRXGate"
    elif g == 'cry':
        execstr += "<<FN('quafu',1).CRYGate"
    elif g == 'crz':
        execstr += "<<FN('quafu',1).CRZGate"
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
    else:
        execstr += '.' + g

    if nps == 0:
        execstr += "(" + get_args_assign_str('qbits', nqs) + ")"
    else:
        execstr += "(" + get_args_assign_str('qbits', nqs) + "," + get_args_assign_str('paras', nps) + ")"
    return execstr


# Translate the circuit applying into the code of calling in qiskit
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
