# _qframes/translate_scripts/pyquafu.py
#    2025/7/4
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from ..code_translate import get_standard_gatename, get_standard_subroutine_name, FrameworkMapError
import packaging.version

# The interpret protocol
INTERPRET_PROTOCOL = 'l'
# Wether support inverse circuit
SUPPORT_INVERSE = False
# Wether support remap the index of bits
SUPPORT_REMAP = False
# Set of supported quantum subroutines
SUPPORT_SUBROUTINES = set()


def CODE(cir_name : str, module_name : str,
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
    return CODE("qc", "framework_modules('pyquafu', 1)", gate_name, qbits, paras)


def CIRCUIT(is_remap : bool, is_inv : bool) -> str:
    # unsupport
    raise FrameworkMapError('Quantum circuit operations are not supported by quafu.')


def MIXED_CIRCUIT(remap_q : bool, remap_c : bool) -> str:
    # unsupport
    raise FrameworkMapError('Quantum-classical-mixed circuit operations are not supported by quafu.')


def NEW(contains_cbits : bool) -> str:
    if contains_cbits:
        return "framework_modules('pyquafu', 0).QuantumCircuit(nqbits, ncbits)"
    return "framework_modules('pyquafu', 0).QuantumCircuit(nqbits)"


def BITS(ret_cbit : bool, ret_list : bool) -> str:
    if ret_list:
        return "list(range(qc.cbits_num))" if ret_cbit else "qc.used_qubits"
    else:
        return "qc.cbits_num" if ret_cbit else "len(qc.used_qubits)"


def RUN(options : dict) -> str:
    return """
res = qvm(qc, shots=run_shots) if qvm == framework_modules('pyquafu', 0).simulate else None
RESULT = res.counts
    """


def SUBROUTINE(qsub_name : str, qbits : list[int], paras : list) -> str:
    # unsupport
    raise FrameworkMapError('Quantum subroutines are not supported by quafu.')
