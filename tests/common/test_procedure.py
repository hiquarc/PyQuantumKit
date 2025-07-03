# test: common/test_procedure.py
#    2025/6/27
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

import unittest as UT
from .common import *
from pyquantumkit import *
from pyquantumkit.classical.run_result import *
from pyquantumkit.classical.common import *
from pyquantumkit.procedure.generic import *
from pyquantumkit.procedure.paulis import *
from pyquantumkit.program_check.program_relation import *


class Test_procedure_generic(UT.TestCase):
    """
    Test cases for subpackage "procedure/generic"
    """
    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
        self._fm = ''
        self._qvm = None
    def setUp(self):
        self.skipTest('Do not test base class')

    def test_quantum_gates(self):
        cases = {
            'I' : ((0,), ()),
            'X' : ((1,), ()),
            'Y' : ((2,), ()),
            'Z' : ((3,), ()),
            'S' : ((0,), ()),
            'T' : ((1,), ()),
            'H' : ((2,), ()),
            'RX' : ((3,), (0.5,)),
            'RY' : ((0,), (1.0,)),
            'RZ' : ((1,), (1.5,)),
            'SD' : ((2,), ()),
            'TD' : ((3,), ()),
            'U1' : ((0,), (2.0,)),
            'U3' : ((1,), (2.5, 3.0, 3.5)),
            'CX' : ((0, 1), ()),
            'CY' : ((1, 2), ()),
            'CZ' : ((2, 3), ()),
            'CH' : ((1, 0), ()),
            'SW' : ((0, 2), ()),
            'ISW' : ((2, 0), ()),
            'CRX' : ((0, 3), (0.6,)),
            'CRY' : ((3, 0), (1.1,)),
            'CRZ' : ((3, 2), (1.7,)),
            'RXX' : ((1, 3), (1.8,)),
            'RYY' : ((3, 1), (1.9,)),
            'RZZ' : ((0, 1), (2.2,)),
            'CU1' : ((1, 3), (2.8,)),
            'CSW' : ((0, 2, 1), ()),
            'CCX' : ((1, 2, 3), ()),
            'CCZ' : ((3, 2, 1), ()),
        }
        for input in cases:
            with self.subTest(input):
                qbitlist = list(cases[input][0])
                paras = list(cases[input][1])
                T_run(self._fm, self._qvm, 4, apply_gate, input, qbitlist, paras)

    def test_apply_measure(self):
        cases = {
            ((), ()) : None,
            ((1,), (1,)) : None,
            ((0,), (3,)) : None,
            ((1,2), (0,3)) : None,
            ((0,1,2,3), (0,1,2,3)) : None,
            ((0,1,2,3), (3,2,1,0)) : None,
            # error cases have different behavior on different frameworks,
            #  so temporarily skip these tests.
            #((1,2,3), (1,2)) : IndexError,
            #((0,4), (0,3)) : IndexError,
            #((0,2), (4,3)) : IndexError,
        }
        for input in cases:
            with self.subTest(input):
                qbits = input[0]
                cbits = input[1]
                if is_exception(cases[input]):
                    self.assertRaises(cases[input], T_run, self._fm, self._qvm, 4,
                                      apply_measure, qbits, cbits)
                else:
                    T_run(self._fm, self._qvm, 4, apply_measure, qbits, cbits)



class Test_procedure_paulis(UT.TestCase):
    """
    Test cases for subpackage "procedure/paulis"
    """
    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
        self._fm = ''
        self._qvm = None
    def setUp(self):
        self.skipTest('Do not test base class')

    def test_apply_measure_z(self):
        cases = {
            ((0,), (0,)),
            ((0,1,2), (0,1,2)),
            ((0,1,2), (2,1,0)),
            ((0,3,1,2), (2,0,1,3)),
        }
        for input in cases:
            with self.subTest(input):
                qbits = list(input[0])
                nqbits = indexlist_length(qbits)
                cbits = list(input[1])
                ncbits = indexlist_length(qbits)
                result = T_equivalence(self._fm, self._qvm, nqbits, ncbits,
                                    apply_measure, apply_measure_z, [qbits, cbits], [qbits, cbits])
                self.assertTrue(result)
