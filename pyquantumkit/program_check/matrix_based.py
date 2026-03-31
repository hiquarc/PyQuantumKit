# program_check/matrix_based.py
#    2025/12/29
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

import numpy
import numpy.linalg

# Default epsilon
DEFAULT_TOLERANCE = 0.001

# Built-in norms in numpy
def numpy_frobenius_norm(mat : numpy.array) -> float:
    return numpy.linalg.norm(mat, 'fro')
def numpy_1_norm(mat : numpy.array) -> float:
    return numpy.linalg.norm(mat, 1)
def numpy_2_norm(mat : numpy.array) -> float:
    return numpy.linalg.norm(mat, 2)
def numpy_inf_norm(mat : numpy.array) -> float:
    return numpy.linalg.norm(mat, numpy.inf)


def numeric_equivalence_check(cirmat1 : numpy.array, cirmat2 : numpy.array, ignore_global_phase : bool = True,
                              tolerance : float = DEFAULT_TOLERANCE, norm = numpy_2_norm) -> bool:
    """
    Equivalence checking based on the norm of matrices difference of two circuits.

        cirmat1   : the numpy matrix first quantum program.
        cirmat2   : the numpy matrix second quantum program.
        ignore_global_phase : (bool) whether to ignore the global phase in judgment, default True.
        tolerance : (float) the judgment threshold.
        norm      : the norm function (matrix -> float) to be used, default numpy_2_norm.

            Other built-in norms: numpy_1_norm, numpy_frobenius_norm, numpy_inf_norm

    -> Return : True if cirmat1 is equivalence to cirmat2; otherwise False.
    """
    fact_cirmat2 = cirmat2
    if ignore_global_phase:
        magnitudes = numpy.abs(cirmat2)
        max_index = numpy.unravel_index(numpy.argmax(magnitudes), magnitudes.shape)
        factor = cirmat1[max_index] / cirmat2[max_index]
        fact_cirmat2 *= factor
    if norm(cirmat1 - fact_cirmat2) > tolerance:
        return False
    return True

def numeric_identity_check(cirmat : numpy.array, ignore_global_phase : bool = True,
                           tolerance : float = DEFAULT_TOLERANCE, norm = numpy_2_norm) -> bool:
    """
    Identity checking based on the norm of matrices difference of target circuit and identity.

        cirmat    : the numpy matrix of target quantum program.
        ignore_global_phase : (bool) whether to ignore the global phase in judgment, default True.
        tolerance : (float) the judgment threshold.
        norm      : the norm function (matrix -> float) to be used, default numpy_2_norm.

            Other built-in norms: numpy_1_norm, numpy_frobenius_norm, numpy_inf_norm

    -> Return : True if cirmat is equivalence to identity; otherwise False.
    """
    matid = numpy.eye(cirmat.shape[0], dtype=cirmat.dtype)
    return numeric_equivalence_check(matid, cirmat, ignore_global_phase, tolerance, norm)
