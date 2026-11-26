# Storage and Interpretation of Measurement Results
For a quantum variable, in addition to deciding the allocation of its qubits, if it is measured, one also needs to consider the storage of the classical results (0 or 1) obtained by the measurement. In most quantum development frameworks, in addition to qubits, developers often need to allocate classical bits to collect measurement results. Therefore, in order to compile a high-level-language quantum program into an executable quantum circuit, and at the same time correctly identify the substring corresponding to each quantum variable from the resulting `'0'`/`'1'` string, the allocation of classical bits for storing measurement results also needs to be considered for the measurement operation.

## 1. Allocation of classical bits for storing measurement results
In the main function of a quantum program, the measurement operation is completed by calling the `measure()` method on the `QProgramBuilder` object, where the parameters list in order the quantum variables to be measured.
```python
def qmain1(builder : QProgramBuilder):
    qarr1 = QubitArray(3, 'qarr1')
    qarr2 = QubitArray(4, 'qarr2')
    builder.declare_qvars(qarr1, qarr2)

    # Measure qarr1, qarr2 in order
    builder.measure(qarr1, qarr2)
    # Can be equivalently replaced with builder.measure_all()
```
Just as calling the `declare_qvars()` function completes the allocation of qubits, the process of calling the `measure()` function also performs the allocation of the classical bits for storing the measurement results. In the above example, PyQuantumKit allocates classical bits 0 through 2 to store the measurement result of `qarr1`, and classical bits 3 through 6 to store the measurement result of `qarr2`.

Since the parameters and their order of calling `declare_qvars()` and `measure()` are the same, the `measure_all()` method (with no parameters) can be used in place of `measure(qarr1, qarr2)`.

The quantum circuit compiled from program `qmain1` will contain 7 qubits and 7 classical bits for storing measurement results, and since the parameters and their order of calling `declare_qvars()` and `measure()` are the same, the qubits and classical bits with the same index are in one-to-one correspondence.

### Different measurement orders
When calling `measure()`, the order of the parameters does not necessarily have to be the same as when calling `declare_qvars()`; in this case the allocation of classical bits for storing measurement results differs.

For the following program
```python
def qmain2(builder : QProgramBuilder):
    qarr1 = QubitArray(3, 'qarr1')
    qarr2 = QubitArray(4, 'qarr2')
    builder.declare_qvars(qarr1, qarr2)

    # Measure qarr2 first, then qarr1
    builder.measure(qarr2, qarr1)
```
the order when calling `measure()` is `qarr2, qarr1`, at which point PyQuantumKit allocates classical bits 0 through 3 to store the measurement result of `qarr2`, and classical bits 4 through 6 to store the measurement result of `qarr1`.

However, the order when calling `declare_qvars()` in this example is `qarr1, qarr2`, so the qubit allocation is: qubits 0 through 2 are allocated to `qarr1`, and qubits 3 through 6 are allocated to `qarr2`. Here, a situation arises where the qubit indices and the classical bit indices for storing the measurement results of the same quantum variable are inconsistent.

### Measuring only some of the quantum variables
When calling `measure()`, it is also allowed to measure only some of the quantum variables.

For the following program
```python
def qmain3(builder : QProgramBuilder):
    qarr1 = QubitArray(3, 'qarr1')
    qarr2 = QubitArray(4, 'qarr2')
    builder.declare_qvars(qarr1, qarr2)

    # Measure only qarr2
    builder.measure(qarr2)
```
although two quantum variables `qarr1` and `qarr2` are declared, only `qarr2` is measured. Therefore, PyQuantumKit allocates classical bits 0 through 3 to store the measurement result of `qarr2`, and the quantum circuit compiled from program `qmain3` will contain 7 qubits and 4 classical bits for storing measurement results, with these 4 classical bits exactly storing the measurement result of `qarr2`.


## 2. Is the measurement result string read from the left or from the right?
In most quantum development frameworks, the result of running a quantum circuit is a dictionary composed of entries of the form `'0'/'1' measurement-result string : occurrence count`, for example the running result of a quantum circuit that prepares and measures a Bell state usually has the following form:
```
{'00': 491, '11': 509}
```
That is, the occurrence counts of the measurement results `'00'` and `'11'` are 491 and 509 respectively.

Here is a question: which qubit's measurement result does the first `'0'` and the second `'0'` in `'00'` correspond to respectively? In fact, different quantum development frameworks have different conventions for this question. The Bell state example does not reveal the difference, so let's look at another example.

