# Quantum Data Type System

PyQuantumKit provides the ability to define custom quantum data types based on Python syntax. The design of the type system references the C language, providing basic quantum data types as well as composite data types such as arrays, structs, and unions.

## 1. Basic Quantum Data Type: Qubit

Most programming languages provide some basic data types, such as integer (`int`), floating-point (`float`/`double`), character (`char`), and boolean (`bool`), and more complex data types can usually be built by combining these basic data types.

In PyQuantumKit quantum programming, there is only one basic quantum data type, namely the qubit `Qubit`. By simply importing the `pyquantumkit.program.std` module, users can directly define variables of type `Qubit`:

```python
from pyquantumkit import QProgramBuilder
from pyquantumkit.program.std import *

def qmain(builder : QProgramBuilder):
    q1 = Qubit('q1')
    q2 = Qubit('q2')
    builder.declare_qvars(q1, q2)

    gate('H', [q1])
    gate('CNOT', [q1, q2])

    builder.measure_all()
```

The `gate()` function can be used to apply a quantum gate on a variable of type `Qubit`.

The measurement result of a `Qubit` type variable will be interpreted as a single character `'0'` or `'1'`:
```python
print(qpbuilder.interpret_output_str('00', 'r'))    # Output: {'q1': '0', 'q2': '0'}
print(qpbuilder.interpret_output_str('01', 'r'))    # Output: {'q1': '1', 'q2': '0'}
print(qpbuilder.interpret_output_str('10', 'r'))    # Output: {'q1': '0', 'q2': '1'}
print(qpbuilder.interpret_output_str('11', 'r'))    # Output: {'q1': '1', 'q2': '1'}
```

### The base type of quantum variables `QVar`
In PyQuantumKit, the base type of all data types containing qubits is `QVar`, including the qubit `Qubit` as well as the arrays, structs, unions, and so on that will be discussed later. Therefore, in what follows, the term "quantum variable" refers to an object of a subclass of the `QVar` class.

### Anonymous variables
When defining a quantum variable, it is usually necessary to assign a name to the variable, and this name is used as the key of the corresponding result dictionary when interpreting the results.
```python
def qmain(builder : QProgramBuilder):
    q1 = Qubit('q1')     # Define a variable of type Qubit and name it 'q1'
    # ......
```
Result interpretation:
```
{'q1': '0'}
```

In some cases, the variable name can be omitted (or specified as `None`), and a variable defined in this way is called an **anonymous variable**:
```python
def qmain(builder : QProgramBuilder):
    q1 = Qubit()        # Omit the variable name to define an anonymous variable
    q2 = Qubit(None)    # Specify the variable name as None to define an anonymous variable
    # ......
```
Note: in this example, the `q1` and `q2` on the left are merely local references to the quantum variables inside the `qmain` function; we have not actually named the quantum variables.

Anonymous variables are typically used in nested data types that do not require variable names, such as elements of arrays, fields of tuples, etc.

PyQuantumKit requires that all quantum variables directly declared in `declare_qvars()` be named.

## 2. Arrays (QArray)
An array is composed of several quantum variables of the same type, and its elements can be accessed using the subscript operator `[]`.

### Defining an array: the `make_qarray()` function

The `make_qarray()` function provided by `pyquantumkit.program.std` can be used to define the corresponding array from a base type. The prototype of this function is:
```python
def make_qarray(base : type|QVar, length : int, varname : str = None)
```

- The `base` parameter indicates the base type of the array, and can be a quantum variable type name (generally a class derived from `QVar`) or a specific quantum variable;
- The `length` parameter gives the length of the generated array;
- The `varname` parameter gives the name of the generated array variable, and defaults to `None` (i.e., an anonymous variable);
- The function returns a new array variable.

The following code defines an array containing 5 qubits and names it `my_array`:
```python
def qmain(builder : QProgramBuilder):
    my_array = make_qarray(Qubit, 5, 'my_array')
    builder.declare_qvars(my_array)
```

The `make_qarray` function can be called nestedly to define multi-dimensional arrays:
```python
def qmain(builder : QProgramBuilder):
    two_dim = make_qarray(make_qarray(Qubit, 6), 2, 'two_dim')
    builder.declare_qvars(two_dim)
```
Here the inner 6-element array uses an anonymous variable, and the outer one is 2-dimensional, so there are 12 qubits in total, and the name of the entire two-dimensional array is `'two_dim'`.

The subscript access operator `[]` can be used to access the elements, with subscripts starting from 0.
```python
# Access the elements of the one-dimensional array my_array
gate('X', [my_array[0]])
gate('CNOT', [my_array[3], my_array[4]])

# Access the elements of the two-dimensional array two_dim
gate('X', [two_dim[0][0]])
gate('CZ', [two_dim[1][2], two_dim[1][4]])
```
In the above access to the two-dimensional array, the first `[]` accesses the outer array (2-dimensional), and the second `[]` accesses the inner array (6-dimensional).

The `len()` function can be used to obtain the length (number of elements) of an array:
```python
    print(len(my_array))    # -> 5
    print(len(two_dim))     # -> 2; this returns the length of the outermost array
```

