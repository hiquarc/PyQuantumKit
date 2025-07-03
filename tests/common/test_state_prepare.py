# test: common/test_state_prepare.py
#    2025/6/23
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

import unittest as UT
from .common import *
from pyquantumkit import *
from pyquantumkit.classical.run_result import *
from pyquantumkit.classical.common import *
from pyquantumkit.state_prepare.by_string import *
from pyquantumkit.state_prepare.int_state import *
from pyquantumkit.state_prepare.pauli_eigenstate import *
from pyquantumkit.procedure.generic import *


class Test_state_prepare_int_state(UT.TestCase):
    """
    Test cases for subpackage "state_prepare/int_state"
    """
    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
        self._fm = ''
        self._qvm = None
    def setUp(self):
        self.skipTest('Do not test base class')

    def test_create_ket_int_le(self):
        cases = {
            (0, 0) : set(),
            (2, -2) : ValueError,
            (1, 2) : {'0'},
            (1, 1) : {'1'},
            (5, 22) : {'01101'},      # 22 = 10110b
            (3, 22) : {'011'},        # overflow case
        }
        for input in cases:
            with self.subTest(input):
                nbits = input[0]
                number = input[1]
                qbitlist = range(nbits)
                if is_exception(cases[input]):
                    self.assertRaises(cases[input], T_run, self._fm, self._qvm, nbits,
                                      create_ket_int_le, number, qbitlist)
                else:
                    result = T_measure_result(self._fm, self._qvm, nbits,
                                              create_ket_int_le, number, qbitlist)
                    self.assertEqual(result, cases[input])

    def test_create_ket_int_be(self):
        cases = {
            (0, 0) : set(),
            (2, -2) : ValueError,
            (1, 2) : {'0'},
            (1, 1) : {'1'},
            (5, 22) : {'10110'},      # 22 = 10110b
            (3, 22) :   {'110'},      # overflow case
        }
        for input in cases:
            with self.subTest(input):
                nbits = input[0]
                number = input[1]
                qbitlist = range(nbits)
                if is_exception(cases[input]):
                    self.assertRaises(cases[input], T_run, self._fm, self._qvm, nbits,
                                      create_ket_int_be, number, qbitlist)
                else:
                    result = T_measure_result(self._fm, self._qvm, nbits,
                                              create_ket_int_be, number, qbitlist)
                    self.assertEqual(result, cases[input])

    def test_uncompute_ket_int_le(self):
        cases = {
            (0, 0) : None,
            (2, -2) : ValueError,
            (1, 2) : None,
            (1, 1) : None,
            (5, 22) : None,
            (3, 22) : None,
        }
        for input in cases:
            with self.subTest(input):
                nbits = input[0]
                qbitlist = range(nbits)
                number = input[1]
                if is_exception(cases[input]):
                    self.assertRaises(cases[input], T_run, self._fm, self._qvm, nbits,
                                      uncompute_ket_int_le, number, qbitlist)
                else:
                    result = T_create_uncompute(self._fm, self._qvm, nbits,
                                                create_ket_int_le, uncompute_ket_int_le, number, qbitlist)
                    self.assertTrue(result)
        
    def test_uncompute_ket_int_be(self):
        cases = {
            (0, 0) : None,
            (2, -2) : ValueError,
            (1, 2) : None,
            (1, 1) : None,
            (5, 22) : None,
            (3, 22) : None,
        }
        for input in cases:
            with self.subTest(input):
                nbits = input[0]
                qbitlist = range(nbits)
                number = input[1]
                if is_exception(cases[input]):
                    self.assertRaises(cases[input], T_run, self._fm, self._qvm, nbits,
                                      uncompute_ket_int_le, number, qbitlist)
                else:
                    result = T_create_uncompute(self._fm, self._qvm, nbits,
                                                create_ket_int_le, uncompute_ket_int_le,
                                                number, qbitlist)
                    self.assertTrue(result)


    def test_create_ket_int_plus_eiphi_neg_le(self):
        cases = {
            (0, 0, 0.0) : set(),
            (2, -2, -1.0) : ValueError,
            (1, 0, 0.0) : {'0', '1'},
            (1, 1, 1.0) : {'0', '1'},
            (5, 22, 2.0) : {'01101', '10010'},
            (5,  9, 3.0) : {'01101', '10010'},
            (3, 22, 4.0) : {'011',   '100'},        # overflow case
        }
        for input in cases:
            with self.subTest(input):
                nbits = input[0]
                number = input[1]
                phi = input[2]
                qbitlist = range(nbits)
                if is_exception(cases[input]):
                    self.assertRaises(cases[input], T_run, self._fm, self._qvm, nbits,
                                      create_ket_int_plus_eiphi_neg_le, number, phi, qbitlist)
                else:
                    result = T_measure_result(self._fm, self._qvm, nbits,
                                              create_ket_int_plus_eiphi_neg_le, number, phi, qbitlist)
                    self.assertEqual(result, cases[input])

    def test_create_ket_int_plus_eiphi_neg_be(self):
        cases = {
            (0, 0, 0.0) : set(),
            (2, -2, -1.0) : ValueError,
            (1, 0, 0.0) : {'0', '1'},
            (1, 1, 1.0) : {'0', '1'},
            (5, 22, 2.0) : {'10110', '01001'},
            (5,  9, 3.0) : {'10110', '01001'},
            (3, 22, 4.0) : {  '110',   '001'},      # overflow case
        }
        for input in cases:
            with self.subTest(input):
                nbits = input[0]
                number = input[1]
                phi = input[2]
                qbitlist = range(nbits)
                if is_exception(cases[input]):
                    self.assertRaises(cases[input], T_run, self._fm, self._qvm, nbits,
                                      create_ket_int_plus_eiphi_neg_be, number, phi, qbitlist)
                else:
                    result = T_measure_result(self._fm, self._qvm, nbits,
                                              create_ket_int_plus_eiphi_neg_be, number, phi, qbitlist)
                    self.assertEqual(result, cases[input])

    def test_uncompute_ket_int_plus_eiphi_neg_le(self):
        cases = {
            (0, 0, 0.0) : None,
            (2, -2, -1.0) : ValueError,
            (1, 0, 0.0) : None,
            (1, 1, 1.0) : None,
            (5, 22, 2.0) : None,
            (5,  9, 3.0) : None,
            (3, 22, 4.0) : None,
        }
        for input in cases:
            with self.subTest(input):
                nbits = input[0]
                number = input[1]
                phi = input[2]
                qbitlist = range(nbits)
                if is_exception(cases[input]):
                    self.assertRaises(cases[input], T_run, self._fm, self._qvm, nbits,
                                      uncompute_ket_int_plus_eiphi_neg_le,
                                      number, phi, qbitlist)
                else:
                    result = T_create_uncompute(self._fm, self._qvm, nbits,
                                                create_ket_int_plus_eiphi_neg_le, uncompute_ket_int_plus_eiphi_neg_le,
                                                number, phi, qbitlist)
                    self.assertTrue(result)

    def test_uncompute_ket_int_plus_eiphi_neg_be(self):
        cases = {
            (0, 0, 0.0) : None,
            (2, -2, -1.0) : ValueError,
            (1, 0, 0.0) : None,
            (1, 1, 1.0) : None,
            (5, 22, 2.0) : None,
            (5,  9, 3.0) : None,
            (3, 22, 4.0) : None,
        }
        for input in cases:
            with self.subTest(input):
                nbits = input[0]
                number = input[1]
                phi = input[2]
                qbitlist = range(nbits)
                if is_exception(cases[input]):
                    self.assertRaises(cases[input], T_run, self._fm, self._qvm, nbits,
                                      uncompute_ket_int_plus_eiphi_neg_be,
                                      number, phi, qbitlist)
                else:
                    result = T_create_uncompute(self._fm, self._qvm, nbits,
                                                create_ket_int_plus_eiphi_neg_be, uncompute_ket_int_plus_eiphi_neg_be,
                                                number, phi, qbitlist)
                    self.assertTrue(result)


    def test_create_ket_int1_plus_eiphi_ket_int2_le(self):
        cases = {
            (0, 0, 0, 0.0) : set(),
            (2, -2, 3, -1.0) : ValueError,
            (1, 0, 0, 0.5) : {'0'},
            (1, 0, 1, 1.0) : {'0', '1'},
            (5, 22, 22, 1.5) : {'01101'},               # same case
            (5,  9, 22, 2.0) : {'01101', '10010'},      # complementary case
            (6, 44, 58, 2.5) : {'001101', '010111'},    # general case
            (3, 44, 58, 3.0) : {'001'   , '010'   },    # overflow case
        }
        for input in cases:
            with self.subTest(input):
                nbits = input[0]
                num1 = input[1]
                num2 = input[2]
                phi = input[3]
                qbitlist = range(nbits)
                if is_exception(cases[input]):
                    self.assertRaises(cases[input], T_run, self._fm, self._qvm, nbits,
                                      create_ket_int1_plus_eiphi_ket_int2_le,
                                      num1, num2, phi, qbitlist)
                else:
                    result = T_measure_result(self._fm, self._qvm, nbits,
                                              create_ket_int1_plus_eiphi_ket_int2_le,
                                              num1, num2, phi, qbitlist)
                    self.assertEqual(result, cases[input])

    def test_create_ket_int1_plus_eiphi_ket_int2_be(self):
        cases = {
            (0, 0, 0, 0.0) : set(),
            (2, 2, -3, -1.0) : ValueError,
            (1, 0, 0, 0.5) : {'0'},
            (1, 0, 1, 1.0) : {'0', '1'},
            (5, 22, 22, 1.5) : {'10110'},               # same case
            (5,  9, 22, 2.0) : {'10110', '01001'},      # complementary case
            (6, 44, 58, 2.5) : {'101100', '111010'},    # general case
            (3, 44, 58, 3.0) : {   '100',    '010'},    # overflow case
        }
        for input in cases:
            with self.subTest(input):
                nbits = input[0]
                num1 = input[1]
                num2 = input[2]
                phi = input[3]
                qbitlist = range(nbits)
                if is_exception(cases[input]):
                    self.assertRaises(cases[input], T_run, self._fm, self._qvm, nbits,
                                      create_ket_int1_plus_eiphi_ket_int2_be,
                                      num1, num2, phi, qbitlist)
                else:
                    result = T_measure_result(self._fm, self._qvm, nbits,
                                              create_ket_int1_plus_eiphi_ket_int2_be,
                                              num1, num2, phi, qbitlist)
                    self.assertEqual(result, cases[input])

    def test_uncompute_ket_int1_plus_eiphi_ket_int2_le(self):
        cases = {
            (0, 0, 0, 0.0) : None,
            (2, 2, -3, -1.0) : ValueError,
            (1, 0, 0, 0.5) : None,
            (1, 0, 1, 1.0) : None,
            (5, 22, 22, 1.5) : None,
            (5,  9, 22, 2.0) : None,
            (6, 44, 58, 2.5) : None,
            (3, 44, 58, 3.0) : None,
        }
        for input in cases:
            with self.subTest(input):
                nbits = input[0]
                num1 = input[1]
                num2 = input[2]
                phi = input[3]
                qbitlist = range(nbits)
                if is_exception(cases[input]):
                    self.assertRaises(cases[input], T_run, self._fm, self._qvm, nbits,
                                      uncompute_ket_int1_plus_eiphi_ket_int2_le,
                                      num1, num2, phi, qbitlist)
                else:
                    result = T_create_uncompute(self._fm, self._qvm, nbits,
                                                create_ket_int1_plus_eiphi_ket_int2_le, uncompute_ket_int1_plus_eiphi_ket_int2_le,
                                                num1, num2, phi, qbitlist)
                    self.assertTrue(result)

    def test_uncompute_ket_int1_plus_eiphi_ket_int2_be(self):
        cases = {
            (0, 0, 0, 0.0) : None,
            (2, -2, 3, -1.0) : ValueError,
            (1, 0, 0, 0.5) : None,
            (1, 0, 1, 1.0) : None,
            (5, 22, 22, 1.5) : None,
            (5,  9, 22, 2.0) : None,
            (6, 44, 58, 2.5) : None,
            (3, 44, 58, 3.0) : None,
        }
        for input in cases:
            with self.subTest(input):
                nbits = input[0]
                num1 = input[1]
                num2 = input[2]
                phi = input[3]
                qbitlist = range(nbits)
                if is_exception(cases[input]):
                    self.assertRaises(cases[input], T_run, self._fm, self._qvm, nbits,
                                      uncompute_ket_int1_plus_eiphi_ket_int2_be,
                                      num1, num2, phi, qbitlist)
                else:
                    result = T_create_uncompute(self._fm, self._qvm, nbits,
                                                create_ket_int1_plus_eiphi_ket_int2_be, uncompute_ket_int1_plus_eiphi_ket_int2_be,
                                                num1, num2, phi, qbitlist)
                    self.assertTrue(result)



