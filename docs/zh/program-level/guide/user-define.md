# 自定义量子数据类型
PyQuantumKit的量子类型系统为构建具有复杂结构的量子数据类型提供了支持。

在PyQuantumKit中，所有量子数据类型的基类型都是`QVar`这个抽象类，因此若需构建自定义量子数据类型，需要从`QVar`类直接或间接派生子类。在大多数情况下，用户通常不需要直接从`QVar`类派生，而是从其子类（例如量子比特`Qubit`、结构体`QStruct`、量子比特数组`QubitArray`等）派生。

数据类型通常将数据和操作数据的方法绑定在一起。Python类提供了定义从属于该类对象的函数（称为“方法”）的机制，利用此机制，PyQuantumKit允许为自定义量子数据类型添加或改写从属于该类型方法。

## 一、继承与组合

在经典程序设计中，自定义数据类型有两种方式：**继承**和**组合**。基于Python的面向对象类型系统，PyQuantumKit同样也支持这两种方式自定义量子数据类型。

### 继承方式定义量子数据类型
以下例子通过继承`Qubit`类来定义一个`QuBool`类型，它继承了`Qubit`类型的所有功能，只是将输出结果解读方式由生成`'0'`/`'1'`修改为生成`False`/`True`。
```python
class QuBool(Qubit):
    def _interpret_(self, output):
        return (True if super()._interpret_(output) == '1' else False)
```
每个量子变量都有`_interpret_`特殊方法（见后文），它定义了该类型对结果字符串的解读方式。上述例子中，`QuBool`类改写了其父类`Qubit`的此方法：首先调用父类方法，如果父类方法返回`1`则返回`True`；否则返回`False`。`Qubit`类型的`_interpret_`方法已包含对不合法字符串（非`'0'`/`'1'`串）的错误检查与报错的逻辑，因此`QuBool`类型的`_interpret_`不需要额外处理不合法字符串。

和经典程序设计类似，继承方式表达的是“是一个”（is-a）语义，因此本例表达的具体语义是： *`QuBool`类型是一种特殊的`Qubit`类型。* 

### 组合方式定义量子数据类型
`pyquantumkit.program.quint`模块中定义了无符号量子整型`QuUnsignedInt`（`QuInt`其实是该类型的别名），它的定义大致框架如下所示：
```python
class QuUnsignedInt(QStruct):
    def __init__(self, length, varname = None):
        super().__init__(varname)
        self.__qubits = QubitArray(length)
        self.init_qstruct(self.__qubits)

    def _interpret(self, output : str):
        # ......
    def __len__(self):
        # ......
    def create_classical_value(self, number : int):
        # ......
    def create_two_value_superposition(self, x : int, y : int, phi : float = None):
        # ......
    
    # ......
```
即，`QuUnisgnedInt`类型本身是一个结构体，结构体内封装了一个私有的量子比特数组类型（`QubitArray`）的字段`self.__qubits`。我们编写了解读结果字符串的方法`_interpret_`、使用`len()`函数获得长度的魔法方法`__len__`，还增加了制备代表经典整数的量子态的方法`create_classical_value`和制备二值叠加态的方法`create_two_value_superposition`等。

`QuUnisgnedInt`类型并不是通过直接继承`QubitArray`类型来构建，而是在结构体内封装了一个`QubitArray`类型的字段。这是因为如果采用继承方式，则`QuUnisgnedInt`会继承`QubitArray`类型的所有方法，例如按每个量子比特操作的`create_state_by_01pm_str`方法。然而作为一个具有“整数”语义的变量，我们并不希望用户调用这类低层级的方法。

在多数情况下，自定义量子数据类型都是通过组合来构建的。组合方式表达的是“拥有一个”（has-a）语义，因此本例表达的语义是： *量子整型拥有用于存储信息的量子比特数组。* 基于此例子，**我们相信“组合优于继承”的原则对于量子数据类型的构建依然适用。**

## 二、特殊方法
PyQuantumKit的量子数据类型提供了一些特殊方法，这些方法通常不需要直接调用，而是在执行某个特定操作（例如初始化、测量或解读结果字符串）时会被自动调用。每个量子变量都存在默认的或显式定义的特殊方法。

在PyQuantumKit中，约定量子类型的特殊方法以“单下划线开头、单下划线结尾”命名。下列分别介绍各特殊方法。

### 初始化操作`_initialize_`
在对量子变量执行`declare_qvars()`操作时，变量（以及其中的各元素或字段）的初始化操作`_initialize_`会被自动调用，通常用于为量子变量分配初始量子态。初始化操作类似于C++中的构造函数或Python类的`__init__`方法。

