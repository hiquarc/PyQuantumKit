# 量子线路的构建
## 一、基本构建
### 1. 应用量子门

在PyquantumKit中，以统一的方式构建量子线路的关键是`apply_gate`函数，下面用几个例子来说明函数的用法。

**例1**. 在下标为2的量子位上应用一个S门，代码编写为
```python
apply_gate(circuit, 'S', [2])
```
**详细说明**

- `circuit`是受支持的量子开发框架中的量子线路类的对象（例如qiskit的`QuantumCircuit`、pyqpanda3的`QCircuit`或`QProg`、quafu的`QuantumCircuit`或cqlib的`Circuit`）。
- 字符串`'S'`指示应用的是一个S门，[点此查看](./api/supported-gates.md)具体量子门对应的字符串。
- 数组`[2]`指示应用量子门的下标，数组元素个数应与门的比特数相同。注意无论量子门是单比特还是多比特，都需要**以列表的方式指派此参数**。

**例2**. 对下标为0、2和3的量子位应用Toffoli门
```python
apply_gate(circuit, 'CCNOT', [0, 2, 3])
```

**例3**. 对下标为1的量子位应用 $R_x$ 门，参数 $\theta=0.1$
```python
apply_gate(circuit, 'Rx', [1], [0.1])
```

- 第四个参数`[0.1]`用于指示量子门的参数，对于无参数门，此参数省略。

**例4**. 对下标为0的量子位应用 $U_3$ 门，参数 $\theta=0.2,\phi=0.3,\lambda=0.4$
```python
apply_gate(circuit, 'U3', [0], [0.2, 0.3, 0.4])
```

