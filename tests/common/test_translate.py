# test: common/test_translate.py
#    2025/6/29
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

import unittest as UT
from pyquantumkit.translate.common import *
from .common import is_exception

class Test_translate_common(UT.TestCase):
    def test_get_args_assign_str(self):
        cases = {
            ('arr', ()) : "",
            ('arr', (0,)) : "arr[0]",
            ('arr', (0, 1)) : "arr[0],arr[1]",
            ('Tree', (0, 1, 2)) : "Tree[0],Tree[1],Tree[2]",
            ('Tree', (2, 1, 0)) : "Tree[2],Tree[1],Tree[0]",
            ('List', (0, 1, 2, 3)) : "List[0],List[1],List[2],List[3]",
            ('List', (0, 3, 1, 4)) : "List[0],List[3],List[1],List[4]",
            ('c', (5, 3, 4), '(', ')', ';') : "c(5);c(3);c(4)",
        }
        for input in cases:
            with self.subTest(input):
                output = cases[input]
                self.assertEqual(get_args_assign_str(*input), output)

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
            'abc' : FrameworkMapError,
        }
        for input in cases:
            with self.subTest(input):
                if is_exception(cases[input]):
                    self.assertRaises(cases[input], get_standard_gatename, input)
                else:
                    self.assertEqual(get_standard_gatename(input), cases[input])
