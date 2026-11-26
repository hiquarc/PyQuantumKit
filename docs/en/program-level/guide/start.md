# Getting Started Writing Quantum Programs

The high-level-language quantum programming capability provided by PyQuantumKit allows users to use Python syntax to define quantum variables and write quantum programs, and also to use arrays, structs, tuples, and unions containing quantum variables to build custom quantum data types. This section briefly introduces how to write a high-level-language quantum program based on PyQuantumKit.

## 1. The main function of a quantum program
Like a classical program, a group of quantum programs also needs a unique entry point (the main function). In PyQuantumKit, the first parameter of a quantum main function must be a `QProgramBuilder` object, which can bind the quantum variables in the program and compile the entire quantum program into a quantum circuit. It is recommended to name the function `qmain` and write the first parameter as `builder : QProgramBuilder`.

The structure of the main function is divided into three parts: **variable declaration, function body, and measurement operations**, and **this order must be maintained**.

- In the **variable declaration** part, first define local variables inside the function body, and after the definition is complete call `builder.declare_qvars(...)` to associate the local variables with `builder`, so that subsequent qubit allocation and compilation into a quantum circuit can be performed. **This function can only be called once**, so if there are multiple variables to declare, simply list them in order in the parameter list, for example `builder.declare_qvars(var1, var2, var3)`. If this function is called multiple times, a `QuantumProgramBuildError` exception is thrown at compile time, indicating a compilation error.
- In the **function body** part, write the specific operations on the declared quantum variables; only variables that have been declared (i.e., listed in the parameters of `declare_qvars()`) can be operated on.
- In the **measurement operation** part, simply call `builder.measure(...)`, where the parameters list in order the quantum variables to be measured. Like the declaration, this function can only be called once; if it is called multiple times, an error occurs at compile time. Please note that PyQuantumKit currently does not support operating on quantum variables after measurement, nor repeated measurement of the same quantum variable within one program.

As long as there is any operation on a quantum variable in the function body, the variable declaration part is required, because only declared quantum variables can be operated on in the main function. A program that declares no quantum variables can also be compiled, and the quantum circuit generated in this case is an empty circuit.

A quantum program that does not measure any quantum variable can also be compiled into a quantum circuit smoothly; such a quantum circuit contains only quantum gates and no measurement operations, and usually cannot be run on a quantum development platform to obtain results.

The following program declares two qubit variables `q1` and `q2`, and calls the `gate()` function on them to apply an H gate and a CNOT gate, finally preparing a Bell state.
```python
from pyquantumkit import QProgramBuilder
from pyquantumkit.program.std import Qubit, gate

def qmain(builder : QProgramBuilder):
    # ------ Variable declaration part ------
    q1 = Qubit('q1')    # Declare a qubit type variable q1
    q2 = Qubit('q2')    # Declare a qubit type variable q2
    builder.declare_qvars(q1, q2)
    # ------ End of variable declaration ------

    # ------ Function body part ------
    gate('H', [q1])
    gate('CNOT', [q1, q2])
    # ------ End of function body ------

    # ------ Measurement operation part ------
    builder.measure(q1, q2)
    # Can also be equivalently replaced with builder.measure_all()
    # ------ End of measurement operation ------
```

The `gate()` function here is similar to the `apply_gate()` function in circuit-level programming ([view details](../../circuit-level/api/construct.md)), and its prototype is:
```python
def gate(gate_str : str, qubits : list[Qubit], paras : list = None):
```
Its differences from `apply_gate()` are:

1. Compared to `apply_gate()`, the `gate()` function does not need to specify the quantum circuit object, so it omits the first parameter of the quantum circuit.
2. In the `apply_gate()` function, the `qubits` parameter assigns an integer list representing the qubit indices; while in the `gate()` function, the `qubits` parameter assigns a list of `Qubit` type elements, which is equivalent to using `Qubit` variables to refer to the target qubits instead of indices.

## 2. Defining functions
You can also use Python syntax to define functions that accept quantum variables, to achieve procedural quantum program development. For example, the following program defines a function that prepares a Bell state.
```python
def create_bell(a : Qubit, b : Qubit):
    if not (isinstance(a, Qubit) and isinstance(b, Qubit)):
        raise TypeError("the type of a and b must be Qubit!")
    gate('H', [a])
    gate('CNOT', [a, b])
```
Since Python is a weakly typed language, in this example we wrote our own type check.

It can be called like an ordinary function in a quantum program:
```python
def qmain(builder : QProgramBuilder):
    q1 = Qubit('q1')
    q2 = Qubit('q2')
    builder.declare_qvars(q1, q2)

    # Call the create_bell() function, passing the declared quantum variables q1, q2 as function arguments.
    create_bell(q1, q2)

    builder.measure(q1, q2)
```

