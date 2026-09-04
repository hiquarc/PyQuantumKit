# program_build/qtypes.py
#    2026/8/17
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

import abc, copy
from pyquantumkit import PyQuantumKitError

class QuantumProgramBuildError(PyQuantumKitError):
    pass
class ResultInterpretError(PyQuantumKitError):
    pass


class QVar(abc.ABC):
    @abc.abstractmethod
    def __init__(self, varname : str = None):
        self._varname = varname
        self._relative_address = 0
        self._address = None
        self._m_address = None
        self._builder = None

    def get_varname(self) -> str:
        return self._varname
    def get_address(self) -> int:
        return self._address
    def get_builder(self):
        return self._builder

    def _locate(self, builder, address : int) -> None:
        self._builder = builder
        self._address = address + self._relative_address
    def _measure(self, m_address : int) -> None:
        self._m_address = m_address

    # def get_pointer_toq(self):
    #     #TODO: finish
    #     pass

    @abc.abstractmethod
    def n_qubits(self) -> int|None:
        pass
    def n_measure_cbits(self) -> int|None:
        return self.n_qubits()

    @abc.abstractmethod
    def _interpret_output_str(self, output : str):
        pass


class QStruct(QVar, abc.ABC):
    @abc.abstractmethod
    def __init__(self, varname = None):
        super().__init__(varname)
        self._items = None

    def init_qstruct(self, *args):
        current_address = 0
        for item in args:
            if not isinstance(item, QVar):
                raise QuantumProgramBuildError(str(item) + " is not a quantum variable.")
            item._relative_address = current_address
            current_address += item.n_qubits()
        self._items = args

    def _locate(self, builder, address : int) -> None:
        super()._locate(builder, address)
        for item in self._items:
            item._locate(builder, self._address)
    def _measure(self, m_address : int) -> None:
        super()._measure(m_address)
        offset = 0
        for item in self._items:
            item._measure(self._m_address + offset)
            offset += item.n_measure_cbits()

    def n_qubits(self) -> int|None:
        ret = 0
        for item in self._items:
            item_nq = item.n_qubits()
            if item_nq is None:
                return None
            else:
                ret += item_nq
        return ret
    def n_measure_cbits(self) -> int|None:
        ret = 0
        for item in self._items:
            item_nmc = item.n_measure_cbits()
            if item_nmc is None:
                return None
            else:
                ret += item_nmc
        return ret

    def __len__(self) -> int:
        return len(self._items)

    def _interpret_output_str(self, output : str):
        ret = {}
        for item in self._items:
            ret[item.get_varname()] = item._interpret_output_str(output)
        return ret


class QTuple(QStruct):
    @abc.abstractmethod
    def __init__(self, varname = None):
        super().__init__(varname)
    def __getitem__(self, index : int):
        return self._items[index]
    def _interpret_output_str(self, output : str):
        ret = []
        for item in self._items:
            ret.append(item._interpret_output_str(output))
        return ret


class QUnion(QVar, abc.ABC):
    @abc.abstractmethod
    def __init__(self, varname = None):
        super().__init__(varname)
        self._items = None
        self._activity_item = None

    def init_qunion(self, *args):
        for item in args:
            if not isinstance(item, QVar):
                raise QuantumProgramBuildError(str(item) + " is not a quantum variable.")
            item._relative_address = 0
        self._items = args

    def _locate(self, builder, address : int) -> None:
        super()._locate(builder, address)
        for item in self._items:
            item._locate(builder, self._address)
    def _measure(self, m_address : int) -> None:
        if self._activity_item is None:
            raise QuantumProgramBuildError("No activity item is specified before measurement.")
        super()._measure(m_address)
        self._activity_item._measure(self._m_address)

    def n_qubits(self) -> int|None:
        ret = 0
        for item in self._items:
            item_nq = item.n_qubits()
            if item_nq is None:
                return None
            else:
                ret = item_nq if item_nq > ret else ret
        return ret
    def n_measure_cbits(self) -> int|None:
        if self._activity_item is None:
            raise QuantumProgramBuildError("No activity item is specified.")
        return self._activity_item.n_measure_cbits()

    def __len__(self) -> int:
        return len(self._items)

    def set_activity_item(self, act_item : QVar) -> None:
        if act_item not in self._items:
            raise QuantumProgramBuildError(str(act_item) + " is not the item of QUnion " + str(self))
        self._activity_item = act_item

    def _interpret_output_str(self, output : str):
        if self._activity_item is None:
            raise QuantumProgramBuildError("No activity item is specified.")
        ret = {}
        ret[self._activity_item.get_varname()] = self._activity_item._interpret_output_str(output)
        return ret


class QArray(QVar, abc.ABC):
    @abc.abstractmethod
    def __init__(self, varname = None):
        super().__init__(varname)
        self._length = None
        self._base_obj = None
        self._items = None

    def init_qarray(self) -> None:
        if not isinstance(self._base_obj, QVar):
            raise QuantumProgramBuildError(str(self._base_obj) + " is not a quantum variable.")
        if self._length is None:
            return
        if self._length < 0:
            raise QuantumProgramBuildError("The length of array must >= 0.")
        if self._length == 0:
            self._items = []
            return
        self._items = [self._base_obj] + \
                       [copy.deepcopy(self._base_obj) for _ in range(self._length - 1)]
        len_base_obj = self._base_obj.n_qubits()
        for i in range(self._length):
            self._items[i]._relative_address = i * len_base_obj

    def _locate(self, builder, address : int) -> None:
        super()._locate(builder, address)
        if self._length is None:
            raise QuantumProgramBuildError("Cannot call _locate() on the undetermined-length QArray: " + str(self))
        for item in self._items:
            item._locate(builder, self._address)
    def _measure(self, m_address : int) -> None:
        super()._measure(m_address)
        if self._length is None:
            raise QuantumProgramBuildError("Cannot measure the undetermined-length QArray: " + str(self))
        offset = 0
        for item in self._items:
            item._measure(self._m_address + offset)
            offset += item.n_measure_cbits()

    def n_qubits(self) -> int|None:
        if self._length is None:
            return None
        base_nq = self._base_obj.n_qubits()
        if base_nq is None:
            return None
        if self._length == 0:
            return 0
        return self._length * base_nq
    def n_measure_cbits(self) -> int|None:
        if self._length is None:
            return None
        base_nmc = self._base_obj.n_measure_cbits()
        if base_nmc is None:
            return None
        if self._length == 0:
            return 0
        return self._length * base_nmc
    
    def __len__(self) -> int|None:
        return self._length
    def __getitem__(self, index : int):
        return self._items[index]

    def _interpret_output_str(self, output : str):
        ret = []
        for item in self._items:
            ret.append(item._interpret_output_str(output))
        return ret

