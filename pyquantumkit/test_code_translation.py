# test_code_translation.py
#    2026/11/6
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from pyquantumkit import CircuitIO, apply_gate, apply_measure
from pyquantumkit.classical.common import indexlist_length
from pyquantumkit.translate.common import get_standard_gatename

def _specific_gate_circuit(gatestr : str, qbitlist : list[int], paras : list = None) -> CircuitIO:
    nqbits = indexlist_length(qbitlist)
    ncbits = indexlist_length(paras) if get_standard_gatename(gatestr) == 'M' else 0
    qc = CircuitIO(nqbits, ncbits)
    apply_gate(qc, gatestr, qbitlist, paras)
    return qc

def _all_gates_circuit() -> CircuitIO:
    qc = CircuitIO(5, 5)
    apply_gate(qc, 'I', [0])
    qc.apply_gate('X', [0])
    apply_gate(qc, 'y', [1])
    apply_gate(qc, 'Z', [2])
    apply_gate(qc, 's', [3])
    apply_gate(qc, 't', [4])
    apply_gate(qc, 'h', [0])
    apply_gate(qc, 'CNOT', [1, 2])
    apply_gate(qc, 'cy', [3, 4])
    apply_gate(qc, 'cz', [0, 1])
    apply_gate(qc, 'CH', [2, 3])
    apply_gate(qc, 'Rx', [4], [1.1])
    apply_gate(qc, 'Ry', [0], [2.2])
    apply_gate(qc, 'rZ', [1], [3.3])
    apply_gate(qc, 'Swap', [2, 3])
    apply_gate(qc, 'iSWAP', [4, 0])
    qc.apply_gate('CRx', [1, 3], [0.123])
    apply_gate(qc, 'cry', [2, 4], [0.456])
    apply_gate(qc, 'CRZ', [0, 2], [0.789])
    apply_gate(qc, 'Rxx', [1, 4], [3])
    apply_gate(qc, 'ryy', [0, 3], [2])
    apply_gate(qc, 'RZZ', [2, 1], [1])
    apply_gate(qc, 'Fredkin', [0, 1, 2])
    qc.apply_gate('Toffoli', [1, 2, 3])
    apply_gate(qc, 'ccz', [2, 3, 4])
    apply_gate(qc, 'sdagger', [0])
    apply_gate(qc, 'tdag', [4])
    apply_gate(qc, 'P', [1], [-1])
    apply_gate(qc, 'CP', [2, 3], [-2])
    apply_gate(qc, 'u3', [4], [-3, 1e1, -2e-3])
    apply_gate(qc, 'SqrtX', [0])
    apply_gate(qc, 'SXD', [1])
    apply_gate(qc, 'CS', [2, 3])
    apply_gate(qc, 'csdag', [2, 4])
    apply_measure(qc, range(5), range(5))
    return qc


def test_apply_gate(language : str, circuit_name : str,
                            gatestr : str, qbitlist : list[int], paras : list = None) -> str:
    """
    Test the translated code for the apply_gate() function. Print the code.

        language : the name of frameworks
        circuit_name : the name of applied quantum circuit
        gate_str  : a string to identify the quantum gate
        qbits     : the indexes of applied qubits
        paras     : (optional) the parameters of the gate

    Return -> the printed code
    """
    cio = _specific_gate_circuit(gatestr, qbitlist, paras)
    code = cio.export_standalone_code(language, circuit_name)
    print(code)
    return code

def test_apply_measure(language : str, circuit_name : str,
                        qindex : list[int], cindex : list[int]) -> str:
    """
    Test the translated code for the apply_measure() function. Print the code.

        language : the name of frameworks
        circuit_name : applied quantum circuit
        qindex    : the indexes of measured qubits
        cindex    : the indexes of cbits to contain results

    Return -> the printed code
    """
    return test_apply_gate(language, circuit_name, 'M', qindex, cindex)

def test_apply_gate_all(language : str, circuit_name : str) -> str:
    """
    The the translated code for all gates in PyQuantumKit. Print the code.

        language : the name of frameworks
        circuit_name : applied quantum circuit

    Return -> the printed code
    """
    cio = _all_gates_circuit()
    code = cio.export_standalone_code(language, circuit_name)
    print(code)
    return code

# def test_apply_subroutine(language : str, qsub_name : str) -> str:
#     pass

# def test_apply_support_subroutine(language : str) -> str:
#     pass
