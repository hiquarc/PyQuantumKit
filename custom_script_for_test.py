# test: script_for_test.py
#    2026/11/11
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from pyquantumkit.translate.common import get_standard_gatename, get_standard_subroutine_name, \
                                                 FrameworkMapError, get_args_assign_str

# Supported quantum subroutines
SUPPORT_SUBROUTINES = {}

EXPORT_CONSTANTS = {
    'comment' : "TEST comment",
    'prefix' : "TEST prefix",
    'suffix' : "TEST suffix",
    'stdlib_name' : 'stdlib',
}

def IMPORT(module_name : str) -> str:
    return f'TEST IMPORT "{module_name}"'

def DECLARE(cir_name : str, module_name : str,
            mixed : bool, nqbits : int, ncbits : int) -> str:
    return f"TEST DECLARE {cir_name} {module_name} {mixed} {nqbits} {ncbits}"

def APPLY(cir_name : str, module_name : str,
          op_name : str, qbits : list[int], paras : list,
          is_qsub : bool = False) -> str:
    return f"TEST APPLY {cir_name} {module_name} {op_name} {qbits} {paras} {is_qsub}"
