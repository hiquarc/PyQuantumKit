# QProcedure/Paulis.py
#    2025/6/13
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from .Common import *

Pauli_Strings = ['I', 'X', 'Y', 'Z']

def MeasureX(q_circuit, qindex : list[int], cindex : list[int]):
    ApplyGate(q_circuit, 'H', qindex)
    return Measure(q_circuit, qindex, cindex)

def MeasureY(q_circuit, qindex : list[int], cindex : list[int]):
    ApplyGate(q_circuit, 'SD', qindex)
    ApplyGate(q_circuit, 'H', qindex)
    return Measure(q_circuit, qindex, cindex)

def MeasureZ(q_circuit, qindex : list[int], cindex : list[int]):
    return Measure(q_circuit, qindex, cindex)

