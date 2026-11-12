# 自定义量子开发框架支持
PyQuantumKit采用“代码翻译”的方式将统一的量子线路构建代码翻译为不同量子开发平台上的相应代码，以实现跨平台支持。从PyQuantumKit v.0.2.1开始，允许用户添加自定义代码翻译脚本，以增加更多的量子开发框架和量子编程语言的支持。

这里需要区分术语“**量子开发框架**”和“**量子编程语言**”，因为PyQuantumKit对二者提供不同程度的支持。

本文中，**量子开发框架**指的是**用于支持量子线路编写第三方Python包**，例如qiskit、pyqpanda3、cqlib等。由于PyQuantumKit基于Python实现，因此对于这些Python包，PyQuantumKit提供较为完善的翻译过程支持，既支持生成文本形式的代码，也支持对这些开发包中的量子线路对象的直接操作。

与之相对应的是，**量子编程语言**指的是**独立的第三方量子编程语言**，例如Q\#、OpenQASM 2.0等。PyQuantumKit的翻译过程只支持生成文本形式的代码，不提供对这些语言具体代码的进一步操作。

## 一、编写翻译到量子编程语言的脚本
本文首先介绍如何编写翻译到量子编程语言的脚本，因为它相对简单。

### 翻译脚本中的动作和常量
代码翻译过程的实质是：给定用PyQuantumKit编写构建量子线路的代码，将构建过程的每一步分别翻译为对应量子编程语言中实现相应功能的代码。这里的“每一步”称为一个**动作**（Action），例如声明一个量子线路、应用一个量子门（调用`apply_gate()`函数）、应用一个测量操作等都是一个动作。翻译脚本给出了各类不同的动作如何进行翻译。此外，翻译脚本还需要包含一些在代码翻译过程中会用到的**常量**（Constant），例如标准库的名称、支持的量子子例程及其对应库的名称等。

在PyQuantumKit中，一个代码翻译脚本通常编写为一个Python文件（.py），文件中定义了表达翻译过程所需的一系列**常量**和**动作**。其中，“常量”实现为Python全局变量，而“动作”实现为Python函数。

具体而言，翻译到量子编程语言的脚本需要包含如下3个动作：`IMPORT`、`DECLARE`、`APPLY`；还需要包含如下2个常量的定义：`SUPPORT_SUBROUTINES`、`EXPORT_CONSTANTS`。为了强调，PyQuantumKit约定所有常量和动作的命名均采用全大写。下面分别介绍各个动作和常量的具体信息。

### 动作：IMPORT
在PyQuantumKit中，**特定动作需要实现为具有特定形参类型的函数，返回值为代表翻译结果的字符串，函数体描述了具体的动作如何实现。** 具体到`IMPORT`动作，它给出了“**导入包**”这一过程如何翻译到目标量子编程语言。它需要的函数原型为：

```python
def IMPORT(module_name : str) -> str:
    # 翻译过程
    # 返回翻译结果字符串
```

`IMPORT`动作需要接受一个参数`module_name`，指示要导入的包名。

这里用Python语言来说明函数体的编写，Python语言导入包使用的语法为`import xxx`，因此相应的函数体可写为：

```python
# 例：将“导入包”动作翻译为Python语法的函数体编写
def IMPORT(module_name : str) -> str:
    return "import " + module_name
```

### 动作：DECLARE
`DECLARE`动作给出了“**声明一个可应用量子操作的实体**”这一过程如何翻译到目标量子编程语言。这里“可应用量子操作的实体”指的是量子线路、量子比特寄存器等，通常为量子门的作用对象。`DECLARE`动作需要的函数原型为：

```python
def DECLARE(cir_name : str, module_name : str,
            mixed : bool, nqbits : int, ncbits : int) -> str:
```

- `cir_name`指示声明对象的名称（变量名）。
- `module_name`指示声明对象时需要引用的包名。
- `mixed`指示声明的对象只包含量子比特（`False`）还是允许既有量子比特又有经典比特（`True`）。引入此参数的原因是在某些开发框架中会做此类区分。
- `nqbits`指示声明对象包含的量子比特数。
- `ncbits`指示声明对象包含的经典比特数（当`mixed=False`时此项无效）。

### 动作：APPLY
`APPLY`动作给出了“**应用一个量子操作（门、测量、子例程）**”这一过程如何翻译到目标量子编程语言。`APPLY`动作需要的函数原型为：

```python
def APPLY(cir_name : str, module_name : str,
          op_name : str, qbits : list[int], paras : list,
          is_qsub : bool = False) -> str:
```

- `cir_name`指示要应用量子操作的实体（量子线路、量子比特寄存器对象）。
- `module_name`指示量子操作需要的包名。
- `op_name`指示要应用的量子操作名。
- `qbits`指示应用的量子比特下标数组。
- `paras`指示量子操作对应的经典参数。
- `is_qsub`指示应用的操作是否为量子子例程。

