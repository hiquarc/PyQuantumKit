# test: frameworks/custom_script.py
#    2026/11/11
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

import unittest as UT
from pyquantumkit.translate.customize import *
from pyquantumkit.test_code_translation import test_apply_gate

class Test_translate_customize(UT.TestCase):
    def test_update_language_translation(self):
        fname = 'TestScript'
        script = 'custom_script_for_test'
        update_language_translation(fname, script)
        return_code = test_apply_gate('TestScript', 'qc', 'Rxx', [1, 3, 2], [0.54321])
        expected_code = """TEST comment
TEST IMPORT "stdlib"
TEST prefix
TEST DECLARE qc None False 4 0
TEST APPLY qc None RXX [1, 3, 2] [0.54321] False
TEST suffix
"""
        self.assertEqual(return_code, expected_code)

if __name__ == '__main__':
    UT.main()
