# _qframes/_qiskit.py
#    2025/6/10
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from .code_translate import get_args_assign_str, get_standard_gatename

# Whether the reverse of output 0/1 string is required to let the index of characters match corresponding cbits
REVERSE_OUTPUT_STRING = True

# Translate the gate applying into the code of calling in qiskit
def GATE(gate_name : str, nqs : int, nps : int) -> str:
    g = get_standard_gatename(gate_name).lower()
    if g == 'i':
        return ''
    if g == 'm':
        execstr = "qc.measure([" + get_args_assign_str('qbits', nqs) + "],[" + get_args_assign_str('paras', nps) + "])"
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

    execstr = "qc." + g + "("
    if nps == 0:
        execstr += get_args_assign_str('qbits', nqs) + ")"
    else:
        execstr += get_args_assign_str('paras', nps) + "," + get_args_assign_str('qbits', nqs) + ")"
    return execstr


# Translate the circuit applying into the code of calling in qiskit
def CIRCUIT(dest_none : bool, is_remap : bool, is_inv : bool) -> str:
    execstr = ""
    if dest_none:
        execstr += "tempqc=Framework_Namespace['qiskit'].QuantumCircuit(qc_src);tempqc"
    else:
        execstr += "qc_dest"
    execstr += ".compose(qc_src"
    if is_inv:
        execstr += ".inverse()"
    if is_remap:
        execstr += ",rmlist"
    execstr += ",inplace=True)"
    return execstr


def PROGRAM(dest_none : bool, remap_q : bool, remap_c : bool) -> str:
    execstr = ""
    if dest_none:
        execstr += "tempqp=Framework_Namespace['qiskit'].QuantumCircuit(qp_src);tempqp"
    else:
        execstr += "qp_dest"
    execstr += ".compose(qp_src"
    if remap_q:
        execstr += ",qbits_remap"
    if remap_c:
        execstr += ",cbits_remap"
    execstr += ",inplace=True)"
    return execstr


def NEW(is_qprog : bool) -> str:
    if is_qprog:
        return "Framework_Namespace['qiskit'].QuantumCircuit(nqbits, ncbits)"
    return "Framework_Namespace['qiskit'].QuantumCircuit(nqbits)"


def BITS(ret_cbit : bool, ret_list : bool) -> str:
    if ret_list:
        return "list(range(qc.num_clbits))" if ret_cbit else "list(range(qc.num_qubits))"
    else:
        return "qc.num_clbits" if ret_cbit else "qc.num_qubits"


def RUN(line : int, model) -> str:
    if line == 1:
        return "job=qvm.run(qc,shots=run_shots)"
    if line == 2:
        return "job.result().get_counts()"
    return ""
