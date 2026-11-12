# Getting Started with Writing Quantum Programs

The high-level-language-level quantum programming capability provided by PyQuantumKit enables users to use Python syntax to define quantum variables and write quantum programs, and also to use arrays, structs, tuples and unions containing quantum variables to build custom quantum data types. This section briefly introduces how to write a high-level-language-level quantum program based on PyQuantumKit.

## I. The main Function of a Quantum Program
Like classical programs, a set of quantum programs also needs a unique entry point (the main function). In PyQuantumKit, the first parameter of the quantum main function must be a `QProgramBuilder` object, which can bind the quantum variables in the program and compile the entire quantum program into a quantum circuit. It is recommended to name the function `qmain` and write the first parameter as `builder : QProgramBuilder`.

The structure of the main function is divided into three major parts: **variable declaration, function body, measurement operation**, and **this order must be maintained**.

- In the **variable declaration** part, first define local variables within the function body; after the definitions are complete, call the `builder.declare_qvars(...)` function to associate the local variables with `builder`, so that they can undergo the subsequent qubit allocation and compilation into quantum circuits. **This function can only be called once**, so if there are multiple variables to declare, simply list them in order in the parameter list, for example `builder.declare_qvars(var1, var2, var3)`. If this function is called repeatedly, a `QuantumProgramBuildError` exception is thrown during compilation, representing a compilation error.
- In the **function body** part, write the specific operations on the declared quantum variables; only variables that have been declared (that is, listed in the parameters of `declare_qvars()`) can be operated on.
- In the **measurement operation** part, simply call the `builder.measure(...)` function, where the parameters list, in order, the quantum variables to be measured. Like declaration, this function can only be called once; if it is called repeatedly, an error occurs during compilation. Please note that PyQuantumKit currently does not yet support operating on quantum variables after measurement, nor performing repeated measurement on the same quantum variable within one program.

As long as there is any operation on any quantum variable in the function body part, the variable declaration part is required, because only declared quantum variables can be operated on in the main function. A program that declares no quantum variables can also be compiled, and the resulting quantum circuit is an empty circuit.

A quantum program that measures no quantum variables can also be compiled successfully into a quantum circuit; such a quantum circuit contains only quantum gates and no measurement operation, and usually cannot be run on a quantum development platform to obtain results.

The following program declares two qubit variables `q1` and `q2`, and calls the `gate()` function on them to apply an H gate and a CNOT gate, finally preparing a Bell state.
```python
from pyquantumkit import QProgramBuilder
from pyquantumkit.program.std import Qubit, gate

def qmain(builder : QProgramBuilder):
    # ------ variable declaration part ------
    q1 = Qubit('q1')    # declare the qubit-type variable q1
    q2 = Qubit('q2')    # declare the qubit-type variable q2
    builder.declare_qvars(q1, q2)
    # ------ end of variable declaration ------

    # ------ function body part ------
    gate('H', [q1])
    gate('CNOT', [q1, q2])
    # ------ end of function body ------

    # ------ measurement operation part ------
    builder.measure(q1, q2)
    # can also be equivalently replaced by builder.measure_all()
    # ------ end of measurement operation ------
```

The `gate()` function here is similar to the `apply_gate()` function in quantum circuit-level programming ([see details](../../circuit-level/api/construct.md)); the function prototype is:
```python
def gate(gate_str : str, qubits : list[Qubit], paras : list = None):
```
Its difference from `apply_gate()` lies in:

1. Compared with `apply_gate()`, the `gate()` function does not need to specify a quantum circuit object, hence it lacks the first quantum circuit parameter.
2. In the `apply_gate()` function, the `qubits` parameter specifies a list of integers representing qubit indices; while in the `gate()` function, the `qubits` parameter specifies a list of `Qubit` type elements, which is equivalent to using `Qubit` variables instead of indices to refer to the target qubits.

## II. Defining Functions
You can also use Python syntax to define functions that accept quantum variables, in order to implement procedural quantum program development. For example, the following program defines a function that prepares a Bell state.
```python
def create_bell(a : Qubit, b : Qubit):
    if not (isinstance(a, Qubit) and isinstance(b, Qubit)):
        raise TypeError("the type of a and b must be Qubit!")
    gate('H', [a])
    gate('CNOT', [a, b])
```
Since Python is a weakly typed language, we wrote our own type check in this example.