PyQuantumKit currently only supports fixed-length arrays, and the subscript access operator `[]` currently only supports a single integer as the subscript, and does not yet support range subscripts.

The measurement result of an array type variable will be interpreted as a list composed of the measurement results of its elements.

For the following program
```python
def qmain(builder : QProgramBuilder):
    my_array = make_qarray(Qubit, 5, 'my_array')
    builder.declare_qvars(my_array)

    gate('X', [my_array[0]])
    gate('X', [my_array[3]])

    builder.measure_all()
```
the running result (assuming 1000 shots) is interpreted as:
```
[({'my_array': ['1', '0', '0', '1', '0']}, 1000)]
```

For the following program involving a two-dimensional array
```python
def qmain(builder : QProgramBuilder):
    two_dim = make_qarray(make_qarray(Qubit, 6), 2, 'two_dim')
    builder.declare_qvars(two_dim)

    gate('X', [two_dim[0][0]])
    gate('X', [two_dim[0][5]])
    gate('X', [two_dim[1][2]])
    gate('X', [two_dim[1][4]])

    builder.measure_all()
```
the running result is interpreted as
```
[({'two_dim': [['1', '0', '0', '0', '0', '1'], ['0', '0', '1', '0', '1', '0']]}, 1000)]
```

### Dedicated type for arrays of qubits: `QubitArray`
An array composed of qubits is a very commonly used data type in quantum program development, so PyQuantumKit separately provides the `QubitArray` type, which can replace `make_qarray(Qubit, ...)`. The definitions of the `my_array` and `two_dim` variables above can be rewritten as:
```python
def qmain(builder : QProgramBuilder):
    my_array = QubitArray(5, 'my_array')
    builder.declare_qvars(my_array)
```
and
```python
def qmain(builder : QProgramBuilder):
    # Use QubitArray for the inner array of qubits
    two_dim = make_qarray(QubitArray(6), 2, 'two_dim')
    builder.declare_qvars(two_dim)
```

The measurement result of a `QubitArray` type variable will be interpreted as a `'0'`/`'1'` string, which is more readable, for example in the following forms:
```
[({'my_array': '10010'}, 1000)]
[({'two_dim': ['100001', '001010']}, 1000)]
```

Compared to the general array definition `make_qarray(Qubit, ...)`, the `QubitArray` type provides convenient functions for constructing quantum states on it. For example, the member function `create_state_by_01pm_str` allows users to specify the quantum states $\ket{0}$, $\ket{1}$, $\ket{+}$, $\ket{-}$ to be generated for each qubit in the array using a `'0'`/`'1'`/`'+'`/`'-'` string.

The following program prepares and measures the quantum state $\ket{0}\ket{1}\ket{+}\ket{-}\ket{0}$ on an array containing 5 qubits.
```python
def qmain(builder : QProgramBuilder):
    my_array = QubitArray(5, 'my_array')
    builder.declare_qvars(my_array)

    # Prepare the |0>|1>|+>|->|0> state
    my_array.create_state_by_01pm_str('01+-0')

    builder.measure_all()
```
The running result is interpreted as:
```
[({'my_array': '01000'}, 239), ({'my_array': '01100'}, 254),
 ({'my_array': '01010'}, 255), ({'my_array': '01110'}, 252)]
```

Therefore, **when the semantics of "array of qubits" needs to be expressed, it is recommended to directly use the `QubitArray` type** and avoid `make_qarray(Qubit, ...)`.


## 3. Structs (QStruct) and Tuples (QTuple)
A struct is composed of several quantum variable fields, each with its own variable name, and the fields can have different types. The member access operator `.` can be used to access a particular field.

### Defining a struct

Users define their own struct by **deriving a class from `QStruct`** and defining the fields in the `__init__` method of the derived class.
```python
class MyStruct(QStruct):
    def __init__(self, varname=None):
        # This line is required; call the parent class's __init__
        super().__init__(varname)

        # Define the fields of the struct
        self.x = QubitArray(3, 'x')
        self.y = make_qarray(QubitArray(2), 2, 'y')
        self.z = Qubit('z')

        # This line is also required; initialize the struct
        self.init_qstruct(self.x, self.y, self.z)
```
The above code defines a struct type `MyStruct` that contains three fields: the field `self.x` is an array of qubits containing 3 qubits; the field `self.y` is a 2×2 two-dimensional array of qubits; and the field `self.z` is a single qubit.

The `__init__` of a derived class of a custom struct needs to first call `super()`'s `__init__`, so the beginning is usually written as:
```python
class MyStruct(QStruct):
    def __init__(self, varname=None):
        super().__init__(varname)
        # ......
```
If you use the VSCode code editor, the above code should be auto-completed.

Each field is defined as a member variable of the class (in the form of `self.xxx`).

Finally, the `self.init_qstruct(...)` method needs to be called to complete the initialization of the struct, and the parameters simply list each field in order.

Users can define a struct that does not contain any quantum variable fields (an empty struct); when defining it, the `self.init_qstruct()` method must still be called.
```python
class EmptyStruct(QStruct):
    def __init__(self, varname=None):
        super().__init__(varname)
        self.init_qstruct()     # When defining an empty struct, this line is also required
```

