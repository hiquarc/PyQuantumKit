# 量子类型系统

PyQuantumKit提供了基于Python的语法来自定义量子数据类型的功能。类型系统的设计参考了C语言，提供基本量子数据类型以及数组、结构体、联合体等复合数据类型构建。

## 一、基本量子数据类型：Qubit

大多数编程语言提供了一些基本数据类型，例如整型（`int`）、浮点型（`float`/`double`）、字符型（`char`）、布尔型（`bool`）等，更复杂的数据类型往往可以通过这些基本数据类型组合而来。

在PyQuantumKit量子编程中，基本量子数据类型只有一个，即量子比特`Qubit`。只需导入`pyquantumkit.program.std`模块，用户就可以直接定义`Qubit`类型的变量：

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

可用`gate()`函数在`Qubit`类型的变量上应用量子门。

`Qubit`类型变量的测量结果将被解读为单个字符`'0'`或`'1'`：
```python
print(qpbuilder.interpret_output_str('00', 'qiskit'))    # 输出：{'q1': '0', 'q2': '0'}
print(qpbuilder.interpret_output_str('01', 'qiskit'))    # 输出：{'q1': '1', 'q2': '0'}
print(qpbuilder.interpret_output_str('10', 'qiskit'))    # 输出：{'q1': '0', 'q2': '1'}
print(qpbuilder.interpret_output_str('11', 'qiskit'))    # 输出：{'q1': '1', 'q2': '1'}
```

### 量子变量的基类型`QVar`
在PyQuantumKit中，所有包含量子比特的数据类型的基类型都是`QVar`，包括量子比特`Qubit`以及后文将要涉及的数组、结构体、联合体等。因此在后文中，“量子变量”这个术语指代的是`QVar`类的子类的对象。

### 匿名变量
在定义量子变量时，通常需要为变量指定名称，该名称在进行结果解读时会作为相应结果字典的键。
```python
def qmain(builder : QProgramBuilder):
    q1 = Qubit('q1')     # 命名为'q1'
    # ......
```
结果解读
```
{'q1': '0'}
```

在一些情况下，也可以省略变量名（或将其指定为`None`），这样定义的变量称为**匿名变量**：
```python
def qmain(builder : QProgramBuilder):
    q1 = Qubit()     # 匿名变量
    # ......
```
注意：本例中左边的`q1`仅仅是该量子变量在`qmain`函数中的局部指代，我们并未给该量子变量命名。

匿名变量通常用于不需要变量名的嵌套数据类型中，例如数组的元素、元组的字段等。

PyQuantumKit要求凡是在`declare_qvars()`中直接声明的量子变量都需要命名。

## 二、数组（QArray）
量子数组由若干个相同类型的量子变量组成，可用下标运算符`[]`访问其中的元素。

### 定义数组：`make_qarray()`函数

可以使用`pyquantumkit.program.std`提供的`make_qarray()`函数由基类型定义相应的数组，该函数的原型为：
```python
def make_qarray(base : type|QVar, length : int, varname : str = None)
```
- `base`指示数组基类型，可用类型名（`QVar`类的派生类）或一个具体的量子变量来指示。
- `length`参数给出生成的数组的长度。
- `varname`参数给出生成的数组变量的名称，默认为`None`（即匿名变量）。

下列代码定义了一个包含5个量子比特的数组，并命名为`my_array`：
```python
def qmain(builder : QProgramBuilder):
    my_array = make_qarray(Qubit, 5, 'my_array')
    builder.declare_qvars(my_array)
```

可以嵌套调用`make_qarray`函数来定义多维数组：
```python
def qmain(builder : QProgramBuilder):
    two_dim = make_qarray(make_qarray(Qubit, 6), 2, 'two_dim')
    builder.declare_qvars(two_dim)
```
这里内层的6维数组使用了匿名变量，外层是2维，因此一共包含12个量子比特，整个二维数组的名称为`'two_dim'`。

可用下标访问运算符`[]`来访问其中的元素，下标从0开始。
```python
# 访问一维数组my_array的元素
gate('X', [my_array[0]])
gate('CNOT', [my_array[3], my_array[4]])

# 访问二维数组two_dim的元素
gate('X', [two_dim[0][0]])
gate('CZ', [two_dim[1][2], two_dim[1][4]])
```
在上述二维数组的访问中，第一个`[]`访问了外层数组（2维），第二个`[]`访问了内层数组（6维）。

可用`len()`获得量子数组的长度：
```python
print(len(my_array))
```

