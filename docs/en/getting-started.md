# Installation and Usage
## Install PyQuantumKit

PyQuantumKit can be installed using the `pip install` command:

```sh
pip install pyquantumkit
```

PyQuantumKit requires Python version >= 3.8 and depends on the following Python packages:

- sympy >= 1.8
- numpy >= 1.22.0

Typically, PyQuantumKit needs to be used in conjunction with supported Python-based quantum development frameworks (e.g., qiskit or pyqpanda3). You can install PyQuantumKit along with a supported quantum development framework. For example, use the following command to install PyQuantumKit and qiskit simultaneously:

```sh
pip install "pyquantumkit[qiskit]"
```

## GitHub

PyQuantumKit is open-source software licensed under the MIT License. [Click here to access](https://github.com/hiquarc/PyQuantumKit) the PyQuantumKit GitHub repository.

Copy the PyQuantumKit repository to your local machine using the `git clone` command:

```sh
git clone https://github.com/hiquarc/PyQuantumKit.git
```

## Usage Examples
This section uses a simple example to illustrate how to use PyQuantumKit to construct quantum circuits in a unified way across different quantum development frameworks.

Requirement: Construct a quantum circuit that generates the GHZ state, run it 1000 times, and obtain the statistical results of the measurements. Write the code once to build the quantum circuit using three quantum development frameworks (qiskit, pyqpanda3, and quafu) respectively, and print the constructed quantum circuit and the results of running it on a simulator.

### 1. Import Required Quantum Development Packages and PyQuantumKit

**Note:** In Python code, **`import pyquantumkit` must be placed after importing the specific quantum development packages** to ensure PyQuantumKit can recognize the imported quantum development package modules.

```python
# import quantum development kits.
import pyqpanda3.core as qpanda
import qiskit, qiskit_aer
import quafu

# import PyQuantumKit
# NOTE: the import of pyquantumkit must be put behind the quantum development kits.
import pyquantumkit as PQK
```

### 2. Write the Circuit Using Functions Provided by PyQuantumKit
Here, two functions `apply_gate` and `apply_measure` are used. [Click here to view](circuit-level/circuit.md) the function details.

```python
def ghz_state(circuit, nqbits : int):
    PQK.apply_gate(circuit, 'H', [0])               # Apply H gate on qubit with index 0
    for i in range(1, nqbits):
        PQK.apply_gate(circuit, 'cnot', [0, i])     # Apply CNOT gate on qubit with index 0 and i
    # Measure all qubits
    PQK.apply_measure(circuit, range(nqbits), range(nqbits))
```

### 3. Set Running Parameters
Here, 5 qubits are used, and the number of running shots is 1000:

```python
# The number of qubits
Nqs = 5
# The number of running shots
Nshots = 1000
```

### 4. Run on qiskit

```python
print(' ### Run on qiskit ### ')

qiskit_circuit = qiskit.QuantumCircuit(Nqs, Nqs)
ghz_state(qiskit_circuit, Nqs)    # unified quantum circuit construction
print(qiskit_circuit)             # print quantum circuit

qiskit_qvm = qiskit_aer.Aer.get_backend('aer_simulator')
qiskit_job = qiskit_qvm.run(qiskit_circuit, shots = Nshots)
qiskit_result = qiskit_job.result().get_counts()
print(qiskit_result)        # print running results
```

The running results are:
<div align="left">
<img src=../../imgs/ghz_qiskit.jpg width=50% />
</div>

### 5. Run on pyqpanda3

```python
print(' ### Run on pyqpanda3 ### ')

qpanda_circuit = qpanda.QProg(Nqs)
ghz_state(qpanda_circuit, Nqs)    # unified quantum circuit construction
print(qpanda_circuit)             # print quantum circuit

qpanda_qvm = qpanda.CPUQVM()
qpanda_qvm.run(qpanda_circuit, Nshots)
qpanda_result = qpanda_qvm.result().get_counts()
print(qpanda_result)        # print running results
```

The running results are:
<div align="left">
<img src=../../imgs/ghz_qpanda.jpg width=50% />
</div>

### 6. Run on quafu

```python
print(' ### Run on quafu ### ')

quafu_circuit = quafu.QuantumCircuit(Nqs, Nqs)
ghz_state(quafu_circuit, Nqs)    # unified quantum circuit construction
quafu_circuit.draw_circuit()     # print quantum circuit

quafu_result = quafu.simulate(quafu_circuit, shots = Nshots)
print(quafu_result.counts)    # print running results
```

The running results are:
<div align="left">
<img src=../../imgs/ghz_quafu.jpg width=50% />
</div>