### Using a struct

You can declare a struct type variable and access a particular field through the member access operator `.`.
```python
def qmain(builder : QProgramBuilder):
    mydata = MyStruct('mydata')
    builder.declare_qvars(mydata)

    mydata.x.create_state_by_01pm_str('101')
    gate('X', [mydata.y[0][0]])
    mydata.y[1].create_state_by_01pm_str('11')
    gate('H', [mydata.z])

    builder.measure_all()
```

The measurement result of a struct type variable will be interpreted as a dictionary with the field variable names as keys and the corresponding field interpretation results as values. The running result of the above program is interpreted as:
```
[({'mydata': {'x': '101', 'y': ['10', '11'], 'z': '0'}}, 493),
 ({'mydata': {'x': '101', 'y': ['10', '11'], 'z': '1'}}, 507)]
```

**Note:** `QStruct` itself is an abstract class, and its `__init__` is an abstract method, so a `QStruct` class object cannot be directly defined. You must derive a class and define the fields of the struct in the `__init__` of the derived class, and then use the derived class to define struct variables.

### Tuples: structs with field names omitted and fields accessed by subscript
A tuple is a struct with field names omitted and fields accessed by subscript. The `make_qtuple()` function can be used to define a tuple, and its prototype is:
```python
def make_qtuple(element_list : tuple[type|QVar], varname : str = None)
```

- The `element_list` parameter assigns the type of each field using a Python tuple;
- The `varname` parameter gives the name of the generated tuple variable, and defaults to `None` (i.e., an anonymous variable);
- The function returns a new tuple variable.

The subscript access operator `[]` can be used to access the fields of a tuple, with subscripts starting from 0.

The measurement result of a tuple type variable will be interpreted as a list composed of the interpretation results of its fields.

The following code uses a tuple to implement functionality equivalent to the `mydata` of the previous example:
```python
def qmain(builder : QProgramBuilder):
    # Define a tuple variable mytuple that contains 3 fields:
    #    subscript 0: an array of qubits containing 3 qubits
    #    subscript 1: a 2x2 two-dimensional array of qubits
    #    subscript 2: a qubit
    mytuple = make_qtuple(( QubitArray(3),                   # specify the type of subscript 0
                            make_qarray(QubitArray(2), 2),   # specify the type of subscript 1
                            Qubit ),                         # specify the type of subscript 2
                          'mytuple')
    builder.declare_qvars(mytuple)


    mytuple[0].create_state_by_01pm_str('101')
    gate('X', [mytuple[1][0][0]])
    mytuple[1][1].create_state_by_01pm_str('11')
    gate('H', [mytuple[2]])

    builder.measure_all()
```
The running result is interpreted as:
```
[({'mytuple': ['101', ['10', '11'], '0']}, 497),
 ({'mytuple': ['101', ['10', '11'], '1']}, 503)]
```

## 4. Unions (QUnion)
Similar to a struct, a union is also composed of several quantum variable fields, each with its own variable name, and the fields can have different types. The member access operator `.` can be used to access a particular field. Unlike a struct, **all fields in a union share the same segment of quantum memory address**, and PyQuantumKit guarantees that the starting address of all fields in the union is equal to the address of the union itself. A union can be used in situations where qubits need to be saved through sharing, or where qubits need to be reinterpreted.

The way to define a union is similar to defining a struct, except that you need to **derive from the `QUnion` class**, and the initialization function is `self.init_qunion(...)`.

When measuring a union type variable, the measurement operation acts on the "**active field**" of the union. The member function `set_activity_item()` can be used to set or change the active field. An error is reported when measuring a union variable for which no active field has been set. The interpretation of the measurement result of a union type variable will only contain the result of the active field.

The following code defines a union `QNumberRepresentation`
```python
from pyquantumkit.program.std import *
from pyquantumkit.program.quint import *

class QNumberRepresentation(QUnion):
    def __init__(self, varname=None):
        super().__init__(varname)

        self.number = QuInt(6, 'number')
        self.binary = QubitArray(6, 'binary')

        self.init_qunion(self.number, self.binary)
```
It contains two fields, `number` and `binary`. The `number` field is a quantum integer containing 6 qubits, and the `binary` field is an array containing 6 qubits; the two fields share the same segment of quantum memory.

Because they are shared, operations on one field will affect the content of the other field:
```python
def qmain(builder : QProgramBuilder):
    qnr = QNumberRepresentation('qnr')
    builder.declare_qvars(qnr)

    qnr.binary.create_state_by_01pm_str('010011')

    # A union variable must set the active field before measurement; here it is set to number
    qnr.set_activity_item(qnr.number)
    builder.measure_all()
```
The above code prepares the quantum state $\ket{0}\ket{1}\ket{0}\ket{0}\ket{1}\ket{1}$ on the `binary` field, and then measures with `number` as the active field. The running result is interpreted as:
```
[({'qnr': {'number': 50}}, 1000)]
```
The interpretation result only contains the result of the active field `number`; the integer corresponding to the little-endian binary of `'010011'` is exactly 50 (whose binary representation is 110010b).