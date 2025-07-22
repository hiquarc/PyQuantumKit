# test: frameworks/on_quafu.py
#    2025/7/5
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from quafu import simulate
import unittest as UT
import tests.common.test_procedure as T_P
import tests.common.test_state_prepare as T_SP
import tests.common.test_program_check as T_PC

RUN_TEST_FRAMEWORK = 'quafu'
RUN_TEST_MACHINE = simulate

# BEGIN ---------- procedure ----------
class On_quafu_Test_procedure_generic(T_P.Test_procedure_generic):
    def setUp(self):
        self._fm = RUN_TEST_FRAMEWORK
        self._qvm = RUN_TEST_MACHINE

    def test_apply_measure(self):
        pass

# class On_quafu_Test_procedure_paulis(T_P.Test_procedure_paulis):
#     def setUp(self):
#         self._fm = RUN_TEST_FRAMEWORK
#         self._qvm = RUN_TEST_MACHINE
# END ---------- procedure ----------

# BEGIN ---------- state_prepare ----------
class On_quafu_Test_state_prepare_int_state(T_SP.Test_state_prepare_int_state):
    def setUp(self):
        self._fm = RUN_TEST_FRAMEWORK
        self._qvm = RUN_TEST_MACHINE

class On_quafu_Test_state_prepare_by_string(T_SP.Test_state_prepare_by_string):
    def setUp(self):
        self._fm = RUN_TEST_FRAMEWORK
        self._qvm = RUN_TEST_MACHINE

class On_quafu_Test_state_prepare_pauli_eigenstate(T_SP.Test_state_prepare_pauli_eigenstate):
    def setUp(self):
        self._fm = RUN_TEST_FRAMEWORK
        self._qvm = RUN_TEST_MACHINE
# END ---------- state_prepare ----------

# BEGIN ---------- program_check ----------
# class On_quafu_Test_program_check_program_relation(T_PC.Test_program_check_program_relation):
#     def setUp(self):
#         self._fm = RUN_TEST_FRAMEWORK
#         self._qvm = RUN_TEST_MACHINE
# END ---------- program_check ----------

if __name__ == '__main__':
    UT.main()
