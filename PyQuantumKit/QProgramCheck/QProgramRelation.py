# QProgramCheck/QProgramRelation.py
#    2025/6/12
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from random import randint
from math import pi
from PyQuantumKit.Classical.Common import *
from PyQuantumKit.QStatePrepare.IntState import *
from PyQuantumKit.QStatePrepare.PauliState import *
from PyQuantumKit.QProcedure.SwapTest import *

# Implement the relation checking for quantum programs,
#   based on the article: https://arxiv.org/abs/2307.01481

#---------- Default running parameters ----------
# Equivalence checking
Default_Equivalence_NPoints = 4
Default_Equivalence_NSTrepeat = 1545
Default_Equivalence_NTrace = 20
Default_Equivalence_epsilon = 0.15

# Identity checking
Default_Identity_NPoints = 50

# Keep-purity checking
Default_KeepPurity_NPoints = 10
Default_KeepPurity_NTrace = 20

# Unitarity checking
Default_Unitarity_NPoints = 4
Default_Unitarity_NSTrepeat = 469
Default_Unitarity_NTrace = 20
Default_Unitarity_epsilon = 0.15

# Keep-basis checking
Default_KeepBasis_NPoints = 10
Default_KeepBasis_NRepeat = 20


# ---------- Checking functions ----------


def RunEquivalenceCheck(qvm, TargetProc1, TargetProc2,
                        NPoints : int = Default_Equivalence_NPoints, NSTrepeat : int = Default_Equivalence_NSTrepeat,
                        NTrace : int = Default_Equivalence_NTrace, epsilon : float = Default_Equivalence_epsilon) -> bool:
    """
    Run equivalence checking for a pair of quantum programs.

        qvm : run on which quantum machine
        TargetProc1 : the first quantum program
        TargetProc2 : the second quantum program
        NPoints, NSTrepeat, NTrace, epsilon : running parameters

    -> Return : True -- PASS, False -- FAIL
    """
    framework = GetFrameworkFromObject(TargetProc1)
    Nqs = GetNQubits(TargetProc1)
    if (Nqs != GetNQubits(TargetProc2)):
        return False
    Ncs1 = GetNCbits(TargetProc1)
    Ncs2 = GetNCbits(TargetProc2)
    
    qlist1 = GetQubitList(TargetProc1)
    qlist2 = [x + Nqs for x in qlist1]
    #tp1 = CopyProgram(TargetProc1)
    #tp2 = CopyProgram(TargetProc2)

    for i in range(0, NPoints):
        STprocA = NewProgram(framework, 2 * Nqs, 2 * Ncs1)
        STprocB = NewProgram(framework, 2 * Nqs, 2 * Ncs2)
        STprocAB = NewProgram(framework, 2 * Nqs, Ncs1 + Ncs2)
        randompaulis = [randint(0, 5) for _ in qlist1]

        CreatePauliState(STprocA, randompaulis, qlist1)
        CreatePauliState(STprocA, randompaulis, qlist2)
        AppendProgram(STprocA, ParallelCircuits(TargetProc1, TargetProc1))
        CreatePauliState(STprocB, randompaulis, qlist1)
        CreatePauliState(STprocB, randompaulis, qlist2)
        AppendProgram(STprocB, ParallelCircuits(TargetProc2, TargetProc2))
        CreatePauliState(STprocAB, randompaulis, qlist1)
        CreatePauliState(STprocAB, randompaulis, qlist2)
        AppendProgram(STprocAB, ParallelCircuits(TargetProc1, TargetProc2))
        
        Pa = CheckTrRho1Rho2Equals1(qvm, STprocA, qlist1, qlist2, NTrace)
        Pb = CheckTrRho1Rho2Equals1(qvm, STprocB, qlist1, qlist2, NTrace)
        if (Pa != Pb):
            return False
        if Pa:
            Pab = CheckTrRho1Rho2Equals1(qvm, STprocAB, qlist1, qlist2, NTrace)
            if (not Pab):
                return False
        else:
            Na = RunSwapTest(qvm, STprocA, qlist1, qlist2, NSTrepeat)
            Nb = RunSwapTest(qvm, STprocB, qlist1, qlist2, NSTrepeat)
            Nab = RunSwapTest(qvm, STprocAB, qlist1, qlist2, NSTrepeat)
            r = float(2 * Nab - Na - Nb) / float(NSTrepeat)
            if (abs(r) > epsilon):
                return False
    return True



def RunIdentityCheck(qvm, TargetProc, NPoints : int = Default_Identity_NPoints) -> bool:
    """
    Run identity checking for a quantum program.

        qvm : run on which quantum machine
        TargetProc : target quantum program
        NPoints : running parameters

    -> Return : True -- PASS, False -- FAIL
    """
    framework = GetFrameworkFromObject(TargetProc)
    fw_req_reverse = GetReverseRunOutputString(framework)
    Nqs = GetNQubits(TargetProc)
    Ncs = GetNCbits(TargetProc)
    qlist = GetQubitList(TargetProc)
    mlist = [x + Ncs for x in qlist]

    for i in range(0, NPoints):
        ptest = NewProgram(framework, Nqs, Ncs + Nqs)
        randompaulis = [randint(0, 5) for _ in qlist]

        CreatePauliState(ptest, randompaulis, qlist)
        AppendProgram(ptest, TargetProc)
        UncomputePauliState(ptest, randompaulis, qlist)
        ApplyMeasure(ptest, qlist, mlist)

        counts = CountLastBitsOfResultDict(RunAndGetCounts(qvm, ptest, 1), Nqs, fw_req_reverse)
        result = int(FirstResultStr(counts, fw_req_reverse))
        if result != 0:
            return False
    return True



