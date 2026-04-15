# 量子线路的构建
## 一、基本构建
### 1.应用量子门

在PyquantumKit中，以统一的方式构建量子线路的关键是`apply_gate`函数，[点此查看](../api/construct.md#apply_gate)该函数的详细说明。下面用几个例子来说明函数的用法。

**例1**：在下标为2的量子位上应用一个S门，代码编写为：
```python
apply_gate(circuit, 'S', [2])
```
**详细说明**

- `circuit`是受支持的量子开发框架中的量子线路类的对象（例如qiskit的`QuantumCircuit`、pyqpanda3的`QCircuit`或`QProg`、quafu的`QuantumCircuit`或cqlib的`Circuit`）。
- 字符串`'S'`指示应用的是一个S门，[点此查看](../api/supported-gates.md)具体量子门对应的字符串。
- 数组`[2]`指示应用量子门的下标，数组元素个数应与门的比特数相同。

**例2**：对下标为0、2和3的量子位应用Toffoli门
```python
apply_gate(circuit, 'CCNOT', [0, 2, 3])
```

**例3**：对下标为1的量子位应用 $R_x$ 门，参数 $\theta=0.1$
```python
apply_gate(circuit, 'Rx', [1], [0.1])
```

- 第四个参数`[0.1]`用于指示量子门的参数，对于无参数门，此参数省略。

**例4**：对下标为0的量子位应用 $U_3$ 门，参数 $\theta=0.2,\phi=0.3,\lambda=0.4$
```python
apply_gate(circuit, 'U3', [0], [0.2, 0.3, 0.4])
```

### 2. 应用测量

在PyquantumKit中，`apply_measure`函数可以测量一个或一组量子比特，并将结果写入指定的经典比特中。

**例5**：测量下标为2的量子比特，并将结果存入下标为0的经典比特中
```python
apply_measure(circuit, [2], [0])
```

**例6**：测量下标为0~4的量子比特（一共5个），并将结果存入下标为0~4的经典比特中
```python
apply_measure(circuit, [0, 1, 2, 3, 4], [0, 1, 2, 3, 4])
```
或
```python
apply_measure(circuit, range(5), range(5))
```

## 二、量子线路的模块化构建（实验性）

**注1：此节内容可能只适用于部分量子开发平台**，[点此查看详情](../api/supported-platforms.md)。

Coming soon

## 三、CircuitIO类
PyQuantumKit提供了一个CircuitIO类，用于暂存构建的量子线路。CircuitIO类可以像一个量子开发框架的量子线路类一样使用，也可以对其执行`apply_gate`, `apply_measure`等操作。CircuitIO对象保存了量子线路的信息，随后可以格式化输出为字符串或插入具体的量子开发框架的量子线路对象中。

以下代码定义了一个包含2个量子比特的CircuitIO对象

```python
import pyquantumkit as PQK

cio = PQK.CircuitIO(2, 2)        # define a CircuitIO object
PQK.apply_gate(cio, 'H', [0])    # Use generic function <gate_apply>
cio.apply_gate('CX', [0, 1])     # Use CircuitIO member function <gate_apply>
```

[点此查看](../api/circuitio.md)CircuitIO类的具体成员函数。

### 3.1 利用CircuitIO类在不受支持的量子开发平台上构造

由于某些量子开发框架不支持自动生成逆线路和量子比特的重映射，可以利用CircuitIO对象间接完成构造：先在CircuitIO对象上构造线路并生成逆线路或重映射（使用`inverse`和`remap_qbits`、`remap_cbits`成员函数），然后利用`>>`运算符（或等价的，`append_into_actual_circuit`成员函数）将CircuitIO包含的量子线路插入到具体量子开发框架的量子线路中。

```python
# quafu framework does not support qubits remap and circuit auto-inverse
# Here we use CircuitIO object to implement indirectly
cio.inverse()              # inverse the circuit in CircuitIO object cio
cio.remap_qbits([1, 0])    # remap the circuit in cio
quafu_circuit = quafu.QuantumCircuit(2, 2)
cio >> quafu_circuit       # insert the CircuitIO object cio into quafu's circuit
```

### 3.2 利用CircuitIO类导出代码

可以使用CircuitIO类的`get_circuit_code`函数将量子线路转换为受支持的框架或语言的代码（[点此查看](../api/supported-platforms.md)受支持的框架和语言）。

下面的例子给出了一个将CircuitIO对象中的量子线路导出为qiskit代码和Microsoft Q#代码的例子。

```python
# import PyQuantumKit
import pyquantumkit as PQK

# Define the unified quantum circuit construction function using PyQuantumKit
def ghz_state(circuit, nqbits : int):
    PQK.apply_gate(circuit, 'H', [0])               # Apply H gate on qubit with index 0
    for i in range(1, nqbits):
        PQK.apply_gate(circuit, 'cnot', [0, i])     # Apply CNOT gate on qubit with index 0 and i
    # Measure all qubits

cio = PQK.CircuitIO(5)
ghz_state(cio, 5)

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
