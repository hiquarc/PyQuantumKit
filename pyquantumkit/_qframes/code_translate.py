# _qframes/code_translate.py
#    2025/6/10
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from pyquantumkit import PyQuantumKitError

Standard_Gate_Name = {
    'I', 'X', 'Y', 'Z', 'S', 'T', 'H', 'M',
    'CX', 'CY', 'CZ', 'CH', 'RX', 'RY', 'RZ', 'SW', 'ISW',
    'CRX', 'CRY', 'CRZ', 'RXX', 'RYY', 'RZZ', 'CSW',
    'CCX', 'CCZ', 'SD', 'TD', 'U1', 'CU1', 'U3',
}

def get_args_assign_str(argname : str, nargs : int) -> str:
    s = ""
    for i in range(nargs):
        s += (argname + "[" + str(i) + "]")
        if i != nargs - 1:
            s += ","
    return s

# Map the original gate name into standard name
def get_standard_gatename(origin_gate_name : str) -> str:
    g = origin_gate_name.upper()

    # Convert the nonstandard gate name into standard gate name
    if g in {'M', 'MA', 'MEASURE'}:
        return 'M'
    if g in {'I', 'ID'}:
        return 'I'
    if g in {'CX', 'CNOT'}:
        return 'CX'
    if g in {'SW', 'SWAP'}:
        return 'SW'
    if g in {'ISW', 'ISWAP'}:
        return 'ISW'
    if g in {'CCX', 'CCNOT', 'TOFFOLI'}:
        return 'CCX'
    if g in {'CSW', 'CSWAP', 'FREDKIN'}:
        return 'CSW'
    if g in {'SD', 'SDG', 'SDAG', 'SDAGGER'}:
        return 'SD'
    if g in {'TD', 'TDG', 'TDAG', 'TDAGGER'}:
        return 'TD'
    if g in {'U1', 'R1', 'P'}:
        return 'U1'
    if g in {'CU1', 'CR1', 'CR', 'CP'}:
        return 'CU1'
    if g in {'U3', 'U'}:
        return 'U3'

    if g in Standard_Gate_Name:
        return g
    raise PyQuantumKitError("Gate is not supported: " + g)
