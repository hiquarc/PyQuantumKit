# Quantum Type System

PyQuantumKit provides the capability to define custom quantum data types based on Python syntax. The design of the type system references the C language, providing basic quantum data types as well as composite data type constructs such as arrays, structs and unions.

## I. The Basic Quantum Data Type: Qubit

Most programming languages provide some basic data types, such as integer (`int`), floating point (`float`/`double`), character (`char`), boolean (`bool`), etc., and more complex data types can often be composed from these basic data types.

In PyQuantumKit quantum programming, there is only one basic quantum data type, namely the qubit `Qubit`. Simply by importing the `pyquantumkit.program.std` module, users can directly define variables of the `Qubit` type:

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

The `gate()` function can be used to apply quantum gates on variables of the `Qubit` type.

The measurement result of a `Qubit` type variable will be interpreted as a single character `'0'` or `'1'`:
```python
print(qpbuilder.interpret_output_str('00', 'r'))    # output: {'q1': '0', 'q2': '0'}
print(qpbuilder.interpret_output_str('01', 'r'))    # output: {'q1': '1', 'q2': '0'}
print(qpbuilder.interpret_output_str('10', 'r'))    # output: {'q1': '0', 'q2': '1'}
print(qpbuilder.interpret_output_str('11', 'r'))    # output: {'q1': '1', 'q2': '1'}
```

### The base type of quantum variables, `QVar`
In PyQuantumKit, the base type of all data types containing qubits is `QVar`, including the qubit `Qubit` and the arrays, structs, unions, etc. to be covered later. Therefore, in what follows, the term "quantum variable" refers to an object of a subclass of the `QVar` class.

### Anonymous variables
When defining a quantum variable, a name usually needs to be specified for the variable, which will be used as the key of the corresponding result dictionary when interpreting the results.
```python
def qmain(builder : QProgramBuilder):
    q1 = Qubit('q1')     # define a variable of Qubit type and name it 'q1'
    # ......
```
Result interpretation
```
{'q1': '0'}
```

In some cases, the variable name can also be omitted (or specified as `None`); variables defined in this way are called **anonymous variables**:
```python
def qmain(builder : QProgramBuilder):
    q1 = Qubit()        # omit the variable name to define an anonymous variable
    q2 = Qubit(None)    # specify the variable name as None to define an anonymous variable
    # ......
```
Note: In this example, `q1` and `q2` on the left are merely the local references to this quantum variable within the `qmain` function; we did not name the quantum variable.

Anonymous variables are usually used in nested data types that do not need variable names, such as array elements and tuple fields.

PyQuantumKit requires that any quantum variable directly declared in `declare_qvars()` must be named.

## II. Arrays (QArray)
An array is composed of several quantum variables of the same type, and its elements can be accessed with the index operator `[]`.

### Defining an array: the `make_qarray()` function

You can use the `make_qarray()` function provided by `pyquantumkit.program.std` to define the corresponding array from a base type. The prototype of this function is:
```python
def make_qarray(base : type|QVar, length : int, varname : str = None)
```

- The `base` parameter indicates the base type of the array; it can be indicated by the quantum variable type name (which should generally be a derived class of the `QVar` class) or by a specific quantum variable;
- The `length` parameter gives the length of the generated array;
- The `varname` parameter gives the name of the generated array variable; the default is `None` (that is, an anonymous variable);
- The function returns a new array variable.

The following code defines an array containing 5 qubits and names it `my_array`:
```python
def qmain(builder : QProgramBuilder):
    my_array = make_qarray(Qubit, 5, 'my_array')
    builder.declare_qvars(my_array)
```

The `make_qarray` function can be called in a nested manner to define multidimensional arrays:
```python
def qmain(builder : QProgramBuilder):
    two_dim = make_qarray(make_qarray(Qubit, 6), 2, 'two_dim')
    builder.declare_qvars(two_dim)
```
Here the inner 6-dimensional array uses an anonymous variable, and the outer is 2-dimensional, so it contains 12 qubits in total, and the name of the entire two-dimensional array is `'two_dim'`.

The index access operator `[]` can be used to access its elements, with indices starting from 0.
```python
# access the elements of the one-dimensional array my_array
gate('X', [my_array[0]])
gate('CNOT', [my_array[3], my_array[4]])

# access the elements of the two-dimensional array two_dim
gate('X', [two_dim[0][0]])
gate('CZ', [two_dim[1][2], two_dim[1][4]])
```
In the above access to the two-dimensional array, the first `[]` accesses the outer array (2-dimensional), and the second `[]` accesses the inner array (6-dimensional).

