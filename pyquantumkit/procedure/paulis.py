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
