# Modular Construction of Quantum Circuits
**Note: This feature is experimental, has not undergone systematic testing, and its interface may change in the future. Please use it with caution.**

PyQuantumKit provides modular construction functions for quantum circuits, enabling concatenation, parallelization, inversion, qubit remapping, and other operations on quantum circuits. These functions will be translated into the corresponding operations (concatenation, parallelization, inversion, qubit remapping) of quantum circuit objects in the specific quantum development framework. **Therefore, these functions require support from the target quantum framework to be implemented. For unsupported frameworks, it is recommended to use the CircuitIO class to achieve this indirectly, [see here](../stable/circuit.md#iii-circuitio-class) for details.**

PyQuantumKit distinguishes two types of quantum circuits: one is called Circuit, which only contains quantum gates and no measurements; the other is called Program, which can contain measurements and classical bits for storing measurement results in addition to quantum gates. Functions ending with `circuit` apply to Circuit, and functions ending with `program` apply to Program.

## I. Quantum Circuit Operations
### new_circuit
The `new_circuit` function creates a new quantum circuit object on the target quantum development framework.

```python
def new_circuit(framework : str, nqbits : int)
```
- The string parameter `framework` indicates the specific framework name (e.g., `'qiskit'`, `'pyqpanda3'`).
- The integer parameter `nqbits` specifies the number of qubits contained in the quantum circuit.

The function returns a quantum circuit object of the specific quantum development framework (e.g., Qiskit's `QuantumCircuit` object or QPanda3's `QCircuit` object).

### new_program
The `new_program` function creates a new quantum circuit object on the target quantum development framework.

```python
def new_program(framework : str, nqbits : int, ncbits : int = 0)
```
- The string parameter `framework` indicates the specific framework name (e.g., `'qiskit'`, `'pyqpanda3'`).
- The integer parameter `nqbits` specifies the number of qubits contained in the quantum circuit.
- The integer parameter `ncbits` specifies the number of classical bits contained in the quantum circuit.

The function returns a quantum circuit object of the specific quantum development framework (e.g., Qiskit's `QuantumCircuit` object or QPanda3's `QProg` object).

### copy_circuit
The `copy_circuit` function copies the source quantum circuit and returns an additional independent copy of it. Inversion and qubit remapping operations can be performed during the copying process.

```python
def copy_circuit(src_qcir, remap : int|list|range = None, inverse : bool = False)
```
- The parameter `src_qcir` specifies the source quantum circuit.
- The parameter `qbits_remap` specifies the qubit remapping method, which can be passed as an `int` or `list[int]` type, with a default value of `None` (indicating no remapping). When an `int` type is passed, the index of each qubit in the source quantum circuit will be increased by this integer value during concatenation; when a `list[int]` type is passed, remapping will be performed according to the instructions of this array during concatenation.
- The parameter `cbits_remap` specifies the classical bit remapping method, which can be passed as an `int` or `list[int]` type, with a default value of `None` (indicating no remapping). When an `int` type is passed, the index of each classical bit in the source quantum circuit will be increased by this integer value during concatenation; when a `list[int]` type is passed, remapping will be performed according to the instructions of this array during concatenation.

The function returns a new Circuit object.

### copy_program
The `copy_program` function copies the source quantum circuit and returns an additional independent copy of it. Inversion and bit remapping operations can be performed during the copying process.

```python
def copy_program(src_qp, qbits_remap : int|list|range = None, cbits_remap : int|list|range = None)
```
- The parameter `src_qcir` specifies the source quantum circuit.
- The parameter `qbits_remap` specifies the qubit remapping method, which can be passed as an `int` or `list[int]` type, with a default value of `None` (indicating no remapping). When an `int` type is passed, the index of each qubit in the source quantum circuit will be increased by this integer value during concatenation; when a `list[int]` type is passed, remapping will be performed according to the instructions of this array during concatenation.
- The parameter `cbits_remap` specifies the classical bit remapping method, which can be passed as an `int` or `list[int]` type, with a default value of `None` (indicating no remapping). When an `int` type is passed, the index of each classical bit in the source quantum circuit will be increased by this integer value during concatenation; when a `list[int]` type is passed, remapping will be performed according to the instructions of this array during concatenation.

The function returns a new Program object.

### append_circuit
The `append_circuit` function concatenates a source quantum circuit to the end of a target quantum circuit. Inversion and qubit remapping operations can be performed during the concatenation process.

```python
def append_circuit(dest_qcir, src_qcir, remap : int|list|range = None, inverse : bool = False)
```
- The parameter `dest_qcir` specifies the target quantum circuit.
- The parameter `src_qcir` specifies the source quantum circuit.
- The parameter `remap` specifies the qubit remapping method, which can be passed as an `int` or `list[int]` type, with a default value of `None` (indicating no remapping). When an `int` type is passed, the index of each qubit in the source quantum circuit will be increased by this integer value during concatenation; when a `list[int]` type is passed, remapping will be performed according to the instructions of this array during concatenation.
- The parameter `inverse` specifies whether to invert the source quantum circuit during concatenation, with a default value of `False`.

The function returns `dest_qcir`.

### append_program
The `append_program` function concatenates a source quantum circuit to the end of a target quantum circuit. Inversion and bit remapping operations can be performed during the concatenation process.

```python
def append_program(dest_qp, src_qp, qbits_remap : int|list|range = None, cbits_remap : int|list|range = None)
```
- The parameter `dest_qcir` specifies the target quantum circuit.
- The parameter `src_qcir` specifies the source quantum circuit.
- The parameter `qbits_remap` specifies the qubit remapping method, which can be passed as an `int` or `list[int]` type, with a default value of `None` (indicating no remapping). When an `int` type is passed, the index of each qubit in the source quantum circuit will be increased by this integer value during concatenation; when a `list[int]` type is passed, remapping will be performed according to the instructions of this array during concatenation.
- The parameter `cbits_remap` specifies the classical bit remapping method, which can be passed as an `int` or `list[int]` type, with a default value of `None` (indicating no remapping). When an `int` type is passed, the index of each classical bit in the source quantum circuit will be increased by this integer value during concatenation; when a `list[int]` type is passed, remapping will be performed according to the instructions of this array during concatenation.

The function returns `dest_qcir`.

### parallel_circuits
The `parallel_circuits` function parallelizes several source quantum circuits, and qubit remapping will be performed on the source quantum circuits in sequence during the parallelization process.

```python
def parallel_circuits(*args)
```

Example: The following code
```python
import pyquantumkit
qc1 = pyquantumkit.new_circuit('qiskit', 2)
qc2 = pyquantumkit.new_circuit('qiskit', 5)
qc3 = pyquantumkit.new_circuit('qiskit', 3)
parallel_qc = pyquantumkit.parallel_circuits(qc1, qc2, qc3)
```
The returned `parallel_qc` will contain 2+5+3=10 qubits, where `qc1` acts on qubits with indices 0 and 1, `qc2` acts on qubits with indices 2, 3, 4, 5, 6, and `qc3` acts on qubits with indices 7, 8, 9.

### parallel_programs
The `parallel_programs` function parallelizes several source quantum circuits, and qubit and classical bit remapping will be performed on the source quantum circuits in sequence during the parallelization process.

```python
def parallel_programs(*args)
```

## II. Getting the Number of Bits
### get_n_qubits
The `get_n_qubits` function returns the number of qubits of the quantum circuit.
```python
def get_n_qubits(q_prog) -> int
```

### get_qubit_list
The `get_qubit_list` function returns an array of qubit indices used by the quantum circuit.
```python
def get_qubit_list(q_prog) -> list[int]
```

### get_n_cbits
The `get_n_cbits` function returns the number of classical bits of the quantum circuit.
```python
def get_n_cbits(q_prog) -> int
```

### get_cbit_list
The `get_cbit_list` function returns an array of classical bit indices used by the quantum circuit.
```python
def get_cbit_list(q_prog) -> list[int]
```