PyQuantumKit目前暂时只支持定长数组，下标访问运算符`[]`目前暂时只支持以单个整数作为下标，暂时不支持范围下标。

量子数组类型的变量的测量结果将被解读为由其各元素的测量结果组成的列表。

以下程序
```python
def qmain(builder : QProgramBuilder):
    my_array = make_qarray(Qubit, 5, 'my_array')
    builder.declare_qvars(my_array)

    gate('X', [my_array[0]])
    gate('X', [my_array[3]])

    builder.measure_all()
```
的运行结果（设运行1000轮）被解读为：
```
[({'my_array': ['1', '0', '0', '1', '0']}, 1000)]
```

以下涉及二维数组的程序
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
的运行结果被解读为
```
[({'two_dim': [['1', '0', '0', '0', '0', '1'], ['0', '0', '1', '0', '1', '0']]}, 1000)]
```

### 量子比特数组的单独类型：`QubitArray`
由量子比特组成的数组是量子程序开发中非常常用的一种数据类型，因此PyQuantumKit单独提供了`QubitArray`类型，可代替`make_qarray(Qubit, ...)`。上述`my_array`和`two_dim`变量的定义可改写为：
```python
def qmain(builder : QProgramBuilder):
    my_array = QubitArray(5, 'my_array')
    builder.declare_qvars(my_array)
```
和
```python
def qmain(builder : QProgramBuilder):
    # 内层量子比特数组用QubitArray代替
    two_dim = make_qarray(QubitArray(6), 2, 'two_dim')
    builder.declare_qvars(two_dim)
```

`QubitArray`类型的变量的测量结果将被解读为`'0'`/`'1'`字符串，可读性更好，例如具有如下形式：
```
[({'my_array': '10010'}, 1000)]
[({'two_dim': ['100001', '001010']}, 1000)]
```

相比于采用量子数组的一般定义方式`make_qarray(Qubit, ...)`，`QubitArray`类型提供了方便的在其上构造量子态的函数。例如成员函数`create_state_by_01pm_str`允许用户使用`'0'`/`'1'`/`'+'`/`'-'`字符串指定数组中各量子比特要生成的量子态 $\ket{0}$, $\ket{1}$, $\ket{+}$, $\ket{-}$。

下列程序在一个包含5个量子比特的数组上制备了量子态 $\ket{0}\ket{1}\ket{+}\ket{-}\ket{0}$ 并测量。
```python
def qmain(builder : QProgramBuilder):
    my_array = QubitArray(5, 'my_array')
    builder.declare_qvars(my_array)

    # 制备 |0>|1>|+>|->|0> 态
    my_array.create_state_by_01pm_str('01+-0')

    builder.measure_all()
```
运行结果解读为：
```
[({'my_array': '01000'}, 239), ({'my_array': '01100'}, 254), ({'my_array': '01010'}, 255), ({'my_array': '01110'}, 252)]
```

因此，**当需要表达“量子比特数组”的语义时，建议直接使用`QubitArray`类型**，避免使用`make_qarray(Qubit, ...)`。


## 三、结构体（QStruct）和元组（QTuple）
量子结构体由若干个量子变量字段组成，每个字段有自己的变量名，各个字段可以有不同的类型，可以使用成员访问运算符`.`来访问其中的某个字段。

### 定义结构体

用户通过派生`QStruct`类来定义自己的结构体，在派生类的`__init__()`中定义各字段。
```python
class MyStruct(QStruct):
    def __init__(self, varname=None):
        # 这一行是必须的，调用父类的__init__()
        super().__init__(varname)

        # 定义结构体的各字段
        self.x = QubitArray(3, 'x')
        self.y = make_qarray(QubitArray(2), 2, 'y')
        self.z = Qubit('z')

        # 这一行也是必须的，初始化结构体
        self.init_qstruct(self.x, self.y, self.z)
```
上述代码定义了一个结构体类型`MyStruct`，其中包含三个字段：字段`self.x`是一个包含3个量子比特的量子比特数组；字段`self.y`是一个2×2的二维量子比特数组；字段`self.z`是单个量子比特。

自定义结构体的派生类的`__init__`需要先调用`super()`的`__init__`，因而开头通常写为：
```python
class MyStruct(QStruct):
    def __init__(self, varname=None):
        super().__init__(varname)
        # ......
```
如果使用VSCode代码编辑器，上述代码应该能自动补全。

各字段被定义为类的成员变量（`self.xxx`的形式）。

