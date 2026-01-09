# library/hamiltonian.py
#    2025/11/24
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

import copy, sympy
from pyquantumkit.procedure.paulis import apply_exp_pauli
from pyquantumkit import PyQuantumKitError
from pyquantumkit.symbol.gate import symbol_gate_matrix

def normalize_pauli_string(origin_str : str) -> str:
    paulistr = origin_str.upper()
    for i in range(len(paulistr)):
        if paulistr[i] not in {'I', 'X', 'Y', 'Z'}:
            paulistr[i] = 'I'
    return paulistr

class PauliHamiltonian:
    def __init__(self, set_nqbits : int):
        """
        Construct a PauliHamiltonian object

            set_nqbits : (int) the number of qubits
        """
        self._nqbits = set_nqbits
        self._paulis = []
        self._factors = []
        self._focuslist = []

    def __len__(self):
        """
        Return the number of Paulis
        """
        return len(self._paulis)
    
    def get_nqbits(self) -> int:
        """
        Return the number of qubits
        """
        return self._nqbits
    
    def append_pauli(self, paulistr : str, factor : float, focus : int = 0) -> None:
        """
        Append a Pauli term
            paulistr : 'I'/'X'/'Y'/'Z' string to represent the tensor product of Pauli operators
                       NOTE: the length of string should be consistent with the number of qubits 
            factor   : (float) the factor of the Pauli term
            foucs    : (optional) the index of non-I Paulis which is applied the core rotation, default 0
        """
        if len(paulistr) != self._nqbits:
            raise PyQuantumKitError('Pauli string \"' + paulistr + '\" does not match nqbits='\
                                    + str(self._nqbits))
        self._paulis.append(normalize_pauli_string(paulistr))
        self._factors.append(factor)
        self._focuslist.append(focus)

    def append_subpauli_on_qubits(self, subpauli : str, qindex : list[int], factor : float,
                                  focus : int = 0) -> None:
        """
        Append a Pauli term, by applying some Pauli on some indexes
            paulistr : 'I'/'X'/'Y'/'Z' string to represent the tensor product of Pauli operators
                       NOTE: the length of string should not be greater than the number of qubits
            qindex   : the indexes of applied qubits
            factor   : (float) the factor of the Pauli term
            foucs    : (optional) the index of non-I Paulis which is applied the core rotation, default 0
        """
        if len(subpauli) > self._nqbits:
            raise PyQuantumKitError('Pauli string \"' + subpauli + '\" cannot be applied on nqbits='\
                                    + str(self._nqbits))
        paulistr = 'I' * self._nqbits
        normsubpauli = normalize_pauli_string(subpauli)
        for i in range(len(subpauli)):
            paulistr[qindex[i]] = normsubpauli[i]
        self.append_pauli(paulistr, factor, focus)

    def append_pauli_list(self, paulis : tuple[str], factors : tuple[float],
                          focuses : tuple[int] = None) -> None:
        """
        Append a list of Pauli terms
            paulis  : 'I'/'X'/'Y'/'Z' strings to represent the tensor product of Pauli operators
                       NOTE: the length of string should be consistent with the number of qubits 
            factors  : (float) the factors of the Pauli term
            foucss   : (optional) the indexes of non-I Paulis which is applied the core rotation, default 0
        """
        l = len(paulis)
        if l != len(factors):
            raise PyQuantumKitError('Inconsistent length of <paulis> and <factors>!')
        for i in range(l):
            f = 0 if focuses is None else focuses[i]
            self.append_pauli(paulis[i], factors[i], f)  

    def __iadd__(self, other):
        """
        Add two PauliHamiltonian object: merge the list of Pauli terms
        """
        if self.get_nqbits() != other.get_nqbits():
            raise PyQuantumKitError('Inconsistent number of qubits!')
        for i in range(len(other)):
            self.append_pauli(*other.get_pauli_info_by_index(i))
        return self

    def __add__(self, other):
        """
        Add two PauliHamiltonian object: merge the list of Pauli terms
        """
        if self.get_nqbits() != other.get_nqbits():
            raise PyQuantumKitError('Inconsistent number of qubits!')
        ret = copy.deepcopy(self)
        ret += other
        return ret

    def get_pauli_info_by_index(self, index : int) -> tuple:
        """
        Add two PauliHamiltonian object: merge the list of Pauli terms
        """
        return (self._paulis[index], self._factors[index], self._focuslist[index])
    
    def get_factor_by_pauli(self, paulistr : str) -> float:
        """
        Given a pauli string, search the corresponding factor

            paulistr : 'I'/'X'/'Y'/'Z' string to represent the tensor product of Pauli operators

        -> Return : The corresponding factor. If the term does not exsit, return 0.0
        """
        for i in len(self._paulis):
            if self._paulis[i] == paulistr:
                return self._factors[i]
        return 0.0
    
    def get_factor_focus_by_pauli(self, paulistr : str) -> tuple:
        """
        Given a pauli string, search the corresponding factor and focus

            paulistr : 'I'/'X'/'Y'/'Z' string to represent the tensor product of Pauli operators

        -> Return : (factor, focus)
        """
        for i in len(self._paulis):
            if self._paulis[i] == paulistr:
                return (self._factors[i], self._focuslist[i])
        return (0.0, 0)
    
    def pop(self, index : int = -1) -> None:
        """
        Given an index, remove the corresponding Pauli term
        """
        self._paulis.pop(index)
        self._factors.pop(index)
        self._focuslist.pop(index)

    def remove(self, paulistr : str) -> None:
        """
        Given a pauli string, remove the corresponding Pauli term
        """
        for i in range(len(self._paulis)):
            if self._paulis[i] == paulistr:
                self._paulis.pop(i)
                self._factors.pop(i)
                self._focuslist.pop(i)

    def get_matrix(self) -> sympy.Matrix:
        """
        Get the corresponding matrix of this PauliHamiltonian

        -> Return : the sympy.Matrix object with dimension 2^n x 2^n,
                    where n is the number of qubits
        """
        # TODO: Develop
        for i in len(self._paulis):
            pass


