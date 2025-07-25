# PyQuantumKit简介

PyQuantumKit是一个基于Python的量子软件开发辅助工具，设计目标包括：

- 提供统一的方式在不同的基于Python的量子软件栈上构建量子线路，实现代码复用；
- 提供常用的量子算法和开发辅助功能，提升量子软件开发效率和正确性；
- 软件架构具有扩展性，未来可方便地添加更多的功能和量子软件栈的支持。

## 一、安装说明

PyQuantumKit无法单独使用，需要与至少一个受支持的量子软件栈联合使用，请确保您已安装需要使用的量子软件栈。

**注意：**在Python代码中，**`import pyquantumkit`需放置在对量子软件栈的导入之后**，以确保PyQuantumKit能识别已导入的量子软件栈模块。

## 二、使用示例

这里以一个简单的示例来说明如何利用PyQuantumKit在不同的量子软件栈构建量子线路，本例是`./examples/ghz_state.py`。

需求：构造一个生成GHZ状态的量子线路，运行1000次并获得测量的统计结果。编写一次代码，分别使用qiskit、pyqpanda3和quafu三个量子软件栈的模拟器运行。

#### 1. 导入需要的量子软件栈和PyQuantumKit

**请注意pyquantumkit需在量子软件栈之后导入**

```python
# import quantum software stacks
import pyqpanda3.core as qpanda
import qiskit, qiskit_aer
import quafu
# import PyQuantumKit
import pyquantumkit as PQK
```

#### 2. 利用PyQuantumKit提供的函数编写线路

```python
def ghz_state(circuit, nqbits : int):
    PQK.apply_gate(circuit, 'H', [0])               # Apply H gate on qubit with index 0
    for i in range(1, nqbits):
        PQK.apply_gate(circuit, 'cnot', [0, i])     # Apply CNOT gate on qubit with index 0 and i
    # Measure all qubits
    PQK.apply_measure(circuit, range(nqbits), range(nqbits))
```

#### 3. 设定运行参数
这里使用5个qubit，运行轮数为1000

```python
# The number of qubits
Nqs = 5
# The number of running shots
Nshots = 1000
```

#### 4. 在qiskit上运行

```python
print(' ### Run on qiskit ### ')

qiskit_circuit = qiskit.QuantumCircuit(Nqs, Nqs)
ghz_state(qiskit_circuit, Nqs)    # unified quantum circuit construction
print(qiskit_circuit)             # print quantum circuit

qiskit_qvm = qiskit_aer.Aer.get_backend('aer_simulator')
qiskit_job = qiskit_qvm.run(qiskit_circuit, shots = Nshots)
qiskit_result = qiskit_job.result().get_counts()
print(qiskit_result)        # print running results
```

运行结果为：
![qiskit运行结果](./_readme_imgs/ghz_qiskit.jpg)

#### 5. 在pyqpanda3上运行

```python
print(' ### Run on pyqpanda3 ### ')

qpanda_circuit = qpanda.QProg(Nqs)
ghz_state(qpanda_circuit, Nqs)    # unified quantum circuit construction
print(qpanda_circuit)             # print quantum circuit

qpanda_qvm = qpanda.CPUQVM()
qpanda_qvm.run(qpanda_circuit, Nshots)
qpanda_result = qpanda_qvm.result().get_counts()
print(qpanda_result)        # print running results
```

运行结果为：
![qpanda运行结果](./_readme_imgs/ghz_qpanda.jpg)

#### 6. 在quafu上运行

```python
print(' ### Run on quafu ### ')

quafu_circuit = quafu.QuantumCircuit(Nqs, Nqs)
ghz_state(quafu_circuit, Nqs)    # unified quantum circuit construction
quafu_circuit.draw_circuit()     # print quantum circuit

quafu_result = quafu.simulate(quafu_circuit, shots = Nshots)
print(quafu_result.counts)    # print running results
```

运行结果为：
![quafu运行结果](./_readme_imgs/ghz_quafu.jpg)

#### 7. 更多的例子可在`./examples`文件夹下找到。

## 三、功能简介

基于v.0.1.2版本

### 3.1 当前支持的量子软件栈

PyQuantumKit采用“代码翻译”的方式实现对多个量子软件栈的支持，通过识别函数参数中的量子线路的类型及其所属的量子软件栈，将该函数调用翻译为对应量子软件栈的调用代码。当前支持的量子软件栈如下：

