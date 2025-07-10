# procedure/generic.py
#    2025/6/9
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from pyquantumkit import get_framework_from_object, PyQuantumKitError
from pyquantumkit._qframes.framework_map import quantum_action, Action
from pyquantumkit.classical.common import indexlist_length


def derivative(q_circuit, qbitlist : list[int], createfunc : callable, rev_endian = False, uncomp = False,\
                *args, **kwargs):
    """
    Generate the derivative circuit based on quantum circuit function <createfunc>

        q_circuit  : the circuit to be appended
        qbitlist   : index of qubit list to apply the circuit
        createfunc : the functions to create target quantum circuit
        rev_endian : whether reverse the order of target quantum circuit
        uncomp     : whether generate the inverse version of target quantum circuit
        ...        : the parameters required in <createfunc>

    -> Return : q_circuit; if q_circuit is None, create a new circuit
    """
    f = get_framework_from_object(q_circuit)
    tempqc = new_circuit(f, indexlist_length(qbitlist))
    createfunc(tempqc, *args, **kwargs)
    if rev_endian:
        append_circuit(q_circuit, tempqc, range(0, len(qbitlist))[::-1], uncomp)
    else:
        append_circuit(q_circuit, tempqc, None, uncomp)
    return q_circuit


def apply_gate(q_circuit, gate_str : str, qbits : list[int], paras : list = None):
    """
    Apply a quantum gate on a quantum circuit

        q_circuit : applied quantum circuit
        gate_str  : a string to identify the quantum gate
        qbits     : the indexes of applied qubits
        paras     : (optional) the parameters of the gate

    -> Return : q_circuit
    """
    quantum_action(Action.GATE, 0, q_circuit, gate_str, qbits, paras)
    return q_circuit


def apply_measure(q_circuit, qindex : list[int], cindex : list[int]):
    """
    Apply measurement operation on a quantum circuit

        q_circuit : applied quantum circuit
        qindex    : the indexes of measured qubits
        cindex    : the indexes of cbits to contain results

    -> Return : q_circuit
    """
    quantum_action(Action.GATE, 0, q_circuit, 'M', qindex, cindex)
    return q_circuit


def multi_apply_sqgate(q_circuit, gate_str : str, qbitlist : list[int], paras : list = None):
    """
    Apply a series of same single-qubit gate on a quantum circuit

        q_circuit : applied quantum circuit
        gate_str  : a string to identify the single-qubit quantum gate
        qbitlist  : the indexes of applied qubits
        paras     : (optional) the parameters of the gate

    -> Return : q_circuit
    """
    for i in qbitlist:
        apply_gate(q_circuit, gate_str, [i], paras)
    return q_circuit