**`APPLY`动作是翻译脚本的核心，通常需要较大篇幅，需要仔细编写。** 具体的编写方式可参考[内置翻译脚本](./api/scripts.md)。

PyQuantumKit支持用不同的字符串来应用同一个门（例如`'CCX'`,`'CCNOT'`,`'Toffoli'`），因此，该函数通常需要先将`'op_name'`转换为PyQuantumKit中的统一的标准形式，然后再进行下一步操作。`pyquantumkit.translate.common`包提供了`get_standard_gatename()`函数，用于将非标准的量子门名称字符串转换为标准形式。`pyquantumkit.translate.common`的常变量`Standard_Gate_Name`给出了所有受支持的量子门的标准形式：

```python
Standard_Gate_Name = {
    'I', 'X', 'Y', 'Z', 'S', 'T', 'H', 'M',
    'CX', 'CY', 'CZ', 'CH', 'RX', 'RY', 'RZ', 'SW', 'ISW',
    'CRX', 'CRY', 'CRZ', 'RXX', 'RYY', 'RZZ', 'CSW',
    'CCX', 'CCZ', 'SD', 'TD', 'U1', 'CU1', 'U3',
    'SX', 'SXD', 'CS', 'CSD',
}
```

编写的翻译代码应当能处理以上所有门的翻译（[点此查看](./api/supported-gates.md)各量子门的具体定义）。如果目标平台不直接支持某个门，则应当翻译为等价的其他受支持门的组合。

测量操作通过将量子门名称指定为`'M'`来实现，此时参数`paras`为存放测量结果的经典比特数组。

### 常量：SUPPORT_SUBROUTINES
常量`SUPPORT_SUBROUTINES`是一个以字符串为键，字符串为值的字典，用于指示目标量子编程语言支持的子例程以及对应的库名称，用于支持`APPLY`动作中对应用量子子例程的翻译。注意字典的键对应`APPLY`动作的`op_name`参数传入的名称，而不是在目标量子编程语言中的名称。

例如，已知Q\#语言的标准库提供了量子傅里叶变换函数`ApplyQFT()`，它位于`Microsoft.Quantum.Canon`包。假设在PyQuantumKit中，应用量子傅里叶变换子例程的字符串为`'QFT'`。则为了支持对应用量子操作`'QFT'`的翻译，`SUPPORT_SUBROUTINES`需包含一项：

```
'QFT' : "Microsoft.Quantum.Canon"
```

### 常量：EXPORT_CONSTANTS
常量`EXPORT_CONSTANTS`是一个字典，指示导出到代码的过程中需要的一系列常量及其对应的值。对于翻译到量子编程语言的脚本，为了能够翻译为完整、独立的目标量子编程语言的代码，需要指定以下几个常量的值：

- `'comment'`：导出代码的开头注释；
- `'prefix'`：具体应用量子门的代码之前的代码块；
- `'suffix'`：具体应用量子门的代码之后的代码块；
- `'stdlib_name'`：目标语言标准库（通常为包含量子门的库）名称。

## 二、编写翻译到量子开发框架的脚本
对于翻译到量子开发框架的脚本，除了上述生成字符串的动作和常量`IMPORT`、`DECLARE`、`APPLY`、`SUPPORT_SUBROUTINES`、`EXPORT_CONSTANTS`外，还需要一组额外的动作和常量，它们用于对相应量子开发框架中的对象的操作。

### 动作：NEW
`NEW`动作执行语义上类似于“新建一个量子线路”的动作，其对应`DECLARE`动作的具体执行，可复用`DECLARE`动作的返回值。`NEW`动作需要的函数原型为：

```python
def NEW(mixed_circuit : bool, nqbits : int, ncbits : int) -> str:
```

这里以翻译为Qiskit的脚本的`NEW`动作来说明，为了方便说明，这里一并列出脚本的`EXPORT_CONSTANTS`常量和`DECLARE`和`NEW`动作：

```python
# Selected from translate script qiskit.py
EXPORT_CONSTANTS = {
    'comment' : "# Qiskit code exported from PyQuantumKit",
    'prefix' : "",
    'suffix' : "",
    'stdlib_name' : 'qiskit',
}

def DECLARE(cir_name : str, module_name : str,
            mixed : bool, nqbits : int, ncbits : int) -> str:
    circuit_type = "QuantumCircuit"
    declare_str = "" if cir_name is None else cir_name + " = "
    module_str = "" if module_name is None else module_name + "."
    if mixed:
        return f"{declare_str}{module_str}{circuit_type}({nqbits}, {ncbits})"
    else:
        return f"{declare_str}{module_str}{circuit_type}({nqbits})"

def NEW(mixed_circuit : bool, nqbits : int, ncbits : int) -> str:
    std = EXPORT_CONSTANTS['stdlib_name']
    return DECLARE(None, f"framework_modules('qiskit', '{std}')", mixed_circuit, nqbits, ncbits)
```