def pqk_hsim_paulis_trotter(q_circuit, hamiltonian : PauliHamiltonian, t : float, n : int, qindex : list[int]):
    """
    Hamiltonian simulation for H which is represented by the sum of Pauli tensors
    Using Lie-Trotter decomposition, with error O(t^2)

        q_circuit   : applied quantum circuit
        hamiltonian : the PauliHamiltonian object to represent target Hamiltonian
        t           : (float) evolution time
        n           : (int) rounds of decomposition
        qindex      : the indexes of applied qubits
    """
    nqbits = hamiltonian.get_nqbits()
    if nqbits != len(qindex):
        raise PyQuantumKitError("Inconsistent number of qubits of <hamiltonian> and <qindex>!")
    
    for i in range(n):
        for j in range(len(hamiltonian)):
            (pauli, factor, focus) = hamiltonian.get_pauli_info_by_index(j)
            dt = t / n * factor
            apply_exp_pauli(q_circuit, pauli, dt, qindex, focus)

    return q_circuit

def pqk_hsim_paulis_suzuki2(q_circuit, hamiltonian : PauliHamiltonian, t : float, n : int, qindex : list[int]):
    """
    Hamiltonian simulation for H which is represented by the sum of Pauli tensors
    Using 2-order Suzuki decomposition, with error O(t^3)

        q_circuit   : applied quantum circuit
        hamiltonian : the PauliHamiltonian object to represent target Hamiltonian
        t           : (float) evolution time
        n           : (int) rounds of decomposition
        qindex      : the indexes of applied qubits
    """
    nqbits = hamiltonian.get_nqbits()
    if nqbits != len(qindex):
        raise PyQuantumKitError("Inconsistent number of qubits of <hamiltonian> and <qindex>!")
    
    for i in range(n):
        for j in range(len(hamiltonian)):
            (pauli, factor, focus) = hamiltonian.get_pauli_info_by_index(j)
            dt = t / n / 2.0 * factor
            apply_exp_pauli(q_circuit, pauli, dt, qindex, focus)
        for j in range(len(hamiltonian) - 1, -1, -1):
            (pauli, factor, focus) = hamiltonian.get_pauli_info_by_index(j)
            dt = t / n / 2.0 * factor
            apply_exp_pauli(q_circuit, pauli, dt, qindex, focus)

    return q_circuit
