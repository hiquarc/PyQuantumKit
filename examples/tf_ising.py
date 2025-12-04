# example/tf_ising.py
#    2025/11/26
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

import pyqpanda3.core as qpanda
import qiskit, qiskit_aer
import pyquantumkit as PQK
import pyquantumkit.library.hamiltonian as PQKHami

N = 5           # number of particles
J = 1.0         # interaction
B = 1.0         # magnatic field
t = 1.0         # evolution time
n = 4           # rounds of decomposition

# ----- Build the Hamiltonian -----
# construct a PauliHamiltonian object, the parameter is the number of qubits
TFIsing = PQKHami.PauliHamiltonian(N)
# interaction terms
TFIsing.append_pauli('ZZIII', -J)
TFIsing.append_pauli('IZZII', -J)
TFIsing.append_pauli('IIZZI', -J)
TFIsing.append_pauli('IIIZZ', -J)
TFIsing.append_pauli('ZIIIZ', -J)
# magnatic field terms
TFIsing.append_pauli('XIIII', -B)
TFIsing.append_pauli('IXIII', -B)
TFIsing.append_pauli('IIXII', -B)
TFIsing.append_pauli('IIIXI', -B)
TFIsing.append_pauli('IIIIX', -B)

# construct circuit on qpanda
qpanda_circuit = qpanda.QCircuit(N)
PQKHami.pqk_hsim_paulis_trotter(qpanda_circuit, TFIsing, t, n, range(N))
print(qpanda_circuit)

# construct circuit on qiskit
qiskit_circuit = qiskit.QuantumCircuit(N)
PQKHami.pqk_hsim_paulis_trotter(qiskit_circuit, TFIsing, t, n, range(N))
print(qiskit_circuit)
