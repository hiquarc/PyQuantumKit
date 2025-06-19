# QProcedure/Common.py
#    2025/6/9
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from PyQuantumKit import GetFrameworkFromObject
from PyQuantumKit.qframes.framework_map import *
from PyQuantumKit.Classical.Common import LengthOfIndexList


def Derivative(q_circuit, qbitlist : list[int], createfunc : callable, rev_endian = False, uncomp = False, *args, **kwargs):
    """
    Generate the derivative circuit based on quantum circuit function <createfunc>

        q_circuit  : the circuit to be appended
        qbitlist   : index of qubit list to apply the circuit
        createfunc : the functions to create target quantum circuit
        rev_endian : whether reverse the order of target quantum circuit
        uncomp     : whether generate the inverse version of target quantum circuit
        ...        : the parameters required in <createfunc>

    -> Return : q_circuit; if q_circuit == None, create a new circuit
    """
    f = GetFrameworkFromObject(q_circuit)
    tempqc = NewCircuit(f, LengthOfIndexList(qbitlist))
    createfunc(tempqc, *args, **kwargs)
    if rev_endian:
        AppendCircuit(q_circuit, tempqc, range(0, len(qbitlist))[::-1], uncomp)
    else:
        AppendCircuit(q_circuit, tempqc, None, uncomp)
    return q_circuit


def ApplyGate(q_circuit, gate_str : str, qbits : list[int], paras : list = []):
    """
    Apply a quantum gate on a quantum circuit

        q_circuit : applied quantum circuit
        gate_str  : a string to identify the quantum gate
        qbits     : the indexes of applied qubits
        paras     : (optional) the parameters of the gate

    -> Return : q_circuit
    """
    QuantumActionMap(Action.GATE, q_circuit, gate_str, qbits, paras)
    return q_circuit


def ApplyMeasure(q_circuit, qindex : list[int], cindex : list[int]):
    """
    Apply measurement operation on a quantum circuit

        q_circuit : applied quantum circuit
        qindex    : the indexes of measured qubits
        cindex    : the indexes of cbits to contain results

    -> Return : q_circuit
    """
    QuantumActionMap(Action.GATE, q_circuit, 'M', qindex, cindex)
    return q_circuit


def MultiApplySQGate(q_circuit, gate_str : str, qbitlist : list[int], paras : list = []):
    """
    Apply a series of same single-qubit gate on a quantum circuit

        q_circuit : applied quantum circuit
        gate_str  : a string to identify the single-qubit quantum gate
        qbitlist  : the indexes of applied qubits
        paras     : (optional) the parameters of the gate

    -> Return : q_circuit
    """
    for i in qbitlist:
        ApplyGate(q_circuit, gate_str, [i], paras)
    return q_circuit