`len()` can be used to obtain the length (number of elements) of the array:
```python
    print(len(my_array))    # -> 5
    print(len(two_dim))     # -> 2 , here it returns the length of the outermost array
```

PyQuantumKit currently only supports fixed-length arrays, and the index access operator `[]` currently only supports a single integer as the index, not range indexing for now.

The measurement result of a variable of array type will be interpreted as a list composed of the measurement results of its elements.

The following program
```python
def qmain(builder : QProgramBuilder):
    my_array = make_qarray(Qubit, 5, 'my_array')
    builder.declare_qvars(my_array)

    gate('X', [my_array[0]])
    gate('X', [my_array[3]])

    builder.measure_all()
```
its running result (suppose 1000 rounds are run) is interpreted as:
```
[({'my_array': ['1', '0', '0', '1', '0']}, 1000)]
```

The following program involving a two-dimensional array
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
its running result is interpreted as
```
[({'two_dim': [['1', '0', '0', '0', '0', '1'], ['0', '0', '1', '0', '1', '0']]}, 1000)]
```

### The separate type for qubit arrays: `QubitArray`
An array composed of qubits is a very commonly used data type in quantum program development, so PyQuantumKit separately provides the `QubitArray` type, which can replace `make_qarray(Qubit, ...)`. The definitions of the above `my_array` and `two_dim` variables can be rewritten as:
```python
def qmain(builder : QProgramBuilder):
    my_array = QubitArray(5, 'my_array')
    builder.declare_qvars(my_array)
```
and
```python
def qmain(builder : QProgramBuilder):
    # the inner qubit array is replaced by QubitArray
    two_dim = make_qarray(QubitArray(6), 2, 'two_dim')
    builder.declare_qvars(two_dim)
```

The measurement result of a variable of `QubitArray` type will be interpreted as a `'0'`/`'1'` string, which is more readable, for example in the following form:
```
[({'my_array': '10010'}, 1000)]
[({'two_dim': ['100001', '001010']}, 1000)]
```

Compared with the general way of defining an array `make_qarray(Qubit, ...)`, the `QubitArray` type provides convenient functions for constructing quantum states on it. For example, the member function `create_state_by_01pm_str` allows users to use a `'0'`/`'1'`/`'+'`/`'-'` string to specify the quantum state $\ket{0}$, $\ket{1}$, $\ket{+}$, $\ket{-}$ to be generated for each qubit in the array.

The following program prepares and measures the quantum state $\ket{0}\ket{1}\ket{+}\ket{-}\ket{0}$ on an array containing 5 qubits.
```python
def qmain(builder : QProgramBuilder):
    my_array = QubitArray(5, 'my_array')
    builder.declare_qvars(my_array)

    # prepare the |0>|1>|+>|->|0> state
    my_array.create_state_by_01pm_str('01+-0')

    builder.measure_all()
```
The running result is interpreted as:
```
[({'my_array': '01000'}, 239), ({'my_array': '01100'}, 254),
 ({'my_array': '01010'}, 255), ({'my_array': '01110'}, 252)]
```

Therefore, **when the semantics of a "qubit array" need to be expressed, it is recommended to use the `QubitArray` type directly**, avoiding `make_qarray(Qubit, ...)`.


## III. Structs (QStruct) and Tuples (QTuple)
A struct is composed of several quantum variable fields, each field has its own variable name, the fields can have different types, and the member access operator `.` can be used to access a certain field.

### Defining a struct

Users define their own struct by **deriving from the `QStruct` class**, defining the fields in the `__init__` method of the derived class.
```python
class MyStruct(QStruct):
    def __init__(self, varname=None):
        # this line is required; call the __init__ of the parent class
        super().__init__(varname)

        # define the fields of the struct
        self.x = QubitArray(3, 'x')
        self.y = make_qarray(QubitArray(2), 2, 'y')
        self.z = Qubit('z')

        # this line is also required; initialize the struct
        self.init_qstruct(self.x, self.y, self.z)
```
The above code defines a struct type `MyStruct`, which contains three fields: the field `self.x` is a qubit array containing 3 qubits; the field `self.y` is a 2×2 two-dimensional qubit array; the field `self.z` is a single qubit.

The `__init__` of the derived class of a custom struct needs to call `super()`'s `__init__` first, so the beginning is usually written as:
```python
class MyStruct(QStruct):
    def __init__(self, varname=None):
        super().__init__(varname)
        # ......
```
If you use the VSCode code editor, the above code should be auto-completed.

