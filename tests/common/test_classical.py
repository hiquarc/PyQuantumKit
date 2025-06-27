#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

import unittest as UT
from pyquantumkit.classical.common import *
from pyquantumkit.classical.run_result import *
from .common import is_exception

class Test_classical_common(UT.TestCase):
    def test_rand_diff_int_pair(self):
        cases = {
            (0, 1), (2, 13), (15, 17), (23, 24),
        }
        for input in cases:
            for i in range(10):
                with self.subTest():
                    rndpair = rand_diff_int_pair(input[0], input[1])
                    self.assertIn(rndpair[0], range(input[0], input[1] + 1))
                    self.assertIn(rndpair[1], range(input[0], input[1] + 1))
                    self.assertNotEqual(rndpair[0], rndpair[1])

    def test_get_int_from_binstr_le(self):
        cases = {
            '0' : 0,
            '1' : 1,
            '10110' : 13,
            '11010010' : 75,
            '00110100' : 44,
        }
        for input in cases:
            with self.subTest():
                self.assertEqual(cases[input], get_int_from_binstr_le(input))

    def test_get_int_from_binstr_be(self):
        cases = {
            '0' : 0,
            '1' : 1,
            '10110' : 22,
            '11010010' : 210,
            '00110100' : 52,
        }
        for input in cases:
            with self.subTest():
                self.assertEqual(cases[input], get_int_from_binstr_be(input))

    def test_indexlist_length(self):
        cases = {
            None         : 0,
            ()           : 0,
            (0, 1, 2, 3) : 4,
            (0, 2, 4, 7) : 8,
        }
        for input in cases:
            with self.subTest():
                self.assertEqual(cases[input], indexlist_length(input))


# Convert tuple to dict: the even indices are keys, the odd indices are values
def tuple2dict(t : tuple) -> dict:
    if t is None:
        return None
    N = len(t)
    d = {}
    for i in range(0, N, 2):
        k = t[i]
        v = t[i + 1]
        d[k] = v
    return d


class Test_classical_run_result(UT.TestCase):
    def test_get_substr_by_indexlist(self):
        cases = {
            ('', (), True) : '',
            ('', (0,), False) : IndexError,
            ('abcdef', (0,2,3), False) : 'acd',
            ('abcdef', (0,2,3), True)  : 'fdc',
            ('12345', (1,4,6), False) : IndexError,
        }
        for input in cases:
            with self.subTest():
                inputstr = input[0]
                indexlist = list(input[1])
                reverse = input[2]
                if is_exception(cases[input]):
                    self.assertRaises(cases[input], get_substr_by_indexlist,
                                      inputstr, indexlist, reverse)
                else:
                    result = get_substr_by_indexlist(inputstr, indexlist, reverse)
                    self.assertEqual(cases[input], result)


    def test_count_subset_of_result_dict(self):
        cases = {
            ((), (), True) : {},
            ((), (0,), False) : {},
            (('00',5 , '01',6 , '10',7 , '11',8), (), False) : {},
            (('00',5 , '01',6 , '10',7 , '11',8), (0,), False) : {'0' : 11, '1' : 15},
            (('00',5 , '01',6 , '10',7 , '11',8), (1,), False) : {'0' : 12, '1' : 14},
            (('01100',12 , '01101',13 , '01110',14 , '01111',15), (0, 1, 4), False) : {'010' : 26, '011' : 28},
            (('01100',12 , '01101',13 , '01110',14 , '01111',15), (0, 1, 4), True) : {'000' : 12, '100' : 13, '010' : 14, '110' : 15},
            (('00',5 , '01',6 , '10',7 , '11',8), (1,2), True) : IndexError
        }
        for input in cases:
            with self.subTest():
                inputdict = tuple2dict(input[0])
                indexlist = list(input[1])
                reverse = input[2]
                if is_exception(cases[input]):
                    self.assertRaises(cases[input], count_subset_of_result_dict,
                                      inputdict, indexlist, reverse)
                else:
                    result = count_subset_of_result_dict(inputdict, indexlist, reverse)
                    self.assertEqual(cases[input], result)

    def test_count_first_bits_of_result_dict(self):
        cases = {
            ((), 0, True) : {},
            ((), 3, False) : {},
            (('000',5 , '010',6 , '100',7 , '110',8), 2, False) : {'00' : 5, '01' : 6, '10' : 7, '11' : 8},
            (('000',5 , '010',6 , '100',7 , '110',8), 0, False) : {},
            (('000',5 , '010',6 , '100',7 , '110',8), 2, True) : {'00' : 12, '01' : 14},
            (('0001',2 , '1000',3 , '1100',4), 3, True) : {'100' : 2, '000' : 3, '001' : 4},
            (('000',5 , '010',6 , '100',7 , '110',8), 4, True) : IndexError,
        }
        for input in cases:
            with self.subTest():
                inputdict = tuple2dict(input[0])
                indexlen = input[1]
                reverse = input[2]
                if is_exception(cases[input]):
                    self.assertRaises(cases[input], count_first_bits_of_result_dict,
                                      inputdict, indexlen, reverse)
                else:
                    result = count_first_bits_of_result_dict(inputdict, indexlen, reverse)
                    self.assertEqual(cases[input], result)

    def test_count_last_bits_of_result_dict(self):
        cases = {
            ((), 0, True) : {},
            ((), 3, False) : {},
            (('000',5 , '010',6 , '100',7 , '110',8), 2, False) : {'00' : 12, '10' : 14},
            (('000',5 , '010',6 , '100',7 , '110',8), 0, False) : {},
            (('000',5 , '010',6 , '100',7 , '110',8), 2, True) : {'00' : 5, '10' : 6, '01' : 7, '11' : 8},
            (('0001',2 , '1000',3 , '1100',4), 3, True) : {'000' : 2, '001' : 3, '011' : 4},
            (('000',5 , '010',6 , '100',7 , '110',8), 4, True) : IndexError,
        }
        for input in cases:
            with self.subTest():
                inputdict = tuple2dict(input[0])
                indexlen = input[1]
                reverse = input[2]
                if is_exception(cases[input]):
                    self.assertRaises(cases[input], count_last_bits_of_result_dict,
                                      inputdict, indexlen, reverse)
                else:
                    result = count_last_bits_of_result_dict(inputdict, indexlen, reverse)
                    self.assertEqual(cases[input], result)


    def test_get_result_str_set(self):
        cases = {
            (None, False) : {},
            ((), True) : {},
            (('000',5 , '010',6 , '100',7 , '110',8), False) : {'000', '010', '100', '110'},
            (('000',5 , '010',6 , '100',7 , '110',8), True) : {'000', '010', '001', '011'},
        }
        for input in cases:
            with self.subTest():
                inputdict = tuple2dict(input[0])
                reverse = input[1]
                if is_exception(cases[input]):
                    self.assertRaises(cases[input], get_result_str_set,
                                      inputdict, reverse)
                else:
                    result = get_result_str_set(inputdict, reverse)
                    self.assertEqual(cases[input], result)

