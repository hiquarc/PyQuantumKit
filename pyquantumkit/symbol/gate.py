# symbol/gate.py
#    2025/12/15
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

import sympy
from pyquantumkit import PyQuantumKitError
from pyquantumkit._qframes.code_translate import get_standard_gatename
from pyquantumkit.classical.common import reverse_endianness, dim2nbits

# Matrices for basic single-qubit gates
Id = sympy.Matrix([[1, 0],
                   [0, 1]])
X = sympy.Matrix([[0, 1],
                  [1, 0]])
Y = sympy.Matrix([[0, -sympy.I * 1],
                  [sympy.I * 1, 0]])
Z = sympy.Matrix([[1, 0],
                  [0, -1]])
S = sympy.Matrix([[1, 0],
                  [0, sympy.I]])
T = sympy.Matrix([[1, 0],
                  [0, sympy.exp(sympy.I * sympy.pi / 4)]])
H = 1 / sympy.sqrt(2) * sympy.Matrix([[1, 1],
                                      [1, -1]])
Sdag = sympy.Matrix([[1, 0],
                     [0, -sympy.I]])
Tdag = sympy.Matrix([[1, 0],
                     [0, sympy.exp(-sympy.I * sympy.pi / 4)]])

# Matrices for two-qubit gates
CNOT = sympy.Matrix([[1, 0, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, 0, 1],
                     [0, 0, 1, 0]])
CNOT21 = sympy.Matrix([[1, 0, 0, 0],
                       [0, 0, 0, 1],
                       [0, 0, 1, 0],
                       [0, 1, 0, 0]])
SWAP = sympy.Matrix([[1, 0, 0, 0],
                     [0, 0, 1, 0],
                     [0, 1, 0, 0],
                     [0, 0, 0, 1]])
CZ = sympy.Matrix([[1, 0, 0, 0],
                   [0, 1, 0, 0],
                   [0, 0, 1, 0],
                   [0, 0, 0, -1]])
iSWAP = sympy.Matrix([[1, 0, 0, 0],
                      [0, 0, sympy.I, 0],
                      [0, sympy.I, 0, 0],
                      [0, 0, 0, 1]])

# Matrices for three-qubit gates
Toffoli = sympy.Matrix([[1, 0, 0, 0, 0, 0, 0, 0],
                        [0, 1, 0, 0, 0, 0, 0, 0],
                        [0, 0, 1, 0, 0, 0, 0, 0],
                        [0, 0, 0, 1, 0, 0, 0, 0],
                        [0, 0, 0, 0, 1, 0, 0, 0],
                        [0, 0, 0, 0, 0, 1, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 1],
                        [0, 0, 0, 0, 0, 0, 1, 0]])
Fredkin = sympy.Matrix([[1, 0, 0, 0, 0, 0, 0, 0],
                        [0, 1, 0, 0, 0, 0, 0, 0],
                        [0, 0, 1, 0, 0, 0, 0, 0],
                        [0, 0, 0, 1, 0, 0, 0, 0],
                        [0, 0, 0, 0, 1, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 1, 0],
                        [0, 0, 0, 0, 0, 1, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 1]])
CCZ = sympy.Matrix([[1, 0, 0, 0, 0, 0, 0, 0],
                    [0, 1, 0, 0, 0, 0, 0, 0],
                    [0, 0, 1, 0, 0, 0, 0, 0],
                    [0, 0, 0, 1, 0, 0, 0, 0],
                    [0, 0, 0, 0, 1, 0, 0, 0],
                    [0, 0, 0, 0, 0, 1, 0, 0],
                    [0, 0, 0, 0, 0, 0, 1, 0],
                    [0, 0, 0, 0, 0, 0, 0, -1]])

# Matrices for rotation gates
def Rx(theta_) -> sympy.Matrix:
    return sympy.Matrix([[sympy.cos(theta_ / 2), -sympy.I * sympy.sin(theta_ / 2)],
                         [-sympy.I * sympy.sin(theta_ / 2), sympy.cos(theta_ / 2)]])
