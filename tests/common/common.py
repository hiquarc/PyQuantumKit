# test: common/common.py
#    2025/6/23
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from pyquantumkit import *
from pyquantumkit._qframes.framework_map import get_reverse_output_str
from pyquantumkit.procedure.circuit_io import *
from pyquantumkit.classical.run_result import *
from pyquantumkit.classical.common import *
from pyquantumkit.program_check.program_relation import *
from pyquantumkit.program_check.matrix_based import *

Repeat_Times_Of_State_Check = 20

def is_exception(thing) -> bool:
    if isinstance(thing, type) and issubclass(thing, Exception):
        return True
    return False


# ---------- Test execution encapsulation functions --------

def T_run(framework : str, machine, nbits : int,
          Proc : callable, *args, **kwargs) -> None:
    qc = new_program(framework, nbits, nbits)
    Proc(qc, *args, **kwargs)
    run_and_get_counts(machine, qc, Repeat_Times_Of_State_Check)


def T_measure_result_mp(framework : str, machine, nbits : int,
                        Procs : list[callable], ProcArgs : list[list]) -> set[str]:
    fw_req_reverse = get_reverse_output_str(framework)
    qc = new_program(framework, nbits, nbits)

    for i in range(len(Procs)):
        Procs[i](qc, *ProcArgs[i])

    apply_measure(qc, range(nbits), range(nbits))
    counts = run_and_get_counts(machine, qc, Repeat_Times_Of_State_Check)
    resstrs = get_result_str_set(counts, fw_req_reverse)
    return resstrs

def T_measure_result(framework : str, machine, nbits : int,
                     Proc : callable, *args, **kwargs) -> set[str]:
    fw_req_reverse = get_reverse_output_str(framework)
    qc = new_program(framework, nbits, nbits)

    Proc(qc, *args, **kwargs)

    apply_measure(qc, range(nbits), range(nbits))
    counts = run_and_get_counts(machine, qc, Repeat_Times_Of_State_Check)
    resstrs = get_result_str_set(counts, fw_req_reverse)
    return resstrs


def T_identity_mp(framework : str, machine, nbits : int,
                  Procs : list[callable], ProcArgs : list[list]) -> bool:
    qc = new_program(framework, nbits, nbits)

    for i in range(len(Procs)):
        Procs[i](qc, *ProcArgs[i])

    res = bool(run_identity_check(machine, qc, Repeat_Times_Of_State_Check))
    return res

def T_create_uncompute(framework : str, machine, nbits : int, C_proc : callable,
                       U_proc : callable, *args) -> bool:
    return T_identity_mp(framework, machine, nbits, [C_proc, U_proc], [args, args])

def T_equivalence(framework : str, machine, nqbits : int, ncbits : int,
                  Proc1 : callable, Proc2 : callable, ProcArgs1 : list, ProcArgs2 : list) -> bool:
    qc1 = new_program(framework, nqbits, ncbits)
    qc2 = new_program(framework, nqbits, ncbits)

    Proc1(qc1, *ProcArgs1)
    Proc2(qc2, *ProcArgs2)

    res = bool(run_equivalence_check(machine, qc1, qc2))
    return res


# ---------- Common test quantum programs ----------

# Correct programs:
def EmptyCir(framework : str):
    return new_circuit(framework, 4)

def OnlyGlobalPhase(framework : str):
    qc = new_circuit(framework, 4)
    apply_gate(qc, 'Z', [0])
    apply_gate(qc, 'Rz', [0], [math.pi])
    return qc

def CancelCir(framework : str):
    cio = CircuitIO(4)
    cio1 = CircuitIO(4)
    cio2 = CircuitIO(4)
    cio3 = CircuitIO(4)

    apply_gate(cio3, 'CRX', [0, 3], [-0.3])
    apply_gate(cio3, 'CRY', [0, 3], [-0.6])
    apply_gate(cio3, 'CRZ', [0, 3], [-0.9])
    apply_gate(cio1, 'RX', [0], [0.5])
    apply_gate(cio1, 'RY', [0], [1.5])
    apply_gate(cio1, 'RZ', [0], [2.5])
    apply_gate(cio2, 'RXX', [1, 2], [0.7])
    apply_gate(cio2, 'RYY', [1, 2], [1.4])
    apply_gate(cio2, 'RZZ', [1, 2], [2.1])

    cio << cio1 << cio2 << cio3
    cio1.inverse()
    cio2.inverse()
    cio3.inverse()
    cio << cio3 << cio2 << cio1

    qc = new_circuit(framework, 4)
    cio >> qc
    return qc

def CancelCir2(framework : str):
    origincio = CircuitIO(1)
    cio = CircuitIO(1)
    origincio.apply_gate('U1', [0], [-1.9])
    origincio.apply_gate('U3', [0], [-1.2, -2.4, 3.6])

    origincio.inverse()
    cio << origincio
    origincio.inverse()
    cio << origincio

    qc = new_circuit(framework, 1)
    cio >> qc
    return qc

