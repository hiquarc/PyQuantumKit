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

            # special pass cases: equivalence gates
            (Rxx_Normal, Rxx_Decomposition) : True,
            (Ryy_Normal, Ryy_Decomposition) : True,
            (Rzz_Normal, Rzz_Decomposition) : True,
            (iSWAP_Normal, iSWAP_Decomposition) : True,
            (CH_Normal, CH_Decomposition) : True,
            (CS_Normal, CS_Decomposition) : True,
            (CSD_Normal, CSD_Decomposition) : True,
            (CU1_Normal, CU1_Decomposition) : True,
            (SqrtX_Normal, SqrtX_Decomposition) : True,
            (SqrtXdag_Normal, SqrtXdag_Decomposition) : True,
            (Fredkin_Normal, Fredkin_Decomposition) : True,
            (U3_Normal, U3_Decomposition) : True,
            
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
            OnlyGlobalPhase : True,
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


class Test_program_check_matrix_based(UT.TestCase):
    """
    Test cases for subpackage "program_check/matrix_based"
    """
    def test_numeric_equivalence_check(self):
        cases = {
            # PASS cases
            (EmptyCir, CancelCir, False) : True,
            (EmptyCir, CancelCir, True) : True,
            (EmptyCir, OnlyGlobalPhase, True) : True,   # Eq when ignore the global phase
            (Cir1A, Cir1B, False) : True,
            (Cir1A, Cir1C, False) : True,
            (Cir1A, Cir1B, True) : True,
            (Cir1A, Cir1C, True) : True,
            (U1gate, Rzgate, True) : True,

            # special pass cases: equivalence gates
            (Rxx_Normal, Rxx_Decomposition, False) : True,
            (Ryy_Normal, Ryy_Decomposition, False) : True,
            (Rzz_Normal, Rzz_Decomposition, False) : True,
            (iSWAP_Normal, iSWAP_Decomposition, False) : True,
            (CH_Normal, CH_Decomposition, False) : True,
            (CS_Normal, CS_Decomposition, False) : True,
            (CSD_Normal, CSD_Decomposition, False) : True,
            (CU1_Normal, CU1_Decomposition, False) : True,
            (SqrtX_Normal, SqrtX_Decomposition, False) : True,
            (SqrtXdag_Normal, SqrtXdag_Decomposition, False) : True,
            (Fredkin_Normal, Fredkin_Decomposition, False) : True,
            (U3_Normal, U3_Decomposition, False) : True,
            
            # FAIL cases
            (EmptyCir, OnlyGlobalPhase, False) : False,   # A difference about global phase
            (EmptyCir, Empty_bug2, False) : False,
            (EmptyCir, Empty_bug2, True) : False,
            (Cir1B, Cir1A_bug1, False) : False,
            (Cir1B, Cir1A_bug2, False) : False,
            (Cir1B, Cir1A_bug3, False) : False,
            (Cir1B, Cir1A_bug4, False) : False,
            (Cir1B, Cir1A_bug1, True) : False,
            (Cir1B, Cir1A_bug2, True) : False,
            (Cir1B, Cir1A_bug3, True) : False,
            (Cir1B, Cir1A_bug4, True) : False,
            (U1gate, Rzgate, False) : False,
        }
        for input in cases:
            with self.subTest(input):
                p1 = input[0]('pyquantumkit')
                p2 = input[1]('pyquantumkit')
                ign_gp = input[2]
                mat1 = p1.get_numpy_matrix()
                mat2 = p2.get_numpy_matrix()
                output = numeric_equivalence_check(mat1, mat2, ign_gp)
                self.assertEqual(output, cases[input])

    def test_run_identity_check(self):
        cases = {
            # PASS cases
            (EmptyCir, True) : True,
            (CancelCir, True) : True,
            (CancelCir2, True) : True,
            (EmptyCir, False) : True,
            (CancelCir, False) : True,
            (CancelCir2, False) : True,
            (OnlyGlobalPhase, True) : True,
            # FAIL cases
            (Empty_bug2, False) : False,
            (Cir1A, False) : False,
            (Cir1B, False) : False,
            (Empty_bug2, True) : False,
            (Cir1A, True) : False,
            (Cir1B, True) : False,
            (OnlyGlobalPhase, False) : False,
        }
        for input in cases:
            with self.subTest(input):
                p = input[0]('pyquantumkit')
                ign_gp = input[1]
                mat = p.get_numpy_matrix()
                output = numeric_identity_check(mat, ign_gp)
                self.assertEqual(output, cases[input])
