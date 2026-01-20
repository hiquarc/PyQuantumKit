# test: common/test_qframes.py
#    2025/6/29
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

import unittest as UT
from pyquantumkit._qframes.code_translate import *
from .common import is_exception

class Test_qframes_code_translate(UT.TestCase):
    def test_get_args_assign_str(self):
        cases = {
            ('arr', 0) : '',
            ('arr', 1) : 'arr[0]',
            ('arr', 2) : 'arr[0],arr[1]',
            ('List', 4) : 'List[0],List[1],List[2],List[3]',
        }
        for input in cases:
            with self.subTest(input):
                argname = input[0]
                narg = input[1]
                output = cases[input]
                self.assertEqual(get_args_assign_str(argname, narg), output)

    def test_get_standard_gatename(self):
        cases = {
            'meaSuRe' : 'M',
            'iD' : 'I',
            'cnot' : 'CX',
            'SWAP' : 'SW',
            'iSWAP' : 'ISW',
            'toffoli' : 'CCX',
            'cswaP' : 'CSW',
            'Sdagger' : 'SD',
            'Tdag' : 'TD',
            'R1' : 'U1',
            'cr1' : 'CU1',
            'u3' : 'U3',
            'y' : 'Y',
            'Rx' : 'RX',
            'csdag' : 'CSD',
            'SqrtX' : 'SX',
            'abc' : PyQuantumKitError,
        }
        for input in cases:
            with self.subTest(input):
                if is_exception(cases[input]):
                    self.assertRaises(cases[input], get_standard_gatename, input)
                else:
                    self.assertEqual(get_standard_gatename(input), cases[input])

