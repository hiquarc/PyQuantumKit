# qframes/code_translate.py
#    2025/6/10
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from PyQuantumKit import UnsupportedError

Standard_Gate_Name = [
    'I', 'X', 'Y', 'Z', 'S', 'T', 'H',
    'CX', 'CY', 'CZ', 'CH', 'RX', 'RY', 'RZ', 'SW', 'ISW',
    'CRX', 'CRY', 'CRZ', 'RXX', 'RYY', 'RZZ', 'CSW',
    'CCX', 'CCZ', 'SD', 'TD', 'U1', 'CU1', 'U3',
    'M', 'MA'
]


def ArgsAssignStr(argname : str, nargs : int) -> str:
    s = ""
    for i in range(nargs):
        s += (argname + "[" + str(i) + "]")
        if i != nargs - 1:
            s += ","
    return s


# Map the original gate name into standard name
def ConvertToSandard(origin_gate_name : str) -> str:
    g = origin_gate_name.upper()

    # Convert the nonstandard gate name into standard gate name
    if g == 'M' or g == 'MEASURE':
        return 'M'
    if g == 'I' or g == 'ID':
        return 'I'
    if g == 'CX' or g == 'CNOT':
        return 'CX'
    if g == 'SW' or g == 'SWAP':
        return 'SW'
    if g == 'ISW' or g == 'ISWAP':
        return 'ISW'
    if g == 'CCX' or g == 'TOFFOLI' or g == 'CCNOT':
        return 'CCX'
    if g == 'CSW' or g == 'CSWAP':
        return 'CSW'
    if g == 'SD' or g == 'SDG' or g == 'SDAG' or g == 'SDAGGER':
        return 'SD'
    if g == 'TD' or g == 'TDG' or g == 'TDAG' or g == 'TDAGGER':
        return 'TD'
    if g == 'U1' or g == 'R1' or g == 'P':
        return 'U1'
    if g == 'CU1' or g == 'CR1' or g == 'CR' or g == 'CP':
        return 'CU1'
    if g == 'U3' or g == 'U':
        return 'U3'
    
    if g in Standard_Gate_Name:
        return g
    raise UnsupportedError("Gate is not supported: " + g)