It can be called in a quantum program like an ordinary function:
```python
def qmain(builder : QProgramBuilder):
    q1 = Qubit('q1')
    q2 = Qubit('q2')
    builder.declare_qvars(q1, q2)

    # Call the create_bell() function, passing the declared quantum variables q1, q2 as function parameters.
    create_bell(q1, q2)

    builder.measure(q1, q2)
```

However, considering the limitations of quantum simulators and hardware, **PyQuantumKit currently does not support declaring local quantum variables inside non-main functions; quantum variables can currently only be declared in the main function** (but local classical variables can be defined, which Python itself supports). When calling a function, the declared quantum variables can be passed in as parameters. Since Python passes function parameters by reference, the operations inside the `create_bell()` function in the above code act on the contents corresponding to the variables `q1`, `q2`.

## III. Compiling into a Quantum Circuit
First declare a QProgramBuilder object, then call the member method `build()` with the `qmain` function as the parameter, and the quantum program `qmain` can be compiled into a quantum circuit. The compilation result is a `CircuitIO` object, which contains the generated quantum circuit (which can be understood as a kind of intermediate representation of a platform-independent quantum circuit); the member method `get_built_circuit()` can be used to obtain this `CircuitIO` object.
```python
qpbuilder = QProgramBuilder()
qpbuilder.build(qmain)
qpbuilder.get_built_circuit()
```

The `CircuitIO` object generated by compilation can be inserted into the quantum circuit of a specific quantum development framework.

## IV. Interpreting the Output Results
### Interpretation of a single `'0'`/`'1'` string
For a `'0'`/`'1'` string representing the output result of one measurement, you can call the `interpret_output_str()` method on a `QProgramBuilder` object whose circuit compilation has been completed. The method prototype is:

```python
def interpret_output_str(self, output_str : str, protocol : str = 'l') -> dict:
```

- `output_str` is the `'0'`/`'1'` string representing one measurement result. Please note that the length of the input string must match the number of measured bits corresponding to the quantum program, and it cannot contain any characters other than `'0'`, `'1'`.
- The `protocol` parameter specifies the convention according to which the interpretation is performed. Two protocols are currently supported:
    - `'l'` or `'L'`: interpret according to the convention of starting from the left (the default method);
    - `'r'` or `'R'`: interpret according to the convention of starting from the right.

Different quantum development frameworks have different interpretation order conventions; for example, `'qiskit'` and `'pyqanda3'` start from the right, while `'pyquafu'` starts from the left. You can call the `framework_interpret_protocol()` static method of the `QProgramBuilder` class to obtain the interpretation convention of a specific framework:
```python
print(framework_interpret_protocol('qiskit'))       # -> 'r'
print(framework_interpret_protocol('pyqpanda3'))    # -> 'r'
print(framework_interpret_protocol('pyquafu'))      # -> 'l'
```

Now consider the aforementioned quantum program that prepares and measures a Bell state. It contains two qubits, so the length of the measurement result `'0'`/`'1'` string is 2. The measurement result will be interpreted in the form `quantum variable : value`:

```python
print(qpbuilder.interpret_output_str('01', 'l'))    # -> {'q1': '0', 'q2': '1'}
print(qpbuilder.interpret_output_str('10', 'l'))    # -> {'q1': '1', 'q2': '0'}
print(qpbuilder.interpret_output_str('01', 'r'))    # -> {'q1': '1', 'q2': '0'}
print(qpbuilder.interpret_output_str('10', 'r'))    # -> {'q1': '0', 'q2': '1'}
```

### Interpretation of the running result dictionary
Since in most quantum development frameworks the result of running a quantum program is a dictionary composed of entries of the form `measurement result '0'/'1' string : occurrence count`, you can use the `interpret_result_dict()` method of the `QProgramBuilder` object to interpret the entire result dictionary. The prototype of this function's parameters is:
```python
def interpret_result_dict(self, output_dict : dict, protocol : str = 'l') -> list:
```
where `output_dict` is the measurement result dictionary, which usually can be directly the dictionary of the running result of the quantum circuit on the quantum development framework corresponding to the `framework` parameter. The `protocol` parameter specifies the convention according to which the interpretation is performed (`l` and `r` are currently supported).

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

In the raw measurement result dictionary, the keys are `'0'`/`'1'` strings, and strings are hashable, so they can be used as dictionary keys. However, the interpretation result of the `'0'`/`'1'` forms a new dictionary (for example, in this example, the raw string `'11'` is interpreted as `{'q1': '1', 'q2': '1'}`), and dictionaries themselves are not hashable and cannot be used as dictionary keys, so the interpretation result is represented as a list composed of tuples `(interpretation result, occurrence count)`.
