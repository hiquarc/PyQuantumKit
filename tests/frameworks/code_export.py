# test: frameworks/code_export.py
#    2026/3/25
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

import unittest as UT
from pyquantumkit.test_code_translation import *

class Test_translate_scripts(UT.TestCase):
    def test_qiskit(self):
        print(test_apply_gate_all('qiskit', 'qc'))
    def test_pyquafu(self):
        print(test_apply_gate_all('pyquafu', 'qc'))
    def test_pyqpanda3(self):
        print(test_apply_gate_all('pyqpanda3', 'qc'))
    def test_cqlib(self):
        print(test_apply_gate_all('cqlib', 'qc'))

class Test_extra_languages(UT.TestCase):
    def test_qsharp(self):
        print(test_apply_gate_all('Q#', 'qs'))
    def test_isq(self):
        print(test_apply_gate_all('isQ', 'qs'))
    def test_openqasm2(self):
        print(test_apply_gate_all('OpenQASM2.0', 'qs'))

if __name__ == '__main__':
    UT.main()
# To TEST: copy the output text into a source file of the target language, and then compile it.