However, considering the limitations of quantum simulators and hardware, **PyQuantumKit currently does not support declaring local quantum variables inside non-main functions; quantum variables can currently only be declared in the main function** (but local classical variables can be defined, which is supported by Python itself). When calling a function, the declared quantum variables can be passed into the function as arguments. Since Python passes function arguments by reference, in the above code the `create_bell()` function operates on the content corresponding to the variables `q1` and `q2`.

## 3. Compiling into a quantum circuit
First declare a QProgramBuilder object, then call the member method `build()` with the `qmain` function as the argument, which compiles the quantum program `qmain` into a quantum circuit. The compilation result is a `CircuitIO` object, which contains the generated quantum circuit (which can be understood as a platform-independent intermediate representation of a quantum circuit), and can be obtained using the member method `get_built_circuit()`.
```python
qpbuilder = QProgramBuilder()
qpbuilder.build(qmain)
qpbuilder.get_built_circuit()
```

The compiled `CircuitIO` object can be inserted into the quantum circuit of a specific quantum development framework.

## 4. Interpreting the output results
### Interpretation of a single `'0'`/`'1'` string
For a `'0'`/`'1'` string representing the output result of a single measurement, the `interpret_output_str()` method can be called on the `QProgramBuilder` object that has completed the circuit compilation. The prototype of the method is:

```python
def interpret_output_str(self, output_str : str, protocol : str = 'l') -> dict:
```

- `output_str` is a `'0'`/`'1'` string representing the result of a single measurement. Note that the length of the input string must match the number of measurement bits corresponding to the quantum program, and must not contain characters other than `'0'` and `'1'`.
- The `protocol` parameter specifies the convention according to which the interpretation is performed, and two protocols are currently supported:
    - `'l'` or `'L'`: interpret according to the read-from-the-left convention (the default);
    - `'r'` or `'R'`: interpret according to the read-from-the-right convention.

Different quantum development frameworks have different interpretation order conventions; for example, `'qiskit'` and `'pyqpanda3'` read from the right, while `'pyquafu'` (the old Quafu framework) reads from the left. The static method `framework_interpret_protocol()` of the `QProgramBuilder` class can be called to obtain the interpretation convention of a specific framework:
```python
print(framework_interpret_protocol('qiskit'))       # -> 'r'
print(framework_interpret_protocol('pyqpanda3'))    # -> 'r'
print(framework_interpret_protocol('pyquafu'))      # -> 'l'
```

Now consider the quantum program mentioned earlier that prepares and measures a Bell state; it contains two qubits, so the length of the measurement result `'0'`/`'1'` string is 2. The measurement result will be interpreted in the form `quantum variable : value`:

```python
print(qpbuilder.interpret_output_str('01', 'l'))    # -> {'q1': '0', 'q2': '1'}
print(qpbuilder.interpret_output_str('10', 'l'))    # -> {'q1': '1', 'q2': '0'}
print(qpbuilder.interpret_output_str('01', 'r'))    # -> {'q1': '1', 'q2': '0'}
print(qpbuilder.interpret_output_str('10', 'r'))    # -> {'q1': '0', 'q2': '1'}
```

### Interpretation of the running result dictionary
Since in most quantum development frameworks the result of running a quantum program is a dictionary composed of entries of the form `measurement-result '0'/'1' string : occurrence count`, the `interpret_result_dict()` method of the `QProgramBuilder` object can be used to interpret the entire result dictionary. The prototype of this function's parameters is:
```python
def interpret_result_dict(self, output_dict : dict, protocol : str = 'l') -> list:
```
where `output_dict` is the measurement result dictionary, which can usually be the dictionary of the result of running the quantum circuit on the quantum development framework corresponding to the `framework` parameter directly. The `protocol` parameter specifies the convention according to which the interpretation is performed (currently supporting `l` and `r`).

```python
qiskit_cir = qiskit.QuantumCircuit(2, 2)
qpbuilder.get_built_circuit() >> qiskit_cir

qiskit_sim = qiskit_aer.AerSimulator()
result = qiskit_sim.run(qiskit_cir, shots = 1000).result().get_counts()

# call interpret_result_dict()
rec_result = qpbuilder.interpret_result_dict(result, 'r')
print(rec_result)
```
The running result of the above code is:
```
[({'q1': '1', 'q2': '1'}, 490), ({'q1': '0', 'q2': '0'}, 510)]
```

In the original measurement result dictionary, the keys are `'0'`/`'1'` strings, and strings are hashable, so they can serve as dictionary keys. However, the interpretation result of a `'0'`/`'1'` string forms a new dictionary (for example, in this example, the original string `'11'` is interpreted as `{'q1': '1', 'q2': '1'}`), and a dictionary itself is not hashable and cannot serve as a dictionary key, so the interpretation result is represented as a list composed of tuples `(interpretation result, occurrence count)`.