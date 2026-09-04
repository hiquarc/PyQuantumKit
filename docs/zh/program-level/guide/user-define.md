# 自定义量子数据类型
PyQuantumKit的量子类型系统为构建具有复杂结构的量子数据类型提供了支持。

在经典程序设计中，自定义数据类型有两种方式：继承和组合。基于Python的面向对象类型系统，PyQuantumKit同样也支持这两种方式自定义量子数据类型。

## 继承方式
以下例子通过继承`Qubit`类来定义一个`QuBool`类型，它继承了`Qubit`类型的所有功能，只是将输出结果解读方式由生成`'0'`/`'1'`修改为生成`False`/`True`。
```python
class QuBool(Qubit):
    def _interpret_output_str(self, output):
        return (True if super()._interpret_output_str(output) == '1' else False)
```

每个量子变量都有`_interpret_output_str`方法，它定义了该类型对结果字符串的解读方式。上述例子中，`QuBool`类改写了其父类`Qubit`的此方法：首先调用父类方法，如果父类方法返回`1`则返回`True`；否则返回`False`。

和经典程序设计类似，继承方式表达的是“是一个”（is-a）语义。

## 组合方式
在多数情况下，自定义量子数据类型都是通过组合来构建的，组合方式表达的是“拥有一个”（has-a）语义。例如，`pyquantumkit.program.quint`模块中定义了无符号量子整型`QuUnsignedInt`（`QuInt`其实是该类型的别名），它的定义大致框架如下所示：
```python
class QuUnsignedInt(QStruct):
    def __init__(self, length, varname = None):
        super().__init__(varname)
        self.__qubits = QubitArray(length)
        self.init_qstruct(self.__qubits)

    def _interpret_output_str(self, output : str):
        # ......
    def __len__(self):
        # ......
    def create_classical_value(self, number : int):
        # ......
    def create_two_value_superposition(self, x : int, y : int, phi : float = None):
        # ......
    
    # ......
```
即，`QuUnisgnedInt`类型本身是一个结构体，结构体内封装了一个私有的量子比特数组类型（`QubitArray`）的字段`self.__qubits`。我们编写了解读结果字符串的方法`_interpret_output_str`、使用`len()`函数获得长度的魔法方法`__len__`，还增加了制备代表经典整数的量子态的方法`create_classical_value`和制备二值叠加态的方法`create_two_value_superposition`等。

`QuUnisgnedInt`类型并不是通过直接继承`QubitArray`类型来构建，而是在结构体内封装了一个`QubitArray`类型的字段。这是因为如果采用继承方式，则`QuUnisgnedInt`会继承`QubitArray`类型的所有方法，例如按每个量子比特操作的`create_state_by_01pm_str`方法。然而作为一个具有“整数”语义的变量，我们并不希望用户调用这类低层级的方法。基于此例子，**我们相信“组合优于继承”的原则对于量子数据类型的构建依然适用。**

