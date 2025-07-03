# library/tomography.py
#    2025/6/11
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from pyquantumkit.procedure.generic import new_program, append_program, get_n_cbits, get_n_qubits, run_and_get_counts
from pyquantumkit.procedure.paulis import apply_measure_x, apply_measure_y, apply_measure_z
from pyquantumkit import get_framework_from_object
from pyquantumkit._qframes.framework_map import get_reverse_output_str
from pyquantumkit.classical.run_result import count_last_bits_of_result_dict


def run_qubit_tomography(qvm, GenProc, qbitindex : int, Ntimes : int) -> tuple[complex]:
    """
    Run state tomography for a qubit, return the 2x2 density matrix

        qvm       : run on which quantum machine
        GenProc   :  the procedure to generate target quantum state
        qbitindex : index of the target qubit
        Ntimes    : the number of repeat times N

    -> Return : tuple(a, b, c, d) to represent density matrix {{a, b}, {c, d}}
    """
    framework = get_framework_from_object(GenProc)
    fw_req_reverse = get_reverse_output_str(framework)
    Nqs = get_n_qubits(GenProc)
    Ncs = get_n_cbits(GenProc)

    px = new_program(framework, Nqs, Ncs + 1)
    py = new_program(framework, Nqs, Ncs + 1)
    pz = new_program(framework, Nqs, Ncs + 1)
    append_program(px, GenProc)
    append_program(py, GenProc)
    append_program(pz, GenProc)

    apply_measure_x(px, [qbitindex], [Ncs])
    apply_measure_y(py, [qbitindex], [Ncs])
    apply_measure_z(pz, [qbitindex], [Ncs])

    res_x = count_last_bits_of_result_dict(run_and_get_counts(qvm, px, Ntimes), 1, fw_req_reverse)
    Nof0 = res_x.get('0', 0)
    Nof1 = res_x.get('1', 0)
    mx = float(Nof0 - Nof1) / float(Ntimes)

    res_y = count_last_bits_of_result_dict(run_and_get_counts(qvm, py, Ntimes), 1, fw_req_reverse)
    Nof0 = res_y.get('0', 0)
    Nof1 = res_y.get('1', 0)
    my = float(Nof0 - Nof1) / float(Ntimes)

    res_z = count_last_bits_of_result_dict(run_and_get_counts(qvm, pz, Ntimes), 1, fw_req_reverse)
    Nof0 = res_z.get('0', 0)
    Nof1 = res_z.get('1', 0)
    mz = float(Nof0 - Nof1) / float(Ntimes)

    rho00 = complex((1.0 + mz) / 2.0, 0)
    rho01 = complex(mx / 2.0, -my / 2.0)
    rho10 = complex(mx / 2.0,  my / 2.0)
    rho11 = complex((1.0 - mz) / 2.0, 0)
    return (rho00, rho01, rho10, rho11)