def ApplyReverse(q_circuit, qbitlist : list[int]):
    """
    Apply a reverse operation on a qubit array.

        q_circuit : applied quantum circuit
        qbitlist  : index list of the qubit array

    -> Return : q_circuit
    """
    N = len(qbitlist)
    for i in range(0, N // 2):
        ApplyGate(q_circuit, 'SW', [qbitlist[i], qbitlist[N - i - 1]])
    return q_circuit


def AppendCircuit(dest_qcir, src_qcir, remap = 0, inverse : bool = False, control : bool = False):
    """
    Apply a quantum circuit on a qubit array.

        dest_qcir  : destination quantum circuit to be appended
        src_qcir   : source quantum circuit
        remap      : (int or list[int], default 0)
                     if the type of <remap> is int, give the offset of each qubit index
                     if the type of <remap> is list[int], give the remap list of the qubit indices
        inverse    : (default False) whether apply the inverse circuit
        control    : (current unsupported)

    -> Return : dest_qcir
    """
    remaplist = None
    if isinstance(remap, int):
        if remap > 0:
            remaplist = [x + remap for x in GetQubitList(src_qcir)]
    else:
        remaplist = remap
    QuantumActionMap(Action.CIRCUIT, dest_qcir, src_qcir, remaplist, inverse, control)
    return dest_qcir


def CopyCircuit(src_qcir, remap = 0, inverse : bool = False, control : bool = False):
    """
    Copy a quantum circuit

        src_qcir   : source quantum circuit
        remap      : (int or list[int], default 0)
                     if the type of <remap> is int, give the offset of each qubit index
                     if the type of <remap> is list[int], give the remap list of the qubit indices
        inverse    : (default False) whether apply the inverse circuit
        control    : (current unsupported)

    -> Return : a replica quantum circuit of src_qcir
    """
    return AppendCircuit(None, src_qcir, remap, inverse, control)



def AppendProgram(dest_qp, src_qp, qbits_remap = 0, cbits_remap = 0):
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
            qrlist = [x + qbits_remap for x in GetQubitList(src_qp)]
    else:
        qrlist = qbits_remap
    if isinstance(cbits_remap, int):
        if cbits_remap > 0:
            crlist = [x + cbits_remap for x in GetCbitList(src_qp)]
    else:
        crlist = cbits_remap

    QuantumActionMap(Action.PROGRAM, dest_qp, src_qp, qrlist, crlist)
    return dest_qp


def CopyProgram(src_qp, qbits_remap = 0, cbits_remap = 0):
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
    return AppendProgram(None, src_qp, qbits_remap, cbits_remap)



def NewCircuit(framework, nqbits : int):
    """
    Generate an empty quantum circuit

        framework : the string to identify the target framework
        nqbits    : the number of qubits of the circuit

    -> Return : an empty quantum circuit with type of target framework
    """
    return QuantumActionMap(Action.NEW, framework, False, nqbits, 0)


def NewProgram(framework, nqbits : int, ncbits : int = 0):
    """
    Generate an empty quantum program (which contains classical bits)

        framework : the string to identify the target framework
        nqbits    : the number of qubits of the program
        ncbits    : the number of classicl bits of the program

    -> Return : an empty quantum program with type of target framework
    """
    return QuantumActionMap(Action.NEW, framework, True, nqbits, ncbits)


def GetNQubits(q_prog) -> int:
    """
    Get the number of qubits of a quantum circuit or program

        q_prog : target quantum circuit/program

    -> Return : the number of qubits
    """
    return QuantumActionMap(Action.BITS, q_prog, False, False)

def GetQubitList(q_prog) -> list[int]:
    """
    Get the qubit list a quantum circuit or program

        q_prog : target quantum circuit/program

    -> Return : list of the qubits
    """
    return QuantumActionMap(Action.BITS, q_prog, False, True)

def GetNCbits(q_prog) -> int:
    """
    Get the number of classical bits of a quantum program

        q_prog : target quantum program

    -> Return : the number of classical bits
                0 if q_prog is a quantum circuit
    """
    return QuantumActionMap(Action.BITS, q_prog, True, False)

def GetCbitList(q_prog) -> list[int]:
    """
    Get the classical bit list of a quantum program

        q_prog : target quantum program

    -> Return : list of the classical bits
                [] if q_prog is a quantum circuit
    """
    return QuantumActionMap(Action.BITS, q_prog, True, True)


def RunAndGetCounts(q_machine, q_prog, shots : int = 1, model = None):
    return QuantumActionMap(Action.RUN, q_machine, q_prog, shots, model)


def ParallelPrograms(*args, **kwargs):
    """
    Generate a quantum program to parallel several subprograms

        Variable parameters:
            e.g., ParallelPrograms(qp1, qp2, qp3)

    -> Return : result quantum program
    """
    qofflist = []
    cofflist = []
    ntotalqs = 0
    ntotalcs = 0
    f = GetFrameworkFromObject(args[0])

    for i in range(len(args)):
        nqs = GetNQubits(args[i])
        ncs = GetNCbits(args[i])
        qofflist.append(nqs)
        cofflist.append(ncs)
        ntotalqs += nqs
        ntotalcs += ncs

    retqp = NewProgram(f, ntotalqs, ntotalcs)
    for i in range(len(args)):
        AppendProgram(retqp, args[i], qofflist[i], cofflist[i])
    return retqp


def ParallelCircuits(*args, **kwargs):
    """
    Generate a quantum circuit to parallel several subcircuits

        Variable parameters:
            e.g., ParallelCircuits(qc1, qc2, qc3)

    -> Return : result quantum circuit
    """
    qofflist = []
    ntotalqs = 0
    f = GetFrameworkFromObject(args[0])

    for i in range(len(args)):
        nqs = GetNQubits(args[i])
        qofflist.append(ntotalqs)
        ntotalqs += nqs

    retqc = NewCircuit(f, ntotalqs)
    for i in range(len(args)):
        AppendCircuit(retqc, args[i], qofflist[i])
    return retqc
