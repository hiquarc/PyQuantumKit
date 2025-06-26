# state_prepare/int_state.py
#    2025/6/11
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from pyquantumkit.procedure.generic import apply_gate, derivative

def create_ket_int_le(q_circuit, number : int, qbitlist : list[int]):
    """
    Apply a quantum circuit to create classical state, which is given by an integer with little-endian mode.

        e.g., 25 = 11001b --> q[0]=|1>, q[1]=|0>, q[2]=|0>, q[3]=|1>, q[4]=|1>

        NOTE: if number >= 2**len(qbitlist), the high bits of <number> will be discarded

        q_circuit : applied quantum circuit
        number    : the integer to describe the state
        qbitlist  : index list of the target qubit array

    -> Return : q_circuit
    """
    if number < 0:
        raise ValueError('<number> must be a non-negative integer!')
    if qbitlist is None or len(qbitlist) <= 0:
        raise ValueError('<qbitlist> must be an non-empty list!')
    N = len(qbitlist)
    temp = number

    for i in range(0, N):
        if ((temp & 1) == 1):
            apply_gate(q_circuit, 'X', [qbitlist[i]])
        temp >>= 1
    return q_circuit

def create_ket_int_be(q_circuit, number : int, qbitlist : list[int]):
    """
    Apply a quantum circuit to create classical state, which is given by an integer with big-endian mode.

        e.g., 25 = 11001b --> q[0]=|1>, q[1]=|1>, q[2]=|0>, q[3]=|0>, q[4]=|1>

        NOTE: if number >= 2**len(qbitlist), the high bits of <number> will be discarded

        q_circuit : applied quantum circuit
        number    : the integer to describe the state
        qbitlist  : index list of the target qubit array

    -> Return : q_circuit
    """
    return derivative(q_circuit, qbitlist, create_ket_int_le, True, False, number, qbitlist)

def uncompute_ket_int_le(q_circuit, number : int, qbitlist : list[int]):
    """
    Apply a quantum circuit to uncompute classical state, which is given by an integer with little-endian mode.

        e.g., 25 = 11001b --> q[0]=|1>, q[1]=|0>, q[2]=|0>, q[3]=|1>, q[4]=|1>

        NOTE: if number >= 2**len(qbitlist), the high bits of <number> will be discarded

        q_circuit : applied quantum circuit
        number    : the integer to describe the state
        qbitlist  : index list of the target qubit array

    -> Return : q_circuit
    """
    return create_ket_int_le(q_circuit, number, qbitlist)

def uncompute_ket_int_be(q_circuit, number : int, qbitlist : list[int]):
    """
    Apply a quantum circuit to uncompute classical state, which is given by an integer with big-endian mode.

        e.g., 25 = 11001b --> q[0]=|1>, q[1]=|1>, q[2]=|0>, q[3]=|0>, q[4]=|1>

        NOTE: if number >= 2**len(qbitlist), the high bits of <number> will be discarded

        q_circuit : applied quantum circuit
        number    : the integer to describe the state
        qbitlist  : index list of the target qubit array

    -> Return : q_circuit
    """
    return create_ket_int_be(q_circuit, number, qbitlist)



def create_ket_int_plus_eiphi_neg_le(q_circuit, number : int, phi : float, qbitlist : list[int]):
    """
    Apply a quantum circuit to create state |x> + e^{iφ}|~x>, where ~x is the bitwise negation of x, and x is in little-endian mode.

        e.g. 25 = 11001b --> |10011> + e^{iφ}|01100>

        NOTE: if number >= 2**len(qbitlist), the high bits of <number> will be discarded

        q_circuit : applied quantum circuit
        number    : x
        phi       : φ
        qbitlist  : index of target qubits

    -> Return : q_circuit
    """
    if number < 0:
        raise ValueError('<number> must be a non-negative integer!')
    if qbitlist is None or len(qbitlist) <= 0:
        raise ValueError('<qbitlist> must be an non-empty list!')
    N = len(qbitlist)
    temp = number >> 1

    apply_gate(q_circuit, 'H', [qbitlist[0]])
    if ((number & 1) == 1):
        apply_gate(q_circuit, 'U1', [qbitlist[0]], [phi])
        for i in range(1, N):
            if ((temp & 1) == 0):
                apply_gate(q_circuit, 'X', [qbitlist[i]])
            temp >>= 1
            apply_gate(q_circuit, 'CX', [qbitlist[0], qbitlist[i]])
    else:
        apply_gate(q_circuit, 'U1', [qbitlist[0]], [-phi])
        for i in range(1, N):
            if ((temp & 1) == 1):
                apply_gate(q_circuit, 'X', [qbitlist[i]])
            temp >>= 1
            apply_gate(q_circuit, 'CX', [qbitlist[0], qbitlist[i]])

    return q_circuit

def create_ket_int_plus_eiphi_neg_be(q_circuit, number : int, phi : float, qbitlist : list[int]):
    """
    Apply a quantum circuit to create state |x> + e^{iφ}|~x>, where ~x is the bitwise negation of x, and x is in big-endian mode.

        e.g. 25 = 11001b --> |11001> + e^{iφ}|00110>

        NOTE: if number >= 2**len(qbitlist), the high bits of <number> will be discarded

        q_circuit : applied quantum circuit
        number    : x
        phi       : φ
        qbitlist  : index of target qubits

    -> Return : q_circuit
    """
    return derivative(q_circuit, qbitlist, create_ket_int_plus_eiphi_neg_le, True, False, number, phi, qbitlist)