def Cir1A(framework : str):
    qc = new_circuit(framework, 2)
    apply_gate(qc, 'H', [1])
    apply_gate(qc, 'CX', [0, 1])
    multi_apply_sqgate(qc, 'Z', [0, 1])
    apply_gate(qc, 'CX', [0, 1])
    apply_gate(qc, 'H', [1])
    return qc
def Cir1B(framework : str):
    qc = new_circuit(framework, 2)
    apply_gate(qc, 'X', [1])
    return qc
def Cir1C(framework : str):
    cio = CircuitIO()
    cio.apply_gate('H', [0])
    cio.apply_gate('CNOT', [1, 0])
    cio.apply_gate('z', [0])
    cio.apply_gate('Z', [1])
    cio.apply_gate('CX', [1, 0])
    cio.apply_gate('H', [0])
    cio.remap_qbits([1, 0])
    qc = new_circuit(framework, 2)
    cio >> qc
    return qc

# Buggy programs:
def Empty_bug1(framework : str):
    qc = new_program(framework, 4, 1)
    apply_measure(qc, [0], [0])
    return qc
def Empty_bug2(framework : str):
    qc = new_circuit(framework, 4)
    apply_gate(qc, 'T', [0])
    return qc

def Cir1A_bug1(framework : str):
    qc = new_circuit(framework, 2)
    apply_gate(qc, 'H', [1])
    apply_gate(qc, 'CX', [0, 1])
    apply_gate(qc, 'Z', [1])    # bug: remove a Z gate
    apply_gate(qc, 'CX', [0, 1])
    apply_gate(qc, 'H', [1])
    return qc
def Cir1A_bug2(framework : str):
    qc = new_circuit(framework, 2)
    #apply_gate(qc, 'H', [1])   # bug: remove an H gate
    apply_gate(qc, 'CX', [0, 1])
    multi_apply_sqgate(qc, 'Z', [0, 1])
    apply_gate(qc, 'CX', [0, 1])
    apply_gate(qc, 'H', [1])
    return qc
def Cir1A_bug3(framework : str):
    qc = new_circuit(framework, 2)
    apply_gate(qc, 'H', [1])
    apply_gate(qc, 'CX', [0, 1])
    apply_gate(qc, 'Z', [0])
    apply_gate(qc, 'CX', [1, 0])    # bug: add CNOT
    apply_gate(qc, 'Z', [1])
    apply_gate(qc, 'CX', [0, 1])
    apply_gate(qc, 'H', [1])
    return qc
def Cir1A_bug4(framework : str):
    qc = new_circuit(framework, 2)
    apply_gate(qc, 'H', [1])
    apply_gate(qc, 'CX', [1, 0])    # bug: wrong index
    multi_apply_sqgate(qc, 'Z', [0, 1])
    apply_gate(qc, 'CX', [0, 1])
    apply_gate(qc, 'H', [1])
    return qc
def Cir1A_bug5(framework : str):
    qc = new_program(framework, 2, 1)
    apply_gate(qc, 'H', [1])
    apply_gate(qc, 'CX', [0, 1])
    multi_apply_sqgate(qc, 'Z', [0, 1])
    apply_gate(qc, 'CX', [0, 1])
    apply_measure(qc, [0], [0])     # bug: add M
    apply_gate(qc, 'H', [1])
    return qc


# ----- Equivalence gate implementations -----
# Rxx gate
def Rxx_Normal(framework : str):
    qc = new_circuit(framework, 2)
    apply_gate(qc, 'Rxx', [0, 1], [0.2345])
    return qc
def Rxx_Decomposition(framework : str):
    qc = new_circuit(framework, 2)
    apply_gate(qc, 'H', [0])
    apply_gate(qc, 'H', [1])
    apply_gate(qc, 'CNOT', [0, 1])
    apply_gate(qc, 'RZ', [1], [0.2345])
    apply_gate(qc, 'CNOT', [0, 1])
    apply_gate(qc, 'H', [0])
    apply_gate(qc, 'H', [1])
    return qc

# Ryy gate
def Ryy_Normal(framework : str):
    qc = new_circuit(framework, 2)
    apply_gate(qc, 'Ryy', [0, 1], [0.2345])
    return qc
def Ryy_Decomposition(framework : str):
    qc = new_circuit(framework, 2)
    apply_gate(qc, 'SD', [0])
    apply_gate(qc, 'SD', [1])
    apply_gate(qc, 'H', [0])
    apply_gate(qc, 'H', [1])
    apply_gate(qc, 'CNOT', [0, 1])
    apply_gate(qc, 'RZ', [1], [0.2345])
    apply_gate(qc, 'CNOT', [0, 1])
    apply_gate(qc, 'H', [0])
    apply_gate(qc, 'H', [1])
    apply_gate(qc, 'S', [0])
    apply_gate(qc, 'S', [1])
    return qc

