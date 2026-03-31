# test: frameworks/extra_languages.py
#    2026/3/25
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

import unittest as UT
from pyquantumkit import *

def all_gates_circuit() -> CircuitIO:
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

PRECEDING_CODE = {
    'QSharp' : """// For QSharp language
open Microsoft.Quantum.Core;
operation Test_PyQuantumKit_QSharp() : Unit
{
use qs = Qubit[5];
""",

    'isQ' : """// For isQ language
import std;
unit main()
{
qbit qs[5];
""",
}
FOLLOWING_CODE = {
    'QSharp' : """ResetAll(qs);
}
""",
    
    'isQ' : """}
""",
}
CIRCUIT_NAME = "qs"

def generate_test_code(language : str) -> str:
    cio = all_gates_circuit()
    preceding = PRECEDING_CODE[language]
    maincode = cio.get_circuit_code(language, CIRCUIT_NAME)
    following = FOLLOWING_CODE[language]
    return preceding + maincode + following


class Test_extra_languages(UT.TestCase):
    def test_qsharp(self):
        print(generate_test_code('QSharp'))
    def test_isq(self):
        print(generate_test_code('isQ'))

if __name__ == '__main__':
    UT.main()
# To TEST: copy the output text into a source file of the target language, and then compile it.