def uncompute_ket_int_plus_eiphi_neg_le(q_circuit, number : int, phi : float, qbitlist : list[int]):
    """
    Apply a quantum circuit to uncompute state |x> + e^{iφ}|~x>, where ~x is the bitwise negation of x, and x is in little-endian mode.

        NOTE: if number >= 2**len(qbitlist), the high bits of <number> will be discarded

        q_circuit : applied quantum circuit
        number    : x
        phi       : φ
        qbitlist  : index of target qubits

    -> Return : q_circuit
    """
    return derivative(q_circuit, qbitlist, create_ket_int_plus_eiphi_neg_le, False, True, number, phi, qbitlist)

def uncompute_ket_int_plus_eiphi_neg_be(q_circuit, number : int, phi : float, qbitlist : list[int]):
    """
    Apply a quantum circuit to uncompute state |x> + e^{iφ}|~x>, where ~x is the bitwise negation of x, and x is in big-endian mode.

        NOTE: if number >= 2**len(qbitlist), the high bits of <number> will be discarded

        q_circuit : applied quantum circuit
        number    : x
        phi       : φ
        qbitlist  : index of target qubits

    -> Return : q_circuit
    """
    return derivative(q_circuit, qbitlist, create_ket_int_plus_eiphi_neg_le, True, True, number, phi, qbitlist)



def create_ket_int1_plus_eiphi_ket_int2_le(q_circuit, number1 : int, number2 : int, phi : float, qbitlist : list[int]):
    """
    Apply a quantum circuit to create state |x> + e^{iφ}|y>, where integers x and y are in little-endian.

        NOTE: if number1/2 >= 2**len(qbitlist), the high bits of <number1/2> will be discarded

        q_circuit : applied quantum circuit
        number1   : x
        number2   : y
        phi       : φ
        qbitlist  : index of target qubits

    -> Return : q_circuit
    """
    if number1 < 0 or number2 < 0:
        raise ValueError('<number1>,<number2> must be non-negative integers!')
    if qbitlist is None or len(qbitlist) <= 0:
        raise ValueError('<qbitlist> must be an non-empty list!')
    N = len(qbitlist)
    temp1 = number1
    temp2 = number2
    temp3 = 0
    difflist = []

    for i in range(0, N):
        if ((temp1 & 1) == (temp2 & 1)):
            if ((temp1 & 1) == 1):
                apply_gate(q_circuit, 'X', [qbitlist[i]])
        else:
            temp3 |= ((temp1 & 1) << len(difflist))
            difflist.append(i)
        temp1 >>= 1
        temp2 >>= 1

    if (len(difflist) > 0):
        create_ket_int_plus_eiphi_neg_le(q_circuit, temp3, phi, difflist)
    return q_circuit

def create_ket_int1_plus_eiphi_ket_int2_be(q_circuit, number1 : int, number2 : int, phi : float, qbitlist : list[int]):
    """
    Apply a quantum circuit to create state |x> + e^{iφ}|y>, where integers x and y are in big-endian.

        NOTE: if number1/2 >= 2**len(qbitlist), the high bits of <number1/2> will be discarded

        q_circuit : applied quantum circuit
        number1   : x
        number2   : y
        phi       : φ
        qbitlist  : index of target qubits

    -> Return : q_circuit
    """
    return derivative(q_circuit, qbitlist, create_ket_int1_plus_eiphi_ket_int2_le, True, False, number1, number2, phi, qbitlist)

def uncompute_ket_int1_plus_eiphi_ket_int2_le(q_circuit, number1 : int, number2 : int, phi : float, qbitlist : list[int]):
    """
    Apply a quantum circuit to uncompute state |x> + e^{iφ}|y>, where integers x and y are in little-endian.

        NOTE: if number1/2 >= 2**len(qbitlist), the high bits of <number1/2> will be discarded

        q_circuit : applied quantum circuit
        number1   : x
        number2   : y
        phi       : φ
        qbitlist  : index of target qubits

    -> Return : q_circuit
    """
    return derivative(q_circuit, qbitlist, create_ket_int1_plus_eiphi_ket_int2_le, False, True, number1, number2, phi, qbitlist)

def uncompute_ket_int1_plus_eiphi_ket_int2_be(q_circuit, number1 : int, number2 : int, phi : float, qbitlist : list[int]):
    """
    Apply a quantum circuit to uncompute state |x> + e^{iφ}|y>, where integers x and y are in big-endian.

        NOTE: if number1/2 >= 2**len(qbitlist), the high bits of <number1/2> will be discarded

        q_circuit : applied quantum circuit
        number1   : x
        number2   : y
        phi       : φ
        qbitlist  : index of target qubits

    -> Return : q_circuit
    """
    return derivative(q_circuit, qbitlist, create_ket_int1_plus_eiphi_ket_int2_le, True, True, number1, number2, phi, qbitlist)
