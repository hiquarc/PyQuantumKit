# library/qft.py
#    2025/6/27
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

import math
from pyquantumkit.procedure.generic import apply_gate, apply_reverse, derivative
from pyquantumkit.procedure.derivative import derivative
from qiskit.circuit.library import QFT


def pqk_qft_bilo(q_circuit, qbitlist : list[int]):
    """
    Append Quantum Fourier Transfrom (QFT) cirucit which is built in PyQuantumKit with BILO mode

        BILO : the input integer is encoded as big-endian mode (BI),
               the output state is encoded as little-endian mode (LO).

        q_circuit : applied quantum circuit
        qbitlist  : index list of the target qubit array

    -> Return : q_circuit
    """
    N = len(qbitlist)
    for i in range(0, N):
        apply_gate(q_circuit, 'H', [qbitlist[i]])
        for j in range(i + 1, N):
            theta = math.pi / (2 ** (j - i))
            apply_gate(q_circuit, 'CU1', [qbitlist[j], qbitlist[i]], [theta])
    return q_circuit

def pqk_iqft_libo(q_circuit, qbitlist : list[int]):
    """
    Append Inverse Quantum Fourier Transfrom (IQFT) cirucit which is built in PyQuantumKit with LIBO mode

        LIBO : the input integer is encoded as little-endian mode (LI),
               the output state is encoded as big-endian mode (BO).

        NOTE : this circuit is the inverse of QFT with BILO mode!

        q_circuit : applied quantum circuit
        qbitlist  : index list of the target qubit array

    -> Return : q_circuit
    """
    return derivative(q_circuit, qbitlist, pqk_qft_bilo, False, True, q_circuit, qbitlist)


def pqk_qft_bibo(q_circuit, qbitlist : list[int]):
    """
    Append Quantum Fourier Transfrom (QFT) cirucit which is built in PyQuantumKit with BIBO mode

        BIBO : the input integer is encoded as big-endian mode (BI),
               the output state is encoded as big-endian mode (BO).

        q_circuit : applied quantum circuit
        qbitlist  : index list of the target qubit array

    -> Return : q_circuit
    """
    pqk_qft_bilo(q_circuit, qbitlist)
    apply_reverse(q_circuit, qbitlist)
    return q_circuit

def pqk_iqft_bibo(q_circuit, qbitlist : list[int]):
    """
    Append Inverse Quantum Fourier Transfrom (IQFT) cirucit which is built in PyQuantumKit with BIBO mode

        BIBO : the input integer is encoded as big-endian mode (BI),
               the output state is encoded as big-endian mode (BO).

        NOTE : this circuit is the inverse of QFT with BIBO mode!

        q_circuit : applied quantum circuit
        qbitlist  : index list of the target qubit array

    -> Return : q_circuit
    """
    return derivative(q_circuit, qbitlist, pqk_qft_bibo, False, True, q_circuit, qbitlist)


def pqk_qft_libo(q_circuit, qbitlist : list[int]):
    """
    Append Quantum Fourier Transfrom (QFT) cirucit which is built in PyQuantumKit with LIBO mode

        LIBO : the input integer is encoded as little-endian mode (LI),
               the output state is encoded as big-endian mode (BO).

        q_circuit : applied quantum circuit
        qbitlist  : index list of the target qubit array

    -> Return : q_circuit
    """
    return derivative(q_circuit, qbitlist, pqk_qft_bilo, True, False, q_circuit, qbitlist)

def pqk_iqft_bilo(q_circuit, qbitlist : list[int]):
    """
    Append Inverse Quantum Fourier Transfrom (IQFT) cirucit which is built in PyQuantumKit with BILO mode

        BILO : the input integer is encoded as big-endian mode (BI),
               the output state is encoded as little-endian mode (LO).

        NOTE : this circuit is the inverse of QFT with LIBO mode!

        q_circuit : applied quantum circuit
        qbitlist  : index list of the target qubit array

    -> Return : q_circuit
    """
    return derivative(q_circuit, qbitlist, pqk_qft_bilo, True, True, q_circuit, qbitlist)


def pqk_qft_lilo(q_circuit, qbitlist : list[int]):
    """
    Append Quantum Fourier Transfrom (QFT) cirucit which is built in PyQuantumKit with LILO mode

        LILO : the input integer is encoded as little-endian mode (LI),
               the output state is encoded as little-endian mode (LO).

        q_circuit : applied quantum circuit
        qbitlist  : index list of the target qubit array

    -> Return : q_circuit
    """
    return derivative(q_circuit, qbitlist, pqk_qft_bibo, True, False, q_circuit, qbitlist)

def pqk_iqft_lilo(q_circuit, qbitlist : list[int]):
    """
    Append Inverse Quantum Fourier Transfrom (IQFT) cirucit which is built in PyQuantumKit with LILO mode

        LILO : the input integer is encoded as little-endian mode (LI),
               the output state is encoded as little-endian mode (LO).

        NOTE : this circuit is the inverse of QFT with LILO mode!

        q_circuit : applied quantum circuit
        qbitlist  : index list of the target qubit array

    -> Return : q_circuit
    """
    return derivative(q_circuit, qbitlist, pqk_qft_bibo, True, True, q_circuit, qbitlist)
