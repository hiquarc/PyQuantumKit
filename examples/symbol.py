# example/tf_ising.py
#    2026/1/14
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

import pyqpanda3.core as qpanda
import qiskit, qiskit_aer
import quafu
import pyquantumkit as PQK
import sympy

# Declare the used symbols
eta_ = sympy.Symbol('eta')
epsilon_ = sympy.Symbol('epsilon')

# Use PyQuantumKit to build circuits Ufh1 and Ufh2
def build_Ufh1(qc):
    PQK.apply_gate(qc, 'H', [1])
    PQK.apply_gate(qc, 'CNOT', [1, 0])
    PQK.apply_gate(qc, 'CNOT', [1, 2])
    PQK.apply_gate(qc, 'H', [0])
    PQK.apply_gate(qc, 'Rx', [1], [-epsilon_ * eta_ / 2])
    PQK.apply_gate(qc, 'H', [2])
    PQK.apply_gate(qc, 'CNOT', [1, 0])
    PQK.apply_gate(qc, 'H', [0])
    PQK.apply_gate(qc, 'Z', [1])
    PQK.apply_gate(qc, 'S', [0])
    PQK.apply_gate(qc, 'CNOT', [1, 2])
    PQK.apply_gate(qc, 'Rx', [1], [-epsilon_ * eta_ / 2])
    PQK.apply_gate(qc, 'H', [2])
    PQK.apply_gate(qc, 'S', [2])
    PQK.apply_gate(qc, 'CNOT', [1, 2])
    PQK.apply_gate(qc, 'CNOT', [1, 0])
    PQK.apply_gate(qc, 'Sdag', [0])
    PQK.apply_gate(qc, 'H', [1])
    PQK.apply_gate(qc, 'Sdag', [2])

def build_Ufh2(qc):
    PQK.apply_gate(qc, 'SqrtXdag', [1])
    PQK.apply_gate(qc, 'S', [1])
    PQK.apply_gate(qc, 'CNOT', [0, 1])
    PQK.apply_gate(qc, 'SqrtX', [0])
    PQK.apply_gate(qc, 'CNOT', [0, 2])
    PQK.apply_gate(qc, 'Rx', [0], [-epsilon_ * eta_ / 2])
    PQK.apply_gate(qc, 'Ry', [2], [-epsilon_ * eta_ / 2])
    PQK.apply_gate(qc, 'CNOT', [0, 2])
    PQK.apply_gate(qc, 'SqrtXdag', [0])
    PQK.apply_gate(qc, 'CNOT', [0, 1])
    PQK.apply_gate(qc, 'Sdag', [1])
    PQK.apply_gate(qc, 'SqrtX', [1])


# ---------- Usage of CircuitIO class ----------
# Declare two CircuitIO objects
CIO_Ufh1 = PQK.CircuitIO(3)
CIO_Ufh2 = PQK.CircuitIO(3)
# Build circuits on CircuitIO objects
build_Ufh1(CIO_Ufh1)
build_Ufh2(CIO_Ufh2)

# Get the sympy matrices of circuits
mat1 = CIO_Ufh1.get_sympy_matrix()
mat2 = CIO_Ufh2.get_sympy_matrix()
# print(mat1)
# print(mat2)
# Subtract the matrices to compare them
diff = sympy.simplify(mat1 - mat2)
print(diff)


# ---------- Implement on Qiskit ----------
qiskit_circuit1 = qiskit.QuantumCircuit(3)
# Substitute the symbols: eta_ = 1, epsilon_ = 0.3
CIO_Ufh1.append_into_actual_circuit(qiskit_circuit1, {eta_ : 1, epsilon_ : 0.3})
print(qiskit_circuit1)

qiskit_circuit2 = qiskit.QuantumCircuit(3)
# Substitute the symbols: eta_ = 1, epsilon_ = 0.3
CIO_Ufh2.append_into_actual_circuit(qiskit_circuit2, {eta_ : 1, epsilon_ : 0.3})
print(qiskit_circuit2)


# ---------- Implement on QPanda3 ----------
qpanda_circuit1 = qpanda.QCircuit(3)
# Substitute the symbols: eta_ = 2, epsilon_ = 0.2
CIO_Ufh1.append_into_actual_circuit(qpanda_circuit1, {eta_ : 2, epsilon_ : 0.2})
print(qpanda_circuit1)

qpanda_circuit2 = qpanda.QCircuit(3)
# Substitute the symbols: eta_ = 2, epsilon_ = 0.2
CIO_Ufh2.append_into_actual_circuit(qpanda_circuit2, {eta_ : 2, epsilon_ : 0.2})
print(qpanda_circuit2)


# ---------- Implement on Quafu ----------
quafu_circuit1 = quafu.QuantumCircuit(3)
# Substitute the symbols: eta_ = 3, epsilon_ = 0.12
CIO_Ufh1.append_into_actual_circuit(quafu_circuit1, {eta_ : 3, epsilon_ : 0.12})
quafu_circuit1.draw_circuit()

quafu_circuit2 = quafu.QuantumCircuit(3)
# Substitute the symbols: eta_ = 3, epsilon_ = 0.12
CIO_Ufh2.append_into_actual_circuit(quafu_circuit2, {eta_ : 3, epsilon_ : 0.12})
quafu_circuit2.draw_circuit()
