# CircuitIO Class Member Function Quick Reference
This page gives the member functions of the CircuitIO class, for users to consult.

## 1. Initialization and bit count
### Initialization __init__
When defining a CircuitIO object, its initialization method (constructor) `__init__` is called, and its prototype is:

```python
def __init__(self, nqbits : int = 0, ncbits : int = 0) -> None
```

- The parameter `nqbits` specifies the number of qubits contained in the CircuitIO object, and defaults to 0.
- The parameter `ncbits` specifies the number of classical bits contained in the CircuitIO object, and defaults to 0.

**Note: The two parameters "number of qubits" and "number of classical bits" of the CircuitIO class only serve as hints (for example when connecting two quantum circuits in parallel); when applying quantum gates, no check is performed on whether the indices overflow.**

### set_nqbits
The `set_nqbits` function sets the number of qubits of the CircuitIO object, and its prototype is:

```python
def set_nqbits(self, nqbits) -> None
```

- The parameter `nqbits` specifies the number of qubits to be set.

### set_ncbits
The `set_ncbits` function sets the number of classical bits of the CircuitIO object, and its prototype is:

```python
def set_ncbits(self, ncbits) -> None
```

- The parameter `ncbits` specifies the number of classical bits to be set.

### get_nqbits
The `get_nqbits` function returns the number of qubits of the CircuitIO object, and its prototype is:

```python
def get_nqbits(self) -> int
```

### get_ncbits
The `get_ncbits` function returns the number of classical bits of the CircuitIO object, and its prototype is:

```python
def get_ncbits(self) -> int
```

## 2. Applying quantum gates
### apply_gate
The `apply_gate` member function of the CircuitIO class is similar to the global `apply_gate` function, and can apply a quantum gate on the quantum circuit of the CircuitIO object.

```python
def apply_gate(self, gatestr : str, qbits : list[int], paras : list = None) -> None
```

- The parameter `gate_str` is a string indicating the gate to be applied. Considering that the same gate may have multiple different names (for example Toffoli, CCNOT, and CCX all represent the same gate), PyQuantumKit allows different name strings to represent the same gate, and is case-insensitive. [Click here](supported-gates.md) for the specific supported quantum gates and their corresponding strings.
- The parameter `qbits` is an integer list specifying the list of qubit indices to which the gate is applied. Note that regardless of whether the quantum gate is single-bit or multi-bit, **this parameter needs to be assigned in the form of a list**.
- The parameter `paras` is a list used to assign parameters to parameterized gates; for parameterless gates, this parameter does not need to be assigned.

Use the `apply_gate` member function on the CircuitIO object `CircuitIO_Obj`:
```python
CircuitIO_Obj.apply_gate('H', [2])
```
can be equivalently replaced with the global `apply_gate` function, as long as the CircuitIO object is passed as the parameter representing the quantum circuit:
```python
apply_gate(CircuitIO_Obj, 'H', [2])
```

### apply_measure
The `apply_measure` member function of the CircuitIO class is similar to the global `apply_measure` function, and can apply a quantum measurement operation on the quantum circuit of the CircuitIO object.

```python
def apply_measure(self, qindex : list[int], cindex : list[int]) -> None
```

- The parameter `qindex` is an integer list specifying the indices of the qubits to be measured.
- The parameter `cindex` is an integer list specifying the indices of the classical bits where the measurement results are stored. The components of `qindex` and `cindex` correspond to each other respectively, so `qindex` and `cindex` should have the same length.

Use the `apply_measure` member function on the CircuitIO object `CircuitIO_Obj`:
```python
CircuitIO_Obj.apply_measure([0, 1, 2], [0, 1, 2])
```
can be equivalently replaced with the global `apply_measure` function, as long as the CircuitIO object is passed as the parameter representing the quantum circuit:
```python
apply_measure(CircuitIO_Obj, [0, 1, 2], [0, 1, 2])
```

## 3. Modular construction
### inverse
The `inverse` function reverses the quantum circuit in the current CircuitIO object into its inverse circuit (in-place operation).

```python
def inverse(self)
```

### remap_qbits
The `remap_qbits` function remaps the indices of the qubits in the current CircuitIO object (in-place operation).

```python
def remap_qbits(self, remap : int|list|range)
```

- The parameter `remap` assigns the remapping method for the qubits. The type passed can be `int` or `list[int]`, and defaults to `None`, meaning no remapping is performed. When an `int` type is passed, the index of each qubit of the source quantum circuit is increased by this integer value when concatenated; when a `list[int]` type is passed, remapping is performed according to the instructions of this array when concatenated.

### remap_cbits
The `remap_cbits` function remaps the indices of the classical bits in the current CircuitIO object (in-place operation).

```python
def remap_cbits(self, remap : int|list|range)
```

- The parameter `remap` assigns the remapping method for the classical bits. The type passed can be `int` or `list[int]`, and defaults to `None`, meaning no remapping is performed. When an `int` type is passed, the index of each classical bit of the source quantum circuit is increased by this integer value when concatenated; when a `list[int]` type is passed, remapping is performed according to the instructions of this array when concatenated.

### append_circuit_io
The `append_circuit_io` function concatenates the quantum circuit of another CircuitIO object to the end of the quantum circuit of this object.

```python
def append_circuit_io(self, cir_io_obj)
```

- The parameter `cir_io_obj` assigns the source quantum circuit.

### The << operator
The `append_circuit_io` function can be replaced with the `<<` operator.

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

concatenates the quantum circuit in `cio2` to the end of `cio1`. This line can be equivalently replaced with:

`cio1 << cio2`


