# QProcedure/SwapTest.py
#    2025/6/13
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from PyQuantumKit.Classical.RunResult import *
from .Common import *


def AppendSwapTestCircuit(q_circuit, qctrlindex : int, s1indexlist : list[int], s2indexlist : list[int]):
    """
    Generate a quantum circuit for SWAP test

        q_circuit   : the quantum circuit to be appended
        qctrlindex  : the index of controlling qubit
        s1indexlist : the index list of target qubit array 1
        s2indexlist : the index list of target qubit array 2

    -> Return : the SWAP test circuit
    """
    N = len(s1indexlist)
    if N != len(s2indexlist):
        raise ValueError('s1indexlist and s2indexlist must have same length!')
    
    ApplyGate(q_circuit, 'H', [qctrlindex])
    for i in range(0, N):
        ApplyGate(q_circuit, 'CSW', [qctrlindex, s1indexlist[i], s2indexlist[i]])
    ApplyGate(q_circuit, 'H', [qctrlindex])
    return q_circuit


def RunSwapTest(qvm, GenProc, state1qlist : list[int], state2qlist : list[int], Ntimes : int) -> int:
    """
    Run SWAP test for given quantum circuit or program, return the number of result 1

        qvm         : run on which quantum machine
        GenProc     : the procedure to generate target quantum state
        state1qlist : index list of target qubit array 1
        state2qlist : index list of target qubit array 2
        Ntimes      : the number of repeat times N

    -> Return : the number of obtained result 1 in all N times
    """
    framework = GetFrameworkFromObject(GenProc)
    fw_req_reverse = GetReverseRunOutputString(framework)
    Nqs = GetNQubits(GenProc)
    Ncs = GetNCbits(GenProc)

    ptest = NewProgram(framework, Nqs + 1, Ncs + 1)
    AppendProgram(ptest, GenProc)
    AppendSwapTestCircuit(ptest, Nqs, state1qlist, state2qlist)
    Measure(ptest, [Nqs], [Ncs])

    counts = RunAndGetCounts(qvm, ptest, Ntimes)
    res = CountLastBitsOfResultDict(counts, 1, fw_req_reverse)
    return res.get('1', 0)



def CheckTrRho1Rho2Equals1(qvm, GenProc, state1qlist : list[int], state2qlist : list[int], Ntimes : int) -> bool:
    """
    Run SWAP test for given quantum circuit or program to check tr(rho_A rho_B)

        qvm         : run on which quantum machine
        GenProc     : the procedure to generate target quantum state
        state1qlist : index list of target qubit array 1
        state2qlist : index list of target qubit array 2
        Ntimes      : the number of repeat times N

    -> Return : True if trace == 1; otherwise False
    """
    framework = GetFrameworkFromObject(GenProc)
    fw_req_reverse = GetReverseRunOutputString(framework)
    Nqs = GetNQubits(GenProc)
    Ncs = GetNCbits(GenProc)

    ptest = NewProgram(framework, Nqs + 1, Ncs + 1)
    AppendProgram(ptest, GenProc)
    AppendSwapTestCircuit(framework, Nqs, state1qlist, state2qlist)
    Measure(ptest, [Nqs], [Ncs])

    for i in range(0, Ntimes):
        counts = RunAndGetCounts(qvm, ptest, 1)
        result = FirstResultStr(counts, fw_req_reverse)
        if result != '0':
            return False
    return True

