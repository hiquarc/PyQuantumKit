# 量子线路的构建
## 一、应用量子门和测量
### 1.1 应用量子门：apply_gate函数

以统一的方式构建量子线路的关键是`apply_gate`函数，该函数的原型为：


例1：在下标为2的量子位上应用一个S门
```python
apply_gate(circuit, 'S', [2])
```

例2：对下标为0、2和3的量子位应用Toffoli门
```python
apply_gate(circuit, 'CCNOT', [0, 2, 3])
```

例3：对下标为1的量子位应用 $R_x$ 门，参数 $\theta=0.1$
```python
apply_gate(circuit, 'Rx', [1], [0.1])
```

例4：对下标为0的量子位应用 $U_3$ 门，参数 $\theta=0.2,\phi=0.3,\lambda=0.4$
```python
apply_gate(circuit, 'U3', [0], [0.2, 0.3, 0.4])
```

### 1.2 测量：apply_measure函数



## 二、量子线路的模块化构建（实验性）

**注1：此节内容可能只适用于部分量子开发平台**，[点此查看详情](../api/supported-platforms.md)。

除了上述基本的应用量子门和测量外，

## 三、CircuitIO类
PyQuantumKit提供了一个CircuitIO类，用于暂存构建的量子线路。CircuitIO类可以像一个量子开发框架的量子线路类一样使用，也可以对其执行`apply_gate`, `apply_measure`等操作。CircuitIO对象保存了量子线路的信息，随后可以格式化输出为字符串或插入具体的量子开发框架的量子线路对象中。

以下代码定义了一个包含2个量子比特的CircuitIO对象

```python
import pyquantumkit as PQK

cio = PQK.CircuitIO(2, 2)        # define a CircuitIO object
PQK.apply_gate(cio, 'H', [0])    # Use generic function <gate_apply>
cio.apply_gate('CX', [0, 1])     # Use CircuitIO member function <gate_apply>
```

点此查看CircuitIO类的具体成员函数。

### 3.1 利用CircuitIO类在不受支持的量子开发平台上构造

由于某些量子开发框架不支持自动生成逆线路和量子比特的重映射，可以利用CircuitIO类间接完成构造：先在CircuitIO对象上构造线路并生成逆线路或重映射（使用`inverse`和`remap_qbits`、`remap_cbits`成员函数），然后利用`>>`运算符（或等价的，`append_into_actual_circuit`成员函数）将CircuitIO包含的量子线路插入到具体量子开发框架的量子线路中。

```python
# quafu framework does not support qubits remap and circuit auto-inverse
# Here we use CircuitIO object to implement indirectly
cio.inverse()              # inverse the circuit in CircuitIO object cio
cio.remap_qbits([1, 0])    # remap the circuit in cio
quafu_circuit = quafu.QuantumCircuit(2, 2)
cio >> quafu_circuit       # insert the CircuitIO object cio into quafu's circuit
```

### 3.2 利用CircuitIO类导出代码
