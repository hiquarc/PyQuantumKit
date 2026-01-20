# program_check/matrix_based.py
#    2025/12/29
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

import sympy, numpy
from pyquantumkit import PyQuantumKitError
from pyquantumkit.procedure.circuit_io import CircuitIO
from pyquantumkit.symbol.circuit import symbol_apply_gate

# NOTE: this module is in developing!

# def symbol_equivalence_check(circuit1 : sympy.MatrixBase | CircuitIO,
#                              circuit2 : sympy.MatrixBase | CircuitIO,
#                              ignore_global_phase : bool = True):
#     mat1 = None
#     mat2 = None
#     if isinstance(circuit1, sympy.MatrixBase):
#         mat1 = circuit1.simplify()
#     elif isinstance(circuit1, CircuitIO):
#         if circuit1.contains_measure():
#             raise PyQuantumKitError("symbol_equivalence_check function cannot check the equivalence of circuits with measurement!")
#         mat1 = circuit1.get_sympy_matrix()
#     if isinstance(circuit2, sympy.MatrixBase):
#         mat2 = circuit2.simplify()
#     elif isinstance(circuit2, CircuitIO):
#         if circuit2.contains_measure():
#             raise PyQuantumKitError("symbol_equivalence_check function cannot check the equivalence of circuits with measurement!")
#         mat2 = circuit2.get_sympy_matrix()
    
#     if mat1.shape != mat2.shape:
#         return False
#     if ignore_global_phase:
#         ratio = None
#         for i in mat1.rows:
#             for j in mat1.cols:
#                 if (mat1[i, j] == 0 and mat2[i, j] != 0) or (mat1[i, j] != 0 and mat2[i, j] == 0):
#                     return False
#                 if mat1[i, j] != 0 and mat2[i, j] != 0:
#                     if ratio is None:
#                         ratio = sympy.simplify(mat1[i, j] / mat2[i, j])
#                     else:
#                         if sympy.simplify(mat2[i, j] * ratio - mat1[i, j]) != 0:
#                             return False
#         return True
#     else:
#         diff = sympy.simplify(mat1 - mat2)
#         return mat1.is_zero_matrix


# def symbol_identity_check(circuit : sympy.MatrixBase | CircuitIO,
#                           ignore_global_phase : bool = True):
#     mat = None
#     if isinstance(circuit, sympy.MatrixBase):
#         mat = circuit.simplify()
#     elif isinstance(circuit, CircuitIO):
#         if circuit.contains_measure():
#             return False
#         mat = circuit.get_sympy_matrix()
    
#     if not mat.is_square:
#         return False
#     if ignore_global_phase:
#         if not mat.is_diagonal():
#             return False
#         else:
#             for i in range(1, mat.cols):
#                 if sympy.simplify(mat[i, i] - mat[i - 1, i - 1]) != 0:
#                     return False
#             return True
#     else:
#         return mat.is_Identity


def numeric_equivalence_check(circuit1 : numpy.matrix | CircuitIO,
                              circuit2 : numpy.matrix | CircuitIO,
                              epsilon : float) -> bool:
    pass

def numeric_identity_check(circuit : numpy.matrix | CircuitIO,
                           epsilon : float) -> bool:
    pass
