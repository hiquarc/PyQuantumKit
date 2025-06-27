# QProcedure/Paulis.py
#    2025/6/13
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from pyquantumkit.procedure.generic import apply_gate, apply_measure

Pauli_Strings = ['I', 'X', 'Y', 'Z']

def apply_measure_x(q_circuit, qindex : list[int], cindex : list[int]):
    apply_gate(q_circuit, 'H', qindex)
    return apply_measure(q_circuit, qindex, cindex)

def apply_measure_y(q_circuit, qindex : list[int], cindex : list[int]):
    apply_gate(q_circuit, 'SD', qindex)
    apply_gate(q_circuit, 'H', qindex)
    return apply_measure(q_circuit, qindex, cindex)

def apply_measure_z(q_circuit, qindex : list[int], cindex : list[int]):
    return apply_measure(q_circuit, qindex, cindex)

