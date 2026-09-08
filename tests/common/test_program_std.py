# test: common/test_program_std.py
#    2026/9/8
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

import unittest as UT
from .common import is_exception, EmptyCir, Cir1A, OnlyGlobalPhase
from pyquantumkit.program_check.matrix_based import numeric_equivalence_check
from .high_level_programs import *

class Test_program_std(UT.TestCase):
    """
    Test cases for subpackage "program/std"
    """
    def test_program_structure(self):
        cases = {
            # PASS cases
            empty_qmain : True,
            empty_declare : True,
            empty_declare_measure : True,
            empty_measure : True,
            no_measure : True,
            only_measure : True,

            # FAIL cases
            forget_builder : TypeError,
            forget_declare : QuantumProgramBuildError,
            measure_undeclare : QuantumProgramBuildError,
            operate_after_measure : QuantumProgramBuildError,
            declare_twice : QuantumProgramBuildError,
            measure_twice : QuantumProgramBuildError,
            declare_anonymous : QuantumProgramBuildError,
            declare_same_name : QuantumProgramBuildError,
        }
        for input in cases:
            with self.subTest(input):
                qpb = QProgramBuilder()
                if is_exception(cases[input]):
                    self.assertRaises(cases[input], lambda : qpb.build(input))
                else:
                    qpb.build(input)
                
    def test_compile_result(self):
        cases = {
            (prog_EmptyCir, EmptyCir),
            (prog_Cir1A, Cir1A),
            (prog_OnlyGlobalPhase, OnlyGlobalPhase),
            (prog_Create44plus58, Create44plus58),
            (prog_Create01pm0, Create01pm0),
        }
        for item in cases:
            with self.subTest(input):
                qpb = QProgramBuilder()
                qpb.build(item[0])
                cio2 = item[1]('pyquantumkit')
                mat1 = qpb.get_built_circuit().get_numpy_matrix()
                mat2 = cio2.get_numpy_matrix()
                self.assertTrue(numeric_equivalence_check(mat1, mat2, False))

