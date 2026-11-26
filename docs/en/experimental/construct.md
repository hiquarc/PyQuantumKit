# Modular Construction of Quantum Circuits
**Note: This feature is experimental, has not been systematically tested, and its interface may change in the future. Please use it with caution.**

PyQuantumKit provides modular construction functions for quantum circuits, implementing functions such as concatenation, parallelization, inversion, and bit remapping of quantum circuits. On specific quantum development frameworks, these functions will be translated into the corresponding concatenation, parallelization, inversion, and bit remapping of the quantum circuit objects of the framework. **Therefore, these functions require the target quantum framework to support them. For unsupported frameworks, it is recommended to use the CircuitIO class to implement them indirectly; [click here](../circuit-level/circuit.md#circuitio) for details.**

PyQuantumKit distinguishes two kinds of quantum circuits: one is called Circuit, which contains only quantum gates and no measurements; the other is called Program, which, in addition to quantum gates, can also contain measurements and the classical bits storing the measurement results. Functions ending in `circuit` apply to Circuit, and functions ending in `program` apply to Program.

## 1. Quantum circuit operations
### new_circuit
The `new_circuit` function creates a new quantum circuit object on the target quantum development framework.

```python
def new_circuit(framework : str, nqbits : int)
```

- The string parameter `framework` indicates the specific framework name (for example `'qiskit'`, `'pyqpanda3'`).
- The integer parameter `nqbits` assigns the number of qubits contained in the quantum circuit.

The function returns the quantum circuit object of the specific quantum development framework (for example Qiskit's `QuantumCircuit` object or QPanda3's `QCircuit` object).

### new_program
The `new_program` function creates a new quantum circuit object on the target quantum development framework.

```python
def new_program(framework : str, nqbits : int, ncbits : int = 0)
```

- The string parameter `framework` indicates the specific framework name (for example `'qiskit'`, `'pyqpanda3'`).
- The integer parameter `nqbits` assigns the number of qubits contained in the quantum circuit.
- The integer parameter `ncbits` assigns the number of classical bits contained in the quantum circuit.

The function returns the quantum circuit object of the specific quantum development framework (for example Qiskit's `QuantumCircuit` object or QPanda3's `QProg` object).

### copy_circuit
The `copy_circuit` function copies the source quantum circuit and returns an additional independent copy of it, during which inversion and bit remapping operations can be performed.

```python
def copy_circuit(src_qcir, remap : int|list|range = None, inverse : bool = False)
```

- The parameter `src_qcir` assigns the source quantum circuit.
- The parameter `remap` assigns the remapping method for the qubits. The type passed can be `int` or `list[int]`, and defaults to `None`, meaning no remapping is performed. When an `int` type is passed, the index of each qubit of the source quantum circuit is increased by this integer value when concatenated; when a `list[int]` type is passed, remapping is performed according to the instructions of this array when concatenated.
- The parameter `inverse` assigns whether to invert the source quantum circuit, and defaults to `False`.

The function returns a new Circuit object.

### copy_program
The `copy_program` function copies the source quantum circuit and returns an additional independent copy of it, during which inversion and bit remapping operations can be performed.

```python
def copy_program(src_qp, qbits_remap : int|list|range = None, cbits_remap : int|list|range = None)
```

- The parameter `src_qp` assigns the source quantum circuit.
- The parameter `qbits_remap` assigns the remapping method for the qubits. The type passed can be `int` or `list[int]`, and defaults to `None`, meaning no remapping is performed. When an `int` type is passed, the index of each qubit of the source quantum circuit is increased by this integer value when concatenated; when a `list[int]` type is passed, remapping is performed according to the instructions of this array when concatenated.
- The parameter `cbits_remap` assigns the remapping method for the classical bits. The type passed can be `int` or `list[int]`, and defaults to `None`, meaning no remapping is performed. When an `int` type is passed, the index of each classical bit of the source quantum circuit is increased by this integer value when concatenated; when a `list[int]` type is passed, remapping is performed according to the instructions of this array when concatenated.

The function returns a new Program object.

### append_circuit
The `append_circuit` function concatenates a source quantum circuit to the end of a target quantum circuit, during which inversion and bit remapping operations can be performed.

```python
def append_circuit(dest_qcir, src_qcir, remap : int|list|range = None, inverse : bool = False)
```

- The parameter `dest_qcir` assigns the target quantum circuit.
- The parameter `src_qcir` assigns the source quantum circuit.
- The parameter `remap` assigns the remapping method for the qubits. The type passed can be `int` or `list[int]`, and defaults to `None`, meaning no remapping is performed. When an `int` type is passed, the index of each qubit of the source quantum circuit is increased by this integer value when concatenated; when a `list[int]` type is passed, remapping is performed according to the instructions of this array when concatenated.
- The parameter `inverse` assigns whether to invert the source quantum circuit during concatenation, and defaults to `False`.

The function returns `dest_qcir`.

### append_program
The `append_program` function concatenates a source quantum circuit to the end of a target quantum circuit, during which inversion and bit remapping operations can be performed.

```python
def append_program(dest_qp, src_qp, qbits_remap : int|list|range = None, cbits_remap : int|list|range = None)
```

- The parameter `dest_qp` assigns the target quantum circuit.
- The parameter `src_qp` assigns the source quantum circuit.
- The parameter `qbits_remap` assigns the remapping method for the qubits. The type passed can be `int` or `list[int]`, and defaults to `None`, meaning no remapping is performed. When an `int` type is passed, the index of each qubit of the source quantum circuit is increased by this integer value when concatenated; when a `list[int]` type is passed, remapping is performed according to the instructions of this array when concatenated.
- The parameter `cbits_remap` assigns the remapping method for the classical bits. The type passed can be `int` or `list[int]`, and defaults to `None`, meaning no remapping is performed. When an `int` type is passed, the index of each classical bit of the source quantum circuit is increased by this integer value when concatenated; when a `list[int]` type is passed, remapping is performed according to the instructions of this array when concatenated.

The function returns `dest_qp`.

### parallel_circuits
The `parallel_circuits` function connects several source quantum circuits in parallel, during which the source quantum circuits are remapped for qubits in order.

```python
def parallel_circuits(*args)
```

Example: the following code
```python
import pyquantumkit
qc1 = pyquantumkit.new_circuit('qiskit', 2)
qc2 = pyquantumkit.new_circuit('qiskit', 5)
qc3 = pyquantumkit.new_circuit('qiskit', 3)
parallel_qc = pyquantumkit.parallel_circuits(qc1, qc2, qc3)
```
The returned `parallel_qc` will contain 2+5+3=10 qubits, where `qc1` acts on the qubits with indices 0, 1, `qc2` acts on the qubits with indices 2, 3, 4, 5, 6, and `qc3` acts on the qubits with indices 7, 8, 9.

### parallel_programs
The `parallel_programs` function connects several source quantum circuits in parallel, during which the source quantum circuits are remapped for qubits and classical bits in order.

```python
def parallel_programs(*args)
```

## 2. Obtaining the number of bits
### get_n_qubits
The `get_n_qubits` function returns the number of qubits of the quantum circuit.
```python
def get_n_qubits(q_prog) -> int
```

### get_qubit_list
The `get_qubit_list` function returns the array of qubit indices used by the quantum circuit.
```python
def get_qubit_list(q_prog) -> list[int]
```

### get_n_cbits
The `get_n_cbits` function returns the number of classical bits of the quantum circuit.
```python
def get_n_cbits(q_prog) -> int
```

### get_cbit_list
The `get_cbit_list` function returns the array of classical bit indices used by the quantum circuit.
```python
def get_cbit_list(q_prog) -> list[int]
```