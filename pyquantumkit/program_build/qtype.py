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
    """
    QVar: the common base class of all quantum variables.
    """
    @abc.abstractmethod
    def __init__(self, varname : str = None):
        self._varname = varname
        self._relative_address = 0
        self._address = None
        self._m_address = None
        self._builder = None

    def get_varname(self) -> str:
        """
        Get the name of the quantum variable.
        """
        return self._varname
    def get_address(self) -> int|None:
        """
        Get the (absolute) address of the quantum variable.
        """
        return self._address
    def get_builder(self):
        """
        Get the associated QProgramBuilder object.
        """
        return self._builder

    def _locate(self, builder, address : int) -> None:
        """
        (Inner function) Assign the builder and address for the quantum variable.
        """
        # Set the associated QProgramBuilder object
        self._builder = builder
        # Absolute address = target address + relative address
        self._address = address + self._relative_address
    def _measure(self, m_address : int) -> None:
        """
        (Inner function) Assign the measurement address for the quantum variable.
        """
        self._m_address = m_address

    # def get_pointer_toq(self):
    #     #TODO: finish
    #     pass

    # ------ user-define special methods ------
    @abc.abstractmethod
    def n_qubits(self) -> int|None:
        """
        Get the number of qubits of the quantum variable.
        """
        pass

    def n_measure_cbits(self) -> int|None:
        """
        Get the number of measure cbits of the quantum variable.
        """
        return self.n_qubits()

    @abc.abstractmethod
    def _interpret_(self, output : str):
        """
        Define how to interpret the output string for the quantum variable.
        """
        pass

    def _initialize_(self) -> None:
        """
        Initialize operation.
        
        It will be called automatically when the quantum variable is declared.
        """
        pass

    def _premeasure_(self) -> None:
        """
        Pre-measurement operation.

        It will be called automatically before the quantum variable is measured.
        """
        pass


class QStruct(QVar, abc.ABC):
    """
    QStruct: the abstract class for the "quantum Struct"
    """
    @abc.abstractmethod
    def __init__(self, varname = None):
        super().__init__(varname)
        self._items = None

    def init_qstruct(self, *args) -> None:
        """
        init_qstruct() must be called in the user-define QStruct type.

        The parameters are the items in the QStruct.
        """
        current_address = 0
        for item in args:
            if not isinstance(item, QVar):
                raise TypeError(f"{item} is not a quantum variable.")
            # Calculate the relative address for each item.
            #      Contiguous allocation of qubits.
            item._relative_address = current_address
            current_address += item.n_qubits()
        self._items = args

    def _locate(self, builder, address : int) -> None:
        super()._locate(builder, address)
        for item in self._items:
            # Locate each item of QStruct.
            item._locate(builder, self._address)
    def _measure(self, m_address : int) -> None:
        super()._measure(m_address)
        offset = 0
        for item in self._items:
            # Measure each item of QStruct.
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

    def _interpret_(self, output : str):
        ret = {}
        for item in self._items:
            ret[item.get_varname()] = item._interpret_(output)
        return ret

    def _initialize_(self) -> None:
        for item in self._items:
            item._initialize_()
    def _premeasure_(self) -> None:
        for item in self._items:
            item._premeasure_()


class QTuple(QStruct):
    """
    QTuple: the abstract class for the "quantum Tuple"
    """
    @abc.abstractmethod
    def __init__(self, varname = None):
        super().__init__(varname)
    def __getitem__(self, index : int):
        if not isinstance(index, int):
            raise TypeError("The index for QTuple must be integer.")
        return self._items[index]
    def _interpret_(self, output : str):
        ret = []
        for item in self._items:
            ret.append(item._interpret_(output))
        return ret


class QUnion(QVar, abc.ABC):
    @abc.abstractmethod
    def __init__(self, varname = None):
        super().__init__(varname)
        self._items = None
        self._activity_item = None

    def init_qunion(self, *args) -> None:
        """
        init_qunion() must be called in the user-define QUnion type.

        The parameters are the items in the QUnion.
        """
        for item in args:
            if not isinstance(item, QVar):
                raise TypeError(f"{item} is not a quantum variable.")
            # The relative address of all items will be set as 0.
            item._relative_address = 0
        self._items = args

    def _locate(self, builder, address : int) -> None:
        super()._locate(builder, address)
        for item in self._items:
            # Locate each item of QUnion.
            item._locate(builder, self._address)
    def _measure(self, m_address : int) -> None:
        if self._activity_item is None:
            raise QuantumProgramBuildError("No activity item is specified before measurement.")
        super()._measure(m_address)
        # Only the activity item will be measured.
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
        """
        Set the activity item of the QUnion.

            act_item : must be one of the items of this QUnion.
        """
        if act_item not in self._items:
            raise QuantumProgramBuildError(f"{act_item} is not the item of QUnion {self}")
        self._activity_item = act_item

    def _interpret_(self, output : str):
        if self._activity_item is None:
            raise QuantumProgramBuildError("No activity item is specified.")
        ret = {}
        ret[self._activity_item.get_varname()] = self._activity_item._interpret_(output)
        return ret

    def _initialize_(self) -> None:
        for item in self._items:
            item._initialize_()
    def _premeasure_(self) -> None:
        for item in self._items:
            item._premeasure_()


class QArray(QVar, abc.ABC):
    @abc.abstractmethod
    def __init__(self, varname = None):
        super().__init__(varname)
        self._length = None
        self._base_obj = None
        self._items = None

    def init_qarray(self) -> None:
        if not isinstance(self._base_obj, QVar):
            raise TypeError(f"{self._base_obj} is not a quantum variable.")
        if self._length is None:
            return
        if self._length < 0:
            raise ValueError("The length of array must >= 0.")
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
            raise QuantumProgramBuildError(f"Cannot call _locate() on the undetermined-length QArray: {self}")
        for item in self._items:
            # Locate each element of QArray.
            item._locate(builder, self._address)
    def _measure(self, m_address : int) -> None:
        super()._measure(m_address)
        if self._length is None:
            raise QuantumProgramBuildError(f"Cannot measure the undetermined-length QArray: {self}")
        offset = 0
        for item in self._items:
            # Measure each element of QArray.
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
        if not isinstance(index, int):
            raise TypeError("The index for QArray must be integer.")
        return self._items[index]

    def _interpret_(self, output : str):
        ret = []
        for item in self._items:
            ret.append(item._interpret_(output))
        return ret

    def _initialize_(self) -> None:
        for item in self._items:
            item._initialize_()
    def _premeasure_(self) -> None:
        for item in self._items:
            item._premeasure_()
