# QStatePrepare/IntState.py
#    2025/6/11
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from PyQuantumKit.QProcedure.Common import *
from PyQuantumKit.Classical.Common import *


def CreateKetIntLE(q_circuit, number : int, qbitlist : list[int]):
    """
    Apply a quantum circuit to create classical state, which is given by an integer with little-endian mode.

        e.g., 25 = 11001b --> q[0]=|1>, q[1]=|0>, q[2]=|0>, q[3]=|1>, q[4]=|1>

        q_circuit : applied quantum circuit
        number    : the integer to describe the state
        qbitlist  : index list of the target qubit array

    -> Return : q_circuit
    """
    N = len(qbitlist)
    temp = number
    for i in range(0, N):
        if ((temp & 1) == 1):
            ApplyGate(q_circuit, 'X', [qbitlist[i]])
        temp >>= 1
    return q_circuit

def CreateKetIntBE(q_circuit, number : int, qbitlist : list[int]):
    """
    Apply a quantum circuit to create classical state, which is given by an integer with big-endian mode.

        e.g., 25 = 11001b --> q[0]=|1>, q[1]=|1>, q[2]=|0>, q[3]=|0>, q[4]=|1>

        q_circuit : applied quantum circuit
        number    : the integer to describe the state
        qbitlist  : index list of the target qubit array

    -> Return : q_circuit
    """
    return Derivative(q_circuit, qbitlist, CreateKetIntLE, True, False, number, qbitlist)

def UncomputeKetIntLE(q_circuit, number : int, qbitlist : list[int]):
    """
    Apply a quantum circuit to uncompute classical state, which is given by an integer with little-endian mode.

        e.g., 25 = 11001b --> q[0]=|1>, q[1]=|0>, q[2]=|0>, q[3]=|1>, q[4]=|1>

        q_circuit : applied quantum circuit
        number    : the integer to describe the state
        qbitlist  : index list of the target qubit array

    -> Return : q_circuit
    """
    return CreateKetIntLE(q_circuit, number, qbitlist)

def UncomputeKetIntBE(q_circuit, number : int, qbitlist : list[int]):
    """
    Apply a quantum circuit to uncompute classical state, which is given by an integer with big-endian mode.

        e.g., 25 = 11001b --> q[0]=|1>, q[1]=|1>, q[2]=|0>, q[3]=|0>, q[4]=|1>

        q_circuit : applied quantum circuit
        number    : the integer to describe the state
        qbitlist  : index list of the target qubit array

    -> Return : q_circuit
    """
    return CreateKetIntBE(q_circuit, number, qbitlist)



def CreateKetIntPlusEPhiNegationLE(q_circuit, number : int, phi : float, qbitlist : list[int]):
    """
    Apply a quantum circuit to create state |x> + e^{iφ}|~x>, where ~x is the bitwise negation of x, and x is in little-endian mode.

        q_circuit : applied quantum circuit
        number    : x
        phi       : φ
        qbitlist  : index of target qubits

    -> Return : q_circuit
    """
    N = len(qbitlist)
    temp = number >> 1

    ApplyGate(q_circuit, 'H', [qbitlist[0]])
    if ((number & 1) == 1):
        ApplyGate(q_circuit, 'U1', [qbitlist[0]], [phi])
        for i in range(1, N):
            if ((temp & 1) == 0):
                ApplyGate(q_circuit, 'X', [qbitlist[i]])
            temp >>= 1
            ApplyGate(q_circuit, 'CX', [qbitlist[0], qbitlist[i]])
    else:
        ApplyGate(q_circuit, 'U1', [qbitlist[0]], [-phi])
        for i in range(1, N):
            if ((temp & 1) == 1):
                ApplyGate(q_circuit, 'X', [qbitlist[i]])
            temp >>= 1
            ApplyGate(q_circuit, 'CX', [qbitlist[0], qbitlist[i]])

    return q_circuit

def CreateKetIntPlusEPhiNegationBE(q_circuit, number : int, phi : float, qbitlist : list[int]):
    """
    Apply a quantum circuit to create state |x> + e^{iφ}|~x>, where ~x is the bitwise negation of x, and x is in big-endian mode.

        q_circuit : applied quantum circuit
        number    : x
        phi       : φ
        qbitlist  : index of target qubits

    -> Return : q_circuit
    """
    return Derivative(q_circuit, qbitlist, CreateKetIntPlusEPhiNegationLE, True, False, number, phi, qbitlist)