Each field is defined as a member variable of the class (in the form `self.xxx`).

Finally, the `self.init_qstruct(...)` method needs to be called to complete the initialization of the struct; the parameters simply need to be filled in with each field in order.

Users can define a struct that contains no quantum variable fields (an empty struct); the `self.init_qstruct()` method still needs to be called when defining it.
```python
class EmptyStruct(QStruct):
    def __init__(self, varname=None):
        super().__init__(varname)
        self.init_qstruct()     # when defining an empty struct, this line is also required
```

### Using a struct

You can declare a variable of struct type and access a certain field therein through the member access operator `.`.
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

The measurement result of a variable of struct type will be interpreted as a dictionary with the variable name of each field as the key and the corresponding field's interpretation result as the value. The running result of the above program is interpreted as:
```
[({'mydata': {'x': '101', 'y': ['10', '11'], 'z': '0'}}, 493),
 ({'mydata': {'x': '101', 'y': ['10', '11'], 'z': '1'}}, 507)]
```

**Note:** `QStruct` itself is an abstract class, and its `__init__` is an abstract method, so a `QStruct` class object cannot be defined directly. You must derive from it and define each field of the struct in the `__init__` of the derived class, and then use the derived class to define struct variables.

### Tuples: structs with omitted field names and field access by index
A tuple is a kind of struct with omitted field names and field access by index. The `make_qtuple()` function can be used to define a tuple. The function prototype is:
```python
def make_qtuple(element_list : tuple[type|QVar], varname : str = None)
```

- The `element_list` parameter uses a Python tuple to specify the types of each field;
- The `varname` parameter gives the name of the generated tuple variable; the default is `None` (that is, an anonymous variable);
- The function returns a new tuple variable.

The index access operator `[]` can be used to access the fields in the tuple, with indices starting from 0.

The measurement result of a variable of tuple type will be interpreted as a list composed of the interpretation results of the corresponding fields.

The following code uses a tuple to implement functionality equivalent to `mydata` in the previous example:
```python
def qmain(builder : QProgramBuilder):
    # define the tuple variable mytuple, which contains 3 fields:
    #    index 0: a qubit array containing 3 qubits
    #    index 1: a 2x2 two-dimensional qubit array
    #    index 2: one qubit
    mytuple = make_qtuple(( QubitArray(3),                   # specify the type of index 0
                            make_qarray(QubitArray(2), 2),   # specify the type of index 1
                            Qubit ),                         # specify the type of index 2
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

## IV. Unions (QUnion)
Similar to a struct, a union is also composed of several quantum variable fields, each field has its own variable name, the fields can have different types, and the member access operator `.` can be used to access a certain field. Unlike a struct, **all fields in a union share the same segment of quantum memory address**, and PyQuantumKit guarantees that the starting addresses of all fields in the union are equal to the address of the union itself. Unions can be used in cases where qubits need to be saved through sharing, or where qubits need to be reinterpreted.

The way to define a union is similar to defining a struct, except that it needs to **derive from the `QUnion` class**, and the initialization function is `self.init_qunion(...)`.

When measuring a variable of union type, the measurement operation acts on the "**active field**" of the union. The member function `set_activity_item()` can be used to set or change the active field. An error is reported when measuring a union variable for which no active field has been set. The interpretation of the measurement result of a union type variable will only include the result of the active field.

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
which contains two fields, `number` and `binary`. The `number` field is a quantum integer containing 6 qubits, and the `binary` field is an array containing 6 qubits; the two fields share the same segment of quantum memory.

Because they are shared, operations on one field affect the contents of the other field
```python
def qmain(builder : QProgramBuilder):
    qnr = QNumberRepresentation('qnr')
    builder.declare_qvars(qnr)

    qnr.binary.create_state_by_01pm_str('010011')

    # a union variable must have its active field set before measurement; here it is set to number
    qnr.set_activity_item(qnr.number)
    builder.measure_all()
```
The above code prepares the quantum state $\ket{0}\ket{1}\ket{0}\ket{0}\ket{1}\ket{1}$ on the `binary` field, then measures with `number` as the active field. The running result is interpreted as:
```
[({'qnr': {'number': 50}}, 1000)]
```
The interpretation result only contains the result of the active field `number`, and the integer corresponding to the little-endian binary of `'010011'` is exactly 50 (binary representation 110010b).
