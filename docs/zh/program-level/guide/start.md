# 开始编写量子程序

PyQuantumKit提供的高级语言级量子编程能力，使得用户可以利用Python的语法来定义量子变量，编写量子程序，也可以利用包含量子变量的数组、结构体、元组、联合体来构建自定义量子数据类型。

## 一、量子程序的main函数
和经典程序一样，一组量子程序也需要一个唯一的入口点（main函数）。在PyQuantumKit中，量子main函数的第一个参数必须为`QProgramBuilder`对象，它可以绑定程序中的量子变量，并将整个量子程序编译为量子线路。建议将函数名命名为`qmain`，第一个参数写为`builder : QProgramBuilder`。

main函数的结构分为**变量声明、函数主体、测量操作**三大部分，且**必须保持此顺序**。

- 变量声明部分首先在函数体内定义局部变量，定义完成后调用`builder.declare_qvars(*args)`（这里的`builder`为main函数的第一个参数）函数将局部变量与`builder`相关联，以使其能进行后续量子比特分配和编译为量子线路的操作。**该函数需要且只能被调用一次**，因而如果有多个变量需要声明时，直接在参数列表中依次列出，例如`builder.declare_qvars(var1, var2, var3)`。如果该函数重复调用多次，则会抛出`QProgramBuildError`异常。
- 函数主体部分编写对已声明的量子变量的具体操作，只有声明过（即在`declare_qvars()`的参数中列出过）的变量才能进行操作。
- 测量部分只需调用`builder.declare_qvars(*args)`函数，其中参数依次列出需要测量的量子变量。和声明一样，该函数只能被调用一次，如果该函数重复调用多次，则会抛出`QProgramBuildError`异常。测量过后无法再对量子变量进行其他操作，否则会抛出`QProgramBuildError`异常。

下列程序声明了两个量子比特变量`q1`和`q2`，并在其上调用`gate()`函数来应用一个H门和一个CNOT门，最终制备Bell态。
```python
from pyquantumkit import QProgramBuilder
from pyquantumkit.program.std import Qubit, gate

def qmain(builder : QProgramBuilder):
    # ------ 变量声明部分 ------
    q1 = Qubit('q1')    # 声明量子比特型变量q1
    q2 = Qubit('q2')    # 声明量子比特型变量q2
    builder.declare_qvars(q1, q2)
    # ------ 变量声明结束 ------

    # ------ 函数主体部分 ------
    gate('H', [q1])
    gate('CNOT', [q1, q2])
    # ------ 函数主体结束 ------

    # ------ 测量操作部分 ------
    builder.measure(q1, q2)
    # 也可用builder.measure_all()等价替代
    # ------ 测量操作结束 ------
```

其中对量子比特变量应用量子门使用`gate()`函数，它与量子线路级编程中的`apply_gate()`函数类似（[查看详情](../../circuit-level/api/construct.md)），函数原型为：
```python
def gate(gate_str : str, qubits : list[Qubit], paras : list = None):
```
它与`apply_gate()`的区别在于：

1. 相比于`apply_gate()`，`gate()`函数无需指定量子线路对象，因而少了第一个量子线路的参数。
2. 而在`apply_gate()`函数中，`qubits`参数指派的是代表量子比特下标的整数列表；在`gate()`函数中，`qubits`参数指派的是`Qubit`类型元素的列表，相当于不用下标，而是用`Qubit`变量来指代目标量子比特。

## 二、定义函数
也可以利用Python语法来定义接受量子变量的函数，以实现面向过程的量子程序开发。例如，下列程序定义了一个制备Bell态的函数。
```python
def create_bell(a : Qubit, b : Qubit):
    if not (isinstance(a, Qubit) and isinstance(b, Qubit)):
        raise TypeError("the type of a and b must be Qubit!")
    gate('H', [a])
    gate('CNOT', [a, b])
```
由于Python是弱类型语言，因此本例中我们自己编写了一个类型检查。

可以在量子程序中像普通函数一样调用：
```python
def qmain(builder : QProgramBuilder):
    q1 = Qubit('q1')
    q2 = Qubit('q2')
    builder.declare_qvars(q1, q2)

    # 调用create_bell()函数，将已声明的量子变量q1, q2作为函数参数。
    create_bell(q1, q2)

    builder.measure(q1, q2)
```

