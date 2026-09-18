# _qframes/extra/isq.py
#    2026/3/25
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from ..code_translate import get_standard_gatename

def CODE(cir_name : str, gate_lib_name : str,
                gate_name : str, qbits : list[int], paras : list) -> str:
    g = get_standard_gatename(gate_name).upper()

    if g == 'I':
        return ""
    if g == 'M':
        execstr = ""
        for i in range(len(qbits)):
            execstr += f"int c_{paras[i]} = M({cir_name}[{qbits[i]}]); "
        return execstr
    
    # Single qubit gate without parameter
    if g in {'X', 'Y', 'Z', 'S', 'T', 'H'}:
        execstr = f"{g}({cir_name}[{qbits[0]}]);"
        return execstr

    # Sdag and Tdag
    if g in {'SD', 'TD'}:
        execstr = f"inv {g[0]}({cir_name}[{qbits[0]}]);"
        return execstr
    
    # Two qubit gate without parameter
    if g in {'CX', 'CZ'}:
        if g == 'CX':
            g = 'CNOT'
        execstr = f"{g}({cir_name}[{qbits[0]}], {cir_name}[{qbits[1]}]);"
        return execstr
    
    # Single qubit rotation gates
    if g in {'RX', 'RY', 'RZ'}:
        g = g[0] + g[1].lower()
        execstr = f"{g}({paras[0]}, {cir_name}[{qbits[0]}]);"
        return execstr

    # Controlled single qubit gates
    if g in {'CY', 'CH', 'CS', 'CSD'}:
        if g == 'CSD':
            g = 'inv S'
        else:
            g = g[1]
        execstr = f"ctrl {g}({cir_name}[{qbits[0]}], {cir_name}[{qbits[1]}]);"
        return execstr
    
    # Controlled rotation gates
    if g in {'CRX', 'CRY', 'CRZ'}:
        g = 'ctrl R' + g[2].lower()
        execstr = f"{g}({qbits[0]}, {cir_name}[{qbits[0]}], {cir_name}[{qbits[1]}]);"
        return execstr
    
    # U1, CU1, U3, SX, SXD
    if g == 'U1':
        execstr = f"U3(0, 0, {paras[0]}, {cir_name}[{qbits[0]}]);"
        return execstr
    if g == 'CU1':
        execstr = f"ctrl U3(0, 0, {paras[0]}, {cir_name}[{qbits[0]}], {cir_name}[{qbits[1]}]);"
        return execstr
    if g == 'U3':
        execstr = f"U3({paras[0]}, {paras[1]}, {paras[2]}, {cir_name}[{qbits[0]}]);"
        return execstr
    if g == 'SX':
        execstr = f"H({cir_name}[{qbits[0]}]); "
        execstr += f"S({cir_name}[{qbits[0]}]); "
        execstr += f"H({cir_name}[{qbits[0]}]);"
        return execstr
    if g == 'SXD':
        execstr = f"H({cir_name}[{qbits[0]}]); "
        execstr += f"inv S({cir_name}[{qbits[0]}]); "
        execstr += f"H({cir_name}[{qbits[0]}]);"
        return execstr

    # 3-qubit gates and SWAP gate
    if g == 'CCX':
        execstr = f"Toffoli({cir_name}[{qbits[0]}], {cir_name}[{qbits[1]}], {cir_name}[{qbits[2]}]);"
        return execstr
    if g == 'CCZ':
        execstr = f"H({cir_name}[{qbits[2]}]); "
        execstr += f"Toffoli({cir_name}[{qbits[0]}], {cir_name}[{qbits[1]}], {cir_name}[{qbits[2]}]); "
        execstr += f"H({cir_name}[{qbits[2]}]);"
        return execstr
    if g == 'SW':
        execstr = f"CNOT({cir_name}[{qbits[0]}], {cir_name}[{qbits[1]}]); "
        execstr += f"CNOT({cir_name}[{qbits[1]}], {cir_name}[{qbits[0]}]); "
        execstr += f"CNOT({cir_name}[{qbits[0]}], {cir_name}[{qbits[1]}]);"
        return execstr
    if g == 'CSW':
        execstr = f"Toffoli({cir_name}[{qbits[0]}], {cir_name}[{qbits[1]}], {cir_name}[{qbits[2]}]); "
        execstr += f"Toffoli({cir_name}[{qbits[0]}], {cir_name}[{qbits[2]}], {cir_name}[{qbits[1]}]); "
        execstr += f"Toffoli({cir_name}[{qbits[0]}], {cir_name}[{qbits[1]}], {cir_name}[{qbits[2]}]);"
        return execstr
    if g == 'ISW':
        execstr = f"CZ({cir_name}[{qbits[0]}], {cir_name}[{qbits[1]}]); "
        execstr += f"S({cir_name}[{qbits[0]}]); "
        execstr += f"S({cir_name}[{qbits[1]}]); "
        execstr += f"CNOT({cir_name}[{qbits[0]}], {cir_name}[{qbits[1]}]); "
        execstr += f"CNOT({cir_name}[{qbits[1]}], {cir_name}[{qbits[0]}]); "
        execstr += f"CNOT({cir_name}[{qbits[0]}], {cir_name}[{qbits[1]}]);"
        return execstr

    # Rxx, Ryy, Rzz
    if g == 'RZZ':
        execstr = f"CNOT({cir_name}[{qbits[0]}], {cir_name}[{qbits[1]}]); "
        execstr += f"Rz({paras[0]}, {cir_name}[{qbits[0]}]); "
        execstr += f"CNOT({cir_name}[{qbits[0]}], {cir_name}[{qbits[1]}]);"
        return execstr
    if g == 'RXX':
        execstr = f"H({cir_name}[{qbits[0]}]); "
        execstr += f"H({cir_name}[{qbits[1]}]); "
        execstr += f"CNOT({cir_name}[{qbits[0]}], {cir_name}[{qbits[1]}]); "
        execstr += f"Rz({paras[0]}, {cir_name}[{qbits[0]}]); "
        execstr += f"CNOT({cir_name}[{qbits[0]}], {cir_name}[{qbits[1]}]); "
        execstr += f"H({cir_name}[{qbits[0]}]); "
        execstr += f"H({cir_name}[{qbits[1]}]);"
        return execstr
    if g == 'RYY':
        execstr = f"inv S({cir_name}[{qbits[0]}]); "
        execstr += f"inv S({cir_name}[{qbits[1]}]); "
        execstr += f"H({cir_name}[{qbits[0]}]); "
        execstr += f"H({cir_name}[{qbits[1]}]); "
        execstr += f"CNOT({cir_name}[{qbits[0]}], {cir_name}[{qbits[1]}]); "
        execstr += f"Rz({paras[0]}, {cir_name}[{qbits[0]}]); "
        execstr += f"CNOT({cir_name}[{qbits[0]}], {cir_name}[{qbits[1]}]); "
        execstr += f"H({cir_name}[{qbits[0]}]); "
        execstr += f"H({cir_name}[{qbits[1]}]); "
        execstr += f"S({cir_name}[{qbits[0]}]); "
        execstr += f"S({cir_name}[{qbits[1]}]);"
        return execstr
    