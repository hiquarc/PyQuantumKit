# program/exp.py
#    2026/10/10
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from pyquantumkit.program_build.algorithm import QAlg, AutoParas
from pyquantumkit.program.std import gate, QubitArray, QuantumProgramBuildError
import functools

Pauli_Characters = ['I', 'X', 'Y', 'Z']

class QExpPauli(QAlg):
    @staticmethod
    def __origin_impl(focus : int, allow_2qubit_rotgate : bool,
                            paulistr : str, t : float, qubitarray : QubitArray):
        """
        Append an Exp(-i*P*t) operation, where P is the tensor product of several Pauli operators.

            q_circuit : applied quantum circuit
            paulistr  : 'I'/'X'/'Y'/'Z' string to represent the tensor product of Pauli operators
            qindex    : the indexes of applied qubits
            focus     : (optional) the index of non-I Paulis which is applied the core rotation, default 0

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

        focusindex = focus if focus >= 0 else len_noni + focus

        # Consider separately: non-I length 0, 1, 2
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
            if i != focusindex:
                gate('CX', [qubitarray[qi[i]], qubitarray[qi[focusindex]]])
        gate('RZ', [qubitarray[qi[focusindex]]], [t * 2])
        for i in range(len_noni - 1, -1, -1):
            if i != focusindex:
                gate('CX', [qubitarray[qi[i]], qubitarray[qi[focusindex]]])

        for i in range(len_noni):
            if ps[i] == 'X':
                gate('H', [qubitarray[qi[i]]])
            elif ps[i] == 'Y':
                gate('H', [qubitarray[qi[i]]])
                gate('S', [qubitarray[qi[i]]])

    @classmethod
    def impl(cls, focus : int|AutoParas = AutoParas,
                  allow_2qubit_rotgate : bool|AutoParas = AutoParas,
                  compile_option : str = 'auto') -> callable:
        return functools.partial(cls.__origin_impl, focus, allow_2qubit_rotgate)

    @classmethod
    def impl_auto(cls) -> callable:
        return cls.impl(0, True)
