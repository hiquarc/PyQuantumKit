# program_check/program_relation.py
#    2025/6/12
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from random import randint
from math import pi
from pyquantumkit.classical.common import *
from pyquantumkit.classical.run_result import *
from pyquantumkit.procedure.generic import *
from pyquantumkit.state_prepare.int_state import *
from pyquantumkit.state_prepare.pauli_eigenstate import *
from pyquantumkit.procedure.swaptest import *

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


def run_equivalence_check(qvm, TargetProc1, TargetProc2,
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
    framework = get_framework_from_object(TargetProc1)
    Nqs = get_n_qubits(TargetProc1)
    if (Nqs != get_n_qubits(TargetProc2)):
        return False
    Ncs1 = get_n_cbits(TargetProc1)
    Ncs2 = get_n_cbits(TargetProc2)
    
    qlist1 = get_qubit_list(TargetProc1)
    qlist2 = [x + Nqs for x in qlist1]
    #tp1 = copy_program(TargetProc1)
    #tp2 = copy_program(TargetProc2)

    for i in range(0, NPoints):
        STprocA = new_program(framework, 2 * Nqs, 2 * Ncs1)
        STprocB = new_program(framework, 2 * Nqs, 2 * Ncs2)
        STprocAB = new_program(framework, 2 * Nqs, Ncs1 + Ncs2)
        randompaulis = [randint(0, 5) for _ in qlist1]

        create_pauli_eigenstate(STprocA, randompaulis, qlist1)
        create_pauli_eigenstate(STprocA, randompaulis, qlist2)
        append_program(STprocA, juxtapose_circuits(TargetProc1, TargetProc1))
        create_pauli_eigenstate(STprocB, randompaulis, qlist1)
        create_pauli_eigenstate(STprocB, randompaulis, qlist2)
        append_program(STprocB, juxtapose_circuits(TargetProc2, TargetProc2))
        create_pauli_eigenstate(STprocAB, randompaulis, qlist1)
        create_pauli_eigenstate(STprocAB, randompaulis, qlist2)
        append_program(STprocAB, juxtapose_circuits(TargetProc1, TargetProc2))
        
        Pa = check_tr_rho1_rho2_equals_1(qvm, STprocA, qlist1, qlist2, NTrace)
        Pb = check_tr_rho1_rho2_equals_1(qvm, STprocB, qlist1, qlist2, NTrace)
        if (Pa != Pb):
            return False
        if Pa:
            Pab = check_tr_rho1_rho2_equals_1(qvm, STprocAB, qlist1, qlist2, NTrace)
            if (not Pab):
                return False
        else:
            Na = run_swaptest(qvm, STprocA, qlist1, qlist2, NSTrepeat)
            Nb = run_swaptest(qvm, STprocB, qlist1, qlist2, NSTrepeat)
            Nab = run_swaptest(qvm, STprocAB, qlist1, qlist2, NSTrepeat)
            r = float(2 * Nab - Na - Nb) / float(NSTrepeat)
            if (abs(r) > epsilon):
                return False
    return True



def run_identity_check(qvm, TargetProc, NPoints : int = Default_Identity_NPoints) -> bool:
    """
    Run identity checking for a quantum program.

        qvm : run on which quantum machine
        TargetProc : target quantum program
        NPoints : running parameters

    -> Return : True -- PASS, False -- FAIL
    """
    framework = get_framework_from_object(TargetProc)
    fw_req_reverse = get_reverse_output_str(framework)
    Nqs = get_n_qubits(TargetProc)
    Ncs = get_n_cbits(TargetProc)
    qlist = get_qubit_list(TargetProc)
    mlist = [x + Ncs for x in qlist]

    for i in range(0, NPoints):
        ptest = new_program(framework, Nqs, Ncs + Nqs)
        randompaulis = [randint(0, 5) for _ in qlist]

        create_pauli_eigenstate(ptest, randompaulis, qlist)
        append_program(ptest, TargetProc)
        uncompute_pauli_eigenstate(ptest, randompaulis, qlist)
        apply_measure(ptest, qlist, mlist)

        raw = run_and_get_counts(qvm, ptest, 1)
        counts = count_last_bits_of_result_dict(raw, Nqs, fw_req_reverse)
        result = int(list(get_result_str_set(counts))[0])

        if result != 0:
            return False
    return True



def run_keep_purity_check(qvm, TargetProc,
                       NPoints : int = Default_KeepPurity_NPoints, NTrace : int = Default_KeepPurity_NTrace) -> bool:
    """
    Run keep-purity checking for a quantum program.

        qvm : run on which quantum machine
        TargetProc : target quantum program
        NPoints, NTrace : running parameters

    -> Return : True -- PASS, False -- FAIL
    """
    framework = get_framework_from_object(TargetProc)
    Nqs = get_n_qubits(TargetProc)
    Ncs = get_n_cbits(TargetProc)
    qlist1 = get_qubit_list(TargetProc)
    qlist2 = [x + Nqs for x in qlist1]
    #tp = QProg(TargetProc)

    for i in range(0, NPoints):
        STproc = new_program(framework, 2 * Nqs, 2 * Ncs)
        randompaulis = [randint(0, 5) for _ in qlist1]

        create_pauli_eigenstate(STproc, randompaulis, qlist1)
        create_pauli_eigenstate(STproc, randompaulis, qlist2)
        append_program(STproc, juxtapose_programs(TargetProc, TargetProc))

        isTr1 = check_tr_rho1_rho2_equals_1(qvm, STproc, qlist1, qlist2, NTrace)
        if (not isTr1):
            return False
    return True



def run_unitarity_check(qvm, TargetProc,
                      NPoints : int = Default_Unitarity_NPoints, NSTrepeat : int = Default_Unitarity_NSTrepeat,
                      NTrace : int = Default_Unitarity_NTrace, epsilon : float = Default_Unitarity_epsilon) -> bool:
    """
    Run unitarity checking for a quantum program.

        qvm : run on which quantum machine
        TargetProc : target quantum program
        NPoints, NSTrepeat, NTrace, epsilon : running parameters

    -> Return : True -- PASS, False -- FAIL
    """
    kp = run_keep_purity_check(qvm, TargetProc, NPoints, NTrace)
    if not kp:
        return False
    framework = get_framework_from_object(TargetProc)
    Nqs = get_n_qubits(TargetProc)
    Ncs = get_n_cbits(TargetProc)
    qlist1 = get_qubit_list(TargetProc)
    qlist2 = [x + Nqs for x in qlist1]
    #tp = QProg(TargetProc)
    
    for i in range(0, NPoints):
        STproc = new_program(framework, 2 * Nqs, 2 * Ncs)

        if (i <= (NPoints - 1) / 2):
            num = randint(0, (1 << Nqs) - 1)
            create_ket_int_plus_eiphi_neg_le(STproc, num, 0.0, qlist1)
            create_ket_int_plus_eiphi_neg_le(STproc, num, pi, qlist2)
            append_program(STproc, juxtapose_programs(TargetProc, TargetProc))

            Npm = run_swaptest(qvm, STproc, qlist1, qlist2, NSTrepeat)
            r = 1.0 - 2.0 * float(Npm) / float(NSTrepeat)
            if (abs(r) > epsilon):
                return False
        else:
            (num1, num2) = rand_diff_int_pair(0, (1 << Nqs) - 1)
            create_ket_int_le(STproc, num1, qlist1)
            create_ket_int_le(STproc, num2, qlist2)
            append_program(STproc, juxtapose_programs(TargetProc, TargetProc))

            Nab = run_swaptest(qvm, STproc, qlist1, qlist2, NSTrepeat)
            r = 1.0 - 2.0 * float(Nab) / float(NSTrepeat)
            if (abs(r) > epsilon):
                return False
    return True



def run_keep_basis_check(qvm, TargetProc,
                      NPoints : int = Default_KeepBasis_NPoints, NRepeat : int = Default_KeepBasis_NRepeat) -> bool:
    """
    Run keep-basis checking for a quantum program.

        qvm : run on which quantum machine
        TargetProc : target quantum program
        NPoints, NRepeat : running parameters

    -> Return : True -- PASS, False -- FAIL
    """
    framework = get_framework_from_object(TargetProc)
    fw_req_reverse = get_reverse_output_str(framework)
    Nqs = get_n_qubits(TargetProc)
    Ncs = get_n_cbits(TargetProc)
    qlist = get_qubit_list(TargetProc)
    mlist = [x + Ncs for x in qlist]

    for i in range(0, NPoints):
        mr = -1
        num = randint(0, (1 << Nqs) - 1)
        for j in range(0, NRepeat):
            ptest = new_program(framework, Nqs, Ncs + Nqs)

            create_ket_int_le(ptest, num, qlist)
            append_program(ptest, TargetProc)
            apply_measure(ptest, qlist, mlist)

            counts = count_last_bits_of_result_dict(run_and_get_counts(qvm, ptest, 1), Nqs, fw_req_reverse)
            m = int(list(get_result_str_set(counts))[0])
            if mr < 0:
                mr = m
            if mr != m:
                return False
    return True