# Rzz gate
def Rzz_Normal(framework : str):
    qc = new_circuit(framework, 2)
    apply_gate(qc, 'Rzz', [0, 1], [0.2345])
    return qc
def Rzz_Decomposition(framework : str):
    qc = new_circuit(framework, 2)
    apply_gate(qc, 'CNOT', [0, 1])
    apply_gate(qc, 'RZ', [1], [0.2345])
    apply_gate(qc, 'CNOT', [0, 1])
    return qc

# iSWAP gate
def iSWAP_Normal(framework : str):
    qc = new_circuit(framework, 2)
    apply_gate(qc, 'iSWAP', [0, 1])
    return qc
def iSWAP_Decomposition(framework : str):
    qc = new_circuit(framework, 2)
    apply_gate(qc, 'CZ', [0, 1])
    apply_gate(qc, 'S', [0])
    apply_gate(qc, 'S', [1])
    apply_gate(qc, 'SWAP', [0, 1])
    return qc

# U1 gate and Rz gate are equivalence ignoring the global phase
def U1gate(framework : str):
    qc = new_circuit(framework, 1)
    apply_gate(qc, 'U1', [0], [1.3456])
    return qc
def Rzgate(framework : str):
    qc = new_circuit(framework, 1)
    apply_gate(qc, 'Rz', [0], [1.3456])
    return qc

# CH gate
def CH_Normal(framework : str):
    qc = new_circuit(framework, 2)
    apply_gate(qc, 'CH', [0, 1])
    return qc
def CH_Decomposition(framework : str):
    qc = new_circuit(framework, 2)
    apply_gate(qc, 'Ry', [1], [-math.pi / 4])
    apply_gate(qc, 'CZ', [0, 1])
    apply_gate(qc, 'Ry', [1], [math.pi / 4])
    return qc

# CS gate
def CS_Normal(framework : str):
    qc = new_circuit(framework, 2)
    apply_gate(qc, 'CS', [0, 1])
    return qc
def CS_Decomposition(framework : str):
    qc = new_circuit(framework, 2)
    apply_gate(qc, 'T', [0])
    apply_gate(qc, 'CRZ', [0, 1], [math.pi / 2])
    return qc

# CSD gate
def CSD_Normal(framework : str):
    qc = new_circuit(framework, 2)
    apply_gate(qc, 'CSD', [0, 1])
    return qc
def CSD_Decomposition(framework : str):
    qc = new_circuit(framework, 2)
    apply_gate(qc, 'TD', [0])
    apply_gate(qc, 'CRZ', [0, 1], [-math.pi / 2])
    return qc

# CU1 gate
def CU1_Normal(framework : str):
    qc = new_circuit(framework, 2)
    apply_gate(qc, 'CU1', [0, 1], [0.789])
    return qc
def CU1_Decomposition(framework : str):
    qc = new_circuit(framework, 2)
    apply_gate(qc, 'U1', [0], [0.789 / 2])
    apply_gate(qc, 'CRZ', [0, 1], [0.789])
    return qc

# SqrtX and SqrtXdag gate
def SqrtX_Normal(framework : str):
    qc = new_circuit(framework, 1)
    apply_gate(qc, 'SqrtX', [0])
    return qc
def SqrtX_Decomposition(framework : str):
    qc = new_circuit(framework, 1)
    apply_gate(qc, 'H', [0])
    apply_gate(qc, 'S', [0])
    apply_gate(qc, 'H', [0])
    return qc
def SqrtXdag_Normal(framework : str):
    qc = new_circuit(framework, 1)
    apply_gate(qc, 'SqrtXdag', [0])
    return qc
def SqrtXdag_Decomposition(framework : str):
    qc = new_circuit(framework, 1)
    apply_gate(qc, 'H', [0])
    apply_gate(qc, 'Sdag', [0])
    apply_gate(qc, 'H', [0])
    return qc

# Fredkin gate
def Fredkin_Normal(framework : str):
    qc = new_circuit(framework, 3)
    apply_gate(qc, 'Fredkin', [0, 1, 2])
    return qc
def Fredkin_Decomposition(framework : str):
    qc = new_circuit(framework, 3)
    apply_gate(qc, 'CCX', [0, 1, 2])
    apply_gate(qc, 'CCNOT', [0, 2, 1])
    apply_gate(qc, 'Toffoli', [0, 1, 2])
    return qc

# U3 gate
def U3_Normal(framework : str):
    qc = new_circuit(framework, 1)
    apply_gate(qc, 'U3', [0], [1.4, 2.5, 3.6])
    return qc
def U3_Decomposition(framework : str):
    qc = new_circuit(framework, 1)
    apply_gate(qc, 'U1', [0], [3.6])
    apply_gate(qc, 'Ry', [0], [1.4])
    apply_gate(qc, 'U1', [0], [2.5])
    return qc
