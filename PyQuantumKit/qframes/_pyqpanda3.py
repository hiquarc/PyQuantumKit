# qframes/_pyqpanda3.py
#    2025/6/10
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from .code_translate import *

# Whether the reverse of output 0/1 string is required to let the index of characters match corresponding cbits
ReverseRunOutputString = True

# Translate the gate applying into the code of calling in pyqpanda3
def GATE(gate_name : str, nqs : int, nps : int) -> str:
    g = ConvertToSandard(gate_name).upper()
    if g == 'I':
        return ''
    if g == 'M':
        execstr = "qc<<Framework_Namespace['pyqpanda3'].measure([" + ArgsAssignStr('qbits', nqs) + "],[" + ArgsAssignStr('paras', nps) + "])"
        return execstr

    if g == 'CX':
        g = 'CNOT'
    elif g == 'SW':
        g = 'SWAP'
    elif g == 'ISW':
        g = 'ISWAP'
    elif g == 'CCX':
        g = 'TOFFOLI'
    elif g == 'CU1':
        g = 'CR'
    
    execstr = "qc<<Framework_Namespace['pyqpanda3']."
    if g == 'CH' or g == 'CY':
        execstr += g[1] + "(qbits[1]).control(qbits[0])"
        return execstr
    if g == 'CSW':
        execstr += "SWAP(qbits[1],qbits[2]).control(qbits[0])"
        return execstr
    if g == 'CRX' or g == 'CRY' or g == 'CRZ':
        execstr += g[1:3] + "(qbits[1],paras[0]).control(qbits[0])"
        return execstr
    if g == 'SD' or g == 'TD':
        execstr += g[0] + "(qbits[0]).dagger()"
        return execstr
    if g == 'CCZ':
        execstr += "Z(qbits[2]).control([qbits[0],qbits[1]])"
        return execstr

    if nps == 0:
        execstr += g + "(" + ArgsAssignStr('qbits', nqs) + ")"
    else:
        execstr += g + "(" + ArgsAssignStr('qbits', nqs) + "," + ArgsAssignStr('paras', nps) + ")"
    return execstr


# Translate the circuit applying into the code of calling in pyqpanda3
def CIRCUIT(dest_none : bool, is_remap : bool, is_inv : bool, is_ctrl : bool) -> str:
    execstr = "tempqc=Framework_Namespace['pyqpanda3'].QCircuit(qc_src);"
    if dest_none:
        execstr += "tempqc"
    else:
        execstr += "qc_dest<<tempqc"
    if is_inv:
        execstr += ".dagger()"
    #if is_ctrl:
    if is_remap:
        execstr += ".remap(rmlist)"
    return execstr


def PROGRAM(dest_none : bool, remap_q : bool, remap_c : bool) -> str:
    execstr = "tempqp=Framework_Namespace['pyqpanda3'].QProg(qp_src);"
    if dest_none:
        execstr += "tempqp"
    else:
        execstr += "qp_dest<<tempqp"
    if remap_q or remap_c:
        execstr += ".remap(qbits_remap,cbits_remap)"
    return execstr


def NEW(is_qprog : bool) -> str:
    if is_qprog:
        return "Framework_Namespace['pyqpanda3'].QProg(nqbits)"
    return "Framework_Namespace['pyqpanda3'].QCircuit(nqbits)"


def BITS(ret_cbit : bool, ret_list : bool) -> str:
    execstr = "0 if isinstance(qc, Framework_Namespace['pyqpanda3'].QCircuit) else LengthOfIndexList(qc.cbits())" if ret_cbit else "LengthOfIndexList(qc.qubits())"
    if ret_list:
        return "list(range(" + execstr + "))"
    else:
        return execstr
    

def RUN(line : int, model) -> str:
    if line == 1:
        if model == None:
            return "qvm.run(qc,run_shots,model)"
        else:
            return "qvm.run(qc,run_shots)"
    if line == 2:
        return "qvm.result().get_counts()"
    return ""
