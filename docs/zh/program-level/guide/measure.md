# 测量结果的存放与解读
对于一个量子变量，除了需要决定其量子比特的分配外，如果对其进行测量，还需要考虑测量得到的经典结果（0或1）的存放。在大部分量子开发框架中，除了量子比特外，开发者往往还需要分配经典比特（bit）来收集测量结果。因此，为了将高级语言级量子程序编译为可执行的量子线路，同时能正确地从结果`'0'`/`'1'`字符串中识别出各量子变量对应的子串，对于测量操作还需要考虑存放测量结果的经典比特的分配。

## 一、存储测量结果的经典比特分配
在量子程序main函数中，通过对`QProgramBuilder`对象调用`measure()`方法来完成测量操作，其中参数依次填入需要测量的量子变量。
```python
def qmain1(builder : QProgramBuilder):
    qarr1 = QubitArray(3, 'qarr1')
    qarr2 = QubitArray(4, 'qarr2')
    builder.declare_qvars(qarr1, qarr2)

    # 按顺序依次测量qarr1, qarr2
    builder.measure(qarr1, qarr2)
    # 可用builder.measure_all()等价代替
```
正如调用`declare_qvars()`函数完成量子比特的分配，调用`measure()`函数的过程中同样也执行了对存储测量结果的经典比特分配。上述例子中，PyQuantumKit将第0~2号经典比特分配用于存放`qarr1`的测量结果，将第3~6号经典比特分配用于存放`qarr2`的测量结果。

由于调用`declare_qvars()`和`measure()`的参数和顺序相同，因此可以用`measure_all()`方法（无参数）代替`measure(qarr1, qarr2)`。

程序`qmain1`编译生成的量子线路将包含7个量子比特和7个存放测量结果的经典比特，且由于调用`declare_qvars()`和`measure()`的参数和顺序相同，相同下标的量子比特和经典比特是一一对应的。

### 不同的测量顺序
在调用`measure()`时，传入参数的顺序不一定要和调用`declare_qvars()`相同，此时存放测量结果的经典比特分配方式有所不同。

下列程序
```python
def qmain2(builder : QProgramBuilder):
    qarr1 = QubitArray(3, 'qarr1')
    qarr2 = QubitArray(4, 'qarr2')
    builder.declare_qvars(qarr1, qarr2)

    # 先测量qarr2，再测量qarr1
    builder.measure(qarr2, qarr1)
```
在调用`measure()`时的顺序是`qarr2, qarr1`，此时PyQuantumKit将第0~3号经典比特分配用于存放`qarr2`的测量结果，将第4~6号经典比特分配用于存放`qarr1`的测量结果。

然而，本例调用`declare_qvars()`时的顺序是`qarr1, qarr2`，因此量子比特的分配是：第0~2号量子比特分配给`qarr1`，第3~6号量子比特分配给`qarr2`。这里出现了同一个量子变量的量子比特下标和存放测量结果的经典比特的下标不一致的情况。

### 只对部分量子变量进行测量
在调用`measure()`时，还允许只对部分量子变量进行测量。

下列程序
```python
def qmain3(builder : QProgramBuilder):
    qarr1 = QubitArray(3, 'qarr1')
    qarr2 = QubitArray(4, 'qarr2')
    builder.declare_qvars(qarr1, qarr2)

    # 只测量qarr2
    builder.measure(qarr2)
```
虽然声明了两个量子变量`qarr1`, `qarr2`，但只对`qarr2`进行测量。因此PyQuantumKit将第0~3号经典比特分配用于存放`qarr2`的测量结果，程序`qmain3`编译生成的量子线路将包含7个量子比特和4个存放测量结果的经典比特，这4个经典比特刚好存放了`qarr2`的测量结果。


## 二、测量结果字符串是从左开始还是从右开始？
在大多数量子开发框架中，量子线路运行的结果是由形如 `测量结果'0'/'1'字符串 : 出现次数` 的项构成的字典，例如一个制备并测量Bell态的量子线路的运行结果通常具有如下形式：
```
{'00': 491, '11': 509}
```
即，测量得到结果`'00'`和`'11'`的出现次数分别为491次和509次。

这里有一个问题，`'00'`中的第一个`'0'`和第二个`'0'`分别对应哪个量子比特的测量结果？事实上，对于这个问题，不同的量子开发框架有不同的约定。Bell态的例子看不出区别，我们再来看一个例子。

