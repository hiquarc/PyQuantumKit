# test: frameworks/on_classical.py
#    2025/6/27
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

import unittest as UT
from tests.common.test_classical import Test_classical_common, Test_classical_run_result
from tests.common.test_qframes import Test_qframes_code_translate
from tests.common.test_procedure import Test_procedure_circuit_io
from tests.common.test_symbol import Test_symbol_gate, Test_symbol_circuit

if __name__ == '__main__':
    UT.main()
