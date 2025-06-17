# QStatePrepare/ByString.py
#    2025/6/17
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from PyQuantumKit.QProcedure.Common import *
from PyQuantumKit.Classical.Common import *

def CreateStateFromBinStr(q_circuit, binstr : str, qbitlist : list[int]):
    """
    Apply a quantum circuit to create classical state, which is given by a binary string.

        e.g., '11001' --> q[0]=|1>, q[1]=|1>, q[2]=|0>, q[3]=|0>, q[4]=|1>

        q_circuit : applied quantum circuit
        binstr    : the '0'/'1' string to describe the state
        qbitlist  : the target qubit array

    -> Return : q_circuit
    """
    N = len(qbitlist)
    for i in range(0, N):
        if (binstr[i] != '1' and binstr[i] != '0'):
            raise ValueError('binstr must be 0/1 string!')
        if (binstr[i] == '1'):
            ApplyGate(q_circuit, 'X', [qbitlist[i]])
    return q_circuit