class Test_state_prepare_by_string(UT.TestCase):
    """
    Test cases for subpackage "state_prepare/by_string"
    """
    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
        self._fm = ''
        self._qvm = None
    def setUp(self):
        self.skipTest('Do not test base class')

    def test_create_state_by_01pm(self):
        cases = {
            (0, '+-')     : set(),
            (5, '10+-X')  : ValueError,
            (3, '')       : ValueError,
            (2, '1')      : ValueError,
            (6, '111010') : {'111010'},
            (4, '11+0')   : {'1100', '1110'},
            (4, '1-01')   : {'1001', '1101'},
        }
        for input in cases:
            with self.subTest(input):
                nbits = input[0]
                s = input[1]
                qbitlist = range(nbits)
                if is_exception(cases[input]):
                    self.assertRaises(cases[input], T_run, self._fm, self._qvm, nbits,
                                      create_state_by_01pm, s, qbitlist)
                else:
                    result = T_measure_result(self._fm, self._qvm, nbits,
                                              create_state_by_01pm, s, qbitlist)
                    self.assertEqual(result, cases[input])

    def test_uncompute_state_by_01pm(self):
        cases = {
            (0, '+-')     : None,
            (5, '10+-X')  : ValueError,
            (3, '')       : ValueError,
            (2, '1')      : ValueError,
            (6, '111010') : None,
            (4, '11+0')   : None,
            (4, '1-01')   : None,
        }
        for input in cases:
            with self.subTest(input):
                nbits = input[0]
                s = input[1]
                qbitlist = range(nbits)
                if is_exception(cases[input]):
                    self.assertRaises(cases[input], T_run, self._fm, self._qvm, nbits,
                                      uncompute_state_by_01pm, s, qbitlist)
                else:
                    result = T_create_uncompute(self._fm, self._qvm, nbits,
                                                create_state_by_01pm, uncompute_state_by_01pm, s, qbitlist)
                    self.assertTrue(result)


    def test_create_state_by_sqgate_str(self):
        cases = {
            (0, 'XYZ') : set(),
            (7, 'history') : ValueError,
            (3, '') : ValueError,
            (2, 'i') : ValueError,
            (4, 'Zist') : {'0000'},
            (3, 'HIX') : {'001', '101'},
            (7, 'iXYZsth') : {'0110000', '0110001'},
        }
        for input in cases:
            with self.subTest(input):
                nbits = input[0]
                s = input[1]
                qbitlist = range(nbits)
                if is_exception(cases[input]):
                    self.assertRaises(cases[input], T_run, self._fm, self._qvm, nbits,
                                      create_state_by_sqgate_str, s, qbitlist)
                else:
                    result = T_measure_result(self._fm, self._qvm, nbits,
                                              create_state_by_sqgate_str, s, qbitlist)
                    self.assertEqual(result, cases[input])

    def test_uncompute_state_by_sqgate_str(self):
        cases = {
            (0, 'XYZ') : None,
            (7, 'history') : ValueError,
            (3, '') : ValueError,
            (2, 'i') : ValueError,
            (4, 'Zist') : None,
            (3, 'HIX') : None,
            (7, 'iXYZsth') : None,
        }
        for input in cases:
            with self.subTest(input):
                nbits = input[0]
                s = input[1]
                qbitlist = range(nbits)
                if is_exception(cases[input]):
                    self.assertRaises(cases[input], T_run, self._fm, self._qvm, nbits,
                                      uncompute_state_by_sqgate_str, s, qbitlist)
                else:
                    result = T_create_uncompute(self._fm, self._qvm, nbits,
                                                create_state_by_sqgate_str, uncompute_state_by_sqgate_str, s, qbitlist)
                    self.assertTrue(result)



