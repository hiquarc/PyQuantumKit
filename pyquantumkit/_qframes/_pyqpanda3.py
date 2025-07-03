# _qframes/_pyqpanda3.py
#    2025/6/10
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from .code_translate import get_args_assign_str, get_standard_gatename

# Whether the reverse of output 0/1 string is required to let the index of characters match corresponding cbits
REVERSE_OUTPUT_STRING = True

# Translate the gate applying into the code of calling in pyqpanda3
def GATE(gate_name : str, nqs : int, nps : int) -> str:
    g = get_standard_gatename(gate_name).upper()
    if g == 'I':
        return ''
    if g == 'M':
        # NOTE: there are some bugs in measure(list, list) in pyqpanda3 (ver 0.3.1)
        #execstr = "qc<<Framework_Namespace['pyqpanda3'].measure([" + \
        #          get_args_assign_str('qbits', nqs) + "],[" + \
        #          get_args_assign_str('paras', nps) + "])"

        # Temporarily use bit-by-bit operation to avoid the bugs in pyqpanda3
        execstr = "qc"
        for i in range(nqs):
            execstr += "<<Framework_Namespace['pyqpanda3'].measure(qbits["\
                     + str(i) + "],paras[" + str(i) + "])"
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
    # pyqpanda3 verion 0.3 supports CRX, CRY, CRZ directly
    #if g == 'CRX' or g == 'CRY' or g == 'CRZ':
    #    execstr += g[1:3] + "(qbits[1],paras[0]).control(qbits[0])"
    #    return execstr
    if g == 'SD' or g == 'TD':
        execstr += g[0] + "(qbits[0]).dagger()"
        return execstr
    if g == 'CCZ':
        execstr += "Z(qbits[2]).control([qbits[0],qbits[1]])"
        return execstr

    if nps == 0:
        execstr += g + "(" + get_args_assign_str('qbits', nqs) + ")"
    else:
        execstr += g + "(" + get_args_assign_str('qbits', nqs) + "," + \
                   get_args_assign_str('paras', nps) + ")"
    return execstr


# Translate the circuit applying into the code of calling in pyqpanda3
def CIRCUIT(is_remap : bool, is_inv : bool) -> str:
    execstr = "tempqc=Framework_Namespace['pyqpanda3'].QCircuit(qc_src);qc_dest<<tempqc"
    if is_inv:
        execstr += ".dagger()"
    if is_remap:
        execstr += ".remap(rmlist)"
    return execstr


def PROGRAM(remap_q : bool, remap_c : bool) -> str:
    execstr = "tempqp=Framework_Namespace['pyqpanda3'].QProg(qp_src);qp_dest<<tempqp"
    if remap_q or remap_c:
        execstr += ".remap(qbits_remap,cbits_remap)"
    return execstr


def NEW(is_qprog : bool) -> str:
    if is_qprog:
        return "Framework_Namespace['pyqpanda3'].QProg(nqbits)"
    return "Framework_Namespace['pyqpanda3'].QCircuit(nqbits)"


def BITS(ret_cbit : bool, ret_list : bool) -> str:
    execstr = "0 if isinstance(qc, Framework_Namespace['pyqpanda3'].QCircuit) else indexlist_length(qc.cbits())" \
              if ret_cbit else "indexlist_length(qc.qubits())"
    if ret_list:
        return "list(range(" + execstr + "))"
    else:
        return execstr


def RUN(line : int, model) -> str:
    if line == 1:
        if model is None:
            return "qvm.run(qc,run_shots,model)"
        else:
            return "qvm.run(qc,run_shots)"
    if line == 2:
        return "qvm.result().get_counts()"
    return ""
