# Construction of Quantum Circuits
## I. Basic Construction
### 1. Applying Quantum Gates

In PyquantumKit, the key to constructing quantum circuits in a unified manner is the `apply_gate` function. The following examples illustrate the usage of this function.

**Example 1**. Apply an S gate to the qubit with index 2, the code is written as:
```python
apply_gate(circuit, 'S', [2])
```
**Detailed Explanation**

- `circuit` is an object of the quantum circuit class in a supported quantum development framework (e.g., `QuantumCircuit` of qiskit, `QCircuit` or `QProg` of pyqpanda3, `QuantumCircuit` of quafu, or `Circuit` of cqlib).
- The string `'S'` indicates that an S gate is to be applied. [Click here](../api/supported-gates.md) to view the strings corresponding to specific quantum gates.
- The array `[2]` indicates the indices of the qubits to which the quantum gate is applied. The number of elements in the array should be the same as the number of bits of the gate. Note that whether the quantum gate is single-bit or multi-bit, this parameter must be assigned **in the form of a list**.

**Example 2**. Apply a Toffoli gate to the qubits with indices 0, 2, and 3:
```python
apply_gate(circuit, 'CCNOT', [0, 2, 3])
```

**Example 3**. Apply an $R_x$ gate to the qubit with index 1, with parameter $\theta=0.1$:
```python
apply_gate(circuit, 'Rx', [1], [0.1])
```

- The fourth parameter `[0.1]` is used to indicate the parameters of the quantum gate. For parameterless gates, this parameter is omitted.

**Example 4**. Apply a $U_3$ gate to the qubit with index 0, with parameters $\theta=0.2,\phi=0.3,\lambda=0.4$:
```python
apply_gate(circuit, 'U3', [0], [0.2, 0.3, 0.4])
```

The above gives 4 usage examples of the `apply_gate` function. **For a more detailed explanation of this function, please [click here](../api/construct.md#apply_gate).**

### 2. Applying Measurements

In PyquantumKit, the `apply_measure` function can measure one or a set of qubits and write the results into specified classical bits.

**Example 5**. Measure the qubit with index 2 and store the result in the classical bit with index 0:
```python
apply_measure(circuit, [2], [0])
```

**Example 6**. Measure the qubits with indices 0~4 (a total of 5 qubits) and store the results in the classical bits with indices 0~4. There are two ways to write the code: the first is to specify the index corresponding to each bit using an array:
```python
apply_measure(circuit, [0, 1, 2, 3, 4], [0, 1, 2, 3, 4])
```
The second is to specify the index range using the `range` function:
```python
apply_measure(circuit, range(5), range(5))
```

## II. Modular Construction of Quantum Circuits (Experimental)

- **Note 1: The content of this section may only apply to some quantum development frameworks**, [click here for details](../api/supported-platforms.md).
- **Note 2: This feature is experimental, has not undergone systematic testing, and the interface may change in the future. Please use it with caution.**
- **Note 3: If modular construction is required currently, it is recommended to use the CircuitIO class (see below)**

[Click here](../experimental/construct.md) to view the specific content of modular construction of quantum circuits.

## III. CircuitIO Class
PyQuantumKit provides a CircuitIO class for temporarily storing constructed quantum circuits. The CircuitIO class can be used like a quantum circuit class of a quantum development framework, and operations such as `apply_gate` and `apply_measure` can also be performed on it. The CircuitIO object saves the information of the quantum circuit, which can then be formatted and output as a code string or inserted into the quantum circuit object of a specific quantum development framework.

**Example 7**. The following code defines a CircuitIO object containing 2 qubits and 2 classical bits, on which a quantum circuit for preparing a Bell state is constructed:

```python
import pyquantumkit

cio = pyquantumkit.CircuitIO(2, 2)        # define a CircuitIO object
pyquantumkit.apply_gate(cio, 'H', [0])    # Use generic function <gate_apply>
cio.apply_gate('CX', [0, 1])              # Use CircuitIO member function <gate_apply>
```

To apply a quantum gate on a CircuitIO object, you can directly use the general `apply_gate` function, passing the CircuitIO object as the quantum circuit object; or you can use the homonymous member function `CircuitIO.apply_gate` provided by the CircuitIO class.

**For a detailed explanation of the member functions included in the CircuitIO class, please [click here](../api/circuitio.md).** The following gives three typical usages of the CircuitIO class.

### 1. Using the CircuitIO Class for Modular Construction of Quantum Circuits on Unsupported Quantum Development Platforms

Some quantum development frameworks do not support modular construction functions of quantum circuits such as *automatic generation of inverse circuits* and *remapping of qubits*. In this case, the CircuitIO object can be used to complete the construction indirectly: first construct the circuit on the CircuitIO object and generate the inverse circuit or remap (using the `inverse`, `remap_qbits`, and `remap_cbits` member functions), then use the `>>` operator (or equivalently, the `append_into_actual_circuit` member function) to insert the quantum circuit contained in the CircuitIO into the quantum circuit of a specific quantum development framework.

**Example 8**. The Quafu framework does not support qubit remapping and automatic generation of inverse circuits. The following code indirectly implements this by using a CircuitIO object. We define a CircuitIO object, perform qubit remapping and conversion to an inverse circuit on it, and finally output the circuit on the CircuitIO object to the Quafu framework.

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

### 2. Exporting Code Using the CircuitIO Class

The `get_circuit_code` function of the CircuitIO class can be used to convert a quantum circuit into code for supported frameworks or languages ([click here](../api/supported-platforms.md) for supported frameworks and languages). The output of the function is a string that can be copied into the source code file.

**Example 9**. Construct a GHZ state using the CircuitIO class and export it as qiskit code and Microsoft Q# code.

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

The output results are:
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

### 3. Symbolic Representation and Operation Using the CircuitIO Class
PyQuantumKit supports symbolic representation of quantum circuit matrices (implemented based on SymPy). When constructing a quantum circuit on a CircuitIO object, for quantum gates with parameters, their parameters can use SymPy symbolic variables or expressions in addition to numerical values (`int` and `float` types). Moreover, when outputting the quantum circuit to a specific development framework, the SymPy variables can be assigned values and converted into numerical types supported by these development frameworks.

**Example 10**. Apply an $R_{xx}(\alpha+\beta)$ gate using a CircuitIO object, where $\alpha$ and $\beta$ are represented as symbolic variables. Then substitute the values $\alpha=0.5$ and $\beta=0.7$, and output the quantum circuit to the quafu framework.

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
cio.append_into_actual_circuit(qpanda_circuit, {alpha_ : 0.5, beta_ : 0.7})
```

For more detailed content on how to use PyQuantumKit for symbolic representation and operation, please [click here](./symbol.md).
