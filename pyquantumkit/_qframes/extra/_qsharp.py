# _qframes/extra/_qsharp.py
#    2026/3/24
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from ..code_translate import get_standard_gatename

def float_str(num : int|float) -> str:
    ret = str(float(num))
    if '.' in ret:
        return ret
    else:
        return ret + '.0'

def CODE(cir_name : str, gate_lib_name : str,
         gate_name : str, qbits : list[int], paras : list) -> str:
    g = get_standard_gatename(gate_name).upper()

    # Measurement
    if g == 'M':
        execstr = ""
        for i in range(len(qbits)):
            execstr += "let c_" + str(paras[i]) + " = M(" + cir_name + "[" + str(qbits[i]) + "]); "
        return execstr
    
    # Single qubit gate without parameter
    if g in {'I', 'X', 'Y', 'Z', 'S', 'T', 'H', 'SX'}:
        execstr = g + "(" + cir_name + "[" + str(qbits[0]) + "]);"
        return execstr
    
    # Sdag and Tdag
    if g in {'SD', 'TD'}:
        execstr = "Adjoint " + g[0] + "(" + cir_name + "[" + str(qbits[0]) + "]);"
        return execstr
    
    # Two qubit gate without parameter
    if g in {'CX', 'CY', 'CZ', 'SW'}:
        if g == 'CX':
            g = 'CNOT'
        elif g == 'SW':
            g = 'SWAP'
        execstr = g + "(" + cir_name + "[" + str(qbits[0]) + "], " + cir_name + "[" + str(qbits[1]) + "]);"
        return execstr
    
    # Single qubit rotation gates
    if g in {'RX', 'RY', 'RZ', 'U1'}:
        if g[0] == 'R':
            g = g[0] + g[1].lower()
        elif g == 'U1':
            g = 'R1'
        execstr = g + "(" + float_str(paras[0]) + ", " + cir_name + "[" + str(qbits[0]) + "]);"
        return execstr
    
    # Two qubit rotation gates
    if g in {'RXX', 'RYY', 'RZZ'}:
        g = 'R' + g[1].lower() + g[2].lower()
        execstr = g + "(" + float_str(paras[0]) + ", "  + cir_name + "[" + str(qbits[0]) + "], "\
                    + cir_name + "[" + str(qbits[1]) + "]);"
        return execstr
    
    # Controlled single qubit gates
    if g in {'CH', 'CS', 'CSD'}:
        if g == 'CSD':
            g = 'Adjoint S'
        else:
            g = g[1]
        execstr = "Controlled " +  g + "([" + cir_name + "[" + str(qbits[0]) + "]], "\
                    + cir_name + "[" + str(qbits[1]) + "]);"
        return execstr
    
    # Controlled rotation gates
    if g in {'CRX', 'CRY', 'CRZ', 'CU1'}:
        if g[1] == 'R':
            g = 'Controlled R' + g[2].lower()
        elif g == 'CU1':
            g = 'Controlled R1'
        execstr = g + "([" + cir_name + "[" + str(qbits[0]) + "]], ("\
                    + float_str(paras[0]) + ", "  + cir_name + "[" + str(qbits[1]) + "]));"
        return execstr
    
    if g == 'CCX':
        execstr = "CCNOT(" + cir_name + "[" + str(qbits[0]) + "], " + cir_name + "[" + str(qbits[1]) + "], "\
                           + cir_name + "[" + str(qbits[2]) + "]);"
        return execstr
    if g == 'CCZ':
        execstr = "Controlled Z([" + cir_name + "[" + str(qbits[0]) + "], " + cir_name + "[" + str(qbits[1]) + "]], "\
                                   + cir_name + "[" + str(qbits[2]) + "]);"
        return execstr
    if g == 'CSW':
        execstr = "Controlled SWAP([" + cir_name + "[" + str(qbits[0]) + "]], ("\
                                      + cir_name + "[" + str(qbits[1]) + "], " + cir_name + "[" + str(qbits[2]) + "]));"
        return execstr
    if g == 'SXD':
        execstr = "Adjoint SX(" + cir_name + "[" + str(qbits[0]) + "]);"
        return execstr
    if g == 'ISW':
        execstr = "CZ(" + cir_name + "[" + str(qbits[0]) + "], " + cir_name + "[" + str(qbits[1]) + "]); "
        execstr += "S(" + cir_name + "[" + str(qbits[0]) + "]); "
        execstr += "S(" + cir_name + "[" + str(qbits[1]) + "]); "
        execstr += "SWAP(" + cir_name + "[" + str(qbits[0]) + "], " + cir_name + "[" + str(qbits[1]) + "]); "
        return execstr
    if g == 'U3':
        execstr = "R1(" + float_str(paras[2]) + ", " + cir_name + "[" + str(qbits[0]) + "]); "
        execstr += "Ry(" + float_str(paras[0]) + ", " + cir_name + "[" + str(qbits[0]) + "]); "
        execstr += "R1(" + float_str(paras[1]) + ", " + cir_name + "[" + str(qbits[0]) + "]); "
        return execstr