```python
def qmain4(builder : QProgramBuilder):
    qarr1 = QubitArray(3, 'qarr1')
    qarr2 = QubitArray(4, 'qarr2')
    builder.declare_qvars(qarr1, qarr2)

    qarr1.create_state_by_01pm_str('110')
    qarr2.create_state_by_01pm_str('0101')
    
    builder.measure_all()
```
尝试将程序`qmain4`编译为量子线路后在Qiskit、QPanda3和Quafu三个量子开发框架上运行，我们发现同一个量子线路会出现两种运行结果。

在Qiskit和QPanda3上运行的结果为：
```
{'1010011': 1000}
```
而在Quafu上运行的结果为：
```
{'1100101': 1000}
```
可以看到，这两种结果刚好顺序相反。

按照程序`qmain4`的语义，量子变量`qarr1`对应0~2号量子比特，其测量结果存放在第0~2号经典比特；量子变量`qarr2`对应3~6号量子比特，其测量结果存放在第3~6号经典比特。因此如果要求结果字符串的下标刚好匹配经典比特的下标，应该为`'1100101'`，即Quafu框架采用的那种约定：字符串最左侧字符对应第一个量子比特的测量结果，称为**从左开始约定**。Qiskit和QPanda3则采用了与之相反的**从右开始约定**，即结果字符串最右侧字符对应第一个量子比特的测量结果。

从左开始约定的特点是，量子比特的下标与其对应的结果字符在字符串中的下标相同，对于编程处理比较友好。从右开始约定的特点是，如果需要将测量结果按照整数解读，则这种方式刚好就是符合人类阅读习惯的二进制表示（低位在最右侧）。也许Qiskit和QPanda3采用从右开始约定主要是为了方便人类按照二进制形式阅读。

在这些量子开发框架的官方文档中，测量结果字符的顺序均未被重点提及，甚至只字未提。然而，如果要实现跨平台的量子程序开发，不同量子开发框架的测量结果字符顺序约定的差别需要被注意。

## 三、测量结果的解读
在利用`QProgramBuilder`类对象编译完量子程序（调用`build()`方法）后，量子程序的量子比特和存放测量结果的经典比特的分配就完成了，然后就可以调用运行结果解读的相关方法对结果进行解读。

### 单个0/1串的解读：`interpret_output_str()`方法
对代表一次测量的输出结果的`'0'`/`'1'`字符串，可以对已完成线路编译的`QProgramBuilder`对象调用`interpret_output_str()`方法，方法原型为：
```python
def interpret_output_str(self, output_str : str, framework : str = None) -> dict:
```

- `output_str`是代表一次测量结果的`'0'`/`'1'`字符串。请注意，**输入的字符串的长度必须与`QProgramBuilder`中的量子程序分配的存放测量结果的经典比特数相匹配**，且不能包含除`'0'`,`'1'`外的其他字符，否则会抛出`ResultInterpretError`异常。

    - 例如，前文程序`qmain1`、`qmain2`和`qmain4`中分配的经典比特数均为7，因此对编译这三个程序的`QProgramBuilder`类，`'0011001'`、`'1101111'`是调用`interpret_output_str()`方法的合法字符串，而`'110'`、`'1101'`、`'11+-abc'`不是合法字符串。

    - 程序`qmain3`中分配的经典比特数为4，因而`'1101'`是调用的合法字符串，而`'110'`、`'0011001'`不是合法的字符串。

    - 可以调用`QProgramBuilder`对象的`n_measure_cbits()`方法来获得分配的用于存放测量结果的经典比特数。

- `protocol`参数指定按照何种约定进行解读，目前支持两种协议：
    - `'l'`或`'L'`：按照从左开始约定进行解读（默认方式）；
    - `'r'`或`'R'`：按照从右开始约定进行解读。
    - 可以调用`QProgramBuilder`类的`framework_interpret_protocol()`静态方法获得具体框架的解读约定：
        
    ```python
    print(QProgramBuilder.framework_interpret_protocol('qiskit'))       # 返回'r'
    print(QProgramBuilder.framework_interpret_protocol('pyqpanda3'))    # 返回'r'
    print(QProgramBuilder.framework_interpret_protocol('pyquafu'))      # 返回'l'
    ```
        
