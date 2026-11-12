# translate/translate_scripts/pyqpanda3.py
#    Create: 2025/6/10
#    Update: 2026/11/6
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from ..common import get_standard_gatename, get_standard_subroutine_name, FrameworkMapError
import packaging.version

# The interpret protocol
INTERPRET_PROTOCOL = 'r'
# Set of supported quantum subroutines
SUPPORT_SUBROUTINES = {}

EXPORT_CONSTANTS = {
    'comment' : "# PyQPanda3 code exported from PyQuantumKit",
    'prefix' : "",
    'suffix' : "",
    'stdlib_name' : 'pyqpanda3.core',
}

def IMPORT(module_name : str) -> str:
    return f"from {module_name} import *"

def DECLARE(cir_name : str, module_name : str,
            mixed : bool, nqbits : int, ncbits : int) -> str:
    circuit_type = "QProg" if mixed else "QCircuit"
    declare_str = "" if cir_name is None else cir_name + " = "
    module_str = "" if module_name is None else module_name + "."
    return f"{declare_str}{module_str}{circuit_type}({nqbits})"

def APPLY(cir_name : str, module_name : str,
          op_name : str, qbits : list[int], paras : list,
          is_qsub : bool = False) -> str:
    if is_qsub:
        # Translation for quantum subroutines
        s = get_standard_subroutine_name(op_name).upper()
        if s not in SUPPORT_SUBROUTINES:
            raise FrameworkMapError(f"Unsupported quantum subroutine: {s}")
        execstr = cir_name
        slib = '' if module_name is None else module_name + "."

        # Multi-control Gate Series
        if s == 'MCTL':
            # TODO: finish the multi-control
            pass

        return execstr

    else:
        g = get_standard_gatename(op_name).upper()
        execstr = cir_name
        glib = '' if module_name is None else module_name + "."

        #if g == 'I':
        #    return ''
        if g == 'M':
            # NOTE: there are some bugs in measure(list, list) in pyqpanda3 (ver 0.3.1)
            #execstr = f" << framework_modules('pyqpanda3').measure({qbits}, {paras})"
            # Temporarily use bit-by-bit operation to avoid the bugs in pyqpanda3
            for i in range(len(qbits)):
                execstr += f" << {glib}measure({qbits[i]}, {paras[i]})"
            return execstr
        
        # pyqpanda3 does not support SqrtX and SqrtXdag gates,
        #   so translate them into H * S * H and H * Sdag * H
        if g == 'SX':
            execstr += f" << {glib}H({qbits[0]}) << {glib}S({qbits[0]}) << {glib}H({qbits[0]})"
            return execstr
        if g == 'SXD':
            execstr += f" << {glib}H({qbits[0]}) << {glib}S({qbits[0]}).dagger() << {glib}H({qbits[0]})"
            return execstr
        
        execstr += " << " + glib
        if g in {'CH', 'CY', 'CS'}:
            execstr += f"{g[1]}({qbits[1]}).control({qbits[0]})"
            return execstr
        if g == 'CSW':
            execstr += f"SWAP({qbits[1]}, {qbits[2]}).control({qbits[0]})"
            return execstr
        if g in {'SD', 'TD'}:
            execstr += f"{g[0]}({qbits[0]}).dagger()"
            return execstr
        if g == 'CSD':
            execstr += f"S({qbits[1]}).dagger().control({qbits[0]})"
            return execstr
        if g == 'CCZ':
            execstr += f"Z({qbits[2]}).control({qbits[0:2]})"
            return execstr
        
        if g == 'CX':
            g = 'CNOT'
        elif g == 'SW':
            g = 'SWAP'
        elif g == 'ISW':
            g = 'ISWAP'
        elif g == 'CCX':
            g = 'TOFFOLI'
        elif g == 'CU1':
            g = 'CR'

        if not paras:
            execstr += g + "(" + str(qbits)[1:-1] + ")"
        else:
            execstr += g + "(" + str(qbits)[1:-1] + ", " + str(paras)[1:-1] + ")"
        return execstr

# Translate the gate applying into the code of calling in pyqpanda3
def GATE(gate_name : str, qbits : list[int], paras : list) -> str:
    std = EXPORT_CONSTANTS['stdlib_name']
    return APPLY("qc", f"framework_modules('pyqpanda3', '{std}')", gate_name, qbits, paras)

def SUBROUTINE(qsub_name : str, qbits : list[int], paras : list) -> str:
    # unsupport
    raise FrameworkMapError('Quantum subroutines are not supported by pyqpanda3.')

def NEW(mixed_circuit : bool, nqbits : int, ncbits : int) -> str:
    std = EXPORT_CONSTANTS['stdlib_name']
    return DECLARE(None, f"framework_modules('pyqpanda3', '{std}')", mixed_circuit, nqbits, ncbits)

def BITS(ret_cbit : bool, ret_list : bool) -> str:
    std = EXPORT_CONSTANTS['stdlib_name']
    execstr = f"0 if isinstance(qc, framework_modules('pyqpanda3', '{std}').QCircuit) else indexlist_length(qc.cbits())" \
              if ret_cbit else "indexlist_length(qc.qubits())"
    if ret_list:
        return "list(range(" + execstr + "))"
    else:
        return execstr


def RUN(options : dict) -> str:
    if options is not None and options.get('model') is not None:
        return """
qvm.run(qc, run_shots, model=options['model'])
RESULT = qvm.result().get_counts()
        """
    else:
        return """
qvm.run(qc, run_shots)
RESULT = qvm.result().get_counts()
        """


# ---------- Actions just for internal usage ----------
# Translate the circuit applying into the code of calling in pyqpanda3
def CIRCUIT(is_remap : bool, is_inv : bool) -> str:
    std = EXPORT_CONSTANTS['stdlib_name']
    execstr = f"tempqc=framework_modules('pyqpanda3', '{std}').QCircuit(qc_src);qc_dest<<tempqc"
    if is_inv:
        execstr += ".dagger()"
    if is_remap:
        execstr += ".remap(rmlist)"
    return execstr

def MIXED_CIRCUIT(remap_q : bool, remap_c : bool) -> str:
    std = EXPORT_CONSTANTS['stdlib_name']
    execstr = f"tempqp=framework_modules('pyqpanda3', '{std}').QProg(qp_src);qp_dest<<tempqp"
    if remap_q or remap_c:
        execstr += ".remap(qbits_remap,cbits_remap)"
    return execstr
