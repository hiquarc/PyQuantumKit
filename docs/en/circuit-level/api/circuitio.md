# Quick Reference of CircuitIO Class Member Functions
This page presents the member functions of the CircuitIO class for users' reference.

## 1. Initialization and Bit Counts
### Initialization \_\_init\_\_
When defining a CircuitIO object, its initialization method (constructor) `__init__` is called, with the function prototype:

```python
def __init__(self, nqbits : int = 0, ncbits : int = 0) -> None
```
- The parameter `nqbits` specifies the number of quantum bits contained in the CircuitIO object, defaulting to 0.
- The parameter `ncbits` specifies the number of classical bits contained in the CircuitIO object, defaulting to 0.

**Note: The two parameters "number of quantum bits" and "number of classical bits" of the CircuitIO class are only used as hints (e.g., when parallelizing two quantum circuits) and do not check for subscript overflow when applying quantum gates.**

### set_nqbits
The `set_nqbits` function sets the number of quantum bits of the CircuitIO object, with the function prototype:

```python
def set_nqbits(self, nqbits) -> None
```
- The parameter `nqbits` specifies the number of quantum bits to be set.

### set_ncbits
The `set_ncbits` function sets the number of classical bits of the CircuitIO object, with the function prototype:

```python
def set_ncbits(self, ncbits) -> None
```
- The parameter `ncbits` specifies the number of classical bits to be set.

### get_nqbits
The `get_nqbits` function returns the number of quantum bits of the CircuitIO object, with the function prototype:

```python
def get_nqbits(self) -> int
```

### get_ncbits
The `get_ncbits` function returns the number of classical bits of the CircuitIO object, with the function prototype:

```python
def get_ncbits(self) -> int
```

## 2. Applying Quantum Gates
### apply_gate
The `apply_gate` member function of the CircuitIO class is similar to the global `apply_gate` function and can apply quantum gates to the quantum circuit of the CircuitIO object.

```python
def apply_gate(self, gatestr : str, qbits : list[int], paras : list = None) -> None
```
- The parameter `gate_str` is a string indicating the gate to be applied. Considering that the same gate may have multiple different names (e.g., Toffoli, CCNOT, CCX all represent the same gate), PyQuantumKit allows using different name strings to represent the same gate, and the case is insensitive. [Click here to view](supported-gates.md) the specific supported quantum gates and their corresponding strings.
- The parameter `qbits` is a list of integers specifying the list of quantum bit subscripts to which the gate is to be applied. Note that whether the quantum gate is single-qubit or multi-qubit, this parameter must be assigned **in the form of a list**.
- The parameter `paras` is a list used to assign parameters to parameterized gates; for non-parameterized gates, this parameter does not need to be assigned.

Using the `apply_gate` member function on a CircuitIO object `CircuitIO_Obj`:
```python
CircuitIO_Obj.apply_gate('H', [2])
```
can be equivalently replaced with the global `apply_gate` function by passing the CircuitIO object as the parameter representing the quantum circuit:
```python
apply_gate(CircuitIO_Obj, 'H', [2])
```

### apply_measure
The `apply_measure` member function of the CircuitIO class is similar to the global `apply_measure` function and can apply quantum measurement operations to the quantum circuit of the CircuitIO object.

```python
def apply_measure(self, qindex : list[int], cindex : list[int]) -> None
```
- The parameter `qindex` is a list of integers specifying the subscripts of the quantum bits to be measured.
- The parameter `cindex` is a list of integers specifying the subscripts of the classical bits where the measurement results are stored. Each component of `qindex` and `cindex` corresponds respectively, so the lengths of `qindex` and `cindex` should be the same.

Using the `apply_measure` member function on a CircuitIO object `CircuitIO_Obj`:
```python
CircuitIO_Obj.apply_measure([0, 1, 2], [0, 1, 2])
```
can be equivalently replaced with the global `apply_measure` function by passing the CircuitIO object as the parameter representing the quantum circuit:
```python
apply_measure(CircuitIO_Obj, [0, 1, 2], [0, 1, 2])
```

## 3. Modular Construction
### inverse
The `inverse` function inverts the quantum circuit in the current CircuitIO object to the inverse circuit (in-place operation).

```python
def inverse(self)
```

### remap_qbits
The `remap_qbits` function remaps the subscripts of the quantum bits in the current CircuitIO object (in-place operation).

```python
def remap_qbits(self, remap : int|list|range)
```
- The parameter `remap` specifies the remapping method of quantum bits, and the passed type can be `int` or `list[int]`, defaulting to `None`, which means no remapping is performed. When an `int` type is passed, the subscript of each quantum bit in the source quantum circuit will be increased by this integer value during concatenation; when a `list[int]` type is passed, remapping is performed according to the instructions of this array during concatenation.

### remap_cbits
The `remap_cbits` function remaps the subscripts of the classical bits in the current CircuitIO object (in-place operation).

```python
def remap_cbits(self, remap : int|list|range)
```
- The parameter `remap` specifies the remapping method of classical bits, and the passed type can be `int` or `list[int]`, defaulting to `None`, which means no remapping is performed. When an `int` type is passed, the subscript of each classical bit in the source quantum circuit will be increased by this integer value during concatenation; when a `list[int]` type is passed, remapping is performed according to the instructions of this array during concatenation.

