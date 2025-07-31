# test: common/test_program_check.py
#    2025/6/27
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

import unittest as UT
from .common import *
from pyquantumkit import *
from pyquantumkit.classical.run_result import *
from pyquantumkit.classical.common import *
from pyquantumkit.procedure.generic import *


class Test_program_check_program_relation(UT.TestCase):
    """
    Test cases for subpackage "program_check/program_relation"
    """
    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
        self._fm = ''
        self._qvm = None
    def setUp(self):
        self.skipTest('Do not test base class')

    def test_run_equivalence_check(self):
        cases = {
            # PASS cases
            (EmptyCir, CancelCir) : True,
            (Cir1A, Cir1B) : True,
            (Cir1A, Cir1C) : True,
            # FAIL cases
            (EmptyCir, Empty_bug1) : False,
            (EmptyCir, Empty_bug2) : False,
            (Cir1B, Cir1A_bug1) : False,
            (Cir1B, Cir1A_bug2) : False,
            (Cir1B, Cir1A_bug3) : False,
            (Cir1B, Cir1A_bug4) : False,
            (Cir1B, Cir1A_bug5) : False,
        }
        for input in cases:
            with self.subTest(input):
                p1 = input[0]
                p2 = input[1]
                output = run_equivalence_check(self._qvm, p1(self._fm), p2(self._fm))
                self.assertEqual(output, cases[input])

    def test_run_identity_check(self):
        cases = {
            # PASS cases
            EmptyCir : True,
            CancelCir : True,
            CancelCir2 : True,
            # FAIL cases
            Empty_bug1 : False,
            Empty_bug2 : False,
        }
        for input in cases:
            with self.subTest(input):
                output = run_identity_check(self._qvm, input(self._fm))
                self.assertEqual(output, cases[input])

    def test_run_keep_purity_check(self):
        cases = {
            # PASS cases
            EmptyCir : True,
            CancelCir : True,
            Cir1A : True,
            Cir1B : True,
            Empty_bug2 : True,
            Cir1A_bug1 : True,
            Cir1A_bug2 : True,
            Cir1A_bug3 : True,
            Cir1A_bug4 : True,
            # FAIL cases
            Empty_bug1 : False,
            Cir1A_bug5 : False,
        }
        for input in cases:
            with self.subTest(input):
                output = run_keep_purity_check(self._qvm, input(self._fm))
                self.assertEqual(output, cases[input])

    def test_run_unitarity_check(self):
        cases = {
            # PASS cases
            EmptyCir : True,
            CancelCir : True,
            Cir1A : True,
            Cir1B : True,
            Empty_bug2 : True,
            Cir1A_bug1 : True,
            Cir1A_bug2 : True,
            Cir1A_bug3 : True,
            Cir1A_bug4 : True,
            # FAIL cases
            Empty_bug1 : False,
            Cir1A_bug5 : False,
        }
        for input in cases:
            with self.subTest(input):
                output = run_unitarity_check(self._qvm, input(self._fm))
                self.assertEqual(output, cases[input])

    def test_run_keep_basis_check(self):
        cases = {
            # PASS cases
            EmptyCir : True,
            CancelCir : True,
            Cir1A : True,
            Cir1B : True,
            Empty_bug1 : True,
            Empty_bug2 : True,
            Cir1A_bug1 : True,
            Cir1A_bug5 : True,
            # FAIL cases
            Cir1A_bug2 : False,
            Cir1A_bug3 : False,
            Cir1A_bug4 : False,
        }
        for input in cases:
            with self.subTest(input):
                output = run_keep_basis_check(self._qvm, input(self._fm))
                self.assertEqual(output, cases[input])

