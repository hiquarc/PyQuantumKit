# translate/common.py
#    2025/6/10
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from pyquantumkit import PyQuantumKitError

# the error type for mapping code into frameworks
class FrameworkMapError(PyQuantumKitError):
    pass

Standard_Gate_Name = {
    'I', 'X', 'Y', 'Z', 'S', 'T', 'H', 'M',
    'CX', 'CY', 'CZ', 'CH', 'RX', 'RY', 'RZ', 'SW', 'ISW',
    'CRX', 'CRY', 'CRZ', 'RXX', 'RYY', 'RZZ', 'CSW',
    'CCX', 'CCZ', 'SD', 'TD', 'U1', 'CU1', 'U3',
    'SX', 'SXD', 'CS', 'CSD',
    # 'SY', 'SYD', 'GP', 'CCY',    # Reserved gate names
}

def get_args_assign_str(argname : str, indexlist : list[int],
                        left_bracket : str = '[', right_bracket : str = ']',
                        delimiter : str = ',') -> str:
    """
    Assign the indexes as the subscripts of the argname and return the string
    
        argname   : (str)
        indexlist : (list[int])
        left_bracket, right_bracket, delimiter : the format characters, default '[' ']' and ','

        e.g. 'a', [0, 1, 2] --> "a[0],a[1],a[2]"
             'b', [2, 5, 1, 3] --> "b[2],b[5],b[1],b[3]"
             'c', [2, 1, 0], '(', ')', ';' --> "c(2);c(1);c(0)"
    """
    s = ""
    nargs = len(indexlist)
    for i in range(nargs):
        s += argname + left_bracket + str(indexlist[i]) + right_bracket
        if i != nargs - 1:
            s += delimiter
    return s

def get_standard_gatename(origin_gate_name : str) -> str:
    """
    Map the original gate name into standard name
    """
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
    if g in {'SX', 'SQRTX'}:
        return 'SX'
    if g in {'SXD', 'SXDG', 'SXDAG', 'SXDAGGER', 'SQRTXDG', 'SQRTXDAG', 'SQRTXDAGGER'}:
        return 'SXD'
    if g in {'CSD', 'CSDG', 'CSDAG', 'CSDAGGER'}:
        return 'CSD'
    
    # For reserved gate names: SY, SYD, GP
    if g in {'SY', 'SQRTY'}:
        return 'SY'
    if g in {'SYD', 'SYDG', 'SYDAG', 'SYDAGGER', 'SQRTYDG', 'SQRTYDAG', 'SQRTYDAGGER'}:
        return 'SYD'
    if g in {'GP', 'GPHASE', 'GLOBALPHASE'}:
        return 'GP'

    if g in Standard_Gate_Name:
        return g
    raise FrameworkMapError("Gate is not supported: " + g)


Standard_Subroutine_Name = {
    'QFT', 'QFT_NS', 'IQFT', 'IQFT_NS',     # Series of Quantum Fourier Transform
    # 'MCTL',                                 # Multi-Control Gate (reserved)
}

# Map the original subroutine name into standard name
def get_standard_subroutine_name(origin_gate_name : str) -> str:
    sub = origin_gate_name.upper()

    # Convert the nonstandard gate name into standard gate name
    # ......

    if sub in Standard_Subroutine_Name:
        return sub
    raise FrameworkMapError("Subroutine is not supported: " + sub)