def Ry(theta_) -> sympy.Matrix:
    return sympy.Matrix([[sympy.cos(theta_ / 2), -sympy.sin(theta_ / 2)],
                         [sympy.sin(theta_ / 2), sympy.cos(theta_ / 2)]])
def Rz(theta_) -> sympy.Matrix:
    return sympy.Matrix([[sympy.exp(-sympy.I * theta_ / 2), 0],
                         [0, sympy.exp(sympy.I * theta_ / 2)]])
def U1(theta_) -> sympy.Matrix:
    return sympy.Matrix([[1, 0],
                         [0, sympy.exp(sympy.I * theta_)]])
def U3(theta_, phi_, lambda_) -> sympy.Matrix:
    return sympy.Matrix([[sympy.cos(theta_ / 2), -sympy.exp(sympy.I * lambda_) * sympy.sin(theta_ / 2)],
            [sympy.exp(sympy.I * phi_) * sympy.sin(theta_ / 2), sympy.exp(sympy.I * (lambda_ + phi_)) * sympy.cos(theta_ / 2)]])

def Rxx(theta_) -> sympy.Matrix:
    return sympy.Matrix([[sympy.cos(theta_ / 2), 0, 0, -sympy.I * sympy.sin(theta_ / 2)],
                         [0, sympy.cos(theta_ / 2), -sympy.I * sympy.sin(theta_ / 2), 0],
                         [0, -sympy.I * sympy.sin(theta_ / 2), sympy.cos(theta_ / 2), 0],
                         [-sympy.I * sympy.sin(theta_ / 2), 0, 0, sympy.cos(theta_ / 2)]])
def Ryy(theta_) -> sympy.Matrix:
    return sympy.Matrix([[sympy.cos(theta_ / 2), 0, 0, sympy.I * sympy.sin(theta_ / 2)],
                         [0, sympy.cos(theta_ / 2), -sympy.I * sympy.sin(theta_ / 2), 0],
                         [0, -sympy.I * sympy.sin(theta_ / 2), sympy.cos(theta_ / 2), 0],
                         [sympy.I * sympy.sin(theta_ / 2), 0, 0, sympy.cos(theta_ / 2)]])
def Rzz(theta_) -> sympy.Matrix:
    return sympy.Matrix([[sympy.exp(-sympy.I * theta_ / 2), 0, 0, 0],
                         [0, sympy.exp(sympy.I * theta_ / 2), 0, 0],
                         [0, 0, sympy.exp(sympy.I * theta_ / 2), 0],
                         [0, 0, 0, sympy.exp(-sympy.I * theta_ / 2)]])

# Matrices for other controlled gates
CH = sympy.Matrix([[1, 0, 0, 0],
                   [0, 1, 0, 0],
                   [0, 0, 1 / sympy.sqrt(2), 1 / sympy.sqrt(2)],
                   [0, 0, 1 / sympy.sqrt(2), -1 / sympy.sqrt(2)]])
CY = sympy.Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, -sympy.I], [0, 0, sympy.I, 0]])
def CRx(theta_) -> sympy.Matrix:
    return sympy.Matrix([[1, 0, 0, 0],
                         [0, 1, 0, 0],
                         [0, 0, sympy.cos(theta_ / 2), -sympy.I * sympy.sin(theta_ / 2)],
                         [0, 0, -sympy.I * sympy.sin(theta_ / 2), sympy.cos(theta_ / 2)]])
def CRy(theta_) -> sympy.Matrix:
    return sympy.Matrix([[1, 0, 0, 0],
                         [0, 1, 0, 0], 
                         [0, 0, sympy.cos(theta_ / 2), -sympy.sin(theta_ / 2)],
                         [0, 0, sympy.sin(theta_ / 2), sympy.cos(theta_ / 2)]])
def CRz(theta_) -> sympy.Matrix:
    return sympy.Matrix([[1, 0, 0, 0],
                         [0, 1, 0, 0],
                         [0, 0, sympy.exp(-sympy.I * theta_ / 2), 0],
                         [0, 0, 0, sympy.exp(sympy.I * theta_ / 2)]])
