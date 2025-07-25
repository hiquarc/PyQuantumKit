# _qframes/_pyqpanda3.py
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
    g = get_standard_gatename(gate_name).upper()
    execstr = cir_name
    glib = '' if gate_lib_name is None else gate_lib_name + "."

    #if g == 'I':
    #    return ''
    if g == 'M':
        # NOTE: there are some bugs in measure(list, list) in pyqpanda3 (ver 0.3.1)
        #execstr = " << FN('pyqpanda3').measure(" + str(qbits) + ", " + str(paras) + ")"
        # Temporarily use bit-by-bit operation to avoid the bugs in pyqpanda3
        for i in range(len(qbits)):
            execstr += " << " + glib + "measure(" + str(qbits[i]) + ", " + str(paras[i]) + ")"
        return execstr
    
    execstr += " << " + glib
    if g == 'CH' or g == 'CY':
        execstr += g[1] + "(" + str(qbits[1]) + ").control(" + str(qbits[0]) + ")"
        return execstr
    if g == 'CSW':
        execstr += "SWAP(" + str(qbits[1]) + ", " + str(qbits[2]) + ").control(" + str(qbits[0]) + ")"
        return execstr
    # pyqpanda3 verion 0.3 supports CRX, CRY, CRZ directly
    #if g == 'CRX' or g == 'CRY' or g == 'CRZ':
    #    execstr += g[1:3] + "(qbits[1],paras[0]).control(qbits[0])"
    #    return execstr
    if g == 'SD' or g == 'TD':
        execstr += g[0] + "(" + str(qbits[0]) + ").dagger()"
        return execstr
    if g == 'CCZ':
        execstr += "Z(" + str(qbits[2]) + ").control(" + str(qbits[0:2]) + ")"
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

    if not paras:
        execstr += g + "(" + str(qbits)[1:-1] + ")"
    else:
        execstr += g + "(" + str(qbits)[1:-1] + ", " + str(paras)[1:-1] + ")"
    return execstr


# Translate the gate applying into the code of calling in pyqpanda3
def GATE(gate_name : str, qbits : list[int], paras : list) -> str:
    return CODE("qc", "FN('pyqpanda3')", ";", gate_name, qbits, paras)


# Translate the circuit applying into the code of calling in pyqpanda3
def CIRCUIT(is_remap : bool, is_inv : bool) -> str:
    execstr = "tempqc=FN('pyqpanda3').QCircuit(qc_src);qc_dest<<tempqc"
    if is_inv:
        execstr += ".dagger()"
    if is_remap:
        execstr += ".remap(rmlist)"
    return execstr


def PROGRAM(remap_q : bool, remap_c : bool) -> str:
    execstr = "tempqp=FN('pyqpanda3').QProg(qp_src);qp_dest<<tempqp"
    if remap_q or remap_c:
        execstr += ".remap(qbits_remap,cbits_remap)"
    return execstr


def NEW(is_qprog : bool) -> str:
    if is_qprog:
        return "FN('pyqpanda3').QProg(nqbits)"
    return "FN('pyqpanda3').QCircuit(nqbits)"


def BITS(ret_cbit : bool, ret_list : bool) -> str:
    execstr = "0 if isinstance(qc, FN('pyqpanda3').QCircuit) else indexlist_length(qc.cbits())" \
              if ret_cbit else "indexlist_length(qc.qubits())"
    if ret_list:
        return "list(range(" + execstr + "))"
    else:
        return execstr


def RUN(line : int, **kwargs) -> str:
    if line == 1:
        if kwargs is not None and kwargs.get('model') is not None:
            return "qvm.run(qc,run_shots,model=kwargs['model'])"
        else:
            return "qvm.run(qc,run_shots)"
    if line == 2:
        return "qvm.result().get_counts()"
    return ""