- qiskit
- pyqpanda3
- quafu（仅支持量子线路构建）

### 3.2 apply_gate函数简介

以统一的方式构建量子线路的关键是`apply_gate`函数，该函数的原型为：

```python
def apply_gate(q_circuit, gate_str : str, qbits : list[int], paras : list = None)
```

- 参数`q_circuit`指定目标量子线路，它的类型是各量子软件栈的量子线路类（例如qiskit的`QuantumCircuit`，或pyqpanda3的`QCircuit`或`QProg`）。函数将根据此参数所属的量子软件栈，将对量子门的应用翻译为对应量子软件栈的代码。
- 参数`gate_str`是一个字符串，用于指示需要应用的门。考虑到同一个门可能有多个不同的名称（例如Toffoli,CCNOT,CCX都表示同一个门），PyQuantumKit允许以不同的名字字符串来表示同一个门，且不区分大小写。具体支持的字符串见本节后面的说明。
- 参数`qbits`是一个整数列表，指定门要应用的量子比特下标。注意无论量子门是单比特还是多比特，都需要以列表的方式指派此参数。
- 参数`paras`是一个列表，用于为含参数门指派参数，参见本节后面“含参数门”部分；对于无参数门，不用指派此参数。


#### 单比特门

- I门：i, id
- X门：x
- Y门：y
- Z门：z
- S门：s
- T门：t
- H门：h
- $S^{\dagger}$ 门：sd, sdg, sdag, sdagger
- $T^{\dagger}$ 门：td, tdg, tdag, tdagger

例：在下标为2的量子位上应用一个S门
`apply_gate(circuit, 'S', [2])`

#### 多比特门

- CNOT门：cnot, cx
- CZ门：cz
- CY门：cy
- CH门：ch
- SWAP门：swap, sw
- iSWAP门：iswap, isw
- Toffoli门：toffoli, ccx, ccnot
- Fredkin门：fredkin, cswap, csw

例：对下标为0、2和3的量子位应用Toffoli门
`apply_gate(circuit, 'CCNOT', [0, 2, 3])`

#### 含参数门

- $R_x(\theta)$ 门：rx
- $R_y(\theta)$ 门：ry
- $R_z(\theta)$ 门：rz
- $R_1(\theta)$ 门：u1, r1, p
- 受控 $R_x(\theta)$ 门：crx
- 受控 $R_y(\theta)$ 门：cry
- 受控 $R_z(\theta)$ 门：crz
- 受控 $R_1(\theta)$ 门：cu1, cr1, cp
- $R_{xx}(\theta)$ 门：rxx
- $R_{yy}(\theta)$ 门：ryy
- $R_{zz}(\theta)$ 门：rzz
- $U_3(\theta,\phi,\lambda)$ 门：u3, u

含参数门需要使用`apply_gate`函数的第四个参数来指派参数。

例：对下标为1的量子位应用 $R_x$ 门，参数 $\theta=0.1$
`apply_gate(circuit, 'Rx', [1], [0.1])`

例：对下标为0的量子位应用 $U_3$ 门，参数 $\theta=0.2,\phi=0.3,\lambda=0.4$
`apply_gate(circuit, 'U3', [0], [0.2, 0.3, 0.4])`

### 3.3 apply_measure函数简介

`apply_measure`函数测量目标量子比特，函数原型为：

```python
def apply_measure(q_circuit, qindex : list[int], cindex : list[int])
```

- 参数`q_circuit`指定目标量子线路。
- 参数`qindex`是一个整数列表，指定要测量的量子比特下标。
- 参数`cindex`是一个整数列表，指定测量结果存放的经典比特下标。`qindex`和`cindex`各分量分别对应，因此`qindex`和`cindex`长度应相同。

### 3.4 CircuitIO类简介

PyQuantumKit提供了一个`CircuitIO`类，用于暂存构建的量子线路以及控制格式化输入输出。

`CircuitIO`类可以像一个量子软件栈的量子线路类一样使用，也可以对其执行`apply_gate`, `apply_measure`等操作。`CircuitIO`对象保存了量子线路的信息，随后可以格式化输出为字符串或插入具体的量子软件栈的量子线路对象中。

```python
cio = PQK.CircuitIO(2, 2)        # define a CircuitIO object
PQK.apply_gate(cio, 'H', [0])    # Use generic function <gate_apply>
cio.apply_gate('CX', [0, 1])     # Use CircuitIO member function <gate_apply>
```

