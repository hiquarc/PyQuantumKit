# procedure/circuit_io.py
#    2025/7/20
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from pyquantumkit import PyQuantumKitError
from pyquantumkit.procedure.generic import apply_gate
from pyquantumkit.classical.common import indexlist_length
from pyquantumkit._qframes.code_translate import Standard_Gate_Name, get_standard_gatename


def inverse_gate(item : list):
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


class CircuitIO:
    def __init__(self, nqbits : int = 0, ncbits : int = 0) -> None:
        self._gatelist = []
        self._nqbits = nqbits
        self._ncbits = ncbits

    def clear(self):
        self._gatelist.clear()

    def set_nqbits(self, nqbits) -> None:
        self._nqbits = nqbits
    
    def get_nqbits(self) -> int:
        return self._nqbits
    
    def check_nqbits(self, adjust : bool = False) -> bool:
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
        self._ncbits = ncbits
    
    def get_ncbits(self) -> int:
        return self._ncbits
    
    def check_ncbits(self, adjust : bool = False) -> bool:
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
        g = get_standard_gatename(gatestr)
        if g not in Standard_Gate_Name:
            raise PyQuantumKitError("Gate is not supported: " + g)
        self._gatelist.append([g, qbits, paras])

    def apply_measure(self, qindex : list[int], cindex : list[int]) -> None:
        self.apply_gate('M', qindex, cindex)

    def inverse(self) -> None:
        """
        Inverse the whole circuit
        """
        self._gatelist.reverse()
        for item in self._gatelist:
            inverse_gate(item)
    
    def remap_qubits(self, remap : int|list|range) -> None:
        """
        Remap the qubits of the whole circuit
            remap      : (int or list[int])
                        if the type of <remap> is int, give the offset of each qubit index
                        if the type of <remap> is list[int], give the remap list of the qubit indices
        """
        if remap is None:
            return
        if isinstance(remap, int):
            for item in self._gatelist:
                for i in range(0, len(item[1])):
                    item[1][i] += remap
        elif isinstance(remap, (list, range)):
            for item in self._gatelist:
                for i in range(0, len(item[1])):
                    item[1][i] = remap[item[1][i]]
        else:
            raise PyQuantumKitError('Invalid remap: ' + str(remap))

    def remap_cbits(self, remap : int|list|range) -> None:
        """
        Remap the cbits of the whole circuit
            remap      : (int or list[int])
                        if the type of <remap> is int, give the offset of each cbits index
                        if the type of <remap> is list[int], give the remap list of the cbits indices
        """
        if remap is None:
            return
        if isinstance(remap, int):
            for item in self._gatelist:
                if item[0] == 'M':
                    for i in range(0, len(item[2])):
                        item[2][i] += remap
        elif isinstance(remap, (list, range)):
            for item in self._gatelist:
                if item[0] == 'M':
                    for i in range(0, len(item[2])):
                        item[2][i] = remap[item[2][i]]
        else:
            raise PyQuantumKitError('Invalid remap: ' + str(remap))

    def append_circuit_io(self, cir_io_obj):
        self._gatelist += cir_io_obj._gatelist

    def __iadd__(self, cir_io_obj):
        self.append_circuit_io(cir_io_obj)
        return self
    
    def __add__(self, cir_io_obj):
        nqs = max(self._nqbits, cir_io_obj._nqbits)
        ncs = max(self._ncbits, cir_io_obj._ncbits)
        ret = CircuitIO(nqs, ncs)
        ret.append_circuit_io(self)
        ret.append_circuit_io(cir_io_obj)
        return ret

    def append_into_actual_circuit(self, dest_qcir) -> None:
        for item in self._gatelist:
            apply_gate(dest_qcir, item[0], item[1], item[2])
        return dest_qcir
    
    def get_circuit_code(self, language : str, circuit_name : str, linebreak = '\n') -> str:
        """
        Covert the CircuitIO object into string of code

            language     : 
            circuit_name :
        TODO: finish the function
        """
        pass
