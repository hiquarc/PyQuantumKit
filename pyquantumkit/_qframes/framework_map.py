# _qframes/framework_map.py
#    2025/6/11
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from enum import Enum, auto
import importlib
from pyquantumkit import Supported_Frameworks, Framework_Namespace, get_framework_from_object
from pyquantumkit.classical.common import indexlist_length

Translate_Namespace = {}
for fname in Supported_Frameworks:
    Translate_Namespace[fname] = importlib.import_module('pyquantumkit._qframes._' + fname)


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
            exec(Translate_Namespace[framework].GATE(gate, len(qbits), len(paras)))
        return ret

    if action == Action.CIRCUIT:
        def ret(qc_dest, qc_src, rmlist : list[int], inv : bool) -> None:
            exec(Translate_Namespace[framework].CIRCUIT(qc_dest is None, rmlist != None, inv))
        return ret

    if action == Action.PROGRAM:
        def ret(qp_dest, qp_src, qbits_remap, cbits_remap) -> None:
            exec(Translate_Namespace[framework].PROGRAM(qp_dest is None, qbits_remap != None, cbits_remap != None))
        return ret

    if action == Action.NEW:
        def ret(framework, is_qprog : bool, nqbits : int, ncbits : int):
            return eval(Translate_Namespace[framework].NEW(is_qprog))
        return ret

    if action == Action.BITS:
        def ret(qc, ret_cbit : bool, ret_list : bool):
            return eval(Translate_Namespace[framework].BITS(ret_cbit, ret_list))
        return ret

    if action == Action.RUN:
        def ret(qvm, qc, run_shots : int, model):
            try:
                exec(Translate_Namespace[framework].RUN(1, model != None))
                return eval(Translate_Namespace[framework].RUN(2, model != None))
            except Exception:
                return {}
        return ret

    return None


def quantum_action(action : Action, *args, **kwargs):
    framework = get_framework_from_object(args[0])
    apply_func = get_apply_function(action, framework)
    if apply_func != None:
        return apply_func(*args, **kwargs)
    return None

def get_reverse_output_str(framework : str) -> bool:
    return Translate_Namespace[framework].REVERSE_OUTPUT_STRING
