# _qframes/translate_scripts/pyqpanda3.py
#    2025/6/10
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from ..code_translate import get_standard_gatename, get_standard_subroutine_name, FrameworkMapError
import packaging.version

# The interpret protocol
INTERPRET_PROTOCOL = 'r'
# Wether support inverse circuit
SUPPORT_INVERSE = True
# Wether support remap the index of bits
SUPPORT_REMAP = True
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
    return CODE("qc", "framework_modules('pyqpanda3', 0)", gate_name, qbits, paras)


# Translate the circuit applying into the code of calling in pyqpanda3
def CIRCUIT(is_remap : bool, is_inv : bool) -> str:
    execstr = "tempqc=framework_modules('pyqpanda3', 0).QCircuit(qc_src);qc_dest<<tempqc"
    if is_inv:
        execstr += ".dagger()"
    if is_remap:
        execstr += ".remap(rmlist)"
    return execstr


def MIXED_CIRCUIT(remap_q : bool, remap_c : bool) -> str:
    execstr = "tempqp=framework_modules('pyqpanda3', 0).QProg(qp_src);qp_dest<<tempqp"
    if remap_q or remap_c:
        execstr += ".remap(qbits_remap,cbits_remap)"
    return execstr


def NEW(contains_cbits : bool) -> str:
    if contains_cbits:
        return "framework_modules('pyqpanda3', 0).QProg(nqbits)"
    return "framework_modules('pyqpanda3', 0).QCircuit(nqbits)"


def BITS(ret_cbit : bool, ret_list : bool) -> str:
    execstr = "0 if isinstance(qc, framework_modules('pyqpanda3', 0).QCircuit) else indexlist_length(qc.cbits())" \
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


def SUBROUTINE(qsub_name : str, qbits : list[int], paras : list) -> str:
    # unsupport
    raise FrameworkMapError('Quantum subroutines are not supported by pyqpanda3.')