## 4. Property checking
### contains_measure
`contains_measure` checks whether the CircuitIO object contains a measurement operation, and returns `True` if it does.

```python
def contains_measure(self) -> bool
```

### check_nqbits
The `check_nqbits` function checks whether any quantum gate operation in the CircuitIO object has an out-of-range index, that is, whether a qubit index exceeding the number of qubits is used.

```python
def check_nqbits(self, adjust : bool = False) -> bool
```

- The parameter `adjust` specifies whether to automatically adjust the number of qubits to accommodate the indices of the quantum gate operations when an out-of-range index is detected during checking. It defaults to `False`, meaning it is never adjusted.

If there is no out-of-range index, it returns `True`; otherwise it returns `False`, and if the `adjust` parameter is `True`, the number of qubits is automatically adjusted.

### check_ncbits
The `check_ncbits` function checks whether the classical bits of the measurement operations in the CircuitIO object have out-of-range indices, that is, whether a classical bit index exceeding the number of classical bits is used.

```python
def check_ncbits(self, adjust : bool = False) -> bool
```

- The parameter `adjust` specifies whether to automatically adjust the number of classical bits to accommodate the indices of the measurement operations when an out-of-range index is detected during checking. It defaults to `False`, meaning it is never adjusted.

If there is no out-of-range index, it returns `True`; otherwise it returns `False`, and if the `adjust` parameter is `True`, the number of classical bits is automatically adjusted.

## 5. Matrix symbolic representation
### get_sympy_matrix
The `get_sympy_matrix` function computes the matrix representation corresponding to the quantum circuit in the CircuitIO object, and returns a SymPy matrix object.

```python
def get_sympy_matrix(self, subsdict : dict = None, simplify : bool = True) -> sympy.Matrix
```

- The optional parameter `subsdict` is a dictionary used to specify the substitution rules for SymPy symbols. It defaults to None, meaning no symbol substitution is performed. **Note: This parameter only needs to be specified when SymPy symbols are used as quantum gate parameters.** For example, passing `{t : 3, x : 4}` means substituting the symbol `t` with the number 3 and the symbol `x` with the number 4.
- The optional parameter `simplify` specifies whether to simplify during the computation of the matrix representation (i.e., SymPy's simplify operation), and defaults to `True`.

The function returns a SymPy matrix object.

### get_numpy_matrix
The `get_numpy_matrix` function computes the matrix representation corresponding to the quantum circuit in the CircuitIO object, and returns a NumPy matrix object.

```python
def get_numpy_matrix(self, subsdict : dict = None) -> numpy.array
```

- The parameter `subsdict` is a dictionary specifying whether the symbols need to be substituted during the computation, and the substitution method. It defaults to `None`, meaning no substitution is performed.

The function returns a NumPy matrix object.

### symbol_subs
The `symbol_subs` function substitutes the SymPy symbols in the CircuitIO object (in-place operation).

```python
def symbol_subs(self, subsdict : dict)
```

- The parameter `subsdict` is a dictionary specifying the substitution method.

## 6. Exporting the quantum circuit and code
### get_circuit_code
The `get_circuit_code` function exports the quantum circuit in the CircuitIO object to code of a supported programming language.

```python
def get_circuit_code(self, language : str, circuit_name : str,
                     linebreak : str = '\n', include_declare = True,
                     subsdict : dict = None) -> tuple[str, set]:
```

- The parameter `language` is a string specifying the language to export to ([click here](./supported-platforms.md)).
- The parameter `circuit_name` is a string specifying the name of the quantum circuit object in the exported code.
- The parameter `linebreak` is a string specifying the separator between statements in the exported code, and defaults to the newline character `'\n'`.
- The parameter `include_declare` is a boolean variable specifying whether to include the code that declares the quantum circuit. If it is `True`, it is included; otherwise only the code for applying quantum gates is generated.
- The parameter `subsdict` is a dictionary specifying whether the symbols need to be substituted when exporting the code, and the substitution method. It defaults to `None`, meaning no substitution is performed.

The function returns a string containing the exported code.

### export_standalone_code
The `export_standalone_code` function can export code containing the prefix and suffix (package references, main function declaration, etc.) that can be directly run independently. The information such as the prefix and suffix required by the code all comes from the `EXPORT_CONSTANTS` constant of the quantum development framework translation script ([view details](../custom-platform.md#export_constants)).

```python
def export_standalone_code(self, language : str, circuit_name : str,
                            linebreak : str = '\n', subsdict : dict = None) -> str:
```

- The parameter `language` is a string specifying the language to export to ([click here](./supported-platforms.md)).
- The parameter `circuit_name` is a string specifying the name of the quantum circuit object in the exported code.
- The parameter `linebreak` is a string specifying the separator between statements in the exported code, and defaults to the newline character `'\n'`.
- The parameter `subsdict` is a dictionary specifying whether the symbols need to be substituted when exporting the code, and the substitution method. It defaults to `None`, meaning no substitution is performed.

### append_into_actual_circuit
The `append_into_actual_circuit` function inserts the quantum circuit in the CircuitIO object into the quantum circuit object of a specific quantum development framework.

```python
def append_into_actual_circuit(self, dest_qcir, subsdict : dict = None)
```

**Note: When symbol substitution needs to be performed during the process of inserting into the quantum circuit of a specific quantum development framework, the `>>` operator cannot be used; the `append_into_actual_circuit` member function must be used explicitly.**

### The >> operator
In the case of not using symbol substitution, the `append_into_actual_circuit` function can be replaced with the `>>` operator.

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

can be equivalently replaced with

`cio >> qc`