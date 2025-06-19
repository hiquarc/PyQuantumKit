# QProcedure/Paulis.py
#    2025/6/13
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from .Common import *

Pauli_Strings = ['I', 'X', 'Y', 'Z']

def ApplyMeasureX(q_circuit, qindex : list[int], cindex : list[int]):
    ApplyGate(q_circuit, 'H', qindex)
    return ApplyMeasure(q_circuit, qindex, cindex)

def ApplyMeasureY(q_circuit, qindex : list[int], cindex : list[int]):
    ApplyGate(q_circuit, 'SD', qindex)
    ApplyGate(q_circuit, 'H', qindex)
    return ApplyMeasure(q_circuit, qindex, cindex)

def ApplyMeasureZ(q_circuit, qindex : list[int], cindex : list[int]):
    return ApplyMeasure(q_circuit, qindex, cindex)

