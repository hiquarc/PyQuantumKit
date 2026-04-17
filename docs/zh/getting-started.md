# 安装与使用
## 安装PyQuantumKit

使用`pip install`命令可安装PyQuantumKit

```sh
pip install pyquantumkit
```

PyQuantumKit要求Python版本>=3.8，且依赖如下Python包：

- sympy >= 1.8
- numpy >= 1.22.0

通常，PyQuantumKit需要与受支持的基于Python的量子开发框架（例如qiskit或pyqpanda3等）联合使用。可以在安装PyQuantumKit的同时安装受支持的量子开发框架，例如，使用如下命令在安装PyQuantumKit的同时安装qiskit：

```sh
pip install "pyquantumkit[qiskit]"
```

## GitHub

PyQuantumKit是基于MIT协议的开源软件，[点此访问](https://github.com/hiquarc/PyQuantumKit)PyQuantumKit的GitHub仓库。

使用`git clone`命令将PyQuantumKit仓库复制到本地：

```sh
git clone https://github.com/hiquarc/PyQuantumKit.git
```

## 使用示例
这里以一个简单的示例来说明如何利用PyQuantumKit在不同的量子开发框架上以统一的方式构建量子线路。

需求：构造一个生成GHZ状态的量子线路，运行1000次并获得测量的统计结果。编写一次代码，分别使用qiskit、pyqpanda3和quafu三个量子开发框架构建量子线路，打印构建的量子线路及在模拟器上运行的结果。

### 1. 导入需要的量子开发包和PyQuantumKit

**注意：**在Python代码中，**`import pyquantumkit`需放置在具体的量子开发包的导入之后**，以确保PyQuantumKit能识别已导入的量子开发包模块。

```python
# import quantum development kits.
import pyqpanda3.core as qpanda
import qiskit, qiskit_aer
import quafu

# import PyQuantumKit
# NOTE: the import of pyquantumkit must be put behind the quantum development kits.
import pyquantumkit as PQK
```

### 2. 利用PyQuantumKit提供的函数编写线路
这里用到了`apply_gate`和`apply_measure`两个函数，[点此查看](stable/circuit.md)函数详情。

```python
def ghz_state(circuit, nqbits : int):
    PQK.apply_gate(circuit, 'H', [0])               # Apply H gate on qubit with index 0
    for i in range(1, nqbits):
        PQK.apply_gate(circuit, 'cnot', [0, i])     # Apply CNOT gate on qubit with index 0 and i
    # Measure all qubits
    PQK.apply_measure(circuit, range(nqbits), range(nqbits))
```

### 3. 设定运行参数
这里使用5个qubit，运行轮数为1000：

```python
# The number of qubits
Nqs = 5
# The number of running shots
Nshots = 1000
```

### 4. 在qiskit上运行

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
![qiskit运行结果](../imgs/ghz_qiskit.jpg)

### 5. 在pyqpanda3上运行

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
![qpanda运行结果](../imgs/ghz_qpanda.jpg)

### 6. 在quafu上运行

```python
print(' ### Run on quafu ### ')

quafu_circuit = quafu.QuantumCircuit(Nqs, Nqs)
ghz_state(quafu_circuit, Nqs)    # unified quantum circuit construction
quafu_circuit.draw_circuit()     # print quantum circuit

quafu_result = quafu.simulate(quafu_circuit, shots = Nshots)
print(quafu_result.counts)    # print running results
```

运行结果为：
![quafu运行结果](../imgs/ghz_quafu.jpg)