**重要提示**： 由于PyQuantumKit基于Python语法构建量子数据类型，因此在使用时**请注意区分`__init__`和`_initialize_`，前者是作为Python类的`QVar`派生类的初始化，后者才是量子变量在量子程序运行过程中的初始化。**

在定义`_initialize_`方法时，它只需要一个参数`self`，且不需要返回值：
```python
    def _initialize_(self):
        # 具体代码
```

若未给出显式定义，量子比特`Qubit`的默认初始化操作为空操作，数组、结构体、联合体类型变量的默认初始化操作为对其各元素或字段调用相应的初始化操作。

这里联合体需要单独说明一下，由于联合体的各字段共用量子比特，因此初始化的顺序格外重要。PyQuantumKit会按照调用`init_qunion()`时传入的参数顺序来依次调用各字段的初始化函数。

### 测量前操作`_premeasure_`
在对量子变量执行测量操作时，PyQuantumKit会在应用具体的测量门之前自动调用量子变量的测量前操作`_premeasure_`。测量前操作通常用于变换测量的基，以实现更一般的测量操作（非计算基测量）。

在定义`_premeasure_`方法时，它只需要一个参数`self`，且不需要返回值：
```python
    def _premeasure_(self):
        # 具体代码
```

若未给出显式定义，量子比特`Qubit`的默认测量前操作为空操作，数组和结构体类型变量的默认测量前操作为对其各元素或字段调用相应的测量前操作，联合体类型变量只对活跃字段调用测量前操作。

### 结果字符串解读方法`_interpret_`
`_interpret_`方法定义了如何对测量结果的`0`/`1`字符串进行解读。

在定义`_interpret_`方法时，它需要两个参数：`self`和代表测量结果字符串的`output: str`；而它的返回值为解读结果。
```python
    def _interpret_(self, output : str) -> str:
        # 具体代码
        # 最后需要return解读结果
```

对于通过继承或组合方式定义的量子数据类型，其结果字符串的解读往往可以通过父类或包含的字段的结果解读方法经过适当的处理得来。例如之前的`QuBool`类型的例子中，它的`_interpret_`通过对其父类`super()`（`Qubit`类型）调用`_interpret_`的返回结果进行适当的处理后得到：
```python
class QuBool(Qubit):
    def _interpret_(self, output):
        return (True if super()._interpret_(output) == '1' else False)
```

### 对数据类型应用量子门的方法`_gate_`
`_gate_`方法定义了如何对数据类型应用量子门。并非所有的量子变量都有`_gate_`方法：`Qubit`类型有`_gate_`方法，但数组、结构体、联合体类型的变量默认都没有定义`_gate_`方法。定义了`_gate_`方法的量子变量可以被当作量子比特来使用，例如可以对其使用`pyquantumkit.program.std`模块的`gate()`函数应用量子门。

在定义`_gate_`方法时，它需要4个参数，第一个参数是`self`，后面三个参数与`pyquantumkit.program.std`模块的`gate()`函数的参数相同：
```python
    def _gate_(self, gate_name : str, qubit_var_list : list, paras : list) -> Qubit:
        # 具体代码
        # 最后需要return作为应用量子门目标的量子比特
```
函数的返回值为需要被作为应用量子门目标的量子比特。如果是通过继承`Qubit`类型来构建的自定义类型，在编写完前面的处理逻辑后，通常可以直接返回`self`。


### 特殊方法的使用例子
下面给出两个定义专门的量子比特类型的例子来说明特殊方法的使用。

#### **例1.** 定义一个基于 $\ket{+},\ket{-}$ 基的量子比特类型`PMQubit`

先来看看`PMQubit`类型需要实现什么功能。首先，正如普通的量子比特通常初始化为 $\ket{0}$ 态，基于 $\ket{+},\ket{-}$ 基的量子比特也需要取某一个基的状态作为初态。这里我们假设`PMQubit`类型变量的状态默认初始化为 $\ket{+}$ ，这可以通过在 $\ket{0}$ 态上应用H门得到，因此该类型的初始化操作应该为一个H门。

其次，`PMQubit`类型的测量操作需要基于 $\ket{+},\ket{-}$ 基的测量（而非通常的计算基 $\ket{0}, \ket{1}$ 测量），因此需要利用测量前操作定义所需的基变换。由于 $\ket{+},\ket{-}$ 基与 $\ket{0}, \ket{1}$ 基可通过H门相互联系，因此该类型的测量前操作也是一个H门。

然后，`PMQubit`类型的测量结果应当表示为`'+'`/`'-'`而不是`'0'`/`'1'`，这就需要重写结果字符串解读方法。由于 $\ket{+}$ 与 $\ket{0}$ ， $\ket{-}$ 与 $\ket{1}$ 分别通过测量前操作的H门相互联系，因此原始测量结果`'0'`对应最终测量结果`'+'`，`'1'`对应`'-'`。

