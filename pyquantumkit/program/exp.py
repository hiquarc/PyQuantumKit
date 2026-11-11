# program/exp.py
#    2026/10/10
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from pyquantumkit.program_build.algorithm import QAlg, AutoParas
from pyquantumkit.program.std import gate, QubitArray, QuantumProgramBuildError
import functools

Pauli_Characters = ['I', 'X', 'Y', 'Z']

class QExpPauli(QAlg):
    @classmethod
    def _general_impl_(cls, paulistr : str, t : float, qubitarray : QubitArray,
                       center : int = 0, allow_2qubit_rotgate : bool = True):
        """
        Append an Exp(-i*P*t) operation, where P is the tensor product of several Pauli operators.

            paulistr   : 'I'/'X'/'Y'/'Z' string to represent the tensor product of Pauli operators
            t          : the time parameter t
            qubitarray : a QubitArray object to apply
            center     : the index of non-I Paulis which is applied the core rotation, default 0
            allow_2qubit_rotgate : whether use the 2-qubit gate in the implementation

        -> Return : q_circuit
        """
        if len(paulistr) != len(qubitarray):
            raise QuantumProgramBuildError("<paulistr> and <qubitarray> have different length.")
        ps = ''         # record the Pauli string excluding 'I'
        qi = []         # record the corresponding qubit index of <ps>
        for i in range(0, len(paulistr)):
            p = paulistr[i].upper()
            if p not in Pauli_Characters:
                raise ValueError("Error Pauli character: " + p)
            if p in {'X', 'Y', 'Z'}:
                ps += p
                qi.append(i)
        len_noni = len(ps)

        centerindex = center if center >= 0 else len_noni + center

        # Consider separately: non-I with length 0, 1, 2
        if len_noni <= 0:
            return
        if len_noni == 1:
            gate('R' + ps, [qubitarray[qi[0]]], [t * 2])
            return
        if len_noni == 2 and allow_2qubit_rotgate:
            if ps in {'XX', 'YY', 'ZZ'}:
                gate('R' + ps, [qubitarray[qi[0]], qubitarray[qi[1]]], [t * 2])
                return
            if ps == 'XY':
                gate('SD', [qubitarray[qi[1]]])
                gate('RXX', [qubitarray[qi[0]], qubitarray[qi[1]]], [t * 2])
                gate('S', [qubitarray[qi[1]]])
                return
            if ps == 'YX':
                gate('SD', [qubitarray[qi[0]]])
                gate('RXX', [qubitarray[qi[0]], qubitarray[qi[1]]], [t * 2])
                gate('S', [qubitarray[qi[0]]])
                return
            if ps == 'XZ':
                gate('H', [qubitarray[qi[0]]])
                gate('RZZ', [qubitarray[qi[0]], qubitarray[qi[1]]], [t * 2])
                gate('H', [qubitarray[qi[0]]])
                return
            if ps == 'ZX':
                gate('H', [qubitarray[qi[1]]])
                gate('RZZ', [qubitarray[qi[0]], qubitarray[qi[1]]], [t * 2])
                gate('H', [qubitarray[qi[1]]])
                return
            if ps == 'YZ':
                gate('SD', [qubitarray[qi[0]]])
                gate('H', [qubitarray[qi[1]]])
                gate('RXX', [qubitarray[qi[0]], qubitarray[qi[1]]], [t * 2])
                gate('H', [qubitarray[qi[1]]])
                gate('S', [qubitarray[qi[0]]])
                return
            if ps == 'ZY':
                gate('H', [qubitarray[qi[0]]])
                gate('SD', [qubitarray[qi[1]]])
                gate('RXX', [qubitarray[qi[0]], qubitarray[qi[1]]], [t * 2])
                gate('S', [qubitarray[qi[1]]])
                gate('H', [qubitarray[qi[0]]])
                return

        # Algorithm for general cases
        for i in range(len_noni):
            if ps[i] == 'X':
                gate('H', [qubitarray[qi[i]]])
            elif ps[i] == 'Y':
                gate('SD', [qubitarray[qi[i]]])
                gate('H', [qubitarray[qi[i]]])

        for i in range(len_noni):
            if i != centerindex:
                gate('CX', [qubitarray[qi[i]], qubitarray[qi[centerindex]]])
        gate('RZ', [qubitarray[qi[centerindex]]], [t * 2])
        for i in range(len_noni - 1, -1, -1):
            if i != centerindex:
                gate('CX', [qubitarray[qi[i]], qubitarray[qi[centerindex]]])

        for i in range(len_noni):
            if ps[i] == 'X':
                gate('H', [qubitarray[qi[i]]])
            elif ps[i] == 'Y':
                gate('H', [qubitarray[qi[i]]])
                gate('S', [qubitarray[qi[i]]])

    def __init__(self):
        super().__init__()
        self.center = 0
        self.allow_2qubit_rotgate = True

    def build_options():
        pass

    
