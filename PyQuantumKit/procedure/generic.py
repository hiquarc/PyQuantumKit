# procedure/generic.py
#    2025/6/9
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from pyquantumkit import get_framework_from_object
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


def apply_gate(q_circuit, gate_str : str, qbits : list[int], paras : list = []):
    """
    Apply a quantum gate on a quantum circuit

        q_circuit : applied quantum circuit
        gate_str  : a string to identify the quantum gate
        qbits     : the indexes of applied qubits
        paras     : (optional) the parameters of the gate

    -> Return : q_circuit
    """
    quantum_action(Action.GATE, q_circuit, gate_str, qbits, paras)
    return q_circuit


def apply_measure(q_circuit, qindex : list[int], cindex : list[int]):
    """
    Apply measurement operation on a quantum circuit

        q_circuit : applied quantum circuit
        qindex    : the indexes of measured qubits
        cindex    : the indexes of cbits to contain results

    -> Return : q_circuit
    """
    quantum_action(Action.GATE, q_circuit, 'M', qindex, cindex)
    return q_circuit


def multi_apply_sqgate(q_circuit, gate_str : str, qbitlist : list[int], paras : list = []):
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


def append_circuit(dest_qcir, src_qcir, remap = 0, inverse : bool = False):
    """
    Apply a quantum circuit on a qubit array.

        dest_qcir  : destination quantum circuit to be appended
        src_qcir   : source quantum circuit
        remap      : (int or list[int], default 0)
                     if the type of <remap> is int, give the offset of each qubit index
                     if the type of <remap> is list[int], give the remap list of the qubit indices
        inverse    : (default False) whether apply the inverse circuit

    -> Return : dest_qcir
    """
    remaplist = None
    if isinstance(remap, int):
        if remap > 0:
            remaplist = [x + remap for x in get_qubit_list(src_qcir)]
    else:
        remaplist = remap
    quantum_action(Action.CIRCUIT, dest_qcir, src_qcir, remaplist, inverse)
    return dest_qcir


def copy_circuit(src_qcir, remap = 0, inverse : bool = False):
    """
    Copy a quantum circuit

        src_qcir   : source quantum circuit
        remap      : (int or list[int], default 0)
                     if the type of <remap> is int, give the offset of each qubit index
                     if the type of <remap> is list[int], give the remap list of the qubit indices
        inverse    : (default False) whether apply the inverse circuit

    -> Return : a replica quantum circuit of src_qcir
    """
    return append_circuit(None, src_qcir, remap, inverse)



def append_program(dest_qp, src_qp, qbits_remap = 0, cbits_remap = 0):
    """
    Apply a quantum program on a qubit array.

        destqp      : destination quantum program to be appended
        src_qp      : source quantum program
        qbits_remap : (int or list[int], default 0)
                     if the type of <qbits_remap> is int, give the offset of each qubit index
                     if the type of <qbits_remap> is list[int], give the remap list of the qubit indices
        cbits_remap : (int or list[int], default 0)
                     if the type of <cbits_remap> is int, give the offset of each classical bit index
                     if the type of <cbits_remap> is list[int], give the remap list of the classical bit indices

    -> Return : dest_qp
    """
    qrlist = None
    crlist = None
    if isinstance(qbits_remap, int):
        if qbits_remap > 0:
            qrlist = [x + qbits_remap for x in get_qubit_list(src_qp)]
    else:
        qrlist = qbits_remap
    if isinstance(cbits_remap, int):
        if cbits_remap > 0:
            crlist = [x + cbits_remap for x in get_cbit_list(src_qp)]
    else:
        crlist = cbits_remap

    quantum_action(Action.PROGRAM, dest_qp, src_qp, qrlist, crlist)
    return dest_qp


def copy_program(src_qp, qbits_remap = 0, cbits_remap = 0):
    """
    Copy a quantum program

        src_qp      : source quantum program
        qbits_remap : (int or list[int], default 0)
                     if the type of <qbits_remap> is int, give the offset of each qubit index
                     if the type of <qbits_remap> is list[int], give the remap list of the qubit indices
        cbits_remap : (int or list[int], default 0)
                     if the type of <cbits_remap> is int, give the offset of each classical bit index
                     if the type of <cbits_remap> is list[int], give the remap list of the classical bit indices

    -> Return : a replica quantum program of src_qp
    """
    return append_program(None, src_qp, qbits_remap, cbits_remap)



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
    return quantum_action(Action.BITS, q_prog, False, False)

def get_qubit_list(q_prog) -> list[int]:
    """
    Get the qubit list a quantum circuit or program

        q_prog : target quantum circuit/program

    -> Return : list of the qubits
    """
    return quantum_action(Action.BITS, q_prog, False, True)

def get_n_cbits(q_prog) -> int:
    """
    Get the number of classical bits of a quantum program

        q_prog : target quantum program

    -> Return : the number of classical bits
                0 if q_prog is a quantum circuit
    """
    return quantum_action(Action.BITS, q_prog, True, False)

def get_cbit_list(q_prog) -> list[int]:
    """
    Get the classical bit list of a quantum program

        q_prog : target quantum program

    -> Return : list of the classical bits
                [] if q_prog is a quantum circuit
    """
    return quantum_action(Action.BITS, q_prog, True, True)


def run_and_get_counts(q_machine, q_prog, shots : int = 1, model = None):
    """
    Run quantum programs on quantum machine and get the result dict

        q_machine : target quantum machine
        q_prog    : target quantum program
        shots     : running shots (repeat times)
        model     : (current unsupported)

    -> Return : dict of results
    """
    return quantum_action(Action.RUN, q_machine, q_prog, shots, model)


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
        qofflist.append(nqs)
        cofflist.append(ncs)
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
