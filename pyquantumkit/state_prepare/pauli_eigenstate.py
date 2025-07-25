# state_prepare/pauli_eigenstate.py
#    2025/6/12
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from pyquantumkit.procedure.generic import apply_gate
from pyquantumkit.procedure.derivative import derivative

PauliZ_1    = 0
PauliZ_Neg1 = 1
PauliX_1    = 2
PauliX_Neg1 = 3
PauliY_1    = 4
PauliY_Neg1 = 5

def create_pauli_eigenstate(q_circuit, paulilist : list[int], qbitlist : list[int]):
    """
     Apply a quantum circuit to create multi-qubit Pauli eigenstate, where each index takes from 0 to 5

        q_circuit : applied quantum circuit
        paulilist : state number of each qubit

            0  ---  |0>             eigenstate of +1 eigenvalue of Z
            1  ---  |1>             eigenstate of -1 eigenvalue of Z
            2  ---  |+> = |0>+|1>   eigenstate of +1 eigenvalue of X
            3  ---  |-> = |0>-|1>   eigenstate of -1 eigenvalue of X
            4  ---  |0>+i|1>        eigenstate of +1 eigenvalue of Y
            5  ---  |0>-i|1>        eigenstate of -1 eigenvalue of Y

        qbitlist  : the index of target qubits

    -> Return : q_circuit
    """
    if qbitlist is None or len(qbitlist) <= 0:
        return q_circuit
    N = len(qbitlist)
    if N != len(paulilist):
        raise ValueError('<paulilist> and <qbitlist> must be have same length!')

    for i in range(0, N):
        if paulilist[i] > 5 or paulilist[i] < 0:
            raise ValueError('elements in <paulilist> must in [0,1,2,3,4,5]')
        #if paulilist[i] == PauliZ_1:
        #    pass
        if paulilist[i] == PauliZ_Neg1:
            apply_gate(q_circuit, 'X', [qbitlist[i]])
        elif paulilist[i] == PauliX_1:
            apply_gate(q_circuit, 'H', [qbitlist[i]])
        elif paulilist[i] == PauliX_Neg1:
            apply_gate(q_circuit, 'X', [qbitlist[i]])
            apply_gate(q_circuit, 'H', [qbitlist[i]])
        elif paulilist[i] == PauliY_1:
            apply_gate(q_circuit, 'H', [qbitlist[i]])
            apply_gate(q_circuit, 'S', [qbitlist[i]])
        elif paulilist[i] == PauliY_Neg1:
            apply_gate(q_circuit, 'H', [qbitlist[i]])
            apply_gate(q_circuit, 'SD', [qbitlist[i]])
    return q_circuit

def uncompute_pauli_eigenstate(q_circuit, paulilist : list[int], qbitlist : list[int]):
    """
     Apply a quantum circuit to uncompute multi-qubit Pauli eigenstate, where each index takes from 0 to 5

        q_circuit : applied quantum circuit
        paulilist : state number of each qubit

            0  ---  |0>             eigenstate of +1 eigenvalue of Z
            1  ---  |1>             eigenstate of -1 eigenvalue of Z
            2  ---  |+> = |0>+|1>   eigenstate of +1 eigenvalue of X
            3  ---  |-> = |0>-|1>   eigenstate of -1 eigenvalue of X
            4  ---  |0>+i|1>        eigenstate of +1 eigenvalue of Y
            5  ---  |0>-i|1>        eigenstate of -1 eigenvalue of Y

        qbitlist  : the index of target qubits

    -> Return : q_circuit
    """
    return derivative(q_circuit, qbitlist, create_pauli_eigenstate, False, True, paulilist, qbitlist)
