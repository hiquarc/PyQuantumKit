# symbol/qstate.py
#    2025/12/26
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

import sympy

# Ket representation (column vector): |0>, |1>, |+>, |->
Ket0 = sympy.Matrix([[1], [0]])
Ket1 = sympy.Matrix([[0], [1]])
KetPlus = 1 / sympy.sqrt(2) * sympy.Matrix([[1], [1]])
KetMinus = 1 / sympy.sqrt(2) * sympy.Matrix([[1], [-1]])
# Bra representation (row vector): <0|, <1|, <+|, <-|
Bra0 = sympy.Matrix([[1, 0]])
Bra1 = sympy.Matrix([[0, 1]])
BraPlus = 1 / sympy.sqrt(2) * sympy.Matrix([[1, 1]])
BraMinus = 1 / sympy.sqrt(2) * sympy.Matrix([[1, -1]])
# Density matrix representation: |0><0|, |1><1|, |+><+|, |-><-|
Rho0 = Ket0 * Bra0
Rho1 = Ket1 * Bra1
RhoPlus = KetPlus * BraPlus
RhoMinus = KetMinus * BraMinus

# State vectors for Bell states
# Ket
KetBell = 1 / sympy.sqrt(2) * sympy.Matrix([[1], [0], [0], [1]])
KetBell01 = 1 / sympy.sqrt(2) * sympy.Matrix([[0], [1], [1], [0]])
KetBell10 = 1 / sympy.sqrt(2) * sympy.Matrix([[1], [0], [0], [-1]])
KetBell11 = 1 / sympy.sqrt(2) * sympy.Matrix([[0], [1], [-1], [0]])
# Bra
BraBell = 1 / sympy.sqrt(2) * sympy.Matrix([[1, 0, 0, 1]])
BraBell01 = 1 / sympy.sqrt(2) * sympy.Matrix([[0, 1, 1, 0]])
BraBell10 = 1 / sympy.sqrt(2) * sympy.Matrix([[1, 0, 0, -1]])
BraBell11 = 1 / sympy.sqrt(2) * sympy.Matrix([[0, 1, -1, 0]])
# Density Matrix
RhoBell = KetBell * BraBell
RhoBell01 = KetBell01 * BraBell01
RhoBell10 = KetBell10 * BraBell10
RhoBell11 = KetBell11 * BraBell11

# State vectors for state on Bloch sphere
def KetBloch(theta_, phi_, gamma_) -> sympy.Matrix:
    return sympy.exp(sympy.I * gamma_) * sympy.Matrix([[sympy.cos(theta_ / 2)],
                                                       [sympy.exp(sympy.I * phi_) * sympy.sin(theta_ / 2)]])
def BraBloch(theta_, phi_, gamma_) -> sympy.Matrix:
    return sympy.exp(-sympy.I * gamma_) * sympy.Matrix([[sympy.cos(theta_ / 2),
                                                        sympy.exp(-sympy.I * phi_) * sympy.sin(theta_ / 2)]])
def RhoBloch(theta_, phi_, gamma_) -> sympy.Matrix:
    return KetBloch(theta_, phi_, gamma_) * BraBloch(theta_, phi_, gamma_)

# State vectors for all-zero state
def KetAllZero(nqbits : int) -> sympy.Matrix:
    ret = sympy.zeros(2 ** nqbits, 1)
    ret[0, 0] = 1
    return ret
def BraAllZero(nqbits : int) -> sympy.Matrix:
    ret = sympy.zeros(1, 2 ** nqbits)
    ret[0, 0] = 1
    return ret
def RhoAllZero(nqbits : int) -> sympy.Matrix:
    ret = sympy.zeros(2 ** nqbits, 2 ** nqbits)
    ret[0, 0] = 1
    return ret

# State vectors for uniform superposition 
def KetUniformSuperposition(nqbits : int) -> sympy.Matrix:
    ret = 1 / sympy.sqrt(2 ** nqbits) * sympy.ones(2 ** nqbits, 1)
    return ret
def BraUniformSuperposition(nqbits : int) -> sympy.Matrix:
    ret = 1 / sympy.sqrt(2 ** nqbits) * sympy.ones(1, 2 ** nqbits)
    return ret
def RhoUniformSuperposition(nqbits : int) -> sympy.Matrix:
    ret = 1 / (2 ** nqbits) * sympy.ones(2 ** nqbits, 2 ** nqbits)
    return ret