class Test_state_prepare_pauli_eigenstate(UT.TestCase):
    """
    Test cases for subpackage "state_prepare/pauli_eigenstate"
    """
    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
        self._fm = ''
        self._qvm = None
    def setUp(self):
        self.skipTest('Do not test base class')

    def test_create_pauli_eigenstate_1(self):
        cases = {
            (0, (0,1,2,3,4,5)) : '',
            (2, (0,3,2,3)) : ValueError,
            (3, (2,3,6)) : ValueError,
            (4, (0,1,0,1)) : '0101',
            (4, (2,3,3,2)) : '+--+',
            (6, (0,1,2,3,0,1)) : '01+-01',
        }
        for input in cases:
            with self.subTest(input):
                nbits = input[0]
                paulilist = list(input[1])
                qbitlist = range(nbits)
                if is_exception(cases[input]):
                    self.assertRaises(cases[input], T_run, self._fm, self._qvm, nbits,
                                      create_pauli_eigenstate, paulilist, qbitlist)
                else:
                    procs = [create_pauli_eigenstate, uncompute_state_by_01pm]
                    procargs = [[paulilist, qbitlist], [cases[input], qbitlist]]
                    result = T_identity_mp(self._fm, self._qvm, nbits, procs, procargs)
                    self.assertTrue(result)

    def test_create_pauli_eigenstate_2(self):
        cases = {
            (4, (0,1,0,1)) : 'zzzz',
            (4, (2,3,3,2)) : 'xxxx',
            (4, (4,4,5,5)) : 'yyyy',
            (6, (0,1,2,3,4,5)) : 'zzxxyy',
        }
        for input in cases:
            with self.subTest(input):
                nbits = input[0]
                paulilist = list(input[1])
                qbitlist = range(nbits)
                if is_exception(cases[input]):
                    self.assertRaises(cases[input], T_run, self._fm, self._qvm, nbits,
                                      create_pauli_eigenstate, paulilist, qbitlist)
                else:
                    procs = [create_pauli_eigenstate, create_state_by_sqgate_str, uncompute_pauli_eigenstate]
                    procargs = [[paulilist, qbitlist], [cases[input], qbitlist], [paulilist, qbitlist]]
                    result = T_measure_result_mp(self._fm, self._qvm, nbits, procs, procargs)
                    self.assertEqual(result, {'0' * nbits})

    def test_uncompute_pauli_eigenstate(self):
        cases = {
            (0, (0,1,2,3,4,5)) : None,
            (2, (0,3,2,3)) : ValueError,
            (3, (2,3,6)) : ValueError,
            (4, (0,1,0,1)) : None,
            (4, (2,3,3,2)) : None,
            (6, (0,1,2,3,4,5)) : None,
        }
        for input in cases:
            with self.subTest(input):
                nbits = input[0]
                paulilist = list(input[1])
                qbitlist = range(nbits)
                if is_exception(cases[input]):
                    self.assertRaises(cases[input], T_run, self._fm, self._qvm, nbits,
                                      uncompute_pauli_eigenstate, paulilist, qbitlist)
                else:
                    result = T_create_uncompute(self._fm, self._qvm, nbits,
                                                create_pauli_eigenstate, uncompute_pauli_eigenstate,
                                                paulilist, qbitlist)
                    self.assertTrue(result)
