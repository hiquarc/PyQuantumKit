import unittest as UT
from pyquantumkit.classical.common import *

class Test_classical_common(UT.TestCase):
    def test_rand_diff_int_pair(self):
        cases = [
            [0, 1], [2, 13], [15, 17], [23, 24] 
        ]
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


class Test_classical_run_result(UT.TestCase):
    def test_get_substr_by_indexlist(self):
        pass
