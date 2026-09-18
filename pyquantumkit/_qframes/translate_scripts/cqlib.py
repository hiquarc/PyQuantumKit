# _qframes/translate_scripts/cqlib.py
#    2026/3/25
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from ..code_translate import get_standard_gatename, FrameworkMapError
import math

# Whether the reverse of output 0/1 string is required to let the index of characters match corresponding cbits
REVERSE_OUTPUT_STRING = False
# Wether support inverse circuit
SUPPORT_INVERSE = False
# Wether support remap the index of bits
SUPPORT_REMAP = False
# List of supported algorithms
SUPPORT_ALGORITHMS = []


def CODE(cir_name : str, gate_lib_name : str,
          gate_name : str, qbits : list[int], paras : list) -> str:
    g = get_standard_gatename(gate_name).lower()
    execstr = ""

    if g == 'm':
        for i in range(len(qbits)):
            execstr += cir_name + f".measure({qbits[i]}); "
        return execstr[:-2]
    if g == 'i':
        execstr += cir_name + f".i({qbits[0]}, 1)"
        return execstr
    
    if g == 'u1':
        execstr += cir_name + f".u({qbits[0]}, 0, 0, {paras[0]})"
        return execstr
    if g == 'cu1':
        execstr += cir_name + f".u({qbits[0]}, 0, 0, {paras[0] / 2}); "
        execstr += cir_name + f".crz({qbits[0]}, {qbits[1]}, {paras[0]})"
        return execstr
    if g == 'cs':
        execstr += cir_name + f".t({qbits[0]}); "
        execstr += cir_name + f".crz({qbits[0]}, {qbits[1]}, {math.pi / 2})"
        return execstr
    if g == 'csd':
        execstr += cir_name + f".td({qbits[0]}); "
        execstr += cir_name + f".crz({qbits[0]}, {qbits[1]}, {-math.pi / 2})"
        return execstr
    if g == 'ch':
        execstr += cir_name + f".ry({qbits[1]}, {-math.pi / 4}); "
        execstr += cir_name + f".cz({qbits[0]}, {qbits[1]}); "
        execstr += cir_name + f".ry({qbits[1]}, {math.pi / 4})"
        return execstr
    if g == 'sx':
        execstr += cir_name + f".h({qbits[0]}); "
        execstr += cir_name + f".s({qbits[0]}); "
        execstr += cir_name + f".h({qbits[0]})"
        return execstr
    if g == 'sxd':
        execstr += cir_name + f".h({qbits[0]}); "
        execstr += cir_name + f".sd({qbits[0]}); "
        execstr += cir_name + f".h({qbits[0]})"
        return execstr
    
    if g == 'isw':
        execstr += cir_name + f".cz({qbits[0]}, {qbits[1]}); "
        execstr += cir_name + f".s({qbits[0]}); "
        execstr += cir_name + f".s({qbits[1]}); "
        execstr += cir_name + f".swap({qbits[0]}, {qbits[1]})"
        return execstr
    if g == 'ccz':
        execstr += cir_name + f".h({qbits[0]}); "
        execstr += cir_name + f".ccx({qbits[0]}, {qbits[1]}, {qbits[2]}); "
        execstr += cir_name + f".h({qbits[0]})"
        return execstr
    if g == 'csw':
        execstr += cir_name + f".ccx({qbits[0]}, {qbits[1]}, {qbits[2]}); "
        execstr += cir_name + f".ccx({qbits[0]}, {qbits[2]}, {qbits[1]}); "
        execstr += cir_name + f".ccx({qbits[0]}, {qbits[1]}, {qbits[2]})"
        return execstr

    if g == 'rzz':
        execstr += cir_name + f".cx({qbits[0]}, {qbits[1]}); "
        execstr += cir_name + f".rz({qbits[1]}, {paras[0]}); "
        execstr += cir_name + f".cx({qbits[0]}, {qbits[1]})"
        return execstr
    if g == 'rxx':
        execstr += cir_name + f".h({qbits[0]}); "
        execstr += cir_name + f".h({qbits[1]}); "
        execstr += cir_name + f".cx({qbits[0]}, {qbits[1]}); "
        execstr += cir_name + f".rz({qbits[1]}, {paras[0]}); "
        execstr += cir_name + f".cx({qbits[0]}, {qbits[1]}); "
        execstr += cir_name + f".h({qbits[0]}); "
        execstr += cir_name + f".h({qbits[1]})"
        return execstr
    if g == 'ryy':
        execstr += cir_name + f".sd({qbits[0]}); "
        execstr += cir_name + f".sd({qbits[1]}); "
        execstr += cir_name + f".h({qbits[0]}); "
        execstr += cir_name + f".h({qbits[1]}); "
        execstr += cir_name + f".cx({qbits[0]}, {qbits[1]}); "
        execstr += cir_name + f".rz({qbits[1]}, {paras[0]}); "
        execstr += cir_name + f".cx({qbits[0]}, {qbits[1]}); "
        execstr += cir_name + f".h({qbits[0]}); "
        execstr += cir_name + f".h({qbits[1]}); "
        execstr += cir_name + f".s({qbits[0]}); "
        execstr += cir_name + f".s({qbits[1]})"
        return execstr
    
    if g == 'sw':
        g = 'swap'
    if g == 'u3':
        g = 'u'
    execstr += cir_name + "." + g

    if not paras:
        execstr += "(" + str(qbits)[1:-1] + ")"
    else:
        execstr += "(" + str(qbits)[1:-1] + ", " + str(paras)[1:-1] + ")"
    return execstr


def GATE(gate_name : str, qbits : list[int], paras : list) -> str:
    return CODE("qc", "framework_modules('cqlib')", gate_name, qbits, paras)


def CIRCUIT(is_remap : bool, is_inv : bool) -> str:
    # unsupport
    raise FrameworkMapError('Quantum circuit operations are not supported by cqlib.')


def MIXED_CIRCUIT(remap_q : bool, remap_c : bool) -> str:
    # unsupport
    raise FrameworkMapError('Quantum-classical-mixed circuit operations are not supported by cqlib.')


def NEW(contains_cbits : bool) -> str:
    return "framework_modules('cqlib').Circuit(nqbits)"


def BITS(ret_cbit : bool, ret_list : bool) -> str:
    if ret_cbit:
        raise FrameworkMapError('Getting the number of cbits is not supported by cqlib.')
    return "list(range(qc.num_qubits()))" if ret_list else "qc.num_qubits()"


def RUN(line : int, **kwargs) -> str:
    # unsupport
    raise FrameworkMapError('Running are not supported by cqlib.')