由于某些量子软件栈不支持自动生成逆线路和量子比特的重映射，可以利用`CircuitIO`类间接完成构造：先在CircuitIO对象上构造线路并生成逆线路或重映射（使用`inverse`和`remap_qbits`、`remap_cbits`成员函数），然后利用`>>`运算符（或等价的，`append_into_actual_circuit`成员函数）将CircuitIO包含的量子线路插入到具体量子软件栈的量子线路中。

```python
# quafu framework does not support qubits remap and circuit auto-inverse
# Here we use CircuitIO object to implement indirectly
cio.inverse()              # inverse the circuit in CircuitIO object cio
cio.remap_qbits([1, 0])    # remap the circuit in cio
quafu_circuit = quafu.QuantumCircuit(2, 2)
cio >> quafu_circuit       # insert the CircuitIO object cio into quafu's circuit
```

### 一些尚处于实验阶段的功能

这些功能尚处于实验阶段，未经过系统测试，且接口在未来可能改变，请谨慎使用。

#### 模块化量子线路构建

量子线路/程序的新建、复制、串联、并联： `new_circuit`, `new_program`, `copy_circuit`, `copy_program`, `append_circuit`, `append_program`, `parallel_circuits`, `parallel_programs`

获取量子线路的经典比特/量子比特数目： `get_n_qubits`, `get_n_cbits`, `get_qubit_list`, `get_cbit_list`

生成量子线路的逆版本或重排量子比特的版本： `derivative`

Pauli测量： `apply_measure_x`, `apply_measure_y`, `apply_measure_z`, `apply_pauli_measure`

以统一的方式运行量子线路： `run_and_get_counts`

#### classical/run_result模块：运行结果分析

从运行结果字典中提取一个量子比特子集的结果的字典：`count_subset_of_result_dict`, `count_first_bits_of_result_dict`, `count_last_bits_of_result_dict`

提取出现的运行结果集合：`get_result_str_set`

#### state_prepare模块：提供一些量子态制备算法

根据一个字符串制备状态： `create_state_by_01pm`, `uncompute_state_by_01pm`, `create_state_by_sqgate_str`, `uncompute_state_by_sqgate_str`

计算基态 $\ket{x}$ ： `create_ket_int_le`, `create_ket_int_be`, `uncompute_ket_int_le`, `uncompute_ket_int_be`

互补叠加态 $\frac{1}{\sqrt2}(\ket{x}+e^{i\phi}\ket{\bar{x}})$ ，其中 $\bar{x}$ 是 $x$ 的按位取反， $e^{i\phi}$ 是相对相位： `create_ket_int_plus_eiphi_neg_le`, `create_ket_int_plus_eiphi_neg_be`, `uncompute_ket_int_plus_eiphi_neg_le`, `uncompute_ket_int_plus_eiphi_neg_be`

二值叠加态 $\frac{1}{\sqrt2}(\ket{x}+e^{i\phi}\ket{y})$ ： `create_ket_int1_plus_eiphi_ket_int2_le`, `create_ket_int1_plus_eiphi_ket_int2_be`, `uncompute_ket_int1_plus_eiphi_ket_int2_le`, `uncompute_ket_int1_plus_eiphi_ket_int2_be`

Pauli算子的本征态： `create_pauli_eigenstate`, `uncompute_pauli_eigenstate`

#### library模块：提供一些常用量子算法

交换测试（Swap Test）、量子态层析（Tomography）、量子傅里叶变换（QFT）

#### program_check模块：提供量子程序性质检验算法

此模块基于论文 https://arxiv.org/abs/2307.01481 实现。

等价性检验： `run_equivalence_check`
恒同性检验： `run_identity_check`
幺正性检验： `run_unitarity_check`
保持纯态检验： `run_keep_purity_check`
保持计算基态检验： `run_keep_basis_check`


## 四、联系我们

PyQuantumKit由中国科学院高能物理研究所计算中心研发。

项目负责人：龙沛洵
longpx@ihep.ac.cn

## 五、版本历史

2025/7/25 v.0.1.2
- 新增CircuitIO类，用于量子线路的格式化操作
- 修改了应用门的代码的翻译方式，以适应CircuitIO类输出为用户可读代码的功能

2025/7/10 v.0.1.1
- 首个预览版本 (v.0.1.1) 发布
