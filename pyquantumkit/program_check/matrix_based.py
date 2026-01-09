# program_check/matrix_based.py
#    2025/12/29
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

import sympy
from pyquantumkit.procedure.circuit_io import CircuitIO
from pyquantumkit.symbol.circuit import symbol_apply_gate

def matrix_equivalence_check(circuit1 : sympy.MatrixBase | CircuitIO,
                             circuit2 : sympy.MatrixBase | CircuitIO,
                             epsilon : float):
    pass

def matrix_identity_check(circuit : sympy.MatrixBase | CircuitIO, epsilon : float):
    pass
