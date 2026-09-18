# _qframes/extra/qsharp.py
#    2026/3/24
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from ..code_translate import get_standard_gatename

def float_str(num : int|float) -> str:
    ret = str(float(num))
    return ret
    # if '.' in ret:
    #     return ret
    # else:
    #     return ret + '.0'

def CODE(cir_name : str, gate_lib_name : str,
         gate_name : str, qbits : list[int], paras : list) -> str:
    g = get_standard_gatename(gate_name).upper()

    # Measurement
    if g == 'M':
        execstr = ""
        for i in range(len(qbits)):
            execstr += f"let c_{paras[i]} = M({cir_name}[{qbits[i]}]); "
        return execstr
    
    # Single qubit gate without parameter
    if g in {'I', 'X', 'Y', 'Z', 'S', 'T', 'H', 'SX'}:
        execstr = f"{g}({cir_name}[{qbits[0]}]);"
        return execstr
    
    # Sdag and Tdag
    if g in {'SD', 'TD'}:
        execstr = f"Adjoint {g[0]}({cir_name}[{qbits[0]}]);"
        return execstr
    
    # Two qubit gate without parameter
    if g in {'CX', 'CY', 'CZ', 'SW'}:
        if g == 'CX':
            g = 'CNOT'
        elif g == 'SW':
            g = 'SWAP'
        execstr = f"{g}({cir_name}[{qbits[0]}], {cir_name}[{qbits[1]}]);"
        return execstr
    
    # Single qubit rotation gates
    if g in {'RX', 'RY', 'RZ', 'U1'}:
        if g[0] == 'R':
            g = g[0] + g[1].lower()
        elif g == 'U1':
            g = 'R1'
        execstr = f"{g}({float_str(paras[0])}, {cir_name}[{qbits[0]}]);"
        return execstr
    
    # Two qubit rotation gates
    if g in {'RXX', 'RYY', 'RZZ'}:
        g = 'R' + g[1].lower() + g[2].lower()
        execstr = f"{g}({float_str(paras[0])}, {cir_name}[{qbits[0]}], {cir_name}[{qbits[1]}]);"
        return execstr
    
    # Controlled single qubit gates
    if g in {'CH', 'CS', 'CSD'}:
        if g == 'CSD':
            g = 'Adjoint S'
        else:
            g = g[1]
        execstr = f"Controlled {g}([{cir_name}[{qbits[0]}]], {cir_name}[{qbits[1]}]);"
        return execstr
    
    # Controlled rotation gates
    if g in {'CRX', 'CRY', 'CRZ', 'CU1'}:
        if g[1] == 'R':
            g = 'Controlled R' + g[2].lower()
        elif g == 'CU1':
            g = 'Controlled R1'
        execstr = f"{g}([{cir_name}[{qbits[0]}]], ({float_str(paras[0])}, {cir_name}[{qbits[1]}]));"
        return execstr
    
    if g == 'CCX':
        execstr = f"CCNOT({cir_name}[{qbits[0]}], {cir_name}[{qbits[1]}], {cir_name}[{qbits[2]}]);"
        return execstr
    if g == 'CCZ':
        execstr = f"Controlled Z([{cir_name}[{qbits[0]}], {cir_name}[{qbits[1]}]], {cir_name}[{qbits[2]}]);"
        return execstr
    if g == 'CSW':
        execstr = f"Controlled SWAP([{cir_name}[{qbits[0]}]], ({cir_name}[{qbits[1]}], {cir_name}[{qbits[2]}]));"
        return execstr
    if g == 'SXD':
        execstr = f"Adjoint SX({cir_name}[{qbits[0]}]);"
        return execstr
    if g == 'ISW':
        execstr = f"CZ({cir_name}[{qbits[0]}], {cir_name}[{qbits[1]}]); "
        execstr += f"S({cir_name}[{qbits[0]}]); "
        execstr += f"S({cir_name}[{qbits[1]}]); "
        execstr += f"SWAP({cir_name}[{qbits[0]}], {cir_name}[{qbits[1]}]); "
        return execstr
    if g == 'U3':
        execstr = f"R1({float_str(paras[2])}, {cir_name}[{qbits[0]}]); "
        execstr += f"Ry({float_str(paras[0])}, {cir_name}[{qbits[0]}]); "
        execstr += f"R1({float_str(paras[1])}, {cir_name}[{qbits[0]}]); "
        return execstr
