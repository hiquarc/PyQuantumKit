# test: common/common.py
#    2025/6/23
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from pyquantumkit import *
from pyquantumkit._qframes.framework_map import get_reverse_output_str
from pyquantumkit.procedure.generic import *
from pyquantumkit.classical.run_result import *
from pyquantumkit.classical.common import *
from pyquantumkit.program_check.program_relation import *

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

def CancelCir(framework : str):
    qc = new_circuit(framework, 4)
    apply_gate(qc, 'RX', [0], [0.5])
    apply_gate(qc, 'RY', [0], [1.5])
    apply_gate(qc, 'RZ', [0], [2.5])
    apply_gate(qc, 'RXX', [1, 2], [0.7])
    apply_gate(qc, 'RYY', [1, 2], [1.4])
    apply_gate(qc, 'RZZ', [1, 2], [2.1])
    apply_gate(qc, 'CRX', [0, 3], [-0.3])
    apply_gate(qc, 'CRY', [0, 3], [-0.6])
    apply_gate(qc, 'CRZ', [0, 3], [-0.9])

    apply_gate(qc, 'CRZ', [0, 3], [0.9])
    apply_gate(qc, 'CRY', [0, 3], [0.6])
    apply_gate(qc, 'CRX', [0, 3], [0.3])
    apply_gate(qc, 'RZZ', [1, 2], [-2.1])
    apply_gate(qc, 'RYY', [1, 2], [-1.4])
    apply_gate(qc, 'RXX', [1, 2], [-0.7])
    apply_gate(qc, 'RZ', [0], [-2.5])
    apply_gate(qc, 'RY', [0], [-1.5])
    apply_gate(qc, 'RX', [0], [-0.5])
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

