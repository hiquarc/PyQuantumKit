# library/swaptest.py
#    2025/6/13
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from pyquantumkit import apply_gate, new_program, append_program, get_n_cbits, get_n_qubits, apply_measure,\
                         run_and_get_counts, get_framework_from_object
from pyquantumkit._qframes.framework_map import get_reverse_output_str
from pyquantumkit.classical.run_result import count_last_bits_of_result_dict


def append_swaptest_circuit(q_circuit, qctrlindex : int, s1indexlist : list[int], s2indexlist : list[int]):
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
    
    apply_gate(q_circuit, 'H', [qctrlindex])
    for i in range(0, N):
        apply_gate(q_circuit, 'CSW', [qctrlindex, s1indexlist[i], s2indexlist[i]])
    apply_gate(q_circuit, 'H', [qctrlindex])
    return q_circuit


def run_swaptest(qvm, GenProc, state1qlist : list[int], state2qlist : list[int], Ntimes : int) -> int:
    """
    Run SWAP test for given quantum circuit or program, return the number of result 1

        qvm         : run on which quantum machine
        GenProc     : the procedure to generate target quantum state
        state1qlist : index list of target qubit array 1
        state2qlist : index list of target qubit array 2
        Ntimes      : the number of repeat times N

    -> Return : the number of obtained result 1 in all N times
    """
    framework = get_framework_from_object(GenProc)
    fw_req_reverse = get_reverse_output_str(framework)
    Nqs = get_n_qubits(GenProc)
    Ncs = get_n_cbits(GenProc)

    ptest = new_program(framework, Nqs + 1, Ncs + 1)
    append_program(ptest, GenProc)
    append_swaptest_circuit(ptest, Nqs, state1qlist, state2qlist)
    apply_measure(ptest, [Nqs], [Ncs])

    counts = run_and_get_counts(qvm, ptest, Ntimes)
    res = count_last_bits_of_result_dict(counts, 1, fw_req_reverse)
    return res.get('1', 0)



def check_tr_rho1_rho2_equals_1(qvm, GenProc, state1qlist : list[int], state2qlist : list[int], Ntimes : int) -> bool:
    """
    Run SWAP test for given quantum circuit or program to check tr(rho_A rho_B)

        qvm         : run on which quantum machine
        GenProc     : the procedure to generate target quantum state
        state1qlist : index list of target qubit array 1
        state2qlist : index list of target qubit array 2
        Ntimes      : the number of repeat times N

    -> Return : True if trace == 1; otherwise False
    """
    framework = get_framework_from_object(GenProc)
    fw_req_reverse = get_reverse_output_str(framework)
    Nqs = get_n_qubits(GenProc)
    Ncs = get_n_cbits(GenProc)

    ptest = new_program(framework, Nqs + 1, Ncs + 1)
    append_program(ptest, GenProc)
    append_swaptest_circuit(ptest, Nqs, state1qlist, state2qlist)
    apply_measure(ptest, [Nqs], [Ncs])

    for i in range(0, Ntimes):
        counts = run_and_get_counts(qvm, ptest, 1)
        result = count_last_bits_of_result_dict(counts, 1, fw_req_reverse)
        if result.get('1', 0) > 0:
            return False
    return True