`NEW`动作复用了`DECLARE`动作的返回值，但是固定了前两个参数`cir_name`和`module_name`。当传入参数 `mixed_circuit=True`, `nqbits=3`, `ncbits=3`时，`NEW`动作的函数返回值为如下字符串：
```
"framework_modules('qiskit', 'qiskit').QuantumCircuit(3, 3)"
```

这里稍微解释一下为什么在`NEW`动作中`cir_name`和`module_name`要这样选取。事实上，在qiskit中声明一个量子线路变量的语法恰好为
```python
qc = qiskit.QuantumCircuit(3, 3)
```

为了能够支持不同量子开发框架的代码执行，PyQuantumKit维护了一个存储和查询导入的Python包的数据结构，用于对量子开发框架的包导入进行管理。利用函数`framework_modules(框架名, 包名)`可得到导入的包。

总之，**翻译到量子开发框架的脚本的这些额外动作（`NEW`, `GATE`, `SUBROUTINE`, `BITS`等），可视为生成代码动作（`IMPORT`, `DECLARE`, `APPLY`等）的固定特定参数的情形，所固定的这些参数使得代码可以在翻译过程中调用这些动作的环境下执行。**

### 动作：GATE和SUBROUTINE
`GATE`动作和`SUBROUTINE`动作执行语义上类似于“应用一个量子操作”的动作，其对应`APPLY`动作的具体执行，可复用`APPLY`动作的返回值。其中，`GATE`动作固定`is_qsub=False`，`SUBROUTINE`动作固定`is_qsub=True`。它们需要的函数原型为：

```python
def GATE(gate_name : str, qbits : list[int], paras : list) -> str:
def SUBROUTINE(qsub_name : str, qbits : list[int], paras : list) -> str:
```

以qiskit翻译脚本为例，它们的具体实现为：

```python
def GATE(gate_name : str, qbits : list[int], paras : list) -> str:
    return APPLY("qc", None, gate_name, qbits, paras, False)

def SUBROUTINE(qsub_name : str, qbits : list[int], paras : list) -> str:
    return APPLY("qc", None, qsub_name, qbits, paras, True)
```

PyQuantumKit约定，这里`cir_name`参数必须固定为`"qc"`。

### 动作：BITS
`BITS`动作执行语义上类似于“获得比特数”的动作，它们需要的函数原型为：

```python
def BITS(ret_cbit : bool, ret_list : bool) -> str:
```

- ret_cbit参数指定返回的是经典比特数（`True`）还是量子比特数（`False`）。
- ret_list参数指定返回的是数目（例如：4）还是下标列表（例如：`[0, 1, 2, 3]`）。

### 内部保留动作
PyQuantumKit还提供了几个内部保留动作，用于PyQuantumKit开发过程中的测试，对于用户自定义的翻译脚本，通常不需要指定这些动作。包括`CIRCUIT`、`MIXED_CIRCUIT`、`RUN`。

