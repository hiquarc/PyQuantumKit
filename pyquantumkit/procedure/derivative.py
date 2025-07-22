# procedure/derivative.py
#    2025/7/21
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from pyquantumkit import get_framework_from_object
from pyquantumkit.procedure.generic import new_circuit, append_circuit
from pyquantumkit._qframes.framework_map import get_support_inverse, get_support_remap
from pyquantumkit.classical.common import indexlist_length
from pyquantumkit.procedure.circuit_io import CircuitIO


def derivative(q_circuit, qbitlist : list[int], createfunc : callable, rev_endian = False, uncomp = False,\
                *args, **kwargs):
    """
    Generate the derivative circuit based on quantum circuit function <createfunc>

        q_circuit  : the circuit to be appended
        qbitlist   : index of qubit list to apply the circuit
        createfunc : the functions to create target quantum circuit
        rev_endian : whether reverse the order of target quantum circuit
        uncomp     : whether generate the inverse version of target quantum circuit
        ...        : the parameters required in <createfunc>

    -> Return : q_circuit; if q_circuit is None, create a new circuit
    """
    f = get_framework_from_object(q_circuit)
    
    if get_support_inverse(f) and get_support_remap(f):
        tempqc = new_circuit(f, indexlist_length(qbitlist))
        createfunc(tempqc, *args, **kwargs)
        if rev_endian:
            append_circuit(q_circuit, tempqc, range(0, len(qbitlist))[::-1], uncomp)
        else:
            append_circuit(q_circuit, tempqc, None, uncomp)
    else:
        tempqc = CircuitIO(indexlist_length(qbitlist))
        createfunc(tempqc, *args, **kwargs)
        if uncomp:
            tempqc.inverse()
        if rev_endian:
            tempqc.remap_qubits(range(0, len(qbitlist))[::-1])
        tempqc.append_into_actual_circuit(q_circuit)

    return q_circuit
