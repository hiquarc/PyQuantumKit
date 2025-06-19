# QProcedure/Tomography.py
#    2025/6/11
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from PyQuantumKit.Classical.RunResult import *
from .Common import *
from .Paulis import *

def RunQubitTomography(qvm, GenProc, qbitindex : int, Ntimes : int) -> tuple[complex]:
    """
    Run state tomography for a qubit, return the 2x2 density matrix

        qvm       : run on which quantum machine
        GenProc   :  the procedure to generate target quantum state
        qbitindex : index of the target qubit
        Ntimes    : the number of repeat times N

    -> Return : tuple(a, b, c, d) to represent density matrix {{a, b}, {c, d}}
    """
    framework = GetFrameworkFromObject(GenProc)
    fw_req_reverse = GetReverseRunOutputString(framework)
    Nqs = GetNQubits(GenProc)
    Ncs = GetNCbits(GenProc)

    px = NewProgram(framework, Nqs, Ncs + 1)
    py = NewProgram(framework, Nqs, Ncs + 1)
    pz = NewProgram(framework, Nqs, Ncs + 1)
    AppendProgram(px, GenProc)
    AppendProgram(py, GenProc)
    AppendProgram(pz, GenProc)

    ApplyMeasureX(px, [qbitindex], [Ncs])
    ApplyMeasureY(py, [qbitindex], [Ncs])
    ApplyMeasureZ(pz, [qbitindex], [Ncs])

    res_x = CountLastBitsOfResultDict(RunAndGetCounts(qvm, px, Ntimes), 1, fw_req_reverse)
    Nof0 = res_x.get('0', 0)
    Nof1 = res_x.get('1', 0)
    mx = float(Nof0 - Nof1) / float(Ntimes)

    res_y = CountLastBitsOfResultDict(RunAndGetCounts(qvm, py, Ntimes), 1, fw_req_reverse)
    Nof0 = res_y.get('0', 0)
    Nof1 = res_y.get('1', 0)
    my = float(Nof0 - Nof1) / float(Ntimes)

    res_z = CountLastBitsOfResultDict(RunAndGetCounts(qvm, pz, Ntimes), 1, fw_req_reverse)
    Nof0 = res_z.get('0', 0)
    Nof1 = res_z.get('1', 0)
    mz = float(Nof0 - Nof1) / float(Ntimes)

    rho00 = complex((1.0 + mz) / 2.0, 0)
    rho01 = complex(mx / 2.0, -my / 2.0)
    rho10 = complex(mx / 2.0,  my / 2.0)
    rho11 = complex((1.0 - mz) / 2.0, 0)
    return (rho00, rho01, rho10, rho11)