def RunKeepPurityCheck(qvm, TargetProc,
                       NPoints : int = Default_KeepPurity_NPoints, NTrace : int = Default_KeepPurity_NTrace) -> bool:
    """
    Run keep-purity checking for a quantum program.

        qvm : run on which quantum machine
        TargetProc : target quantum program
        NPoints, NTrace : running parameters

    -> Return : True -- PASS, False -- FAIL
    """
    framework = GetFrameworkFromObject(TargetProc)
    Nqs = GetNQubits(TargetProc)
    Ncs = GetNCbits(TargetProc)
    qlist1 = GetQubitList(TargetProc)
    qlist2 = [x + Nqs for x in qlist1]
    #tp = QProg(TargetProc)

    for i in range(0, NPoints):
        STproc = NewProgram(framework, 2 * Nqs, 2 * Ncs)
        randompaulis = [randint(0, 5) for _ in qlist1]

        CreatePauliState(STproc, randompaulis, qlist1)
        CreatePauliState(STproc, randompaulis, qlist2)
        AppendProgram(STproc, ParallelPrograms(TargetProc, TargetProc))

        isTr1 = CheckTrRho1Rho2Equals1(qvm, STproc, qlist1, qlist2, NTrace)
        if (not isTr1):
            return False
    return True



def RunUnitarityCheck(qvm, TargetProc,
                      NPoints : int = Default_Unitarity_NPoints, NSTrepeat : int = Default_Unitarity_NSTrepeat,
                      NTrace : int = Default_Unitarity_NTrace, epsilon : float = Default_Unitarity_epsilon) -> bool:
    """
    Run unitarity checking for a quantum program.

        qvm : run on which quantum machine
        TargetProc : target quantum program
        NPoints, NSTrepeat, NTrace, epsilon : running parameters

    -> Return : True -- PASS, False -- FAIL
    """
    kp = RunKeepPurityCheck(qvm, TargetProc, NPoints, NTrace)
    if not kp:
        return False
    framework = GetFrameworkFromObject(TargetProc)
    Nqs = GetNQubits(TargetProc)
    Ncs = GetNCbits(TargetProc)
    qlist1 = GetQubitList(TargetProc)
    qlist2 = [x + Nqs for x in qlist1]
    #tp = QProg(TargetProc)
    
    for i in range(0, NPoints):
        STproc = NewProgram(framework, 2 * Nqs, 2 * Ncs)

        if (i <= (NPoints - 1) / 2):
            num = randint(0, (1 << Nqs) - 1)
            CreateKetIntPlusEPhiNegationLE(STproc, num, 0.0, qlist1)
            CreateKetIntPlusEPhiNegationLE(STproc, num, pi, qlist2)
            AppendProgram(STproc, ParallelPrograms(TargetProc, TargetProc))

            Npm = RunSwapTest(qvm, STproc, qlist1, qlist2, NSTrepeat)
            r = 1.0 - 2.0 * float(Npm) / float(NSTrepeat)
            if (abs(r) > epsilon):
                return False
        else:
            (num1, num2) = randdiffintpair(0, (1 << Nqs) - 1)
            CreateKetIntLE(STproc, num1, qlist1)
            CreateKetIntLE(STproc, num2, qlist2)
            AppendProgram(STproc, ParallelPrograms(TargetProc, TargetProc))

            Nab = RunSwapTest(qvm, STproc, qlist1, qlist2, NSTrepeat)
            r = 1.0 - 2.0 * float(Nab) / float(NSTrepeat)
            if (abs(r) > epsilon):
                return False
    return True



def RunKeepBasisCheck(qvm, TargetProc,
                      NPoints : int = Default_KeepBasis_NPoints, NRepeat : int = Default_KeepBasis_NRepeat) -> bool:
    """
    Run keep-basis checking for a quantum program.

        qvm : run on which quantum machine
        TargetProc : target quantum program
        NPoints, NRepeat : running parameters

    -> Return : True -- PASS, False -- FAIL
    """
    framework = GetFrameworkFromObject(TargetProc)
    fw_req_reverse = GetReverseRunOutputString(framework)
    Nqs = GetNQubits(TargetProc)
    Ncs = GetNCbits(TargetProc)
    qlist = GetQubitList(TargetProc)
    mlist = [x + Ncs for x in qlist]

    for i in range(0, NPoints):
        mr = -1
        num = randint(0, (1 << Nqs) - 1)
        for j in range(0, NRepeat):
            ptest = NewProgram(framework, Nqs, Ncs + Nqs)

            CreateKetIntLE(ptest, num, qlist)
            AppendProgram(ptest, TargetProc)
            ApplyMeasure(ptest, qlist, mlist)

            counts = CountLastBitsOfResultDict(RunAndGetCounts(qvm, ptest, 1), Nqs, fw_req_reverse)
            m = int(FirstResultStr(counts, fw_req_reverse))
            if mr < 0:
                mr = m
            if mr != m:
                return False
    return True