```python
def qmain4(builder : QProgramBuilder):
    qarr1 = QubitArray(3, 'qarr1')
    qarr2 = QubitArray(4, 'qarr2')
    builder.declare_qvars(qarr1, qarr2)

    qarr1.create_state_by_01pm_str('110')
    qarr2.create_state_by_01pm_str('0101')
    
    builder.measure_all()
```
If we try compiling program `qmain4` into a quantum circuit and running it on the three quantum development frameworks Qiskit, QPanda3, and Quafu, we find that the same quantum circuit produces two kinds of running results.

The result of running on Qiskit and QPanda3 is:
```
{'1010011': 1000}
```
while the result of running on PyQuafu (the old version) is:
```
{'1100101': 1000}
```
It can be seen that these two results are exactly opposite in order.

According to the semantics of program `qmain4`, the quantum variable `qarr1` corresponds to qubits 0 through 2, whose measurement results are stored in classical bits 0 through 2; the quantum variable `qarr2` corresponds to qubits 3 through 6, whose measurement results are stored in classical bits 3 through 6. Therefore, if the subscript of the result string is required to exactly match the subscript of the classical bit, it should be `'1100101'`, which is exactly the convention adopted by the old PyQuafu framework: the leftmost character of the string corresponds to the measurement result of the first qubit, which is called the **read-from-the-left convention**. Qiskit and QPanda3 adopt the opposite **read-from-the-right convention**, where the rightmost character of the result string corresponds to the measurement result of the first qubit.

The characteristic of the read-from-the-left convention is that the subscript of a qubit is the same as the subscript of its corresponding result character in the string, which is more friendly for programmatic processing. The characteristic of the read-from-the-right convention is that, if the measurement result needs to be interpreted as an integer, this method happens to be the binary representation that matches human reading habits (low bits on the far right). Perhaps Qiskit and QPanda3 adopt the read-from-the-right convention mainly for the convenience of humans reading in binary form.

In the official documentation of these quantum development frameworks, the order of the measurement result characters is not prominently mentioned, and there may even be cases where the official order is changed (for example, **the new Quafu platform abandoned the previous read-from-the-left convention of PyQuafu and changed to the read-from-the-right convention compatible with Qiskit**). However, if cross-platform quantum program development is to be realized, the differences in the conventions of the measurement result character order among different quantum development frameworks need to be noted.

## 3. Interpretation of measurement results
After compiling the quantum program using a `QProgramBuilder` class object (calling the `build()` method), the allocation of the qubits of the quantum program and the classical bits for storing the measurement results is complete, and then the relevant methods for interpreting the running results can be called to interpret the results.

### Interpretation of a single 0/1 string: the `interpret_output_str()` method
For a `'0'`/`'1'` string representing the output result of a single measurement, the `interpret_output_str()` method can be called on the `QProgramBuilder` object that has completed the circuit compilation. The prototype of the method is:
```python
def interpret_output_str(self, output_str : str, protocol : str = 'l') -> dict:
```

- `output_str` is a `'0'`/`'1'` string representing the result of a single measurement. Note that **the length of the input string must match the number of classical bits allocated by the quantum program in the `QProgramBuilder` for storing measurement results**, and must not contain characters other than `'0'` and `'1'`, otherwise a `ResultInterpretError` exception is raised.

    - For example, the number of classical bits allocated in the programs `qmain1`, `qmain2`, and `qmain4` above is 7, so for the `QProgramBuilder` class that compiled these three programs, `'0011001'` and `'1101111'` are legal strings for calling the `interpret_output_str()` method, while `'110'`, `'1101'`, and `'11+-abc'` are not legal strings.

    - The number of classical bits allocated in program `qmain3` is 4, so `'1101'` is a legal string for the call, while `'110'` and `'0011001'` are not legal strings.

    - The `n_measure_cbits()` method of the `QProgramBuilder` object can be called to obtain the number of classical bits allocated for storing measurement results.

- The `protocol` parameter specifies the convention according to which the interpretation is performed, and two protocols are currently supported:
    - `'l'` or `'L'`: interpret according to the read-from-the-left convention (the default);
    - `'r'` or `'R'`: interpret according to the read-from-the-right convention.
    - The static method `framework_interpret_protocol()` of the `QProgramBuilder` class can be called to obtain the interpretation convention of a specific framework:
        
    ```python
    print(framework_interpret_protocol('qiskit'))       # -> 'r'
    print(framework_interpret_protocol('pyqpanda3'))    # -> 'r'
    print(framework_interpret_protocol('pyquafu'))      # -> 'l'
    ```
        
