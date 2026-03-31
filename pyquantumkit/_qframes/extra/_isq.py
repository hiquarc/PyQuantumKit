# _qframes/extra/_isq.py
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
            execstr += "int c_" + str(paras[i]) + " = M(" + cir_name + "[" + str(qbits[i]) + "]); "
        return execstr
    
    # Single qubit gate without parameter
    if g in {'X', 'Y', 'Z', 'S', 'T', 'H'}:
        execstr = g + "(" + cir_name + "[" + str(qbits[0]) + "]);"
        return execstr

    # Sdag and Tdag
    if g in {'SD', 'TD'}:
        execstr = "inv " + g[0] + "(" + cir_name + "[" + str(qbits[0]) + "]);"
        return execstr
    
    # Two qubit gate without parameter
    if g in {'CX', 'CZ'}:
        if g == 'CX':
            g = 'CNOT'
        execstr = g + "(" + cir_name + "[" + str(qbits[0]) + "], " + cir_name + "[" + str(qbits[1]) + "]);"
        return execstr
    
    # Single qubit rotation gates
    if g in {'RX', 'RY', 'RZ'}:
        g = g[0] + g[1].lower()
        execstr = g + "(" + str(paras[0]) + ", " + cir_name + "[" + str(qbits[0]) + "]);"
        return execstr

    # Controlled single qubit gates
    if g in {'CY', 'CH', 'CS', 'CSD'}:
        if g == 'CSD':
            g = 'inv S'
        else:
            g = g[1]
        execstr = "ctrl " +  g + "(" + cir_name + "[" + str(qbits[0]) + "], "\
                    + cir_name + "[" + str(qbits[1]) + "]);"
        return execstr
    
    # Controlled rotation gates
    if g in {'CRX', 'CRY', 'CRZ'}:
        g = 'ctrl R' + g[2].lower()
        execstr = g + "(" + str(qbits[0]) + ", " + cir_name + "[" + str(qbits[0]) + "], "\
                    + cir_name + "[" + str(qbits[1]) + "]);"
        return execstr
    
    # U1, CU1, U3, SX, SXD
    if g == 'U1':
        execstr = "U3(0, 0, " + str(paras[0]) + ", " + cir_name + "[" + str(qbits[0]) + "]);"
        return execstr
    if g == 'CU1':
        execstr = "ctrl U3(0, 0, " + str(paras[0]) + ", "\
                 + cir_name + "[" + str(qbits[0]) + "], " + cir_name + "[" + str(qbits[1]) + "]);"
        return execstr
    if g == 'U3':
        execstr = "U3(" + str(paras[0]) + ", " + str(paras[1]) + ", " + str(paras[2]) + ", "\
                        + cir_name + "[" + str(qbits[0]) + "]);"
        return execstr
    if g == 'SX':
        execstr = "H(" + cir_name + "[" + str(qbits[0]) + "]); "
        execstr += "S(" + cir_name + "[" + str(qbits[0]) + "]); "
        execstr += "H(" + cir_name + "[" + str(qbits[0]) + "]);"
        return execstr
    if g == 'SXD':
        execstr = "H(" + cir_name + "[" + str(qbits[0]) + "]); "
        execstr += "inv S(" + cir_name + "[" + str(qbits[0]) + "]); "
        execstr += "H(" + cir_name + "[" + str(qbits[0]) + "]);"
        return execstr

    # 3-qubit gates and SWAP gate
    if g == 'CCX':
        execstr = "Toffoli(" + cir_name + "[" + str(qbits[0]) + "], " + cir_name + "[" + str(qbits[1]) + "], "\
                             + cir_name + "[" + str(qbits[2]) + "]);"
        return execstr
    if g == 'CCZ':
        execstr = "H(" + cir_name + "[" + str(qbits[2]) + "]); "
        execstr += "Toffoli(" + cir_name + "[" + str(qbits[0]) + "], " + cir_name + "[" + str(qbits[1]) + "], "\
                             + cir_name + "[" + str(qbits[2]) + "]); "
        execstr += "H(" + cir_name + "[" + str(qbits[2]) + "]);"
        return execstr
    if g == 'SW':
        execstr = "CNOT(" + cir_name + "[" + str(qbits[0]) + "], " + cir_name + "[" + str(qbits[1]) + "]); "
        execstr += "CNOT(" + cir_name + "[" + str(qbits[1]) + "], " + cir_name + "[" + str(qbits[0]) + "]); "
        execstr += "CNOT(" + cir_name + "[" + str(qbits[0]) + "], " + cir_name + "[" + str(qbits[1]) + "]);"
        return execstr
    if g == 'CSW':
        execstr = "Toffoli(" + cir_name + "[" + str(qbits[0]) + "], " + cir_name + "[" + str(qbits[1]) + "], "\
                             + cir_name + "[" + str(qbits[2]) + "]); "
        execstr += "Toffoli(" + cir_name + "[" + str(qbits[0]) + "], " + cir_name + "[" + str(qbits[2]) + "], "\
                             + cir_name + "[" + str(qbits[1]) + "]); "
        execstr += "Toffoli(" + cir_name + "[" + str(qbits[0]) + "], " + cir_name + "[" + str(qbits[1]) + "], "\
                             + cir_name + "[" + str(qbits[2]) + "]);"
        return execstr
    if g == 'ISW':
        execstr = "CZ(" + cir_name + "[" + str(qbits[0]) + "], " + cir_name + "[" + str(qbits[1]) + "]); "
        execstr += "S(" + cir_name + "[" + str(qbits[0]) + "]); "
        execstr += "S(" + cir_name + "[" + str(qbits[1]) + "]); "
        execstr += "CNOT(" + cir_name + "[" + str(qbits[0]) + "], " + cir_name + "[" + str(qbits[1]) + "]); "
        execstr += "CNOT(" + cir_name + "[" + str(qbits[1]) + "], " + cir_name + "[" + str(qbits[0]) + "]); "
        execstr += "CNOT(" + cir_name + "[" + str(qbits[0]) + "], " + cir_name + "[" + str(qbits[1]) + "]);"
        return execstr

    # Rxx, Ryy, Rzz
    if g == 'RZZ':
        execstr = "CNOT(" + cir_name + "[" + str(qbits[0]) + "], " + cir_name + "[" + str(qbits[1]) + "]); "
        execstr += "Rz(" + str(paras[0]) + ", " + cir_name + "[" + str(qbits[0]) + "]); "
        execstr += "CNOT(" + cir_name + "[" + str(qbits[0]) + "], " + cir_name + "[" + str(qbits[1]) + "]);"
        return execstr
    if g == 'RXX':
        execstr = "H(" + cir_name + "[" + str(qbits[0]) + "]); "
        execstr += "H(" + cir_name + "[" + str(qbits[1]) + "]); "
        execstr += "CNOT(" + cir_name + "[" + str(qbits[0]) + "], " + cir_name + "[" + str(qbits[1]) + "]); "
        execstr += "Rz(" + str(paras[0]) + ", " + cir_name + "[" + str(qbits[0]) + "]); "
        execstr += "CNOT(" + cir_name + "[" + str(qbits[0]) + "], " + cir_name + "[" + str(qbits[1]) + "]); "
        execstr += "H(" + cir_name + "[" + str(qbits[0]) + "]); "
        execstr += "H(" + cir_name + "[" + str(qbits[1]) + "]);"
        return execstr
    if g == 'RYY':
        execstr = "inv S(" + cir_name + "[" + str(qbits[0]) + "]); "
        execstr += "inv S(" + cir_name + "[" + str(qbits[1]) + "]); "
        execstr += "H(" + cir_name + "[" + str(qbits[0]) + "]); "
        execstr += "H(" + cir_name + "[" + str(qbits[1]) + "]); "
        execstr += "CNOT(" + cir_name + "[" + str(qbits[0]) + "], " + cir_name + "[" + str(qbits[1]) + "]); "
        execstr += "Rz(" + str(paras[0]) + ", " + cir_name + "[" + str(qbits[0]) + "]); "
        execstr += "CNOT(" + cir_name + "[" + str(qbits[0]) + "], " + cir_name + "[" + str(qbits[1]) + "]); "
        execstr += "H(" + cir_name + "[" + str(qbits[0]) + "]); "
        execstr += "H(" + cir_name + "[" + str(qbits[1]) + "]); "
        execstr += "S(" + cir_name + "[" + str(qbits[0]) + "]); "
        execstr += "S(" + cir_name + "[" + str(qbits[1]) + "]);"
        return execstr

    print(g)
    