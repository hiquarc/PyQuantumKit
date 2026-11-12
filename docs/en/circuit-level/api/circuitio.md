# CircuitIO Class Member Functions Quick Reference
This page gives the member functions of the CircuitIO class, for users to consult.

## 1. Initialization and Number of Bits
### Initialization __init__
When defining a CircuitIO object, its initialization method (constructor) `__init__` is called. The function prototype is:

```python
def __init__(self, nqbits : int = 0, ncbits : int = 0) -> None
```

- The parameter `nqbits` specifies the number of qubits contained in the CircuitIO object; the default is 0.
- The parameter `ncbits` specifies the number of classical bits contained in the CircuitIO object; the default is 0.

**Note: The two parameters "number of qubits" and "number of classical bits" of the CircuitIO class are only used as hints (for example, when concatenating two quantum circuits in parallel), and when applying quantum gates, no check is performed on whether the indices overflow.**

### set_nqbits
The `set_nqbits` function sets the number of qubits of the CircuitIO object. The function prototype is:

```python
def set_nqbits(self, nqbits) -> None
```

- The parameter `nqbits` specifies the number of qubits to be set.

### set_ncbits
The `set_ncbits` function sets the number of classical bits of the CircuitIO object. The function prototype is:

```python
def set_ncbits(self, ncbits) -> None
```

- The parameter `ncbits` specifies the number of qubits to be set.

### get_nqbits
The `get_nqbits` function returns the number of qubits of the CircuitIO object. The function prototype is:

```python
def get_nqbits(self) -> int
```

### get_ncbits
The `get_ncbits` function returns the number of classical bits of the CircuitIO object. The function prototype is:

```python
def get_ncbits(self) -> int
```

## 2. Applying Quantum Gates
### apply_gate
The `apply_gate` member function of the CircuitIO class is similar to the global `apply_gate` function and can apply quantum gates on the quantum circuit of a CircuitIO object.

```python
def apply_gate(self, gatestr : str, qbits : list[int], paras : list = None) -> None
```

- The parameter `gate_str` is a string used to indicate the gate to be applied. Considering that the same gate may have multiple different names (for example Toffoli, CCNOT and CCX all denote the same gate), PyQuantumKit allows the same gate to be represented by different name strings, and is case-insensitive. [Click here](supported-gates.md) for the specific supported quantum gates and their corresponding strings.
- The parameter `qbits` is a list of integers, specifying the list of qubit indices on which the gate is to be applied. Note that regardless of whether the quantum gate is single-qubit or multi-qubit, this parameter must **be specified as a list**.
- The parameter `paras` is a list used to assign parameters to parameterized gates; for parameter-free gates, this parameter does not need to be assigned.

For a CircuitIO object `CircuitIO_Obj`, using the `apply_gate` member function:
```python
CircuitIO_Obj.apply_gate('H', [2])
```
can be equivalently replaced by the global `apply_gate` function, as long as the CircuitIO object is passed in as the parameter representing the quantum circuit:
```python
apply_gate(CircuitIO_Obj, 'H', [2])
```

### apply_measure
The `apply_measure` member function of the CircuitIO class is similar to the global `apply_measure` function and can apply a measurement operation on the quantum circuit of a CircuitIO object.

```python
def apply_measure(self, qindex : list[int], cindex : list[int]) -> None
```

- The parameter `qindex` is a list of integers, specifying the indices of the qubits to be measured.
- The parameter `cindex` is a list of integers, specifying the indices of the classical bits where the measurement results are stored. The components of `qindex` and `cindex` correspond to each other respectively, so `qindex` and `cindex` should have the same length.

For a CircuitIO object `CircuitIO_Obj`, using the `apply_measure` member function:
```python
CircuitIO_Obj.apply_measure([0, 1, 2], [0, 1, 2])
```
can be equivalently replaced by the global `apply_measure` function, as long as the CircuitIO object is passed in as the parameter representing the quantum circuit:
```python
apply_measure(CircuitIO_Obj, [0, 1, 2], [0, 1, 2])
```

## 3. Modular Construction
### inverse
The `inverse` function reverses the quantum circuit in the current CircuitIO object into an inverse circuit (in-place operation).

```python
def inverse(self)
```

### remap_qbits
The `remap_qbits` function remaps the indices of the qubits in the current CircuitIO object (in-place operation).

```python
def remap_qbits(self, remap : int|list|range)
```

- The parameter `remap` specifies the remapping method of the qubits. The type passed in can be `int` or `list[int]`; the default is `None`, indicating no remapping. When an `int` type is passed in, the index of each qubit of the source quantum circuit is increased by this integer value when concatenated; when a `list[int]` type is passed in, remapping is performed according to the indication of this array when concatenated.

### remap_cbits
The `remap_cbits` function remaps the indices of the classical bits in the current CircuitIO object (in-place operation).

```python
def remap_cbits(self, remap : int|list|range)
```

- The parameter `remap` specifies the remapping method of the classical bits. The type passed in can be `int` or `list[int]`; the default is `None`, indicating no remapping. When an `int` type is passed in, the index of each classical bit of the source quantum circuit is increased by this integer value when concatenated; when a `list[int]` type is passed in, remapping is performed according to the indication of this array when concatenated.

### append_circuit_io
The `append_circuit_io` function concatenates the quantum circuit of another CircuitIO object to the end of the quantum circuit of this object.

```python
def append_circuit_io(self, cir_io_obj)
```

- The parameter `cir_io_obj` specifies the source quantum circuit.

