# translate/framework_map.py
#    2025/6/11
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from enum import Enum, auto
import importlib
from pyquantumkit.classical.common import indexlist_length      # Do not delete this line
from .common import FrameworkMapError, get_standard_gatename, get_standard_subroutine_name
from pyquantumkit import Supported_Frameworks, get_framework_from_object, framework_modules
from pyquantumkit.translate.extra_languages import extra_language_APPLY, extra_language_DECLARE, \
                                        extra_language_IMPORT, extra_language_CONSTANTS, \
                                        extra_languate_SUBROUTINES

Translate_Namespace = {}
for fname in Supported_Frameworks:
    Translate_Namespace[fname] = importlib.import_module('pyquantumkit.translate.translate_scripts.' + fname)

def framework_interpret_protocol(framework : str) -> str:
    if framework == 'pyquantumkit':
        return 'l'
    return Translate_Namespace[framework].INTERPRET_PROTOCOL

def get_reverse_output_str(framework : str) -> bool:
    if framework_interpret_protocol(framework) == 'l':
        return False
    return True

def get_support_inverse(framework : str) -> bool:
    if framework == 'pyquantumkit':
        return True
    return Translate_Namespace[framework].SUPPORT_INVERSE

def get_support_remap(framework : str) -> bool:
    if framework == 'pyquantumkit':
        return True
    return Translate_Namespace[framework].SUPPORT_REMAP

def framework_support_subroutines(framework : str) -> dict[str]:
    if framework == 'pyquantumkit':
        return {'QFT', 'QFT_NS', 'IQFT', 'IQFT_NS'}
    return Translate_Namespace[framework].SUPPORT_SUBROUTINES


class Action(Enum):
    NEW           = auto()
    GATE          = auto()
    CIRCUIT       = auto()
    MIXED_CIRCUIT = auto()
    BITS          = auto()
    RUN           = auto()
    SUBROUTINE    = auto()

def export_constants(language : str) -> dict:
    if language in Translate_Namespace:
        try:
            return Translate_Namespace[language].EXPORT_CONSTANTS
        except Exception:
            return {}
    return extra_language_CONSTANTS(language)

def import_code(language : str, module : str) -> str:
    if language in Translate_Namespace:
        try:
            return Translate_Namespace[language].IMPORT(module)
        except Exception:
            return ""
    return extra_language_IMPORT(language)(module)

def declare_qubits_code(language : str, var_name : str, mixed_circuit : bool,
                        nqbits : int, ncbits : int) -> str:
    if language in Translate_Namespace:
        return Translate_Namespace[language].DECLARE(var_name, None, mixed_circuit, nqbits, ncbits)
    return extra_language_DECLARE(language)(var_name, None, mixed_circuit, nqbits, ncbits)

def op_applying_code(language : str, cir_name : str, op_name : str,
                     qbits : list[int], paras : list, is_qsub : bool) -> tuple[str, str]:
    code = None
    module_name = None
    if language in Translate_Namespace:
        module_name = framework_support_subroutines(language)[get_standard_subroutine_name(op_name)] \
                        if is_qsub else export_constants(language).get('stdlib_name', None)
        code = Translate_Namespace[language].APPLY(cir_name, None, op_name, qbits, paras, is_qsub)
    else:
        module_name = extra_languate_SUBROUTINES(language).get(get_standard_subroutine_name(op_name), None) \
                        if is_qsub else export_constants(language).get('stdlib_name', None)
        code = extra_language_APPLY(language)(cir_name, None, op_name, qbits, paras, is_qsub)
    return (code, module_name)


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

    if action == Action.MIXED_CIRCUIT:
        def ret(qp_dest, qp_src, qbits_remap, cbits_remap) -> None:
            exec(Translate_Namespace[framework].MIXED_CIRCUIT(bool(qbits_remap), bool(cbits_remap)))
        return ret

    if action == Action.NEW:
        def ret(mixed_circuit : bool, nqbits : int, ncbits : int):
            return eval(Translate_Namespace[framework].NEW(mixed_circuit, nqbits, ncbits))
        return ret

    if action == Action.BITS:
        def ret(qc, ret_cbit : bool, ret_list : bool):
            return eval(Translate_Namespace[framework].BITS(ret_cbit, ret_list))
        return ret

    if action == Action.RUN:
        def ret(qvm, qc, run_shots : int, options : dict):
            try:
                # Use an explicit locals dict so exec-created variables are visible to eval
                local_env = {
                    "qvm": qvm,
                    "qc": qc,
                    "run_shots": run_shots,
                    "options": options,
                }
                exec(Translate_Namespace[framework].RUN(options), globals(), local_env)
                return local_env['RESULT']
            except Exception:
                print("PyQuantumKit: some errors are occurred in RUN action.")
                raise
        return ret

    if action == Action.SUBROUTINE:
        def ret(qc, qsub : str, qbits : list[int], paras : list) -> None:
            execstr = Translate_Namespace[framework].SUBROUTINE(qsub, qbits, paras)
            #print(execstr)
            exec(execstr)
        return ret


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

    if action == Action.MIXED_CIRCUIT:
        def ret(qp_dest : CircuitIO, qp_src : CircuitIO, qbits_remap, cbits_remap) -> None:
            tempcio = CircuitIO()
            tempcio.append_circuit_io(qp_src)
            tempcio.remap_qbits(qbits_remap)
            tempcio.remap_cbits(cbits_remap)
            qp_dest.append_circuit_io(tempcio)
        return ret

    if action == Action.NEW:
        def ret(mixed_circuit : bool, nqbits : int, ncbits : int):
            return CircuitIO(nqbits, ncbits)
        return ret

    if action == Action.BITS:
        def ret(qc : CircuitIO, ret_cbit : bool, ret_list : bool):
            n = qc.get_ncbits() if ret_cbit else qc.get_nqbits()
            return list(range(n)) if ret_list else n
        return ret

    if action == Action.RUN:
        def ret(qvm, qc : CircuitIO, run_shots : int, **kwargs):
            raise FrameworkMapError('CircuitIO object does not support RUN action!')
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

    if action == Action.SUBROUTINE:
        def ret(qc : CircuitIO, qsub : str, qbits : list[int], paras : list) -> None:
            qc.apply_subroutine(qsub, qbits, paras)
        return ret


def quantum_action(action : Action, framework_indicator : str|int, *args, **kwargs):
    framework = ''
    is_circuit_io = False

    if isinstance(framework_indicator, int):
        framework = get_framework_from_object(args[framework_indicator])
    elif isinstance(framework_indicator, str):
        framework = framework_indicator
    else:
        raise FrameworkMapError(f"Invalid framework indicator: {framework_indicator}")
    
    if framework.find('pyquantumkit') != -1:
        is_circuit_io = True

    apply_func = get_apply_function_CircuitIO(action) if is_circuit_io \
                  else get_apply_function(action, framework)
    if apply_func is not None:
        return apply_func(*args, **kwargs)
    return None
