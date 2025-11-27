# QProcedure/Paulis.py
#    2025/6/13
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from pyquantumkit.procedure.generic import apply_gate, apply_measure
from pyquantumkit import PyQuantumKitError

Pauli_Strings = ['I', 'X', 'Y', 'Z']

def apply_measure_x(q_circuit, qindex : list[int], cindex : list[int]):
    """
    Apply X measurement operations on a quantum circuit

        result: 0 --- eigenvalue +1;
                1 --- eigenvalue -1

        q_circuit : applied quantum circuit
        qindex    : the indexes of measured qubits
        cindex    : the indexes of cbits to contain results

    -> Return : q_circuit
    """
    apply_gate(q_circuit, 'H', qindex)
    apply_measure(q_circuit, qindex, cindex)
    return q_circuit

def apply_measure_y(q_circuit, qindex : list[int], cindex : list[int]):
    """
    Apply Y measurement operations on a quantum circuit

        result: 0 --- eigenvalue +1;
                1 --- eigenvalue -1

        q_circuit : applied quantum circuit
        qindex    : the indexes of measured qubits
        cindex    : the indexes of cbits to contain results

    -> Return : q_circuit
    """
    apply_gate(q_circuit, 'SD', qindex)
    apply_gate(q_circuit, 'H', qindex)
    apply_measure(q_circuit, qindex, cindex)
    return q_circuit

def apply_measure_z(q_circuit, qindex : list[int], cindex : list[int]):
    """
    Apply Z measurement operations on a quantum circuit

        result: 0 --- eigenvalue +1;
                1 --- eigenvalue -1

        q_circuit : applied quantum circuit
        qindex    : the indexes of measured qubits
        cindex    : the indexes of cbits to contain results

    -> Return : q_circuit
    """
    return apply_measure(q_circuit, qindex, cindex)


def apply_pauli_measure(q_circuit, paulistr : str, qindex : list[int], cindex : list[int]):
    """
    Apply Z measurement operation on a quantum circuit

        result: 0 --- eigenvalue +1;
                1 --- eigenvalue -1

        q_circuit : applied quantum circuit
        paulistr  : 'I'/'X'/'Y'/'Z' strings to represent pauli measurement for each qubit
        qindex    : the indexes of measured qubits
        cindex    : the indexes of cbits to contain results

    -> Return : q_circuit
    """
    s = paulistr.upper()
    for i in range(qindex):
        if s[i] not in Pauli_Strings:
            raise PyQuantumKitError("Error Pauli character: " + s[i])
        if s == 'X':
            apply_gate(q_circuit, 'H', [qindex[i]])
        elif s == 'Y':
            apply_gate(q_circuit, 'SD', [qindex[i]])
            apply_gate(q_circuit, 'H', [qindex[i]])
        if s != 'I':
            apply_measure(q_circuit, [qindex[i]], [cindex[i]])
    return q_circuit


def apply_exp_pauli(q_circuit, paulistr : str, t : float, qindex : list[int], focus : int = 0):
    """
    Append an Exp(-i*P*t) operation, where P is the tensor product of several Pauli operators.

        q_circuit : applied quantum circuit
        paulistr  : 'I'/'X'/'Y'/'Z' strings to represent the tensor product of Pauli operators
        qindex    : the indexes of applied qubits
        focus     : (optional) the index of non-I Paulis which is applied the core rotation, default 0

    -> Return : q_circuit
    """
    # Normalize the Pauli string: uppercase, remove all 'I'
    ps = ''         # record the Pauli string excluding 'I'
    qi = []         # record the corresponding qubit index of <ps>
    for i in range(0, len(paulistr)):
        p = paulistr[i].upper()
        if p not in Pauli_Strings:
            raise PyQuantumKitError("Error Pauli character: " + p)
        if p in {'X', 'Y', 'Z'}:
            ps += p
            qi.append(qindex[i])
    f = focus if focus < len(ps) else len(ps) - 1       # record the corresponding "focus"

    # Consider separately: None, X, Y, Z, XX, YY, ZZ
    if len(ps) <= 0:
        return q_circuit
    if ps in {'X', 'Y', 'Z'}:
        apply_gate(q_circuit, 'R' + ps, [qi[0]], [t * 2])
        return q_circuit
    if ps in {'XX', 'YY', 'ZZ'}:
        apply_gate(q_circuit, 'R' + ps, qi[0:2], [t * 2])
        return q_circuit

    # Algorithm for general cases
    for i in range(0, len(ps)):
        if ps[i] == 'X':
            apply_gate(q_circuit, 'H', [qi[i]])
        elif ps[i] == 'Y':
            apply_gate(q_circuit, 'SD', [qi[i]])
            apply_gate(q_circuit, 'H', [qi[i]])
    for i in range(0, len(ps)):
        if i != f:
            apply_gate(q_circuit, 'CX', [qi[i], qi[f]])

    apply_gate(q_circuit, 'RZ', [qi[f]], [t * 2])

    for i in range(len(ps) - 1, -1, -1):
        if i != f:
            apply_gate(q_circuit, 'CX', [qi[i], qi[f]])
    for i in range(0, len(ps)):
        if ps[i] == 'X':
            apply_gate(q_circuit, 'H', [qi[i]])
        elif ps[i] == 'Y':
            apply_gate(q_circuit, 'H', [qi[i]])
            apply_gate(q_circuit, 'S', [qi[i]])

    return q_circuit