### << operator
The `append_circuit_io` function can be replaced by the `<<` operator.

```python
def __lshift__(self, cir_io_obj)
```

For example, in the following code
```python
import pyquantumkit
cio1 = pyquantumkit.CircuitIO(3)
cio2 = pyquantumkit.CircuitIO(3)
# ... construct circuit code ...
cio1.append_circuit_io(cio2)
```
the last line

`cio1.append_circuit_io(cio2)`

concatenates the quantum circuit in `cio2` to the end of `cio1`. This line can be equivalently replaced by:

`cio1 << cio2`


## 4. Property Checking
### contains_measure
`contains_measure` checks whether the CircuitIO object contains a measurement operation; if so, it returns `True`.

```python
def contains_measure(self) -> bool
```

### check_nqbits
The `check_nqbits` function checks whether any index overflow occurs in the quantum gate operations in the CircuitIO object, that is, whether a qubit index exceeding the number of qubits is used.

```python
def check_nqbits(self, adjust : bool = False) -> bool
```

- The parameter `adjust` specifies whether to automatically adjust the number of qubits to accommodate the indices of the quantum gate operations therein when the check finds index overflow. The default is `False`, that is, never adjust.

If there is no index overflow, `True` is returned; otherwise `False` is returned, and if the `adjust` parameter is `True`, the number of qubits is automatically adjusted.

### check_ncbits
The `check_ncbits` function checks whether any index overflow occurs in the classical bits of the measurement operations in the CircuitIO object, that is, whether a classical bit index exceeding the number of classical bits is used.

```python
def check_ncbits(self, adjust : bool = False) -> bool
```

- The parameter `adjust` specifies whether to automatically adjust the number of classical bits to accommodate the indices of the measurement operations therein when the check finds index overflow. The default is `False`, that is, never adjust.

If there is no index overflow, `True` is returned; otherwise `False` is returned, and if the `adjust` parameter is `True`, the number of classical bits is automatically adjusted.

## 5. Matrix Symbolic Representation
### get_sympy_matrix
The `get_sympy_matrix` function computes the matrix representation corresponding to the quantum circuit in the CircuitIO object and returns a SymPy matrix object.

```python
def get_sympy_matrix(self, subsdict : dict = None, simplify : bool = True) -> sympy.Matrix
```

- The optional parameter `subsdict` is a dictionary used to specify the substitution rules for SymPy symbols. The default is None, that is, no symbol substitution is performed. **Note: This parameter only needs to be specified when SymPy symbols are used as quantum gate parameters.** For example, passing `{t : 3, x : 4}` means substituting the number 3 for the symbol `t` and the number 4 for the symbol `x`.
- The optional parameter `simplify` specifies whether to perform simplification (that is, SymPy's simplify operation) during the computation of the matrix representation. The default is `True`.

The function returns a SymPy matrix object.

### get_numpy_matrix
The `get_numpy_matrix` function computes the matrix representation corresponding to the quantum circuit in the CircuitIO object and returns a NumPy matrix object.

```python
def get_numpy_matrix(self, subsdict : dict = None) -> numpy.array
```

- The parameter `subsdict` is a dictionary specifying whether the symbols therein need to be substituted during the computation, and the substitution method. The default is `None`, that is, no substitution is performed.

The function returns a NumPy matrix object.

### symbol_subs
The `symbol_subs` function substitutes the SymPy symbols in the CircuitIO object (in-place operation).

```python
def symbol_subs(self, subsdict : dict)
```

- The parameter `subsdict` is a dictionary specifying the substitution method.

## 6. Exporting Circuits
### get_circuit_code
The `get_circuit_code` function exports the quantum circuit in the CircuitIO object to code of a supported programming language.

```python
def get_circuit_code(self, language : str, circuit_name : str,
                     gate_lib_name : str = None, linebreak : str = '\n',
                     subsdict : dict = None) -> str
```

- The parameter `language` is a string specifying the language to export to ([click here](./supported-platforms.md)).
- The parameter `circuit_name` is a string specifying the name of the quantum circuit object in the exported code.
- The parameter `gate_lib_name` is a string specifying the package prefix of the quantum circuit object name in the exported code; the default is `None`, that is, no prefix. **Note: To specify no prefix, please specify `None`; do not specify an empty string `''`.**
- The parameter `linebreak` is a string specifying the separator between statements in the exported code; the default is the newline character `'\n'`.
- The parameter `subsdict` is a dictionary specifying whether the symbols therein need to be substituted when exporting the code, and the substitution method. The default is `None`, that is, no substitution is performed.

The function returns a string containing the exported code.

### append_into_actual_circuit
The `append_into_actual_circuit` function inserts the quantum circuit in the CircuitIO object into a quantum circuit object of a specific quantum development framework.

```python
def append_into_actual_circuit(self, dest_qcir, subsdict : dict = None)
```

**Note: When symbol substitution needs to be performed during the insertion into the quantum circuit of a specific quantum development framework, the `>>` operator cannot be used; the `append_into_actual_circuit` member function must be used explicitly.**

### >> operator
When symbol substitution is not used, the `append_into_actual_circuit` function can be replaced by the `>>` operator.

```python
def __rshift__(self, dest_qcir)
```

For example, in the following code
```python
import qiskit
import pyquantumkit
qc = qiskit.QuantumCircuit(3)
cio = pyquantumkit.CircuitIO(3)
# ... construct circuit code ...
cio.append_into_actual_circuit(qc)
```
the last line

`cio.append_into_actual_circuit(qc)`

can be equivalently replaced by

`cio >> qc`