最后，从逻辑上来看，`PMQubit`是一种特殊的`Qubit`，这是is-a语义，因此适合采用继承方式来定义。

定义实现的代码如下：
```python
# 基于 |+>, |-> 基的量子比特类型，通过继承Qubit类来定义
class PMQubit(Qubit):
    # 初始化操作
    def _initialize_(self):
        gate('H', [self])

    # 测量前操作
    def _premeasure_(self):
        gate('H', [self])

    # 解读测量结果
    def _interpret_(self, output : str) -> str:
        return ('+' if super()._interpret_(output) == '0' else '-')
```

在上述代码中，`PMQubit`类型继承了`Qubit`类型，但是改写了`_initialize_`、`_premeasure_`和`_interpret_`方法。其中由于`PMQubit`类型本身就是`Qubit`，因此在初始化操作和测量前操作中应用H门可以直接以`self`作为目标量子比特。

下面编写几个程序来检验`PMQubit`类型的行为。

以下程序
```python
# 检验PMQubit的初始化和测量前操作
def qmain(builder : QProgramBuilder):
    pmq1 = PMQubit('pmq1')
    pmq2 = PMQubit('pmq2')
    builder.declare_qvars(pmq1, pmq2)
    builder.measure_all()
```
声明了两个`PMQubit`变量然后直接测量，编译生成的量子线路和运行结果为：

<div align="left">
<img src=../../../../imgs/pmqubit1.jpg width=50% />
</div>

根据定义，每一个`PMQubit`类型量子变量在声明时会应用一个H门，在测量前也会应用一个H门，因此编译生成的量子线路中一共有4个H门。测量结果被解读为
```
[({'pmq1': '+', 'pmq2': '+'}, 1000)]
```
即从逻辑上看，`PMQubit`类型的变量的默认初始状态为 $\ket{+}$ ，符合要求。

以下程序
```python
# 对PMQubit类型变量的操作
def qmain(builder : QProgramBuilder):
    pmq1 = PMQubit('pmq1')
    pmq2 = PMQubit('pmq2')
    builder.declare_qvars(pmq1, pmq2)

    gate('X', [pmq1])
    gate('Z', [pmq2])

    builder.measure_all()
```
在之前程序的基础上，对`pmq1`应用了X门，对`pmq2`应用了Z门，然后测量。编译生成的量子线路和运行结果为：

<div align="left">
<img src=../../../../imgs/pmqubit2.jpg width=50% />
</div>

可以看到，生成的量子线路在初始化和测量前的一对H门之间分别加入了X门和Z门。测量结果被解读为：
```
[({'pmq1': '+', 'pmq2': '-'}, 1000)]
```
`pmq1`应用X门后的测量结果仍为`+`，而`pmq2`应用Z门后的测量结果则变为`-`，相当于做了一个“比特翻转”。这与 $\ket{0},\ket{1}$ 基下X门翻转量子比特，而Z门仅产生相位变换刚好相反。事实上，根据恒等式 $X=HZH$ 和 $Z=HXH$ ，在 $\ket{+},\ket{-}$ 基下，Z门与X门的地位正好互换。

#### **例2.** 定义一个只允许使用Clifford门的量子比特类型`CliffordQubit`

首先，`CliffordQubit`也是一种特殊的`Qubit`，这还是is-a语义，因此使用继承`Qubit`类型的方式来定义。

然后`CliffordQubit`类型需要在应用量子门时对量子门的种类进行检查，因而需要改写`_gate_`方法，增加量子门种类检查的步骤。

定义实现的代码如下：
```python
# 只允许Clifford门的量子比特
class CliffordQubit(Qubit):
    def _gate_(self, gate_name : str, qubit_var_list : list, paras : list) -> Qubit:
        # 调用get_standard_gatename()函数将gate_name转换为PyQuantumKit标准名称
        standard_name = get_standard_gatename(gate_name)

        # 若使用的门不是Clifford门，报错
        if standard_name not in {'I', 'X', 'Y', 'Z', 'S', 'H', 'CX', 'CY', 'CZ', 'SW', 'ISW'}:
            raise QuantumProgramBuildError(f"Cannot apply non-Clifford gate '{gate_name}' on the CliffordQubit '{self.get_varname()}'")
        
        # 若使用的门是Clifford门，返回self作为调用gate()的目标
        return self
```
在上述代码中，`CliffordQubit`类型继承了`Qubit`类型，但改写了`_gate_`方法。在返回`self`作为应用量子门的目标量子比特之前，首先调用`get_standard_gatename()`函数（该函数由PyQuantumKit提供）将量子门的名称转换为标准名称，然后根据标准名称检验其是否为Clifford门。若不是，则报错。

