# Construction of Quantum Circuits
## 1. Basic Construction
### 1. Applying quantum gates

In PyQuantumKit, the key to constructing quantum circuits in a unified way is the `apply_gate` function. Below we use several examples to illustrate the usage of the function.

**Example 1**. Apply an S gate on the qubit with index 2, written as:
```python
apply_gate(circuit, 'S', [2])
```
**Detailed explanation**

- `circuit` is an object of the quantum circuit class in a supported quantum development framework (for example qiskit's `QuantumCircuit`, pyqpanda3's `QCircuit` or `QProg`, quafu's `QuantumCircuit`, or cqlib's `Circuit`).
- The string `'S'` indicates that an S gate is applied. [Click here](./api/supported-gates.md) for the specific strings corresponding to each quantum gate.
- The array `[2]` indicates the index on which the quantum gate is applied; the number of array elements should be the same as the number of bits of the gate. Note that regardless of whether the quantum gate is single-bit or multi-bit, **this parameter needs to be assigned in the form of a list**.

**Example 2**. Apply a Toffoli gate on the qubits with indices 0, 2, and 3:
```python
apply_gate(circuit, 'CCNOT', [0, 2, 3])
```

**Example 3**. Apply an $R_x$ gate on the qubit with index 1, with parameter $\theta=0.1$:
```python
apply_gate(circuit, 'Rx', [1], [0.1])
```

- The fourth parameter `[0.1]` is used to indicate the parameters of the quantum gate; for a parameterless gate, this parameter is omitted.

**Example 4**. Apply a $U_3$ gate on the qubit with index 0, with parameters $\theta=0.2,\phi=0.3,\lambda=0.4$:
```python
apply_gate(circuit, 'U3', [0], [0.2, 0.3, 0.4])
```

