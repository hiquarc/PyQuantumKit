# _qframes/framework_map.py
#    2025/6/11
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from enum import Enum, auto
import importlib
from pyquantumkit import PyQuantumKitError
from pyquantumkit import Supported_Frameworks, FN, get_framework_from_object
from pyquantumkit.classical.common import indexlist_length
from pyquantumkit._qframes.__extra_lang import Extra_Languages

Translate_Namespace = {}
for fname in Supported_Frameworks:
    Translate_Namespace[fname] = importlib.import_module('pyquantumkit._qframes._' + fname)

def get_reverse_output_str(framework : str) -> bool:
    if framework == 'pyquantumkit':
        return False
    return Translate_Namespace[framework].REVERSE_OUTPUT_STRING

def get_support_inverse(framework : str) -> bool:
    if framework == 'pyquantumkit':
        return True
    return Translate_Namespace[framework].SUPPORT_INVERSE

def get_support_remap(framework : str) -> bool:
    if framework == 'pyquantumkit':
        return True
    return Translate_Namespace[framework].SUPPORT_REMAP


class Action(Enum):
    NEW     = auto()
    GATE    = auto()
    CIRCUIT = auto()
    PROGRAM = auto()
    BITS    = auto()
    RUN     = auto()

def gate_applying_code(language : str, cir_name : str, gate_lib_name : str, linebreak : str,
                       gate_name : str, qbits : list[int], paras : list) -> str:
    if language in Translate_Namespace:
        return Translate_Namespace[language].CODE(cir_name, gate_lib_name, linebreak,
                                                  gate_name, qbits, paras)
    if language in Extra_Languages:
        return Extra_Languages[language](cir_name, gate_lib_name, linebreak,
                                          gate_name, qbits, paras)
    raise PyQuantumKitError('Language ' + language + ' is not supported.')


def get_apply_function(action : Action, framework : str) -> callable:
    if action == Action.GATE:
        def ret(qc, gate : str, qbits : list[int], paras : list) -> None:
            execstr = Translate_Namespace[framework].GATE(gate, qbits, paras)
            #print(execstr)
            exec(execstr)
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
                #import sys
                #sys.stderr.write('PyQuantumKit: some errors are occurred in RUN action.\n')
                return {}
        return ret
    return None


def get_apply_function_CircuitIO(action : Action) -> callable:
    from pyquantumkit.procedure.circuit_io import CircuitIO
    if action == Action.GATE:
        def ret(qc : CircuitIO, gate : str, qbits : list[int], paras : list) -> None:
            qc.apply_gate(gate, qbits, paras)
        return ret

    if action == Action.CIRCUIT:
        def ret(qc_dest : CircuitIO, qc_src : CircuitIO, rmlist : list[int], inv : bool) -> None:
            tempcio = CircuitIO()
            tempcio.append_circuit_io(qc_src)
            tempcio.remap_qbits(rmlist)
            if inv:
                tempcio.inverse()
            qc_dest.append_circuit_io(tempcio)
        return ret

    if action == Action.PROGRAM:
        def ret(qp_dest : CircuitIO, qp_src : CircuitIO, qbits_remap, cbits_remap) -> None:
            tempcio = CircuitIO()
            tempcio.append_circuit_io(qp_src)
            tempcio.remap_qbits(qbits_remap)
            tempcio.remap_cbits(cbits_remap)
            qp_dest.append_circuit_io(tempcio)
        return ret

    if action == Action.NEW:
        def ret(is_qprog : bool, nqbits : int, ncbits : int):
            return CircuitIO(nqbits, ncbits)
        return ret

    if action == Action.BITS:
        def ret(qc : CircuitIO, ret_cbit : bool, ret_list : bool):
            n = qc.get_ncbits() if ret_cbit else qc.get_nqbits()
            return list(range(n)) if ret_list else n
        return ret

    if action == Action.RUN:
        def ret(qvm, qc : CircuitIO, run_shots : int, **kwargs):
            raise PyQuantumKitError('CircuitIO object does not support RUN action!')
            #try:
                # framework = get_framework_from_object(qvm)
                # print(type(qvm).__module__)

                # # Convert CircuitIO into the circuit of qvm's framework
                # nqbits = qc.get_nqbits()
                # ncbits = qc.get_ncbits()
                # qc_dest = eval(Translate_Namespace[framework].NEW(True))
                # qc.append_into_actual_circuit(qc_dest)

                # # Execute the qvm
                # exec(Translate_Namespace[framework].RUN(1, **kwargs))
                # return eval(Translate_Namespace[framework].RUN(2, **kwargs))
            #except Exception:
            #    return {}
        return ret
    return None


def quantum_action(action : Action, framework_indicator : str|int, *args, **kwargs):
    framework = ''
    is_circuit_io = False

    if isinstance(framework_indicator, int):
        framework = get_framework_from_object(args[framework_indicator])
    elif isinstance(framework_indicator, str):
        framework = framework_indicator
    else:
        raise PyQuantumKitError('Invalid framework indicator: ' + str(framework_indicator))
    
    if framework.find('pyquantumkit') != -1:
        is_circuit_io = True

    apply_func = get_apply_function_CircuitIO(action) if is_circuit_io \
                  else get_apply_function(action, framework)
    if apply_func is not None:
        return apply_func(*args, **kwargs)
    return None
