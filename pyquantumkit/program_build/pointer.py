# program_build/pointer.py
#    2026/8/20
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

import copy
from .qtype import QVar

class PointerToQ:
    def __init__(self, other = None):
        if other is None:
            self.set_nullptr()
            return
        if isinstance(other, QVar):
            self.set_ptr_to(other)
            return
        if isinstance(other, PointerToQ):
            self._builder = other._builder
            self._address = other._address
            self._interval = other._interval
            self._interpret_obj = other._interpret_obj
            return
        else:
            raise TypeError("The parameter must be None or have type QVar or PointerToQ.")

    def set_ptr_to(self, ptr_to_obj : QVar):
        if ptr_to_obj is None:
            self.set_nullptr()
            return
        self._builder = ptr_to_obj._builder
        self._address = ptr_to_obj._address
        self._interval = ptr_to_obj.n_qubits()
        self._interpret_obj = ptr_to_obj
    def set_nullptr(self):
        self._builder = None
        self._address = None
        self._interval = 0
        self._interpret_obj = None
    def is_nullptr(self) -> bool:
        return self._address is None

    def reinterpret(self, ) -> None:
        # TODO: finish
        pass

    def __add__(self, other : int):
        if not isinstance(other, int):
            raise TypeError("The right operand of + must be an integer.")
        ret = PointerToQ(self)
        ret._address += ret._interval * other
        return ret
    def __radd__(self, other : int):
        if not isinstance(other, int):
            raise TypeError("The left operand of + must be an integer.")
        ret = PointerToQ(self)
        ret._address += ret._interval * other
        return ret
    def __iadd__(self, other):
        if not isinstance(other, int):
            raise TypeError("The right operand of += must be an integer.")
        self._address += self._interval * other
        return self

    def __sub__(self, other):
        if isinstance(other, int):
            ret = PointerToQ(self)
            ret._address -= ret._interval * other
            return ret
        elif isinstance(other, PointerToQ):
            if self._builder is not other._builder:
                raise TypeError("Two PointerToQ to different builder cannot be substracted.")
            if self._interval != other._interval:
                raise TypeError("Two PointerToQ with different interval cannot be substracted.")
            return (self._address - other._address) // self._interval
        else:
            raise TypeError("The right operand of - must be an integer or PointerToQ.")
    def __isub__(self, other):
        if not isinstance(other, int):
            raise TypeError("The right operand of -= must be an integer.")
        self._address -= self._interval * other
        return self

    def __int__(self) -> int:
        if self.is_nullptr():
            raise TypeError("Cannot convert a null PointerToQ into an integer.")
        return self._address
    def get_address(self) -> int|None:
        return self._address

    def deref(self):
        copy.deepcopy(self._interpret_obj)
        
