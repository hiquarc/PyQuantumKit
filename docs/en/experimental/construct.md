# Modular Construction of Quantum Circuits
**Note: This feature is experimental, has not been systematically tested, and its interface may change in the future. Please use it with caution.**

PyQuantumKit provides functions for modular construction of quantum circuits, implementing features such as concatenation, parallel combination, inversion and bit remapping of quantum circuits. On a specific quantum development framework, these functions will be translated into the concatenation, parallel combination, inversion and bit remapping of the quantum circuit objects of the corresponding framework. **Therefore these features can only be realized if the target quantum framework supports them. For unsupported frameworks, it is recommended to implement them indirectly using the CircuitIO class; [click here](../circuit-level/circuit.md#circuitio) for details.**

PyQuantumKit distinguishes two types of quantum circuits: one is called a Circuit, which contains only quantum gates and no measurement; the other is called a Program, which, besides quantum gates, may also contain measurement and the classical bits that store the measurement results. Functions ending in `circuit` apply to a Circuit, and functions ending in `program` apply to a Program.

## I. Quantum Circuit Operations
### new_circuit
The `new_circuit` function creates a new quantum circuit object on the target quantum development framework.

```python
def new_circuit(framework : str, nqbits : int)
```

- The string parameter `framework` indicates the specific framework name (for example `'qiskit'`, `'pyqpanda3'`).
- The integer parameter `nqbits` specifies the number of qubits contained in the quantum circuit.

The function returns a quantum circuit object of the specific quantum development framework (for example a Qiskit `QuantumCircuit` object or a QPanda3 `QCircuit` object).

### new_program
The `new_program` function creates a new quantum circuit object on the target quantum development framework.

```python
def new_program(framework : str, nqbits : int, ncbits : int = 0)
```

- The string parameter `framework` indicates the specific framework name (for example `'qiskit'`, `'pyqpanda3'`).
- The integer parameter `nqbits` specifies the number of qubits contained in the quantum circuit.
- The integer parameter `ncbits` specifies the number of classical bits contained in the quantum circuit.

The function returns a quantum circuit object of the specific quantum development framework (for example a Qiskit `QuantumCircuit` object or a QPanda3 `QProg` object).

### copy_circuit
The `copy_circuit` function copies the source quantum circuit and returns an additional independent copy of it; during the copy, inversion and bit remapping operations can be performed.

```python
def copy_circuit(src_qcir, remap : int|list|range = None, inverse : bool = False)
```

- The parameter `src_qcir` specifies the source quantum circuit.
- The parameter `qbits_remap` specifies the remapping method of the qubits. The type passed in can be `int` or `list[int]`; the default is `None`, indicating no remapping. When an `int` type is passed in, the index of each qubit of the source quantum circuit is increased by this integer value when concatenated; when a `list[int]` type is passed in, remapping is performed according to the indication of this array when concatenated.
- The parameter `cbits_remap` specifies the remapping method of the classical bits. The type passed in can be `int` or `list[int]`; the default is `None`, indicating no remapping. When an `int` type is passed in, the index of each classical bit of the source quantum circuit is increased by this integer value when concatenated; when a `list[int]` type is passed in, remapping is performed according to the indication of this array when concatenated.

The function returns a new Circuit object.

### copy_program
The `copy_program` function copies the source quantum circuit and returns an additional independent copy of it; during the copy, inversion and bit remapping operations can be performed.

```python
def copy_program(src_qp, qbits_remap : int|list|range = None, cbits_remap : int|list|range = None)
```

- The parameter `src_qcir` specifies the source quantum circuit.
- The parameter `qbits_remap` specifies the remapping method of the qubits. The type passed in can be `int` or `list[int]`; the default is `None`, indicating no remapping. When an `int` type is passed in, the index of each qubit of the source quantum circuit is increased by this integer value when concatenated; when a `list[int]` type is passed in, remapping is performed according to the indication of this array when concatenated.
- The parameter `cbits_remap` specifies the remapping method of the classical bits. The type passed in can be `int` or `list[int]`; the default is `None`, indicating no remapping. When an `int` type is passed in, the index of each classical bit of the source quantum circuit is increased by this integer value when concatenated; when a `list[int]` type is passed in, remapping is performed according to the indication of this array when concatenated.

The function returns a new Program object.

### append_circuit
The `append_circuit` function concatenates a source quantum circuit to the end of the target quantum circuit; during the concatenation, inversion and bit remapping operations can be performed.

```python
def append_circuit(dest_qcir, src_qcir, remap : int|list|range = None, inverse : bool = False)
```

- The parameter `dest_qcir` specifies the target quantum circuit.
- The parameter `src_qcir` specifies the source quantum circuit.
- The parameter `remap` specifies the remapping method of the qubits. The type passed in can be `int` or `list[int]`; the default is `None`, indicating no remapping. When an `int` type is passed in, the index of each qubit of the source quantum circuit is increased by this integer value when concatenated; when a `list[int]` type is passed in, remapping is performed according to the indication of this array when concatenated.
- The parameter `inverse` specifies whether to invert the source quantum circuit during concatenation; the default is `False`.

The function returns `dest_qcir`.

### append_program
The `append_program` function concatenates a source quantum circuit to the end of the target quantum circuit; during the concatenation, inversion and bit remapping operations can be performed.

```python
def append_program(dest_qp, src_qp, qbits_remap : int|list|range = None, cbits_remap : int|list|range = None)
```

- The parameter `dest_qcir` specifies the target quantum circuit.
- The parameter `src_qcir` specifies the source quantum circuit.
- The parameter `qbits_remap` specifies the remapping method of the qubits. The type passed in can be `int` or `list[int]`; the default is `None`, indicating no remapping. When an `int` type is passed in, the index of each qubit of the source quantum circuit is increased by this integer value when concatenated; when a `list[int]` type is passed in, remapping is performed according to the indication of this array when concatenated.
- The parameter `cbits_remap` specifies the remapping method of the classical bits. The type passed in can be `int` or `list[int]`; the default is `None`, indicating no remapping. When an `int` type is passed in, the index of each classical bit of the source quantum circuit is increased by this integer value when concatenated; when a `list[int]` type is passed in, remapping is performed according to the indication of this array when concatenated.

The function returns `dest_qcir`.

### parallel_circuits
The `parallel_circuits` function combines several source quantum circuits in parallel; during the parallel combination, qubit remapping is performed on the source quantum circuits in order.

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
the returned `parallel_qc` will contain 2+5+3=10 qubits, in which `qc1` acts on the qubits with indices 0, 1, `qc2` acts on the qubits with indices 2, 3, 4, 5, 6, and `qc3` acts on the qubits with indices 7, 8, 9.

### parallel_programs
The `parallel_programs` function combines several source quantum circuits in parallel; during the parallel combination, qubit and classical bit remapping is performed on the source quantum circuits in order.

```python
def parallel_programs(*args)
```

## II. Obtaining the Number of Bits
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