def CU1(theta_) -> sympy.Matrix:
    return sympy.Matrix([[1, 0, 0, 0],
                         [0, 1, 0, 0],
                         [0, 0, 1, 0],
                         [0, 0, 0, sympy.exp(sympy.I * theta_)]])

# Other derived gates
SqrtX = H * S * H
SqrtXdag = H * Sdag * H


def symbol_gate_matrix(gatestr : str, paras : list = None) -> sympy.Matrix:
    """
    Given the supported gate string, return the gate matrix

    e.g. CNOT = [[1, 0, 0, 0]   <-- 00    0
                 [0, 1, 0, 0]   <-- 01    1
                 [0, 0, 0, 1]   <-- 10    2
                 [0, 0, 1, 0]]  <-- 11    3
    """
    g = get_standard_gatename(gatestr)
    if g == 'M':
        raise PyQuantumKitError("Measurement cannot be represented as a gate matrix!")

    if g == 'I':
        return Id
    if g == 'X':
        return X
    if g == 'Y':
        return Y
    if g == 'Z':
        return Z
    if g == 'S':
        return S
    if g == 'T':
        return T
    if g == 'H':
        return H
    if g == 'SD':
        return Sdag
    if g == 'TD':
        return Tdag
    
    if g == 'CX':
        return CNOT
    if g == 'CZ':
        return CZ
    if g == 'SW':
        return SWAP
    if g == 'ISW':
        return iSWAP
    if g == 'CSW':
        return Fredkin
    if g == 'CCX':
        return Toffoli
    if g == 'CCZ':
        return CCZ
    
    if g == 'RX':
        return Rx(paras[0])
    if g == 'RY':
        return Ry(paras[0])
    if g == 'RZ':
        return Rz(paras[0])
    if g == 'U1':
        return U1(paras[0])
    if g == 'U3':
        return U3(paras[0], paras[1], paras[2])
    if g == 'RXX':
        return Rxx(paras[0])
    if g == 'RYY':
        return Ryy(paras[0])
    if g == 'RZZ':
        return Rzz(paras[0])
    
    if g == 'CH':
        return CH
    if g == 'CY':
        return CY
    if g == 'CRX':
        return CRx(paras[0])
    if g == 'CRY':
        return CRy(paras[0])
    if g == 'CRZ':
        return CRz(paras[0])
    if g == 'CU1':
        return CU1(paras[0])


def symbol_inverse_gate(mat : sympy.MatrixBase) -> sympy.Matrix:
    """
    Return the matrix of the inverse gate
        NOTE: this function simply returns mat.H, without the judgment of unitarity.
    """
    return mat.H


def is_legal_gate_matrix(mat : sympy.MatrixBase) -> bool:
    """
    Judge whether the given matrix is a legal matrix for a quantum gate,
        i.e., it is a unitary square matrix
    """
    try:
        invmat = mat.inv()
        if sympy.simplify(invmat) == sympy.simplify(mat.H):
            return True
        return False
    except ValueError:
        return False


def reverse_matrix_endianness(mat : sympy.MatrixBase) -> sympy.Matrix:
    """
    Reverse the endianness of the indexes of the matrix of a gate

    e.g. CNOT = [[1, 0, 0, 0]   <-- 00    0
                 [0, 1, 0, 0]   <-- 01    1
                 [0, 0, 0, 1]   <-- 10    2
                 [0, 0, 1, 0]]  <-- 11    3

    reverse_matrix_endianness(CNOT) = CNOT21 = 
                [[1, 0, 0, 0]   <-- 00    0
                 [0, 0, 0, 1]   <-- 10    1
                 [0, 0, 1, 0]   <-- 01    2
                 [0, 1, 0, 0]]  <-- 11    3
    """
    (nrowbits, flag2) = dim2nbits(mat.rows)
    (ncolbits, flag1) = dim2nbits(mat.cols)
    ret = sympy.zeros(mat.rows, mat.cols)
    for i in range(mat.rows):
        reverse_i = reverse_endianness(i, nrowbits)
        for j in range(mat.cols):
            reverse_j = reverse_endianness(j, ncolbits)
            ret[i, j] = mat[reverse_i, reverse_j]
    return ret
