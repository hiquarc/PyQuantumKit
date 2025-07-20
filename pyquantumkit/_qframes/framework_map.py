# _qframes/framework_map.py
#    2025/6/11
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from enum import Enum, auto
import importlib
from pyquantumkit import PyQuantumKitError
from pyquantumkit import Supported_Frameworks, FN, get_framework_from_object
from pyquantumkit.classical.common import indexlist_length

Translate_Namespace = {}
for fname in Supported_Frameworks:
    Translate_Namespace[fname] = importlib.import_module('pyquantumkit._qframes._' + fname)

def get_reverse_output_str(framework : str) -> bool:
    return Translate_Namespace[framework].REVERSE_OUTPUT_STRING

class Action(Enum):
    NEW     = auto()
    GATE    = auto()
    CIRCUIT = auto()
    PROGRAM = auto()
    BITS    = auto()
    RUN     = auto()


def get_apply_function(action : Action, framework : str) -> callable:
    if action == Action.GATE:
        def ret(qc, gate : str, qbits : list[int], paras : list) -> None:
            exec(Translate_Namespace[framework].GATE(gate, len(qbits), len(paras) if paras else 0))
        return ret

    if action == Action.CIRCUIT:
        def ret(qc_dest, qc_src, rmlist : list[int], inv : bool) -> None:
            exec(Translate_Namespace[framework].CIRCUIT(bool(rmlist), inv))
        return ret

    if action == Action.PROGRAM:
        def ret(qp_dest, qp_src, qbits_remap, cbits_remap) -> None:
            exec(Translate_Namespace[framework].PROGRAM(bool(qbits_remap), bool(cbits_remap)))
        return ret

    if action == Action.NEW:
        def ret(is_qprog : bool, nqbits : int, ncbits : int):
            return eval(Translate_Namespace[framework].NEW(is_qprog))
        return ret

    if action == Action.BITS:
        def ret(qc, ret_cbit : bool, ret_list : bool):
            return eval(Translate_Namespace[framework].BITS(ret_cbit, ret_list))
        return ret

    if action == Action.RUN:
        def ret(qvm, qc, run_shots : int, **kwargs):
            try:
                exec(Translate_Namespace[framework].RUN(1, **kwargs))
                return eval(Translate_Namespace[framework].RUN(2, **kwargs))
            except Exception:
                return {}
        return ret
    return None


def quantum_action(action : Action, framework_indicator : str|int, *args, **kwargs):
    framework = None
    if isinstance(framework_indicator, int):
        framework = get_framework_from_object(args[framework_indicator])
    elif isinstance(framework_indicator, str):
        framework = framework_indicator
    else:
        raise PyQuantumKitError('Invalid framework indicator: ' + str(framework_indicator))

    apply_func = get_apply_function(action, framework)
    if apply_func is not None:
        return apply_func(*args, **kwargs)
    return None
