# example/ghz_state.py
#    2025/7/10
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

import pyquantumkit as PQK


# Define the unified quantum circuit construction function using PyQuantumKit
def ghz_state(circuit, nqbits : int):
    PQK.apply_gate(circuit, 'H', [0])               # Apply H gate on qubit with index 0
    for i in range(1, nqbits):
        PQK.apply_gate(circuit, 'cnot', [0, i])     # Apply CNOT gate on qubit with index 0 and i
    # Measure all qubits
    PQK.apply_measure(circuit, range(nqbits), range(nqbits))


Nqs = 5
circuit = PQK.CircuitIO(Nqs, Nqs)
ghz_state(circuit, Nqs)
result = circuit.run()
print(result.counts)
