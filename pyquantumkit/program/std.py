# program/std.py
#    2026/8/17
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from pyquantumkit.program_build.qtype import QVar, QStruct, QTuple, QUnion, QArray, QuantumProgramBuildError, ResultInterpretError
from pyquantumkit.program_build.builder import QProgramBuilder
from pyquantumkit._qframes.code_translate import get_standard_gatename

class Qubit(QVar):
    """
    Qubit: the basic quantum type for "quantum bit".
    """
    def __init__(self, varname : str = None):
        super().__init__(varname)
    def n_qubits(self) -> int:
        return 1
    def _measure(self, m_address : int) -> None:
        super()._measure(m_address)
        self._builder._built_circuit.apply_measure([self._address], [self._m_address])
    def _interpret_(self, output : str) -> str:
        if output[self._m_address] == '0':
            return '0'
        elif output[self._m_address] == '1':
            return '1'
        else:
            raise ResultInterpretError(f"Invalid output string '{output}'")
    def _gate_(self, gate_name : str, qubit_var_list : list, paras : list):
        return self


def gate(gate_name : str, qubit_var_list : list[Qubit], paras : list = None) -> None:
    """
    Apply a quantum gate on one or several Qubit variables.

        gate_name      : (str) a string to identify the quantum gate.
        qubit_var_list : (list[Qubit]) the list of applied Qubit variables.
        paras          : (optional) the parameters of the gate
    """
    builder = qubit_var_list[0]._builder
    if builder is None or (not isinstance(builder, QProgramBuilder)):
        raise QuantumProgramBuildError("Cannot load the builder. Do you forget to declare the quantum variable?")
    for var in qubit_var_list:
        if not isinstance(var, QVar):
            raise QuantumProgramBuildError(f"<{var}> is not qubit variable.")
        if not hasattr(var, '_gate_'):
            raise QuantumProgramBuildError(f"<{var}> does not define the attribute '_gate_'. It cannot be regarded as Qubit.")
        if var._builder is not builder:
            raise QuantumProgramBuildError("Qubits belongs to different QProgramBuilder!")

    index_list = [var._gate_(gate_name, qubit_var_list, paras)._address for var in qubit_var_list]
    builder._apply_gate(gate_name, index_list, paras)