- The return value is the dictionary obtained by interpretation, whose structure is:

    `{variable name 1: value 1, variable name 2: value 2, ...}`
    
    where *variable name* is the string passed when declaring the quantum variable (for example `'qarr1'`, `'qarr2'` in the previous examples), and *value* is the interpretation result for that quantum variable. For a quantum variable of composite type, its elements or fields are also interpreted recursively.

    - The measurement result of a `Qubit` type variable will be interpreted as a single character `'0'` or `'1'`;
    - The measurement result of a `QubitArray` type variable will be interpreted as a `'0'`/`'1'` string;
    - The measurement result of an array (QArray) type variable will be interpreted as a list composed of the interpretation results of its elements.
    - The measurement result of a struct (QStruct) type variable will be interpreted as a dictionary with the field variable names as keys and the interpretation results of the corresponding fields as values.
    - The measurement result of a tuple (QTuple) type variable will be interpreted as a list composed of the interpretation results of its fields.
    - The measurement result of a union (QUnion) type variable will be interpreted as a dictionary containing only one active field.

**Note: The `interpret_output_str()` method only interprets the result string according to the agreed allocation of qubits and classical bits, so its behavior is only related to the variable declaration part and the measurement operation part of the compiled program, and has nothing to do with the function body.** For example, although the function bodies of programs `qmain1` and `qmain4` differ, their variable declaration parts and measurement operation parts are completely identical, so the behavior of calling the `interpret_output_str()` method on the `QProgramBuilder` objects that compiled them is the same.

Below we use `qmain4` to illustrate the execution process of this method. We first use `QProgramBuilder` to compile `qmain4`, and then call its `n_qvars_qubits()` method and `n_measure_cbits()` method respectively to obtain the number of qubits and the number of classical bits allocated for program `qmain4`.
```python
qpb = QProgramBuilder()
qpb.build(qmain4)
print(qpb.n_qvars_qubits())     # -> 7
print(qpb.n_measure_cbits())    # -> 7
```

We call the `interpret_output_str()` method with `'1100101'` and the read-from-the-left convention and print the return value:
```python
print(qpb.interpret_output_str('1100101', 'l'))
```
The output result is:
```
{'qarr1': '110', 'qarr2': '0101'}
```
According to the semantics of program `qmain4`, the measurement result of variable `qarr1` is stored in classical bits 0 through 2, and when using the read-from-the-left convention, the substring `'110'` composed of the characters at indices 0 through 2 of the string `'1100101'` is exactly the result corresponding to variable `qarr1`. Similarly, the measurement result of variable `qarr2` is stored in classical bits 3 through 6, so the substring `'0101'` composed of the characters at indices 3 through 6 of the string `'1100101'` is exactly the result corresponding to variable `qarr2`.

If we switch to the read-from-the-right convention to interpret the same string `'1100101'`
```python
print(qpb.interpret_output_str('1100101', 'r'))
```
the output result is:
```
{'qarr1': '101', 'qarr2': '0011'}
```
It is necessary to first reverse the string so that the character indices correspond to the same indices of each qubit. Reversing `'1100101'` gives `'1010011'`, so variable `qarr1` corresponds to the substring `'101'` composed of indices 0 through 2, and variable `qarr2` corresponds to the substring `'0011'` composed of indices 3 through 6.

### Interpretation of the result dictionary: the `interpret_result_dict()` method
The `interpret_output_str()` method only interprets a single `'0'`/`'1'` string, while the `interpret_result_dict()` method can interpret a dictionary composed of entries of the form `'0'/'1' string : occurrence count`. In most quantum development frameworks, the result of running a quantum circuit is exactly a dictionary of this form, so the measurement result returned by the framework can be interpreted directly. The prototype of this function is:
```python
def interpret_result_dict(self, output_dict : dict, protocol : str = 'l') -> list:
```

- `output_dict` is the measurement result dictionary.
- The `protocol` parameter specifies the convention according to which the interpretation is performed, and two protocols are currently supported:
    - `'l'` or `'L'`: interpret according to the read-from-the-left convention (the default);
    - `'r'` or `'R'`: interpret according to the read-from-the-right convention.
- The return value is a list composed of tuples `(interpretation result, occurrence count)`.

The `interpret_result_dict()` method calls the `interpret_output_str()` method on each key of the passed parameter `output_dict` to interpret it, and then combines it with the corresponding value (occurrence count) to form a tuple of the form `(interpretation result, occurrence count)`. The return value is a list composed of all such tuples.

In the original measurement result dictionary, the keys are `'0'`/`'1'` strings, and strings are hashable, so they can serve as dictionary keys, and thus form a dictionary composed of entries of the form `'0'/'1' string : occurrence count`. However, the interpretation result itself is a dictionary, and a dictionary is not hashable and cannot serve as a dictionary key, so the return result of the `interpret_result_dict()` method is represented as a list, where each element of the list is a tuple of the form `(interpretation result, occurrence count)`.

**Note:** Similar to the `interpret_output_str()` method, **the behavior of the `interpret_result_dict()` method is only related to the variable declaration part and the measurement operation part of the compiled program, and has nothing to do with the function body.**