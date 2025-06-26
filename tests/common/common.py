from pyquantumkit import *
from pyquantumkit._qframes.framework_map import get_reverse_output_str
from pyquantumkit.procedure.generic import *
from pyquantumkit.classical.run_result import *
from pyquantumkit.classical.common import *
from pyquantumkit.program_check.program_relation import run_identity_check

Repeat_Times_Of_State_Check = 20

def is_exception(thing) -> bool:
    if isinstance(thing, type) and issubclass(thing, Exception):
        return True
    return False


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
