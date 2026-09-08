# program_build/builder.py
#    2026/8/17
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from pyquantumkit import CircuitIO
from pyquantumkit._qframes.framework_map import get_reverse_output_str
from .qtype import QVar, QuantumProgramBuildError

class QProgramBuilder:
    """
    QProgramBuilder: the class to build the quantum program.
    """
    def __init__(self):
        self._built_circuit = CircuitIO()
        self._qvars = {}            # name : [obj, type, address, measure_address]
        self._qancillas = {}
        self._measure_qvars = []
        self.__n_variable_qubits = 0
        self.__n_ancilla_qubits = 0
        self.__n_measure_cbits = 0
        self.__declared_qvars = False
        self.__declared_ancilla = False
        self.__measured = False

    def clear(self) -> None:
        """
        Clear the builder.
        """
        self._built_circuit.clear()
        self._qvars.clear()
        self._qancillas.clear()
        self._measure_qvars.clear()
        self.__n_variable_qubits = 0
        self.__n_ancilla_qubits = 0
        self.__n_measure_cbits = 0
        self.__declared_qvars = False
        self.__declared_ancilla = False
        self.__measured = False

    def _apply_gate(self, gate_name : str, index_list : list[int], paras : list) -> None:
        if self.__measured:
            raise QuantumProgramBuildError("Cannot execute code after measurement.")
        self._built_circuit.apply_gate(gate_name, index_list, paras)

    def declare_qvars(self, *args) -> None:
        """
        Declare the quantum variables and associate them to the builder.

            *args : quantum variables.
        """
        if self.__declared_qvars:
            raise QuantumProgramBuildError("declare_qvars() can only be called once!")
        self.__declared_qvars = True
        current_address = 0
        for variable in args:
            if not isinstance(variable, QVar):
                raise QuantumProgramBuildError(str(variable) + " is not a quantum variable.")
            name = variable.get_varname()
            if name is None:
                raise QuantumProgramBuildError("Anonymous variables cannot be directly declared in QProgramBuilder.")
            if name in self._qvars:
                raise QuantumProgramBuildError(f"Variable name '{name}' has been declared.")
            self._qvars[name] = [variable, type(variable), current_address, None]
            variable._locate(self, current_address)
            variable._initialize_()
            current_address += variable.n_qubits()
        self.__n_variable_qubits = current_address

    def measure(self, *args) -> None:
        """
        Measure the quantum variables.

            *args : quantum variables.
        """
        if self.__measured:
            raise QuantumProgramBuildError("Measurement can only be executed once.")
        current_m_address = 0
        for variable in args:
            if not isinstance(variable, QVar):
                raise QuantumProgramBuildError(str(variable) + " is not a quantum variable.")
            if variable.get_varname() not in self._qvars:
                raise QuantumProgramBuildError(f"Cannot measure the undeclared quantum variable {variable}")
            variable._premeasure_()
            variable._measure(current_m_address)
            self._qvars[variable.get_varname()][3] = current_m_address
            self._measure_qvars.append(variable)
            current_m_address += variable.n_measure_cbits()
        self.__n_measure_cbits = current_m_address
        self.__measured = True

    def measure_all(self) -> None:
        """
        Measure all quantum variables according to the parameters when call declare_qvars(...)
        """
        measure_list = []
        for varname in self._qvars:
            measure_list.append(self._qvars[varname][0])
        self.measure(*measure_list)

    def build(self, main_func : callable, *args, **kwargs) -> None:
        """
        Build the quantum program into quantum circuit.

            main_func       : (callable) the quantum main function.
            *args, **kwargs : other parameters of the quantum main function.
        """
        main_func(self, *args, **kwargs)
        self._built_circuit.set_nqbits(self.__n_variable_qubits)
        self._built_circuit.set_ncbits(self.__n_measure_cbits)

    def get_built_circuit(self) -> CircuitIO:
        """
        Get the built CircuitIO object.
        """
        return self._built_circuit
    
    def _print_qvars(self):
        """
        (Inner function) print the quantum variables in the builder.
        """
        print(self._qvars)

    def interpret_output_str(self, output_str : str, framework : str = None) -> dict:
        """
        Interpret an output 0/1 string.

            output_str : (str) the 0/1 string.
            framework  : (str, default None) according to which framework's convention.
        """
        reverse = False if framework is None else get_reverse_output_str(framework)
        correct_str = output_str[::-1] if reverse else output_str
        ret = {}
        for variable in self._measure_qvars:
            ret[variable.get_varname()] = variable._interpret_(correct_str)
        return ret

    def interpret_result_dict(self, output_dict : dict, framework : str = None) -> list:
        """
        Interpret an output dict.

            output_str : (dict) the dict of the running results.
            framework  : (str, default None) according to which framework's convention.
        """
        ret = []
        for output_str in output_dict:
            result = self.interpret_output_str(output_str, framework)
            times = output_dict[output_str]
            ret.append((result, times))
        return ret
    