以上给出了`apply_gate`函数的4个使用例子，**对于该函数更详细说明，请[点此查看](./api/construct.md#apply_gate)。**

### 2. 应用测量

在PyquantumKit中，`apply_measure`函数可以测量一个或一组量子比特，并将结果写入指定的经典比特中。

**例5**. 测量下标为2的量子比特，并将结果存入下标为0的经典比特中
```python
apply_measure(circuit, [2], [0])
```

**例6**. 测量下标为0~4的量子比特（一共5个），并将结果存入下标为0~4的经典比特中。有两种代码编写方式，第一种是使用数组分别指定每一个比特对应的下标：
```python
apply_measure(circuit, [0, 1, 2, 3, 4], [0, 1, 2, 3, 4])
```
第二种是使用`range`函数指定下标范围：
```python
apply_measure(circuit, range(5), range(5))
```

## 二、量子线路的模块化构建（实验性）

- **注1：此节内容可能只适用于部分量子开发框架**，[点此查看详情](./api/supported-platforms.md)。
- **注2：此功能为实验性功能，未经过系统性的测试，且接口在未来可能改变，请谨慎使用。**
- **注3：当前若需要使用模块化构建，推荐使用CircuitIO类（见下文）**

[点此查看](../experimental/construct.md)量子线路的模块化构建具体内容。

## 三、CircuitIO类
PyQuantumKit提供了一个CircuitIO类，用于暂存构建的量子线路。CircuitIO类可以像一个量子开发框架的量子线路类一样使用，也可以对其执行`apply_gate`, `apply_measure`等操作。CircuitIO对象保存了量子线路的信息，随后可以格式化输出为代码字符串或插入具体的量子开发框架的量子线路对象中。

**例7**. 以下代码定义了一个包含2个量子比特、2个经典比特的CircuitIO对象，其上构建了一个制备Bell态的量子线路：

```python
import pyquantumkit

cio = pyquantumkit.CircuitIO(2, 2)        # define a CircuitIO object
pyquantumkit.apply_gate(cio, 'H', [0])    # Use generic function <gate_apply>
cio.apply_gate('CX', [0, 1])              # Use CircuitIO member function <gate_apply>
```

在CircuitIO对象上应用量子门，可以直接使用通用的`apply_gate`函数，将CircuitIO对象作为量子线路对象传入；也可以使用CircuitIO类提供的同名成员函数`CircuitIO.apply_gate`。

**CircuitIO类包含的成员函数的详细说明请[点此查看](./api/circuitio.md)。** 下面给出CircuitIO类的三个典型用法。

### 1. 利用CircuitIO类在不受支持的量子开发平台上进行量子线路的模块化构建

某些量子开发框架不支持*自动生成逆线路*和*量子比特的重映射*等的量子线路模块化构建功能，此时可以利用CircuitIO对象间接完成构造：先在CircuitIO对象上构造线路并生成逆线路或重映射（使用`inverse`和`remap_qbits`、`remap_cbits`成员函数），然后利用`>>`运算符（或等价的，`append_into_actual_circuit`成员函数）将CircuitIO包含的量子线路插入到具体量子开发框架的量子线路中。

**例8**. Quafu框架不支持量子比特重映射和自动生成逆线路，以下代码通过利用CircuitIO对象来间接实现。我们定义了一个CircuitIO对象，在其上执行量子比特重映射和转换为逆线路，最后将CircuitIO对象上的线路输出到Quafu框架。

```python
import quafu
import pyquantumkit

cio = pyquantumkit.CircuitIO(2, 2)
pyquantumkit.apply_gate(cio, 'H', [0])
cio.apply_gate('CX', [0, 1])

cio.inverse()              # inverse the circuit in CircuitIO object cio
cio.remap_qbits([1, 0])    # remap the circuit in cio

quafu_circuit = quafu.QuantumCircuit(2, 2)
cio >> quafu_circuit       # insert the CircuitIO object cio into quafu's circuit
```

### 2. 利用CircuitIO类导出代码

可以使用CircuitIO类的`get_circuit_code`函数将量子线路转换为受支持的框架或语言的代码（[点此查看](./api/supported-platforms.md)受支持的框架和语言）。函数的输出为一个字符串，可以复制到源代码文件中。

**例9**. 利用CircuitIO类构建生成GHZ态，并导出为qiskit代码和Microsoft Q#的代码。

```python
# import PyQuantumKit
import pyquantumkit as PQK

# Define the unified quantum circuit construction function using PyQuantumKit
def ghz_state(circuit, nqbits : int):
    PQK.apply_gate(circuit, 'H', [0])               # Apply H gate on qubit with index 0
    for i in range(1, nqbits):
        PQK.apply_gate(circuit, 'cnot', [0, i])     # Apply CNOT gate on qubit with index 0 and i

Nqs = 5     # Set the numnber of qubits
cio = PQK.CircuitIO(Nqs)
ghz_state(cio, Nqs)     # Construct circuits on CircuitIO object

qiskit_code = cio.get_circuit_code('qiskit', 'qc')     # Output the circuit into qiskit code
print(qiskit_code)

qsharp_code = cio.get_circuit_code('QSharp', 'qs')     # Output the circuit into Q# code
print(qsharp_code)
```

输出结果为：
```python
qc.h(0)
qc.cx(0, 1)
qc.cx(0, 2)
qc.cx(0, 3)
qc.cx(0, 4)
```
```csharp
H(qs[0]);
CNOT(qs[0], qs[1]);
CNOT(qs[0], qs[2]);
CNOT(qs[0], qs[3]);
CNOT(qs[0], qs[4]);
```

### 3. 利用CircuitIO类进行符号表示和运算
PyQuantumKit支持量子线路矩阵的符号表示（基于SymPy实现）。在CircuitIO对象上构建量子线路时，对于带参数量子门，其参数除了使用数值（`int`和`float`类型）外，还支持使用SymPy符号变量或表达式。并且在将量子线路输出到具体开发框架上时，可以对SymPy变量进行赋值，将其转换为这些开发框架上支持的数值类型。

**例10**. 利用CircuitIO对象应用 $R_{xx}(\alpha+\beta)$ 门，其中 $\alpha$, $\beta$ 表示为符号变量。然后代入数值 $\alpha=0.5$, $\beta=0.7$ 后，将量子线路输出到quafu框架。

```python
import quafu
import pyquantumkit
import sympy

alpha_ = sympy.Symbol('alpha')
beta_ = sympy.Symbol('theta')

cio = PQK.CircuitIO(3)
cio.apply_gate('Rxx', [1, 2], [alpha_ + beta_])     # Use SymPy symbol expression as the parameter

# Insert the CircuitIO object cio into quafu's circuit, assigning alpha_ = 0.5, beta_ = 0.7
quafu_circuit = quafu.QuantumCircuit(3, 3)
cio.append_into_actual_circuit(qpanda_circuit, {alpha_ : 0.5, beta_ : 0.7})
```

关于如何利用PyQuantumKit进行符号表示和运算的更详细的内容，请[点此查看](./symbol.md)。