class QubitArray(QArray):
    """
    QubitArray: the quantum type for the array of Qubit.
    """
    def __init__(self, length : int, varname = None):
        """
        Create an array for Qubit.

            length  : (int) the number of elements.
            varname : (str) the name of the QArray variable.
        """
        super().__init__(varname)
        self._length = length
        self._base_obj = Qubit()
        self.init_qarray()
    def _interpret_(self, output : str):
        return ''.join(super()._interpret_(output))

    def create_state_by_01pm_str(self, statestr : str) -> None:
        """
        Create a state according to a 0/1/+/- string on the QubitArray.

            e.g., '01+-' --> q[0]=|0>, q[1]=|1>, q[2]=|+>, q[3]=|->

            statestr  : the '0'/'1'/'+'/'-' string to describe the state
        """
        N = len(statestr)
        if len(statestr) != len(self):
            raise ValueError('the length of <statestr> must match the length of QubitArray.')
        for i in range(0, N):
            if statestr[i] not in {'0', '1', '+', '-'}:
                raise QuantumProgramBuildError('binstr must be 0/1/+/- string!')
            if statestr[i] == '1':
                gate('X', [self[i]])
            elif statestr[i] == '+':
                gate('H', [self[i]])
            elif statestr[i] == '-':
                gate('X', [self[i]])
                gate('H', [self[i]])
    def uncompute_state_by_01pm_str(self, statestr : str) -> None:
        """
        Uncompute a state according to a 0/1/+/- string on the QubitArray.

            statestr  : the '0'/'1'/'+'/'-' string to describe the state
        """
        N = len(statestr)
        if len(statestr) != len(self):
            raise ValueError('the length of <statestr> must match the length of QubitArray.')
        for i in range(0, N):
            if statestr[i] not in {'0', '1', '+', '-'}:
                raise QuantumProgramBuildError('binstr must be 0/1/+/- string!')
            if statestr[i] == '1':
                gate('X', [self[i]])
            elif statestr[i] == '+':
                gate('H', [self[i]])
            elif statestr[i] == '-':
                gate('H', [self[i]])
                gate('X', [self[i]])

    def create_complementary_superposition(self, binstr : str, phi : float = None) -> None:
        """
        Create a complementary superposition state according to statestr.

            e.g., '0100' --> 1/sqrt(2)*(|0100> + e^{iφ}|1011>)

            binstr : (str) the '0'/'1' string to describe one of the components
            phi    : (float) the relative phase angle φ, default 0
        """
        N = len(binstr)
        if N != len(self):
            raise ValueError('the length of <binstr> must match the length of QubitArray.')
        for c in binstr:
            if c not in {'0', '1'}:
                raise QuantumProgramBuildError('binstr must be 0/1 string!')
        gate('H', [self[0]])
        if (binstr[0] == '1'):
            if phi is not None:
                gate('U1', [self[0]], [-phi])
            for i in range(1, N):
                if (binstr[i] == '0'):
                    gate('X', [self[i]])
                gate('CX', [self[0], self[i]])
        else:
            if phi is not None:
                gate('U1', [self[0]], [phi])
            for i in range(1, N):
                if (binstr[i] == '1'):
                    gate('X', [self[i]])
                gate('CX', [self[0], self[i]])

    def create_two_binstr_superposition(self, binstr1 : str, binstr2 : str, phi : float = None) -> None:
        """
        Create a two-value superposition state according to two binary strings.

            e.g., '11001', '01110' --> 1/sqrt(2)*(|11001> + e^{iφ}|01110>)

            binstr1 : (str) the '0'/'1' string to describe one component
            binstr2 : (str) the '0'/'1' string to describe another component
            phi     : (float) the relative phase angle φ, default 0
        """
        N = len(binstr1)
        if N != len(self) or N != len(binstr2):
            raise ValueError('the length of <binstr1>, <binstr2> must match the length of QubitArray.')
        for c in binstr1:
            if c not in {'0', '1'}:
                raise QuantumProgramBuildError('binstr1 must be 0/1 string!')
        for c in binstr2:
            if c not in {'0', '1'}:
                raise QuantumProgramBuildError('binstr2 must be 0/1 string!')

        difflist = []
        for i in range(0, N):
            if (binstr1[i] == binstr2[i]):
                if (binstr1[i] == '1'):
                    gate('X', [self[i]])
            else:
                difflist.append(i)

        Ndiff = len(difflist)
        if (Ndiff > 0):
            gate('H', [self[difflist[0]]])
            if (binstr1[difflist[0]] == '1'):
                if phi is not None:
                    gate('U1', [self[difflist[0]]], [-phi])
                for i in range(1, Ndiff):
                    if (binstr1[difflist[i]] == '0'):
                        gate('X', [self[difflist[i]]])
                    gate('CX', [self[difflist[0]], self[difflist[i]]])
            else:
                if phi is not None:
                    gate('U1', [self[difflist[0]]], [phi])
                for i in range(1, Ndiff):
                    if (binstr1[difflist[i]] == '1'):
                        gate('X', [self[difflist[i]]])
                    gate('CX', [self[difflist[0]], self[difflist[i]]])


def make_qarray(base : type|QVar, length : int, varname : str = None) -> QArray:
    """
    Create an array for a given quantum type.

        base    : (type or QVar) indicate the base type of the QArray.
        length  : (int) the number of elements.
        varname : (str) the name of the QArray variable.
    """
    base_obj = None
    if isinstance(base, QVar):
        base_obj = base
    elif isinstance(base, type) and issubclass(base, QVar):
        base_obj = base()
    else:
        raise QuantumProgramBuildError(str(base) + " is not a quantum type or variable.")
    class QArrayType(QArray):
        def __init__(self, varname = None):
            super().__init__(varname)
            self._length = length
            self._base_obj = base_obj
            self.init_qarray()
    return QArrayType(varname)


def make_qtuple(element_type : tuple[type|QVar], varname : str = None) -> QTuple:
    """
    Create an array for a given quantum type.

        element_type : (tuple[type|QVar]) indicate the base type of each element.
        varname      : (str) the name of the QArray variable.
    """
    element_obj_list = []
    for element in element_type:
        if isinstance(element, QVar):
            element_obj_list.append(element)
        elif isinstance(element, type) and issubclass(element, QVar):
            element_obj_list.append(element())
        else:
            raise QuantumProgramBuildError(str(element) + " is not a quantum type or variable.")
    class QTupleType(QTuple):
        def __init__(self, varname = None):
            super().__init__(varname)
            self.init_qstruct(*element_obj_list)
    return QTupleType(varname)