def UncomputeKetIntPlusEPhiNegationLE(q_circuit, number : int, phi : float, qbitlist : list[int]):
    """
    Apply a quantum circuit to uncompute state |x> + e^{iφ}|~x>, where ~x is the bitwise negation of x, and x is in little-endian mode.

        q_circuit : applied quantum circuit
        number    : x
        phi       : φ
        qbitlist  : index of target qubits

    -> Return : q_circuit
    """
    return Derivative(q_circuit, qbitlist, CreateKetIntPlusEPhiNegationLE, False, True, number, phi, qbitlist)

def UncomputeKetIntPlusEPhiNegationBE(q_circuit, number : int, phi : float, qbitlist : list[int]):
    """
    Apply a quantum circuit to uncompute state |x> + e^{iφ}|~x>, where ~x is the bitwise negation of x, and x is in big-endian mode.

        q_circuit : applied quantum circuit
        number    : x
        phi       : φ
        qbitlist  : index of target qubits

    -> Return : q_circuit
    """
    return Derivative(q_circuit, qbitlist, CreateKetIntPlusEPhiNegationLE, True, True, number, phi, qbitlist)



def CreateKetInt1PlusEPhiKetInt2LE(q_circuit, number1 : int, number2 : int, phi : float, qbitlist : list[int]):
    """
    Apply a quantum circuit to create state |x> + e^{iφ}|y>, where integers x and y are in little-endian.

        q_circuit : applied quantum circuit
        number1   : x
        number2   : y
        phi       : φ
        qbitlist  : index of target qubits

    -> Return : q_circuit
    """
    N = len(qbitlist)
    temp1 = number1
    temp2 = number2
    temp3 = 0
    difflist = []

    for i in range(0, N):
        if ((temp1 & 1) == (temp2 & 1)):
            if ((temp1 & 1) == 1):
                ApplyGate(q_circuit, 'X', [qbitlist[i]])
        else:
            temp3 |= ((temp1 & 1) << len(difflist))
            difflist.append(i)
        temp1 >>= 1
        temp2 >>= 1

    if (len(difflist) > 0):
        CreateKetIntPlusEPhiNegationLE(q_circuit, temp3, phi, difflist)
    return q_circuit

def CreateKetInt1PlusEPhiKetInt2BE(q_circuit, number1 : int, number2 : int, phi : float, qbitlist : list[int]):
    """
    Apply a quantum circuit to create state |x> + e^{iφ}|y>, where integers x and y are in big-endian.

        q_circuit : applied quantum circuit
        number1   : x
        number2   : y
        phi       : φ
        qbitlist  : index of target qubits

    -> Return : q_circuit
    """
    return Derivative(q_circuit, qbitlist, CreateKetInt1PlusEPhiKetInt2LE, True, False, number1, number2, phi, qbitlist)

def UncomputeKetInt1PlusEPhiKetInt2LE(q_circuit, number1 : int, number2 : int, phi : float, qbitlist : list[int]):
    """
    Apply a quantum circuit to uncompute state |x> + e^{iφ}|y>, where integers x and y are in little-endian.

        q_circuit : applied quantum circuit
        number1   : x
        number2   : y
        phi       : φ
        qbitlist  : index of target qubits

    -> Return : q_circuit
    """
    return Derivative(q_circuit, qbitlist, CreateKetInt1PlusEPhiKetInt2LE, False, True, number1, number2, phi, qbitlist)

def UncomputeKetInt1PlusEPhiKetInt2BE(q_circuit, number1 : int, number2 : int, phi : float, qbitlist : list[int]):
    """
    Apply a quantum circuit to uncompute state |x> + e^{iφ}|y>, where integers x and y are in big-endian.

        q_circuit : applied quantum circuit
        number1   : x
        number2   : y
        phi       : φ
        qbitlist  : index of target qubits

    -> Return : q_circuit
    """
    return Derivative(q_circuit, qbitlist, CreateKetInt1PlusEPhiKetInt2LE, True, True, number1, number2, phi, qbitlist)
