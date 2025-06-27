#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from qiskit_aer import Aer
import unittest as UT
import tests.common.test_state_prepare as T_SP

class On_pyqpanda3_Test_state_prepare_int_state(T_SP.Test_state_prepare_int_state):
    def setUp(self):
        self._fm = 'qiskit'
        self._qvm = Aer.get_backend('aer_simulator')

class On_pyqpanda3_Test_state_prepare_by_string(T_SP.Test_state_prepare_by_string):
    def setUp(self):
        self._fm = 'qiskit'
        self._qvm = Aer.get_backend('aer_simulator')

class On_pyqpanda3_Test_state_prepare_pauli_eigenstate(T_SP.Test_state_prepare_pauli_eigenstate):
    def setUp(self):
        self._fm = 'qiskit'
        self._qvm = Aer.get_backend('aer_simulator')

if __name__ == '__main__':
    UT.main()