最后需要调用`self.init_qstruct(...)`函数来完成结构体的初始化，函数参数只需依次填入各字段即可。

除了初始化方法`__init__`需要定义外，用户也可以为结构体添加其他的自定义方法。

### 结构体的使用

可以声明结构体类型变量并通过成员访问运算符`.`来访问其中的某个字段。
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

结构体类型变量的测量结果将被解读为以各字段变量名为键，以对应的字段的解读结果为值的字典。上述程序的运行结果被解读为：
```
[({'mydata': {'x': '101', 'y': ['10', '11'], 'z': '0'}}, 493), ({'mydata': {'x': '101', 'y': ['10', '11'], 'z': '1'}}, 507)]
```

**注意：** `QStruct`本身是个抽象类，其`__init__`为抽象方法，因此无法直接定义`QStruct`类对象。必须派生并在派生类的`__init__`中定义结构体的各字段，然后用派生类来定义结构体变量。

### 元组：省略字段名且通过下标访问字段的结构体
元组是一种省略字段名且通过下标访问字段的结构体，可利用`make_qtuple()`函数定义元组，函数原型为：
```python
def make_qtuple(element_list : tuple[type|QVar], varname : str = None)
```
- `element_list`参数用Python元组指派各字段的类型。
- `varname`参数给出生成的数组变量的名称，默认为`None`（即匿名变量）。

可用下标访问运算符`[]`来访问元组中的字段，下标从0开始。

元组类型变量的测量结果将被解读为相应字段的解读结果组成的列表。

下列代码利用元组实现了和上一个例子的`mydata`等价的功能：
```python
def qmain(builder : QProgramBuilder):
    # 定义元组变量mytuple，它包含3个字段：
    #    下标0：一个包含3个量子比特的量子比特数组
    #    下标1：一个2x2的二维量子比特数组
    #    下标2：一个量子比特
    mytuple = make_qtuple(( QubitArray(3),
                            make_qarray(QubitArray(2), 2),
                            Qubit ),
                          'mytuple')
    builder.declare_qvars(mytuple)


    mytuple[0].create_state_by_01pm_str('101')
    gate('X', [mytuple[1][0][0]])
    mytuple[1][1].create_state_by_01pm_str('11')
    gate('H', [mytuple[2]])

    builder.measure_all()
```
运行结果解读为：
```
[({'mytuple': ['101', ['10', '11'], '0']}, 497), ({'mytuple': ['101', ['10', '11'], '1']}, 503)]
```

## 四、联合体（QUnion）
与结构体类似，量子联合体也是若干个量子变量字段组成，每个字段有自己的变量名，各个字段可以有不同的类型，可以使用成员访问运算符`.`来访问其中的某个字段。与结构体不同的是，联合体中所有字段共用同一段量子内存地址，PyQuantumKit保证联合体内的所有字段的起始地址都等于联合体本身的地址。联合体可用于需要通过共用来节约量子比特的情形，或者需要对量子比特进行重解释的情形。

定义联合体的方式与定义结构体类似，只是需要从`QUnion`类派生，并且初始化函数为`self.init_qunion(...)`。

当测量一个联合体类型的变量时，测量操作作用于联合体的“**活跃字段**”。可以利用成员函数`set_activity_item()`来设置或改变活跃字段。当测量一个未设置活跃字段的联合体变量时会报错。联合体类型变量的测量结果的解读将只包含活跃字段的结果。

下列代码定义了一个联合体`QNumberRepresent`
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
其中包含`number`和`binary`两个字段。`number`字段是包含6个量子比特的量子整型，`binary`字段是包含6个量子比特的量子比特数组，两个字段共用同一段量子内存。

由于共用，对其中一个字段的操作会影响另一个字段的内容
```python
def qmain(builder : QProgramBuilder):
    qnr = QNumberRepresentation('qnr')
    builder.declare_qvars(qnr)

    qnr.binary.create_state_by_01pm_str('010011')

    # 联合体变量在测量前必须设置活跃字段，这里设置为number
    qnr.set_activity_item(qnr.number)
    builder.measure_all()
```
上述代码对在`binary`字段上制备量子态 $\ket{0}\ket{1}\ket{0}\ket{0}\ket{1}\ket{1}$ ，然后以`number`为活跃字段来测量。运行结果解读为：
```
[({'qnr': {'number': 50}}, 1000)]
```
解读结果只包含活跃字段`number`的结果，`'010011'`的小端序二进制对应的整数刚好就是50（二进制表示为110010b）。
