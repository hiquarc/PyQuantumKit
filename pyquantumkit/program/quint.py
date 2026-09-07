# program/quint.py
#    2026/8/27
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from pyquantumkit.classical.common import get_int_from_binstr_le, get_binstr_from_int_le
from .std import QStruct, QubitArray, gate

class QuUnsignedInt(QStruct):
    def __init__(self, length, varname = None):
        super().__init__(varname)
        self.__qubits = QubitArray(length)
        self.init_qstruct(self.__qubits)

    def _interpret_(self, output : str):
        binstr = self.__qubits._interpret_(output)
        return get_int_from_binstr_le(binstr)
    def __len__(self):
        return len(self.__qubits)

    def create_classical_value(self, number : int):
        """
        Create a classical value |number> on QuUnsignedInt.

            NOTE: if number >= 2**len(qbitlist), the high bits of <number> will be discarded

            number : (int) the non-negative integer to describe the state
        """
        if number < 0:
            raise ValueError('<number> must be a non-negative integer!')
        temp = number
        for i in range(0, len(self.__qubits)):
            if ((temp & 1) == 1):
                gate('X', [self.__qubits[i]])
            temp >>= 1
    def uncompute_classical_value(self, number : int):
        """
        Uncompute the classical value |number> on QuUnsignedInt.

            NOTE: if number >= 2**len(qbitlist), the high bits of <number> will be discarded

            number : (int) the non-negative integer to describe the state
        """
        self.create_classical_value(number)

    def create_complementary_superposition(self, x : int, phi : float = None):
        """
        Create state |x> + e^{iφ}|~x>, where ~x is the bitwise negation of x.

            e.g. 25 = 11001b --> |10011> + e^{iφ}|01100>

            NOTE: if number >= 2**len(qbitlist), the high bits of <number> will be discarded

            q_circuit : applied quantum circuit
            x         : (int) the integer x
            phi       : (float) the relative phase angle φ, default 0
        """
        if x < 0:
            raise ValueError('<number> must be a non-negative integer!')
        xbits = get_binstr_from_int_le(x, len(self.__qubits))
        self.__qubits.create_complementary_superposition(xbits, phi)

    def create_two_value_superposition(self, x : int, y : int, phi : float = None):
        """
        Create state |x> + e^{iφ}|y>.

            NOTE: if number1/2 >= 2**len(qbitlist), the high bits of <number1/2> will be discarded

            x   : (int) the integer x
            y   : (int) the integer y
            phi : (float) the relative phase angle φ, default 0
        """
        if x < 0 or y < 0:
            raise ValueError('<number1>,<number2> must be non-negative integers!')
        xbits = get_binstr_from_int_le(x, len(self.__qubits))
        ybits = get_binstr_from_int_le(y, len(self.__qubits))
        self.__qubits.create_two_binstr_superposition(xbits, ybits, phi)


QuInt = QuUnsignedInt