- 返回值为解读得到的字典，该字典的结构为：

    `{变量名1: 值1, 变量名2: 值2, ...}`
    
    其中*变量名*为声明量子变量时传入的字符串（例如前面例子中的`'qarr1'`、`'qarr2'`），*值*为对于该量子变量的解读结果。对于复合类型的量子变量，还会对其元素或字段递归进行解读。

    - `Qubit`类型变量的测量结果将被解读为单个字符`'0'`或`'1'`；
    - `QubitArray`类型的变量的测量结果将被解读为`'0'`/`'1'`字符串；
    - 数组（QArray）类型的变量的测量结果将被解读为由其各元素的解读结果组成的列表。
    - 结构体（QStruct）类型变量的测量结果将被解读为以各字段变量名为键，以对应的字段的解读结果为值的字典。
    - 元组（QTuple）类型变量的测量结果将被解读为其各字段的解读结果组成的列表。
    - 联合体（QUnion）类型变量的测量结果将被解读为只包含一个活跃字段的`变量名 : 解读结果`字典。

**注： `interpret_output_str()`方法仅按照约定量子比特和经典比特的分配来解读结果字符串，因此其返回值仅与被编译程序的变量声明部分和测量操作部分有关，与函数主体无关。** 例如，程序`qmain1`和`qmain4`的变量声明部分和测量操作部分相同，仅有函数主体部分不同，因此对编译它们的`QProgramBuilder`对象调用`interpret_output_str()`方法的行为相同。

下面以`qmain4`来说明该方法的执行过程，我们首先利用`QProgramBuilder`编译`qmain4`，然后分别调用它的`n_qvars_qubits()`方法和`n_measure_cbits()`方法来获得为程序`qmain4`分配的量子比特数和经典比特数。
```python
qpb = QProgramBuilder()
qpb.build(qmain4)
print(qpb.n_qvars_qubits())     # -> 7
print(qpb.n_measure_cbits())    # -> 7
```

我们以`'1100101'`和从左开始约定来调用`interpret_output_str()`方法并打印返回值：
```python
print(qpb.interpret_output_str('1100101', 'l'))
```
输出结果为：
```
{'qarr1': '110', 'qarr2': '0101'}
```
按照程序`qmain4`的语义，变量`qarr1`的测量结果存放在第0~2号经典比特，采用从左开始约定时，字符串`'1100101'`的下标0~2构成的字串`'110'`即为变量`qarr1`对应的结果。同理，变量`qarr2`的测量结果存放在第3~6号经典比特，因而字符串`'1100101'`的下标3~6构成的字串`'0101'`即为变量`qarr1`对应的结果。

如果我们换用从右开始约定来解读同一个字符串`'1100101'`
```python
print(qpb.interpret_output_str('1100101', 'r'))
```
输出结果为：
```
{'qarr1': '101', 'qarr2': '0011'}
```
需要先反转字符串，字符的下标才能和各量子比特的相同下标相对应。`'1100101'`反转后为`'1010011'`，于是变量`qarr1`对应下标0~2构成的字串`'101'`，而变量`qarr2`对应下标3~6构成的字串`'0011'`。

### 结果字典的解读：`interpret_result_dict()`方法
`interpret_output_str()`方法只解读单个`'0'`/`'1'`字符串，而`interpret_result_dict()`方法可以解读由形如 `'0'/'1'字符串 : 出现次数` 的项构成的字典。在大多数量子开发框架中，量子线路运行的结果是正是这样形式的字典，因此可以直接对框架返回的测量结果进行解读。该函数的原型为：
```python
def interpret_result_dict(self, output_dict : dict, protocol : str = 'l') -> list:
```

- `output_dict`是测量结果字典。
- `protocol`参数指定按照何种约定进行解读，目前支持两种协议：
    - `'l'`或`'L'`：按照从左开始约定进行解读（默认方式）；
    - `'r'`或`'R'`：按照从右开始约定进行解读。
- 返回值为由元组 `(解读结果, 出现次数)` 构成的列表。

`interpret_result_dict()`方法会对传入参数`output_dict`的每个键调用`interpret_output_str()`方法进行解读，然后与对应的值组成形如 `(解读结果, 出现次数)` 的元组，返回值为由所有这样的元组构成的列表。

原始测量结果字典中，键是`'0'`/`'1'`字符串，字符串是hashable的，因而可以作为字典的键，进而构成形如 `'0'/'1'字符串 : 出现次数` 的项组成的字典。然而解读结果本身是一个字典，字典不是hashable的，不可作为字典的键，因此`interpret_result_dict()`方法的返回结果以列表形式表示，列表的每个元素是形如 `(解读结果, 出现次数)` 的元组。

**注：** 与`interpret_output_str()`方法类似，**`interpret_output_str()`方法的返回值仅与被编译程序的变量声明部分和测量操作部分有关，与函数主体无关。**
