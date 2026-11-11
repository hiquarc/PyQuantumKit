# translate/translate_scripts/pyquafu.py
#    Create: 2025/7/4
#    Update: 2026/11/6
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from ..common import get_standard_gatename, get_standard_subroutine_name, FrameworkMapError
import packaging.version

# The interpret protocol
INTERPRET_PROTOCOL = 'l'
# Set of supported quantum subroutines
SUPPORT_SUBROUTINES = {}

EXPORT_CONSTANTS = {
    'comment' : "# PyQuafu code exported from PyQuantumKit",
    'prefix' : "",
    'suffix' : "",
    'stdlib_name' : 'quafu.elements.element_gates',
}

def IMPORT(module_name : str) -> str:
    return f"from {module_name} import *"

def DECLARE(cir_name : str, module_name : str,
            mixed : bool, nqbits : int, ncbits : int) -> str:
    circuit_type = "QuantumCircuit"
    declare_str = "" if cir_name is None else cir_name + " = "
    module_str = "" if module_name is None else module_name + "."
    if mixed:
        return f"{declare_str}{module_str}{circuit_type}({nqbits}, {ncbits})"
    else:
        return f"{declare_str}{module_str}{circuit_type}({nqbits})"

def APPLY(cir_name : str, module_name : str,
          op_name : str, qbits : list[int], paras : list,
          is_qsub : bool = False) -> str:
    if is_qsub:
        # Translation for quantum subroutines
        s = get_standard_subroutine_name(op_name).upper()
        if s not in SUPPORT_SUBROUTINES:
            raise FrameworkMapError(f"Unsupported quantum subroutine: {s}")

    else:
        g = get_standard_gatename(op_name).lower()
        execstr = cir_name
        glib = '' if module_name is None else module_name + "."

        if g == 'i':
            g = 'id'
        if g == 'm':
            execstr += f".measure({qbits}, {paras})"
            return execstr
        
        if g == 'ccz':
            execstr += f".mcx({qbits[0:2]}, {qbits[2]})"
            return execstr
        if g == 'ch':
            execstr += f" << {glib}HGate({qbits[1]}).ctrl_by({qbits[0]})"
            return execstr
        if g == 'csd':
            execstr += f" << {glib}SdgGate({qbits[1]}).ctrl_by({qbits[0]})"
            return execstr

        if g == 'u3':
            execstr += f" << {glib}U3Gate"
        elif g == 'crx':
            execstr += f" << {glib}CRXGate"
        elif g == 'cry':
            execstr += f" << {glib}CRYGate"
        elif g == 'crz':
            execstr += f" << {glib}CRZGate"
        elif g == 'sw':
            execstr += '.swap'
        elif g == 'isw':
            execstr += '.iswap'
        elif g == 'csw':
            execstr += '.fredkin'
        elif g == 'u1':
            execstr += ".p"
        elif g == 'cu1':
            execstr += '.cp'
        elif g == 'sd':
            execstr += '.sdg'
        elif g == 'td':
            execstr += '.tdg'
        elif g == 'ccx':
            execstr += '.toffoli'
        elif g == 'sxd':
            execstr += '.sxdg'
        else:
            execstr += '.' + g

        if not paras:
            execstr += "(" + str(qbits)[1:-1] + ")"
        else:
            execstr += "(" + str(qbits)[1:-1] + ", " + str(paras)[1:-1] + ")"
        return execstr

def GATE(gate_name : str, qbits : list[int], paras : list) -> str:
    std = EXPORT_CONSTANTS['stdlib_name']
    return APPLY("qc", f"framework_modules('pyquafu', '{std}')", gate_name, qbits, paras)

def SUBROUTINE(qsub_name : str, qbits : list[int], paras : list) -> str:
    # unsupport
    raise FrameworkMapError('Quantum subroutines are not supported by quafu.')

def NEW(mixed_circuit : bool, nqbits : int, ncbits : int) -> str:
    return DECLARE(None, f"framework_modules('pyquafu', 'quafu')", mixed_circuit, nqbits, ncbits)

def BITS(ret_cbit : bool, ret_list : bool) -> str:
    if ret_list:
        return "list(range(qc.cbits_num))" if ret_cbit else "qc.used_qubits"
    else:
        return "qc.cbits_num" if ret_cbit else "len(qc.used_qubits)"


def RUN(options : dict) -> str:
    return """
res = qvm(qc, shots=run_shots) if qvm == framework_modules('pyquafu', 'quafu').simulate else None
RESULT = res.counts
    """


# ---------- Actions just for internal usage ----------
def CIRCUIT(is_remap : bool, is_inv : bool) -> str:
    # unsupport
    raise FrameworkMapError('Quantum circuit operations are not supported by quafu.')

def MIXED_CIRCUIT(remap_q : bool, remap_c : bool) -> str:
    # unsupport
    raise FrameworkMapError('Quantum-classical-mixed circuit operations are not supported by quafu.')