def apply_reverse(q_circuit, qbitlist : list[int]):
    """
    Apply a reverse operation on a qubit array.

        q_circuit : applied quantum circuit
        qbitlist  : index list of the qubit array

    -> Return : q_circuit
    """
    N = len(qbitlist)
    for i in range(0, N // 2):
        apply_gate(q_circuit, 'SW', [qbitlist[i], qbitlist[N - i - 1]])
    return q_circuit


def append_circuit(dest_qcir, src_qcir, remap = None, inverse : bool = False):
    """
    Apply a quantum circuit on a qubit array.

        dest_qcir  : destination quantum circuit to be appended
            NOTE: <dest_qcir> can be quantum circuit or quantum program
        src_qcir   : source quantum circuit
        remap      : (None or int or list[int], default None)
                     if <remap> is None, no remap will be applied
                     if the type of <remap> is int, give the offset of each qubit index
                     if the type of <remap> is list[int], give the remap list of the qubit indices
        inverse    : (default False) whether apply the inverse circuit

    -> Return : dest_qcir
    """
    remaplist = None
    if remap is None:
        remaplist = None
    elif isinstance(remap, int):
        remaplist = [x + remap for x in get_qubit_list(src_qcir)]
    elif isinstance(remap, (list, range)):
        remaplist = remap
    else:
        raise PyQuantumKitError('Invalid remap: ' + str(remap))
    
    quantum_action(Action.CIRCUIT, 1, dest_qcir, src_qcir, remaplist, inverse)
    return dest_qcir


def copy_circuit(src_qcir, remap = None, inverse : bool = False):
    """
    Copy a quantum circuit

        src_qcir   : source quantum circuit
        remap      : (int or list[int], default None)
                     if <remap> is None, no remap will be applied
                     if the type of <remap> is int, give the offset of each qubit index
                     if the type of <remap> is list[int], give the remap list of the qubit indices
        inverse    : (default False) whether apply the inverse circuit

    -> Return : a replica quantum circuit of src_qcir
    """
    framework = get_framework_from_object(src_qcir)
    nqbits = get_n_qubits(src_qcir)
    retqc = new_circuit(framework, nqbits)
    append_circuit(retqc, src_qcir, remap, inverse)
    return retqc



def append_program(dest_qp, src_qp, qbits_remap = None, cbits_remap = None):
    """
    Apply a quantum program on a qubit array.

        destqp      : destination quantum program to be appended
        src_qp      : source quantum program
        qbits_remap : (None or int or list[int], default None)
                     if the type of <qbits_remap> is int, give the offset of each qubit index
                     if the type of <qbits_remap> is list[int], give the remap list of the qubit indices
        cbits_remap : (None or int or list[int], default None)
                     if the type of <cbits_remap> is int, give the offset of each classical bit index
                     if the type of <cbits_remap> is list[int], give the remap list of the classical bit indices
            NOTE: if one of <qbits_remap> or <cbits_remap> is None, no remap will be applied.

    -> Return : dest_qp
    """
    if qbits_remap is None or cbits_remap is None:
        quantum_action(Action.PROGRAM, 1, dest_qp, src_qp, None, None)
        return dest_qp
    
    qrlist = None
    crlist = None
    if isinstance(qbits_remap, int):
        qrlist = [x + qbits_remap for x in get_qubit_list(src_qp)]
    elif isinstance(qbits_remap, (list, range)):
        qrlist = qbits_remap
    else:
        raise PyQuantumKitError('Invalid qbits_remap: ' + str(qbits_remap))
    if isinstance(cbits_remap, int):
        crlist = [x + cbits_remap for x in get_cbit_list(src_qp)]
    elif isinstance(cbits_remap, (list, range)):
        crlist = cbits_remap
    else:
        raise PyQuantumKitError('Invalid cbits_remap: ' + str(cbits_remap))

    quantum_action(Action.PROGRAM, 1, dest_qp, src_qp, qrlist, crlist)
    return dest_qp


def copy_program(src_qp, qbits_remap = None, cbits_remap = None):
    """
    Copy a quantum program

        src_qp      : source quantum program
            NOTE: <src_qp> can be a quantum circuit. But if so, please remain <qbits_remap> and <cbits_remap> are None.
        qbits_remap : (None or int or list[int], default None)
                     if the type of <qbits_remap> is int, give the offset of each qubit index
                     if the type of <qbits_remap> is list[int], give the remap list of the qubit indices
        cbits_remap : (None or list[int], default None)
                     if the type of <cbits_remap> is int, give the offset of each classical bit index
                     if the type of <cbits_remap> is list[int], give the remap list of the classical bit indices
            NOTE: if one of <qbits_remap> or <cbits_remap> is None, no remap will be applied.

    -> Return : a replica quantum program of src_qp
    """
    framework = get_framework_from_object(src_qp)
    nqbits = get_n_qubits(src_qp)
    ncbits = get_n_cbits(src_qp)
    retqp = new_program(framework, nqbits, ncbits)
    append_program(retqp, src_qp, qbits_remap, cbits_remap)
    return retqp



def new_circuit(framework, nqbits : int):
    """
    Generate an empty quantum circuit

        framework : the string to identify the target framework
        nqbits    : the number of qubits of the circuit

    -> Return : an empty quantum circuit with type of target framework
    """
    return quantum_action(Action.NEW, framework, False, nqbits, 0)


def new_program(framework, nqbits : int, ncbits : int = 0):
    """
    Generate an empty quantum program (which contains classical bits)

        framework : the string to identify the target framework
        nqbits    : the number of qubits of the program
        ncbits    : the number of classicl bits of the program

    -> Return : an empty quantum program with type of target framework
    """
    return quantum_action(Action.NEW, framework, True, nqbits, ncbits)


def get_n_qubits(q_prog) -> int:
    """
    Get the number of qubits of a quantum circuit or program

        q_prog : target quantum circuit/program

    -> Return : the number of qubits
    """
    return quantum_action(Action.BITS, 0, q_prog, False, False)

def get_qubit_list(q_prog) -> list[int]:
    """
    Get the qubit list a quantum circuit or program

        q_prog : target quantum circuit/program

    -> Return : list of the qubits
    """
    return quantum_action(Action.BITS, 0, q_prog, False, True)

def get_n_cbits(q_prog) -> int:
    """
    Get the number of classical bits of a quantum program

        q_prog : target quantum program

    -> Return : the number of classical bits
                0 if q_prog is a quantum circuit
    """
    return quantum_action(Action.BITS, 0, q_prog, True, False)

def get_cbit_list(q_prog) -> list[int]:
    """
    Get the classical bit list of a quantum program

        q_prog : target quantum program

    -> Return : list of the classical bits
                [] if q_prog is a quantum circuit
    """
    return quantum_action(Action.BITS, 0, q_prog, True, True)


def run_and_get_counts(q_machine, q_prog, shots : int = 1, **kwargs):
    """
    Run quantum programs on quantum machine and get the result dict

        q_machine : target quantum machine
        q_prog    : target quantum program
        shots     : running shots (repeat times)
        kwargs    : (optional) Other parameters

    -> Return : dict of results
    """
    return quantum_action(Action.RUN, 1, q_machine, q_prog, shots, **kwargs)


def juxtapose_programs(*args):
    """
    Generate a quantum program to parallel several subprograms

        Variable parameters:
            e.g., juxtapose_programs(qp1, qp2, qp3)

    -> Return : result quantum program
    """
    qofflist = []
    cofflist = []
    ntotalqs = 0
    ntotalcs = 0
    f = get_framework_from_object(args[0])

    for i in range(len(args)):
        nqs = get_n_qubits(args[i])
        ncs = get_n_cbits(args[i])
        qofflist.append(ntotalqs)
        cofflist.append(ntotalcs)
        ntotalqs += nqs
        ntotalcs += ncs

    retqp = new_program(f, ntotalqs, ntotalcs)
    for i in range(len(args)):
        append_program(retqp, args[i], qofflist[i], cofflist[i])
    return retqp


def juxtapose_circuits(*args):
    """
    Generate a quantum circuit to parallel several subcircuits

        Variable parameters:
            e.g., juxtapose_circuits(qc1, qc2, qc3)

    -> Return : result quantum circuit
    """
    qofflist = []
    ntotalqs = 0
    f = get_framework_from_object(args[0])

    for i in range(len(args)):
        nqs = get_n_qubits(args[i])
        qofflist.append(ntotalqs)
        ntotalqs += nqs

    retqc = new_circuit(f, ntotalqs)
    for i in range(len(args)):
        append_circuit(retqc, args[i], qofflist[i])
    return retqc
