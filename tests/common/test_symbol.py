# test: common/test_symbol.py
#    2025/12/25
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

import unittest as UT
from pyquantumkit.symbol.gate import *
from pyquantumkit.symbol.circuit import *
from .common import is_exception

# Symbols for gate parameters
theta_ = sympy.Symbol('theta', real = True)
phi_ = sympy.Symbol('phi', real = True)
lambda_ = sympy.Symbol('lambda', real = True)

# The elements in Python's dictionary must be hashable, so we use a string to represent a sympy.Matrix object.
def str2matrix_test(gatestr : str, paras : list = None) -> sympy.Matrix:
    if gatestr == 'CNOT21':
        return CNOT21
    if gatestr == 'GeneralTwoQubitGate':
        return sympy.Matrix([[11, 12, 13, 14],
                             [21, 22, 23, 24],
                             [31, 32, 33, 34],
                             [41, 42, 43, 44]])
    if gatestr == 'ReversedU':
        return sympy.Matrix([[11, 13, 12, 14],
                             [31, 33, 32, 34],
                             [21, 23, 22, 24],
                             [41, 43, 42, 44]])
    if gatestr == 'ControlledU':
        return sympy.Matrix([[1, 0, 0, 0, 0, 0, 0, 0],
                             [0, 1, 0, 0, 0, 0, 0, 0],
                             [0, 0, 1, 0, 0, 0, 0, 0],
                             [0, 0, 0, 1, 0, 0, 0, 0],
                             [0, 0, 0, 0, 11, 12, 13, 14],
                             [0, 0, 0, 0, 21, 22, 23, 24],
                             [0, 0, 0, 0, 31, 32, 33, 34],
                             [0, 0, 0, 0, 41, 42, 43, 44]])
    if gatestr == 'ApplyCUon021':
        return sympy.Matrix([[1, 0, 0, 0, 0, 0, 0, 0],
                             [0, 1, 0, 0, 0, 0, 0, 0],
                             [0, 0, 1, 0, 0, 0, 0, 0],
                             [0, 0, 0, 1, 0, 0, 0, 0],
                             [0, 0, 0, 0, 11, 13, 12, 14],
                             [0, 0, 0, 0, 31, 33, 32, 34],
                             [0, 0, 0, 0, 21, 23, 22, 24],
                             [0, 0, 0, 0, 41, 43, 42, 44]])
    if gatestr == 'ApplyCUon102':
        return sympy.Matrix([[1, 0, 0, 0, 0, 0, 0, 0],
                             [0, 1, 0, 0, 0, 0, 0, 0],
                             [0, 0, 11, 12, 0, 0, 13, 14],
                             [0, 0, 21, 22, 0, 0, 23, 24],
                             [0, 0,  0,  0, 1, 0,  0,  0],
                             [0, 0,  0,  0, 0, 1,  0,  0],
                             [0, 0, 31, 32, 0, 0, 33, 34],
                             [0, 0, 41, 42, 0, 0, 43, 44]])
    if gatestr == 'ApplyCUon201':
        return sympy.Matrix([[1,  0, 0,  0, 0,  0, 0,  0],
                             [0, 11, 0, 12, 0, 13, 0, 14],
                             [0,  0, 1,  0, 0,  0, 0,  0],
                             [0, 21, 0, 22, 0, 23, 0, 24],
                             [0,  0, 0,  0, 1,  0, 0,  0],
                             [0, 31, 0, 32, 0, 33, 0, 34],
                             [0,  0, 0,  0, 0,  0, 1,  0],
                             [0, 41, 0, 42, 0, 43, 0, 44]])
    if gatestr == 'ApplyUon01':
        return sympy.Matrix([[11, 0, 12, 0, 13, 0, 14, 0],
                             [0, 11, 0, 12, 0, 13, 0, 14],
                             [21, 0, 22, 0, 23, 0, 24, 0],
                             [0, 21, 0, 22, 0, 23, 0, 24],
                             [31, 0, 32, 0, 33, 0, 34, 0],
                             [0, 31, 0, 32, 0, 33, 0, 34],
                             [41, 0, 42, 0, 43, 0, 44, 0],
                             [0, 41, 0, 42, 0, 43, 0, 44]])
    if gatestr == 'ApplyUon12':
        return sympy.Matrix([[11, 12, 13, 14, 0, 0, 0, 0],
                             [21, 22, 23, 24, 0, 0, 0, 0],
                             [31, 32, 33, 34, 0, 0, 0, 0],
                             [41, 42, 43, 44, 0, 0, 0, 0],
                             [ 0,  0,  0,  0, 11, 12, 13, 14],
                             [ 0,  0,  0,  0, 21, 22, 23, 24],
                             [ 0,  0,  0,  0, 31, 32, 33, 34],
                             [ 0,  0,  0,  0, 41, 42, 43, 44]])
    if gatestr == 'ApplyUon02':
        return sympy.Matrix([[11, 12, 0, 0, 13, 14, 0, 0],
                             [21, 22, 0, 0, 23, 24, 0, 0],
                             [0, 0, 11, 12, 0, 0, 13, 14],
                             [0, 0, 21, 22, 0, 0, 23, 24],
                             [31, 32, 0, 0, 33, 34, 0, 0],
                             [41, 42, 0, 0, 43, 44, 0, 0],
                             [0, 0, 31, 32, 0, 0, 33, 34],
                             [0, 0, 41, 42, 0, 0, 43, 44]])
    if gatestr == 'NonSquare':
        return sympy.Matrix([[1, 2, 3], [4, 5, 6]])
    if gatestr == 'NonInvertable':
        return sympy.Matrix([[1, 2, 3, 4],
                             [5, 6, 7, 8],
                             [9, 10, 11, 12],
                             [1, 2, 3, 4]])
    if gatestr == 'NonUnitary':
        return sympy.Matrix([[1, 2, 3, 4],
                             [5, 6, 7, 8],
                             [9, 10, 11, 12],
                             [13, 14, 15, 16]])
    return symbol_gate_matrix(gatestr, paras)