The above gives four usage examples of the `apply_gate` function. **For a more detailed explanation of this function, please [click here](./api/construct.md#apply_gate).**

### 2. Applying measurements

In PyQuantumKit, the `apply_measure` function can measure one or a group of qubits and write the results into the specified classical bits.

**Example 5**. Measure the qubit with index 2 and store the result in the classical bit with index 0:
```python
apply_measure(circuit, [2], [0])
```

**Example 6**. Measure the qubits with indices 0 through 4 (5 in total), and store the results in the classical bits with indices 0 through 4. There are two ways to write the code; the first is to use arrays to specify the index corresponding to each bit:
```python
apply_measure(circuit, [0, 1, 2, 3, 4], [0, 1, 2, 3, 4])
```
The second is to use the `range` function to specify the index range:
```python
apply_measure(circuit, range(5), range(5))
```

## 2. Quantum Subroutines (Experimental)
In addition to quantum gates, some quantum development frameworks also provide reusable building blocks (blocks) for commonly used quantum circuit modules, such as multi-bit controlled gates, the Quantum Fourier Transform (QFT), and so on. Users can directly use these building blocks to avoid repeatedly writing quantum circuits. In order to allow the cross-platform quantum programs written by users to fully utilize these features of the target platform, PyQuantumKit v0.2.1 introduces the concept of quantum subroutines to express reusable quantum circuit building blocks. In terms of programming logic level, it is higher than quantum gates and lower than high-level-language quantum programs.

Users can use the `apply_subroutine` function to apply a quantum subroutine in a unified way; the parameters of this function are the same as `apply_gate`. **For a more detailed explanation of this function, please [click here](./api/construct.md#apply_subroutine).**

**Example 7**. The following code applies the Quantum Fourier Transform (QFT) operation to the 5 qubits with indices 0 through 4:
```python
apply_subroutine(circuit, 'QFT', range(5))
```

**Example 8**. The following code applies the inverse Quantum Fourier Transform (Inverse QFT) operation to the 4 qubits with indices 1, 3, 5, 7:
```python
apply_subroutine(circuit, 'IQFT', [1, 3, 5, 7])
```

It can be seen that the application of a quantum subroutine is similar to a quantum gate. In fact, in PyQuantumKit, a quantum subroutine and a quantum gate have both similarities and some differences.

**Similarities**

- The `apply_subroutine` function and the `apply_gate` function accept the same parameter types: the first parameter is the object of the quantum circuit class in the quantum development framework, the second parameter is the string indicating which subroutine or gate to apply, the third parameter is the array of qubit indices to apply to, and the fourth parameter (optional) is the parameter list of the subroutine or gate.

**Differences**

- The number of qubits a quantum subroutine acts on can be variable, while the number of qubits a quantum gate acts on is fixed (1 to 3 qubits).
- PyQuantumKit guarantees that all quantum gates supported by PyQuantumKit can be correctly translated to the target platform; if the target platform does not support a certain quantum gate, PyQuantumKit translates it into an equivalent combination of supported gates. In contrast, for the translation of quantum subroutines, **if the target platform does not support a certain subroutine, PyQuantumKit directly reports an "unsupported" error**, and does not perform equivalence transformations for compatibility.

## 3. The CircuitIO class
PyQuantumKit provides a CircuitIO class for temporarily storing the constructed quantum circuit. The CircuitIO class can be used like the quantum circuit class of a quantum development framework, and operations such as `apply_gate` and `apply_measure` can also be performed on it. A CircuitIO object saves the information of the quantum circuit, and can subsequently be formatted and output as a code string or inserted into the quantum circuit object of a specific quantum development framework.

**Example 7**. The following code defines a CircuitIO object containing 2 qubits and 2 classical bits, on which a quantum circuit that prepares a Bell state is constructed:

```python
import pyquantumkit

cio = pyquantumkit.CircuitIO(2, 2)        # define a CircuitIO object
pyquantumkit.apply_gate(cio, 'H', [0])    # Use generic function <gate_apply>
cio.apply_gate('CX', [0, 1])              # Use CircuitIO member function <gate_apply>
```

To apply a quantum gate on a CircuitIO object, you can directly use the generic `apply_gate` function, passing the CircuitIO object as the quantum circuit object; or you can use the member function `CircuitIO.apply_gate` of the same name provided by the CircuitIO class.

**For a detailed explanation of the member functions contained in the CircuitIO class, please [click here](./api/circuitio.md).** Below are three typical usages of the CircuitIO class.

### 1. Use the CircuitIO class for modular construction of quantum circuits on unsupported quantum development platforms

Some quantum development frameworks do not support modular circuit construction features such as *automatically generating the inverse circuit* and *qubit remapping*. In this case, the construction can be completed indirectly using a CircuitIO object: first construct the circuit on the CircuitIO object and generate the inverse circuit or remapping (using the `inverse`, `remap_qbits`, and `remap_cbits` member functions), then use the `>>` operator (or equivalently, the `append_into_actual_circuit` member function) to insert the quantum circuit contained in the CircuitIO into the quantum circuit of the specific quantum development framework.

**Example 8**. The Quafu framework does not support qubit remapping and automatic generation of inverse circuits. The following code implements these indirectly by using a CircuitIO object. We define a CircuitIO object, perform qubit remapping and conversion to the inverse circuit on it, and finally output the circuit on the CircuitIO object to the Quafu framework.

```python
import quafu
import pyquantumkit

cio = pyquantumkit.CircuitIO(2, 2)
pyquantumkit.apply_gate(cio, 'H', [0])
cio.apply_gate('CX', [0, 1])

cio.inverse()              # inverse the circuit in CircuitIO object cio
cio.remap_qbits([1, 0])    # remap the circuit in cio

quafu_circuit = quafu.QuantumCircuit(2, 2)
cio >> quafu_circuit       # insert the CircuitIO object cio into quafu's circuit
```

### 2. Use the CircuitIO class to export code

The `get_circuit_code` function of the CircuitIO class can be used to convert a quantum circuit into code of a supported framework or language ([click here](./api/supported-platforms.md) for the supported frameworks and languages). The output of the function is a string that can be copied into a source code file.

**Example 9**. Use the CircuitIO class to construct a circuit that generates a GHZ state, and export it as qiskit code and Microsoft Q# code.

```python
# import PyQuantumKit
import pyquantumkit as PQK

# Define the unified quantum circuit construction function using PyQuantumKit
def ghz_state(circuit, nqbits : int):
    PQK.apply_gate(circuit, 'H', [0])               # Apply H gate on qubit with index 0
    for i in range(1, nqbits):
        PQK.apply_gate(circuit, 'cnot', [0, i])     # Apply CNOT gate on qubit with index 0 and i

Nqs = 5     # Set the numnber of qubits
cio = PQK.CircuitIO(Nqs)
ghz_state(cio, Nqs)     # Construct circuits on CircuitIO object

qiskit_code = cio.get_circuit_code('qiskit', 'qc')     # Output the circuit into qiskit code
print(qiskit_code)

qsharp_code = cio.get_circuit_code('QSharp', 'qs')     # Output the circuit into Q# code
print(qsharp_code)
```

The output result is:
```python
qc.h(0)
qc.cx(0, 1)
qc.cx(0, 2)
qc.cx(0, 3)
qc.cx(0, 4)
```
```csharp
H(qs[0]);
CNOT(qs[0], qs[1]);
CNOT(qs[0], qs[2]);
CNOT(qs[0], qs[3]);
CNOT(qs[0], qs[4]);
```

### 3. Use the CircuitIO class for symbolic representation and computation
PyQuantumKit supports the symbolic representation of quantum circuit matrices (implemented based on SymPy). When constructing a quantum circuit on a CircuitIO object, for parameterized quantum gates, in addition to numeric values (of type `int` and `float`), their parameters also support the use of SymPy symbolic variables or expressions. Moreover, when outputting the quantum circuit to a specific development framework, values can be assigned to the SymPy variables to convert them into numeric types supported by those development frameworks.

**Example 10**. Use a CircuitIO object to apply an $R_{xx}(\alpha+\beta)$ gate, where $\alpha$ and $\beta$ are represented as symbolic variables. Then, after substituting the numeric values $\alpha=0.5$ and $\beta=0.7$, output the quantum circuit to the quafu framework.

```python
import quafu
import pyquantumkit
import sympy

alpha_ = sympy.Symbol('alpha')
beta_ = sympy.Symbol('theta')

cio = PQK.CircuitIO(3)
cio.apply_gate('Rxx', [1, 2], [alpha_ + beta_])     # Use SymPy symbol expression as the parameter

# Insert the CircuitIO object cio into quafu's circuit, assigning alpha_ = 0.5, beta_ = 0.7
quafu_circuit = quafu.QuantumCircuit(3, 3)
cio.append_into_actual_circuit(quafu_circuit, {alpha_ : 0.5, beta_ : 0.7})
```

For more detailed content on how to use PyQuantumKit for symbolic representation and computation, please [click here](./symbol.md).