不过，考虑到量子模拟器和硬件的限制，**PyQuantumKit暂时不支持在非main函数内声明局部量子变量**（但可以定义局部经典变量，这是Python本身支持的），**目前只能在main函数中声明量子变量**。调用函数时，可将已声明的量子变量作为参数传入函数。由于Python对函数参数是按引用传递，因而上述代码中`create_bell()`函数内操作的就是变量`q1`, `q2`对应的内容。

## 三、编译为量子线路
首先声明一个QProgramBuilder对象，然后以`qmain`函数为参数调用成员方法`build()`，即可将量子程序`qmain`编译为量子线路。编译结果为一个`CircuitIO`对象，其中包含了生成的量子线路（可以理解为平台无关的量子线路的一种中间表示），可用成员方法`get_built_circuit()`获得此`CircuitIO`对象。
```python
qpbuilder = QProgramBuilder()
qpbuilder.build(qmain)
qpbuilder.get_built_circuit()
```

编译生成的`CircuitIO`对象可以插入具体量子开发框架的量子线路中。

## 四、解读输出结果
### 单个0/1串的解读
对代表一次测量的输出结果的0/1串，可以对已完成线路编译的`QProgramBuilder`对象调用`interpret_output_str()`方法，方法原型为：

```python
def interpret_output_str(self, output_str : str, framework : str = None) -> dict:
```
- `output_str`是代表一次测量结果的0/1字符串。请注意，输入的字符串的长度必须与对应的量子程序对应的测量比特数相匹配，且不能包含除`'0'`,`'1'`外的其他字符。
- `framework`参数指定按哪个量子开发框架的输出结果约定进行解读，必须为首支持的量子开发框架名。例如，指定为`'qiskit'`, `'pyqanda3'`则右开始解读，指定为`'pyquafu'`则从左开始解读。**若未指定，则默认从左开始解读。**

现在考虑前文提到的制备Bell态并测量的量子程序，它包含两个量子比特，因而测量结果0/1串的长度为2。测量结果会被解读为 `量子变量 : 取值` 的形式：

```python
print(qpbuilder.interpret_output_str('00', 'qiskit'))  #输出：{'q1': '0', 'q2': '0'}
print(qpbuilder.interpret_output_str('01', 'qiskit'))  #输出：{'q1': '1', 'q2': '0'}
print(qpbuilder.interpret_output_str('10', 'qiskit'))  #输出：{'q1': '0', 'q2': '1'}
print(qpbuilder.interpret_output_str('11', 'qiskit'))  #输出：{'q1': '1', 'q2': '1'}
```

### 运行结果字典的解读
由于在大多数量子开发框架中，量子程序运行的结果是由形如 `测量0/1串 : 出现次数` 的项构成的字典，可以使用`QProgramBuilder`对象的`interpret_output_dict`成员函数来解读整个结果字典。该函数的参数的原型为：
```python
def interpret_result_dict(self, output_dict : dict, framework : str = None) -> list:
```
其中`output_dict`是测量结果字典，通常可以直接使用量子线路在`framework`参数相应的量子开发框架上运行结果的字典。

```python
qiskit_cir = qiskit.QuantumCircuit(2, 2)
qpbuilder.get_built_circuit() >> qiskit_cir

qiskit_sim = qiskit_aer.AerSimulator()
result = qiskit_sim.run(qiskit_cir, shots = 1000).result().get_counts()

# call interpret_result_dict()
rec_result = qpbuilder.interpret_result_dict(result, 'qiskit')
print(rec_result)
```
上述代码的运行结果为：
```
[({'q1': '1', 'q2': '1'}, 490), ({'q1': '0', 'q2': '0'}, 510)]
```

原始测量结果字典中，键是0/1字符串，字符串是hashable的，因而可以作为字典的键。然而，对0/1的解读结果会形成一个新的字典（例如本例中，原始字符串`'11'`被解读为`{'q1': '1', 'q2': '1'}`），而字典本身不是hashable的，不可作为字典的键，因此解读结果被表示为由元组 `(解读结果, 出现次数)` 构成的列表。