### 常量：INTERPRET_PROTOCOL
常量`INTERPRET_PROTOCOL`指定该量子开发框架的输出结果`'0'/'1'`字符串是按照从左开始约定（`'l'`）还是从右开始约定（`'r'`）。该常量主要用于高级语言级量子程序的运行结果解读，[点此查看](../program-level/guide/measure.md#_5)详情。

## 三、添加、测试与替换翻译脚本
用户可以调用`update_framework_translation`和`update_language_translation`函数添加或替换翻译脚本，其中前者用于翻译到量子开发框架的脚本（包含代码的执行），后者用于翻译到量子编程语言的脚本（仅包含代码生成，不包含代码执行）。

### 翻译到量子编程语言的脚本
函数`update_language_translation`的原型为：

```python
def update_language_translation(language_name : str, translate_rule_file : str) -> None:
```

- 参数`language_name`为要添加或修改的语言的名称。若名称尚未被添加，则添加该名称及对应的翻译规则到PyQuantumKit；否则，替换该名称对应的翻译规则（也可替换PyQuantumKit内置的翻译规则）。
- 参数`translate_rule_file`指定用于描述翻译规则的Python文件（省略`.py`），通常将翻译规则文件与调用`update_language_translation`的源文件放在同一文件夹下。

例如，设main.py为编写的量子主程序，在其中需要添加翻译脚本my_language.py。假设它们放于同一目录下：

```
my_project/
 |--- main.py
 |--- my_language.py
```

则在main.py中可以按如下添加翻译脚本：

```python title="main.py"
import pyquantumkit as pqk
# 添加my_language.py作为名称'My Language'对应的翻译脚本
pqk.update_language_translation('My Language', 'my_language')
```

### 翻译到量子开发框架的脚本
函数`update_framework_translation`的原型为：

```python
def update_framework_translation(framework_name : str, translate_rule_file : str, import_packages : list[str]) -> None:
```

- 参数`framework_name`为要添加或修改的量子开发框架的名称。若名称尚未被添加，则添加该名称及对应的翻译规则到PyQuantumKit；否则，替换该名称对应的翻译规则（也可替换PyQuantumKit内置的翻译规则）。
- 参数`translate_rule_file`指定用于描述翻译规则的Python文件（省略`.py`），通常将翻译规则文件与调用`update_language_translation`的源文件放在同一文件夹下。
- 参数`import_packages`给出翻译脚本中会用到的Python包的名称，这些包在翻译脚本中可通过`framework_modules(框架名, 包名)`来引用。

### 测试翻译脚本
PyQuantumKit提供了`test_code_translation`模块用于测试翻译脚本的编写。

#### 测试应用单个量子门的翻译
`test_apply_gate`函数用于测试应用单个量子门的代码翻译。例如，可用如下代码来测试并打印在qiskit中应用一个 $R_{xx}(0.123)$ 门到下标为0,2,4的量子比特的翻译结果：

```python
from pyquantumkit import *
import pyquantumkit.test_code_translation as TC
TC.test_apply_gate('qiskit', 'qc', 'Rxx', [0, 2, 4], [0.123])
```

输出为：

```
# Qiskit code exported from PyQuantumKit
from qiskit import *

qc = QuantumCircuit(5)
qc.rxx(0.123, 0, 2, 4)
```

开发者可以通过输出来检验翻译是否正确，只需要将第一个参数修改为自定义量子开发框架名称，即可对自定义翻译脚本进行测试。`test_apply_gate`函数的翻译结果包含前缀和后缀，原则上应是可以独立运行的代码。

#### 测试应用测量操作的翻译
`test_apply_measure`函数用于测试应用量子操作的代码翻译。

```python
from pyquantumkit import *
import pyquantumkit.test_code_translation as TC
TC.test_apply_measure('qsharp', 'qs', [0, 1, 2, 3, 4], [0, 1, 2, 3, 4])
```

输出为：

```
// Q# Code exported from PyQuantumKit
open Microsoft.Quantum.Core;
operation Main() : Unit
{
use qs = Qubit[5];
let c_0 = M(qs[0]); let c_1 = M(qs[1]); let c_2 = M(qs[2]); let c_3 = M(qs[3]); let c_4 = M(qs[4]); 
}
```

#### 测试所有量子门的翻译的有效性
`test_apply_gate_all`函数用于测试所有受PyQuantumKit支持的量子门的翻译。例如，下列代码测试并打印在`pyqpanda3`框架中应用所有量子门的结果。

```python
from pyquantumkit import *
import pyquantumkit.test_code_translation as TC
TC.test_apply_gate_all('pyqpanda3', 'qc')
```

输出为：

```
# PyQPanda3 code exported from PyQuantumKit
from pyqpanda3.core import *

qc = QProg(5)
qc << I(0)
qc << X(0)
qc << Y(1)
qc << Z(2)
qc << S(3)
qc << T(4)
qc << H(0)
qc << CNOT(1, 2)
qc << Y(4).control(3)
qc << CZ(0, 1)
qc << H(3).control(2)
qc << RX(4, 1.1)
qc << RY(0, 2.2)
qc << RZ(1, 3.3)
qc << SWAP(2, 3)
qc << ISWAP(4, 0)
qc << CRX(1, 3, 0.123)
qc << CRY(2, 4, 0.456)
qc << CRZ(0, 2, 0.789)
qc << RXX(1, 4, 3)
qc << RYY(0, 3, 2)
qc << RZZ(2, 1, 1)
qc << SWAP(1, 2).control(0)
qc << TOFFOLI(1, 2, 3)
qc << Z(4).control([2, 3])
qc << S(0).dagger()
qc << T(4).dagger()
qc << U1(1, -1)
qc << CR(2, 3, -2)
qc << U3(4, -3, 10.0, -0.002)
qc << H(0) << S(0) << H(0)
qc << H(1) << S(1).dagger() << H(1)
qc << S(3).control(2)
qc << S(4).dagger().control(2)
qc << measure(0, 0) << measure(1, 1) << measure(2, 2) << measure(3, 3) << measure(4, 4)
```

`test_apply_gate_all`函数会测试受PyQuantumKit支持但不受目标量子开发框架/语言支持的量子门。翻译脚本中应当能将此类门正确地翻译为受目标框架支持的门的等价组合，不应出现任何异常。
