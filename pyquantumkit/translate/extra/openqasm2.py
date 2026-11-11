# translate/extra/openqasm2.py
#    2026/11/4
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from pyquantumkit.translate.common import get_standard_gatename, get_standard_subroutine_name, \
                                                 FrameworkMapError, get_args_assign_str

# Supported quantum subroutines
SUPPORT_SUBROUTINES = {}

EXPORT_CONSTANTS = {
    'comment' : """// OpenQASM 2.0 code exported from PyQuantumKit
OPENQASM 2.0;""",
    'prefix' : "",
    'suffix' : "",
    'stdlib_name' : 'qelib1.inc',
}

def IMPORT(module_name : str) -> str:
    return f'include "{module_name}";'

def DECLARE(cir_name : str, module_name : str,
            mixed : bool, nqbits : int, ncbits : int) -> str:
    ret = f"qreg {cir_name}_q[{nqbits}];"
    if mixed:
        ret += f" creg {cir_name}_c[{ncbits}];"
    return ret

def APPLY(cir_name : str, module_name : str,
          op_name : str, qbits : list[int], paras : list,
          is_qsub : bool = False) -> str:
    if is_qsub:
        # Translation for quantum subroutines
        s = get_standard_subroutine_name(op_name).upper()
        if s not in SUPPORT_SUBROUTINES:
            raise FrameworkMapError(f"Unsupported quantum subroutine: {s}")
    else:
        # Translation for quantum gates
        g = get_standard_gatename(op_name).lower()
        execstr = ""

        if g == 'm':
            for i in range(len(qbits)):
                execstr += f"measure {cir_name}_q[{qbits[i]}] -> {cir_name}_c[{paras[i]}]; "
            return execstr

        if g == 'isw':
            execstr += f"cz {cir_name}_q[{qbits[0]}], {cir_name}_q[{qbits[1]}]; " + \
                        f"s {cir_name}_q[{qbits[1]}]; " + \
                        f"swap {cir_name}_q[{qbits[0]}], {cir_name}_q[{qbits[1]}];"
            return execstr
        if g == 'ryy':
            execstr += f"sdg {cir_name}_q[{qbits[0]}]; " + \
                        f"sdg {cir_name}_q[{qbits[1]}]; " + \
                        f"rxx {cir_name}_q[{qbits[0]}],{cir_name}_q[{qbits[1]}]; " + \
                        f"s {cir_name}_q[{qbits[0]}]; " + \
                        f"s {cir_name}_q[{qbits[1]}];"
            return execstr
        if g == 'ccz':
            execstr += f"h {cir_name}_q[{qbits[2]}]; " + \
                        f"ccx {cir_name}_q[{qbits[0]}],{cir_name}_q[{qbits[1]}],{cir_name}_q[{qbits[2]}]; " + \
                        f"h {cir_name}_q[{qbits[2]}];"
            return execstr
        if g == 'cs':
            execstr += f"cu1(pi/2) {cir_name}_q[{qbits[0]}];"
            return execstr
        if g == 'csd':
            execstr += f"cu1(-pi/2) {cir_name}_q[{qbits[0]}];"
            return execstr

        if g == 'i':
            g = 'id'
        elif g == 'sw':
            g = 'swap'
        elif g == 'csw':
            g = 'cswap'
        elif g == 'sd':
            g = 'sdg'
        elif g == 'td':
            g = 'tdg'
        elif g == 'csd':
            g = 'csdg'
        elif g == 'sxd':
            g = 'sxdg'

        execstr = g
        if not paras:
            execstr += " " + get_args_assign_str(cir_name + "_q", qbits) + ";"
        else:
            execstr += "(" + str(paras)[1:-1] + ") " + get_args_assign_str(cir_name + "_q", qbits) + ";"
        return execstr
