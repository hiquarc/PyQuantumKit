# procedure/circuit_io.py
#    2025/7/20
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

import copy, sympy
from pyquantumkit import PyQuantumKitError, apply_gate
from pyquantumkit._qframes.framework_map import gate_applying_code
from pyquantumkit.classical.common import indexlist_length
from pyquantumkit._qframes.code_translate import Standard_Gate_Name, get_standard_gatename
from pyquantumkit.symbol.gate import symbol_gate_matrix
from pyquantumkit.symbol.circuit import symbol_apply_gate

class CircuitIO:
    def __inverse_gate(self, item : list):
        if item[0] == 'M':
            raise PyQuantumKitError("Measurement cannot be inversed!")
        if item[0] == 'S':
            item[0] = 'SD'
        elif item[0] == 'T':
            item[0] = 'TD'
        elif item[0] == 'SD':
            item[0] = 'S'
        elif item[0] == 'TD':
            item[0] = 'T'
        elif item[0] in {'RX', 'RY', 'RZ', 'CRX', 'CRY', 'CRZ', 'RXX', 'RYY', 'RZZ', 'U1', 'CU1'}:
            item[2] = [-item[2][0]]
        elif item[0] == 'U3':
            item[2] = [-item[2][0], -item[2][2], -item[2][1]]
    
    def __init__(self, nqbits : int = 0, ncbits : int = 0) -> None:
        """
        Construct a CircuitIO object
        """
        self._gatelist = []
        self._nqbits = nqbits
        self._ncbits = ncbits

    def clear(self):
        """
        Clear all gates in the object
        """
        self._gatelist.clear()

    def set_nqbits(self, nqbits) -> None:
        """
        Set the number of qubits PLAN to be used

        NOTE: nqbits is a tip for generic copy_circuit, copy_programs, get_n_qubits,
             get_qubits_list, parallel_circuits, parallel_programs functions
        """
        self._nqbits = nqbits
    
    def get_nqbits(self) -> int:
        """
        Set the number of qubits PLAN to be used

        NOTE: nqbits is a tip for generic copy_circuit, copy_programs, get_n_qubits,
             get_qubits_list, parallel_circuits, parallel_programs functions
        """
        return self._nqbits
    
    def check_nqbits(self, adjust : bool = False) -> bool:
        """
        Check whethe nqbits is sufficient to contain all gates

            adjust : if <adjust> is True, nqubits will be adjust to contain all gates;
                     defaulit False

        -> Return : True if nqbits is sufficient; otherwise False
        """
        maxindex = -1
        for item in self._gatelist:
            for idx in item[1]:
                if idx > maxindex:
                    maxindex = idx
        if self._nqbits <= maxindex:
            if adjust:
                self._nqbits = maxindex + 1
            return False
        return True

    def set_ncbits(self, ncbits) -> None:
        """
        Set the number of cbits PLAN to be used

        NOTE: nqbits is a tip for generic copy_programs, get_n_cbits, get_cbits_list, parallel_programs functions
        """
        self._ncbits = ncbits
    
    def get_ncbits(self) -> int:
        """
        Get the number of cbits PLAN to be used

        NOTE: nqbits is a tip for generic copy_programs, get_n_cbits, get_cbits_list, parallel_programs functions
        """
        return self._ncbits
    
    def check_ncbits(self, adjust : bool = False) -> bool:
        """
        Check whethe cbits is sufficient to contain all measurements

            adjust : if <adjust> is True, ncbits will be adjust to contain all measurements;
                     defaulit False

        -> Return : True if ncbits is sufficient; otherwise False
        """
        maxindex = -1
        for item in self._gatelist:
            if item[0] == 'M':
                for idx in item[2]:
                    if idx > maxindex:
                        maxindex = idx
        if self._ncbits <= maxindex:
            if adjust:
                self._ncbits = maxindex + 1
            return False
        return True

    def apply_gate(self, gatestr : str, qbits : list[int], paras : list = None) -> None:
        """
        Apply a quantum gate on a quantum circuit

            NOTE: this function will not do check for the validity of nqbits and ncbits

            q_circuit : applied quantum circuit
            gate_str  : a string to identify the quantum gate
            qbits     : the indexes of applied qubits
            paras     : (optional) the parameters of the gate

        -> Return : q_circuit
        """
        g = get_standard_gatename(gatestr)
        self._gatelist.append([g, qbits, paras])

    def apply_measure(self, qindex : list[int], cindex : list[int]) -> None:
        """
        Apply measurement operation on a quantum circuit

            NOTE: this function will not do check for the validity of nqbits and ncbits

            q_circuit : applied quantum circuit
            qindex    : the indexes of measured qubits
            cindex    : the indexes of cbits to contain results

        -> Return : q_circuit
        """
        self.apply_gate('M', qindex, cindex)

    def inverse(self) -> None:
        """
        Inverse the whole circuit (inplace)
        """
        self._gatelist.reverse()
        for item in self._gatelist:
            self.__inverse_gate(item)
    
    def remap_qbits(self, remap : int|list|range) -> None:
        """
        Remap the qubits of the whole circuit (inplace)

            remap : (int or list[int])
                     if the type of <remap> is int, give the offset of each qubit index
                     if the type of <remap> is list[int], give the remap list of the qubit indices
        """
        if remap is None:
            return
        if isinstance(remap, int):
            for item in self._gatelist:
                for i in range(len(item[1])):
                    item[1][i] += remap
        elif isinstance(remap, (list, range)):
            for item in self._gatelist:
                for i in range(len(item[1])):
                    item[1][i] = remap[item[1][i]]
        else:
            raise PyQuantumKitError('Invalid remap: ' + str(remap))

    def remap_cbits(self, remap : int|list|range) -> None:
        """
        Remap the cbits of the whole circuit (inplace)

            remap      : (int or list[int])
                        if the type of <remap> is int, give the offset of each cbits index
                        if the type of <remap> is list[int], give the remap list of the cbits indices
        """
        if remap is None:
            return
        if isinstance(remap, int):
            for item in self._gatelist:
                if item[0] == 'M':
                    for i in range(len(item[2])):
                        item[2][i] += remap
        elif isinstance(remap, (list, range)):
            for item in self._gatelist:
                if item[0] == 'M':
                    for i in range(len(item[2])):
                        item[2][i] = remap[item[2][i]]
        else:
            raise PyQuantumKitError('Invalid remap: ' + str(remap))

    def append_circuit_io(self, cir_io_obj):
        """
        Append the gates in other CircuitIO object into this CircuitIO object

        NOTE: You can use operator << to replace this function

            cir_io_obj : the target object (only support CircuitIO object)
        """
        # Must use deepcopy
        self._gatelist.extend(copy.deepcopy(cir_io_obj._gatelist))
        return self

    def __lshift__(self, cir_io_obj):
        return self.append_circuit_io(cir_io_obj)

    def append_into_actual_circuit(self, dest_qcir):
        """
        Append the gates of this CircuitIO object to the destination quantum circuit

        NOTE: You can use operator >> to replace this function

            dest_qcir : the destination object (can be circuit class in concrete
                        quantum software stacks or CircuitIO object)
        """
        for item in self._gatelist:
            apply_gate(dest_qcir, item[0], item[1], item[2])
        return self
    
    def __rshift__(self, dest_qcir):
        return self.append_into_actual_circuit(dest_qcir)
    
    def get_circuit_code(self, language : str, circuit_name : str,
                          gate_lib_name : str = None, linebreak : str = '\n') -> str:
        """
        Convert the CircuitIO object into string of code

            language      : specify the language
            circuit_name  : specify the circuit name will be used in the code
            gate_lib_name : specify the library name of gates used in the code (default None)
            NOTE:   If no gate library name will be used, please specify None (rather than empty str '') 
            linebreak     : the characters of linebreaks in the code (default '\n')

        -> Return : the code string
        """
        ret = ""
        for item in self._gatelist:
            ret += gate_applying_code(language, circuit_name, gate_lib_name, linebreak,
                                        item[0], item[1], item[2])
            ret += linebreak
        return ret
    
    def get_circuit_matrix(self) -> sympy.Matrix:
        """
        Calculate the matrix representation of this CircuitIO object

        -> Return : the sympy.Matrix object with dimension 2^n x 2^n,
                    where n is the number of qubits
        """
        ret = sympy.Identity(2 ** self._nqbits)
        for item in self._gatelist:
            gatemat = symbol_gate_matrix(item[0], item[2])
            gatemat_total = symbol_apply_gate(gatemat, self._nqbits, item[1])
            ret = gatemat_total * ret
        return ret.simplify()
