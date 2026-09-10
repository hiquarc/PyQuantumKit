# test: common/test_program_std.py
#    2026/9/8
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

import unittest as UT
from .common import is_exception, EmptyCir, Cir1A, OnlyGlobalPhase
from pyquantumkit.program_check.matrix_based import numeric_equivalence_check, numpy_frobenius_norm
from .high_level_programs import *

class Test_program_std(UT.TestCase):
    """
    Test cases for subpackage "program/std"
    """
    def test_program_structure(self):
        cases = {
            # PASS cases
            (empty_qmain, True),
            (empty_declare, True),
            (empty_declare_measure, True),
            (empty_measure, True),
            (no_measure, True),
            (only_measure, True),

            # FAIL cases
            (forget_builder, TypeError),
            (forget_declare, QuantumProgramBuildError),
            (measure_undeclare, QuantumProgramBuildError),
            (operate_after_measure, QuantumProgramBuildError),
            (declare_twice, QuantumProgramBuildError),
            (measure_twice, QuantumProgramBuildError),
            (declare_anonymous, QuantumProgramBuildError),
            (declare_same_name, QuantumProgramBuildError),
            (measure_no_act_qunion, QuantumProgramBuildError),
        }
        for input in cases:
            with self.subTest(input):
                qpb = QProgramBuilder()
                if is_exception(input[1]):
                    self.assertRaises(input[1], lambda : qpb.build(input[0]))
                else:
                    qpb.build(input[0])

    def test_compile_bit_count(self):
        cases = {
            (empty_qmain, (0, 0)),
            (empty_declare, (0, 0)),
            (empty_declare_measure, (0, 0)),
            (no_measure, (1, 0)),
            (empty_measure, (1, 0)),
            (only_measure, (0, 0)),

            (prog_EmptyCir, (4, 0)),
            (prog_Cir1A, (2, 0)),
            (prog_OnlyGlobalPhase, (4, 0)),
            (prog_Create44plus58, (6, 6)),
            (prog_Create01pm0, (5, 5)),
            (prog_TestQStruct, (8, 8)),
            (prog_TestQTuple, (8, 8)),
            (prog_TestQUnion, (4, 0)),
            (prog_TestQArray, (8, 7)),
            (prog_TestQUnion_Mx, (4, 3)),
            (prog_TestQUnion_My, (4, 4)),
            (prog_TestQUnion_Mz, (4, 1)),
            (prog_PartialMeasure, (9, 7)),
            (prog_TwoQuInt, (12, 12)),
            (prog_EmptyType, (0, 0)),
        }
        for input in cases:
            with self.subTest(input):
                qpb = QProgramBuilder()
                qpb.build(input[0])
                nbits = (qpb.n_qvars_qubits(), qpb.n_measure_cbits())
                self.assertEqual(input[1], nbits)

    @UT.skip('skip the time consuming case')
    def test_compile_result(self):
        cases = {
            (prog_EmptyCir, EmptyCir),
            (prog_Cir1A, Cir1A),
            (prog_OnlyGlobalPhase, OnlyGlobalPhase),
            (prog_Create44plus58, Create44plus58),
            (prog_Create01pm0, Create01pm0),
            (prog_TestQStruct, cir_TestQStruct),
            (prog_TestQTuple, cir_TestQStruct),
            (prog_TestQUnion, cir_TestQUnion),
            (prog_TestQArray, cir_TestQArray),
        }
        for input in cases:
            with self.subTest(input):
                qpb = QProgramBuilder()
                qpb.set_build_options(ignore_measure = True)
                qpb.build(input[0])
                cio2 = input[1]('pyquantumkit')
                mat1 = qpb.get_built_circuit().get_numpy_matrix()
                mat2 = cio2.get_numpy_matrix()
                self.assertTrue(numeric_equivalence_check(mat1, mat2, False))

    def test_interpret_output_str(self):
        cases = [
            ((empty_qmain, '', 'l'), {}),
            ((empty_qmain, '0011', 'r'), ResultInterpretError),
            ((prog_EmptyCir, '', 'r'), {}),
            ((prog_EmptyCir, '110', 'l'), ResultInterpretError),
            ((prog_EmptyType, '', 'l'), {'eqs': {}, 'equ': {}, 'eqa1': [{},{},{},{},{}], 'eqa2': [], 'eqa3': ''}),
            ((prog_EmptyType, '1', 'r'), ResultInterpretError),

            ((prog_Create44plus58, '101100', 'r'), {'qnum' : 44}),
            ((prog_Create44plus58, '111010', 'r'), {'qnum' : 58}),
            ((prog_Create44plus58, '101100', 'l'), {'qnum' : 13}),

            ((prog_TestQStruct, '01+-1001', 'l'), ResultInterpretError),
            ((prog_TestQStruct, '10110110', 'l'), {'mystruct': {'x': '101', 'y': ['10', '11'], 'z': '0'}}),
            ((prog_TestQStruct, '10110110', 'r'), {'mystruct': {'x': '011', 'y': ['01', '10'], 'z': '1'}}),

            ((prog_TestQUnion_Mx, '1011', 'l'), ResultInterpretError),
            ((prog_TestQUnion_Mx, '110', 'l'), {'myunion': {'x': '110'}}),
            ((prog_TestQUnion_Mx, '110', 'r'), {'myunion': {'x': '011'}}),
            ((prog_TestQUnion_My, '110', 'l'), ResultInterpretError),
            ((prog_TestQUnion_My, '0111', 'l'), {'myunion': {'y': ['01', '11']}}),
            ((prog_TestQUnion_My, '0111', 'r'), {'myunion': {'y': ['11', '10']}}),
            ((prog_TestQUnion_Mz, '0111', 'l'), ResultInterpretError),
            ((prog_TestQUnion_Mz, '1', 'l'), {'myunion': {'z': '1'}}),

            ((prog_TestQArray, '10100111', 'r'), ResultInterpretError),
            ((prog_TestQArray, '1010011', 'l'), {'myarray': [{'y': ['10', '10']}, {'x': '011'}]}),
            ((prog_TestQArray, '1000011', 'r'), {'myarray': [{'y': ['11', '00']}, {'x': '001'}]}),

            ((prog_PartialMeasure, '101100101', 'l'), ResultInterpretError),
            ((prog_PartialMeasure, '1100101', 'l'), {'q1' : '110', 'q3' : '0101'}),
            ((prog_PartialMeasure, '1100101', 'r'), {'q1' : '101', 'q3' : '0011'}),

            ((prog_PartialMeasure2, '1100101', 'l'), ResultInterpretError),
            ((prog_PartialMeasure2, '110010', 'l'), {'q3' : '1100', 'q2' : '10'}),
            ((prog_PartialMeasure2, '110010', 'r'), {'q3' : '0100', 'q2' : '11'}),

            ((prog_TestSpecialMethods, '0', 'l'), {'sqs': 'ZERO'}),
            ((prog_TestSpecialMethods, '1', 'l'), {'sqs': 'ONE'}),
        ]
        for input in cases:
            with self.subTest(input):
                program = input[0][0]
                output_str = input[0][1]
                protocol = input[0][2]
                expected = input[1]

                qpb = QProgramBuilder()
                qpb.build(program)
                if is_exception(expected):
                    self.assertRaises(expected, lambda : qpb.interpret_output_str(output_str, protocol))
                else:
                    result = qpb.interpret_output_str(output_str, protocol)
                    self.assertEqual(result, expected)

    def test_interpret_result_dict(self):
        cases = [
            ((prog_Create44plus58, {'10110': 477, '11010': 523}, 'r'), ResultInterpretError),
            ((prog_Create44plus58, {'101100': 477, '111010': 523}, 'r'), [({'qnum': 44}, 477), ({'qnum': 58}, 523)] ),
            ((prog_Create44plus58, {'001101': 493, '010111': 507}, 'l'), [({'qnum': 44}, 493), ({'qnum': 58}, 507)] ),

            ((prog_TwoQuInt, 
              {'000111101011': 252,
               '001100111001': 248,
               '001100101011': 238,
               '000111111001': 262},
              'r'),
              [({'qnum1': 43, 'qnum2': 7}, 252),
               ({'qnum1': 57, 'qnum2': 12}, 248),
               ({'qnum1': 43, 'qnum2': 12}, 238),
               ({'qnum1': 57, 'qnum2': 7}, 262)]),
               
            ((prog_TwoQuInt, 
              {'000111101011': 252,
               '001100111001': 248,
               '001100101011': 238,
               '000111111001': 262},
              'l'),
              [({'qnum1': 56, 'qnum2': 53}, 252),
               ({'qnum1': 12, 'qnum2': 39}, 248),
               ({'qnum1': 12, 'qnum2': 53}, 238),
               ({'qnum1': 56, 'qnum2': 39}, 262)]),
        ]
        for input in cases:
            with self.subTest(input):
                program = input[0][0]
                result_dict = input[0][1]
                protocol = input[0][2]
                expected = input[1]

                qpb = QProgramBuilder()
                qpb.build(program)
                if is_exception(expected):
                    self.assertRaises(expected, lambda : qpb.interpret_result_dict(result_dict, protocol))
                else:
                    result = qpb.interpret_result_dict(result_dict, protocol)
                    self.assertEqual(result, expected)