class Test_symbol_gate(UT.TestCase):
    def test_reverse_matrix_endianness(self):
        cases = {
            'H' : 'h',
            'cnot' : 'CNOT21',
            'CNOT21' : 'CX',
            'swap' : 'Swap',
            'CCZ' : 'ccz',
            'GeneralTwoQubitGate' : 'ReversedU',
        }
        for input in cases:
            with self.subTest(input):
                expected = str2matrix_test(cases[input])
                result = reverse_matrix_endianness(str2matrix_test(input))
                self.assertEqual(expected, result)
    
    def test_symbol_inverse_gate(self):
        cases = {
            ('H', None) : ('H', None),
            ('X', None) : ('X', None),
            ('Y', None) : ('Y', None),
            ('Z', None) : ('Z', None),
            ('CNOT', None) : ('CNOT', None),
            ('S', None) : ('Sdag', None),
            ('T', None) : ('Tdag', None),
            ('Rx', (theta_,)) : ('Rx', (-theta_,)),
            ('Ry', (theta_,)) : ('Ry', (-theta_,)),
            ('Rz', (theta_,)) : ('Rz', (-theta_,)),
            ('U1', (theta_,)) : ('U1', (-theta_,)),
            ('U3', (theta_, phi_, lambda_)) : ('U3', (-theta_, -lambda_, -phi_)),
        }
        for input in cases:
            with self.subTest(input):
                expected = str2matrix_test(cases[input][0], cases[input][1])
                result = symbol_inverse_gate( str2matrix_test(input[0], input[1]) )
                self.assertEqual(expected.simplify(), result.simplify())

    def test_is_legal_gate_matrix(self):
        cases = {
            ('H', None) : True,
            ('CNOT', None) : True,
            ('Fredkin', None) : True,
            ('Ry', (theta_,)) : True,
            ('Rxx', (theta_,)) : True,
            ('CRz', (theta_,)) : True,
            ('U3', (theta_, phi_, lambda_)) : True,
            ('NonSquare', None) : False,
            ('NonUnitary', None) : False,
        }
        for input in cases:
            with self.subTest(input):
                expected = cases[input]
                result = is_legal_gate_matrix( str2matrix_test(input[0], input[1]) )
                self.assertEqual(expected, result)


class Test_symbol_circuit(UT.TestCase):
    def test_symbol_controlled_gate(self):
        cases = {
            ('X', 1, None) : ('CNOT', None),
            ('Y', 1, None) : ('CY', None),
            ('Z', 1, None) : ('CZ', None),
            ('X', 2, None) : ('CCNOT', None),
            ('Z', 2, None) : ('CCZ', None),
            ('CNOT', 1, None) : ('CCNOT', None),
            ('CZ', 1, None) : ('CCZ', None),
            ('SWAP', 1, None) : ('CSWAP', None),
            ('GeneralTwoQubitGate', 1, None) : ('ControlledU', None),
            ('Rx', 1, (theta_,)) : ('CRx', (theta_,)),
            ('Ry', 1, (theta_,)) : ('CRy', (theta_,)),
            ('Rz', 1, (theta_,)) : ('CRz', (theta_,)),
            ('U1', 1, (theta_,)) : ('CU1', (theta_,)),
        }
        for input in cases:
            with self.subTest(input):
                expected = str2matrix_test(cases[input][0], cases[input][1])
                result = sympy.Matrix( symbol_controlled_gate(str2matrix_test(input[0], input[2]), input[1]) )
                self.assertEqual(expected, result)

    def test_symbol_apply_gate(self):
        cases = {
            ('CNOT', 2, (1, 0)) : 'CNOT21',
            ('ControlledU', 3, (0, 1, 2)) : 'ControlledU',
            ('ControlledU', 3, (0, 2, 1)) : 'ApplyCUon021',
            ('ControlledU', 3, (1, 0, 2)) : 'ApplyCUon102',
            ('ControlledU', 3, (2, 0, 1)) : 'ApplyCUon201',
            ('GeneralTwoQubitGate', 3, (0, 1)) : 'ApplyUon01',
            ('GeneralTwoQubitGate', 3, (1, 2)) : 'ApplyUon12',
            ('GeneralTwoQubitGate', 3, (0, 2)) : 'ApplyUon02',
        }
        for input in cases:
            with self.subTest(input):
                expected = str2matrix_test(cases[input])
                result = sympy.Matrix( symbol_apply_gate(str2matrix_test(input[0]), input[1], input[2]) )
                self.assertEqual(expected, result)