### append_circuit_io
The `append_circuit_io` function concatenates the quantum circuit of another CircuitIO object to the end of the quantum circuit of this object.

```python
def append_circuit_io(self, cir_io_obj)
```
- The parameter `cir_io_obj` specifies the source quantum circuit.

### << Operator
The `append_circuit_io` function can be replaced with the `<<` operator.

```python
def __lshift__(self, cir_io_obj)
```

For example, in the following code:
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


## 4. Attribute Checking
### contains_measure
`contains_measure` checks whether the CircuitIO object contains measurement operations, and returns `True` if it does.

```python
def contains_measure(self) -> bool
```

### check_nqbits
The `check_nqbits` function checks whether the subscript out of bounds occurs in each quantum gate operation in the CircuitIO object, i.e., quantum bit subscripts exceeding the number of quantum bits are used.

```python
def check_nqbits(self, adjust : bool = False) -> bool
```
- The parameter `adjust` specifies whether to automatically adjust the number of quantum bits to adapt to the subscripts of the quantum gate operations when subscript out of bounds is detected during inspection. The default is `False`, which means no adjustment is ever made.

Returns `True` if there is no subscript out of bounds; otherwise returns `False`, and if the `adjust` parameter is `True`, the number of quantum bits is automatically adjusted.

### check_ncbits
The `check_ncbits` function checks whether the subscript out of bounds occurs in the classical bits of the measurement operations in the CircuitIO object, i.e., classical bit subscripts exceeding the number of classical bits are used.

```python
def check_ncbits(self, adjust : bool = False) -> bool
```

- The parameter `adjust` specifies whether to automatically adjust the number of classical bits to adapt to the subscripts of the measurement operations when subscript out of bounds is detected during inspection. The default is `False`, which means no adjustment is ever made.

Returns `True` if there is no subscript out of bounds; otherwise returns `False`, and if the `adjust` parameter is `True`, the number of classical bits is automatically adjusted.

## 5. Matrix Symbolic Representation
### get_sympy_matrix
The `get_sympy_matrix` function calculates the matrix representation corresponding to the quantum circuit in the CircuitIO object and returns a SymPy matrix object.

```python
def get_sympy_matrix(self, subsdict : dict = None, simplify : bool = True) -> sympy.Matrix
```
- The optional parameter `subsdict` is a dictionary used to specify the SymPy symbol substitution rules. The default is None, which means no symbol substitution is performed. **Note: This parameter only needs to be specified when SymPy symbols are used as quantum gate parameters.** For example, passing `{t : 3, x : 4}` means substituting the symbol `t` with the number 3 and the symbol `x` with the number 4.
- The optional parameter `simplify` specifies whether to perform simplification (i.e., SymPy's simplify operation) during the calculation of the matrix representation, defaulting to `True`.

The function returns a SymPy matrix object.

### get_numpy_matrix
The `get_numpy_matrix` function calculates the matrix representation corresponding to the quantum circuit in the CircuitIO object and returns a NumPy matrix object.

```python
def get_numpy_matrix(self, subsdict : dict = None) -> numpy.array
```
- The parameter `subsdict` is a dictionary specifying whether symbols need to be substituted during calculation and the substitution method. The default is `None`, which means no substitution is performed.

The function returns a NumPy matrix object.

### symbol_subs
The `symbol_subs` function substitutes SymPy symbols in the CircuitIO object (in-place operation).

```python
def symbol_subs(self, subsdict : dict)
```
- The parameter `subsdict` is a dictionary specifying the substitution method.

## 6. Exporting Circuits
### get_circuit_code
The `get_circuit_code` function exports the quantum circuit in the CircuitIO object to code in supported programming languages.

```python
def get_circuit_code(self, language : str, circuit_name : str,
                     gate_lib_name : str = None, linebreak : str = '\n',
                     subsdict : dict = None) -> str
```
- The parameter `language` is a string specifying the exported language ([click here to view](./supported-platforms.md)).
- The parameter `circuit_name` is a string specifying the name of the quantum circuit object in the exported code.
- The parameter `gate_lib_name` is a string specifying the package prefix of the quantum circuit object name in the exported code, defaulting to `None`, which means no prefix. **Note: Specify `None` for no prefix, do not specify an empty string `''`.**
- The parameter `linebreak` is a string specifying the separator between each statement in the exported code, defaulting to the newline character `'\n'`.
- The parameter `subsdict` is a dictionary specifying whether symbols need to be substituted during code export and the substitution method. The default is `None`, which means no substitution is performed.

The function returns a string containing the exported code.

### append_into_actual_circuit
The `append_into_actual_circuit` function inserts the quantum circuit in the CircuitIO object into the quantum circuit object of a specific quantum development framework.

```python
def append_into_actual_circuit(self, dest_qcir, subsdict : dict = None)
```

**Note: When symbol substitution needs to be performed during insertion into the quantum circuit of a specific quantum development framework, the `>>` operator cannot be used, and the `append_into_actual_circuit` member function must be explicitly used.**

### >> Operator
Without using symbol substitution, the `append_into_actual_circuit` function can be replaced with the `>>` operator.

```python
def __rshift__(self, dest_qcir)
```

For example, in the following code:
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
