### 量子哈密顿量模拟算法
**注意：此功能为实验性功能，未经过系统性的测试，且接口在未来可能改变，请谨慎使用。**

PyquantumKit提供了一个量子哈密顿量模拟的算法库，可用于构建量子哈密顿量模拟程序。量子哈密顿量模拟算法即实现变换： $U=e^{-iHt}$ ，其中 $H$ 为代表量子系统哈密顿量的厄密矩阵， $t$ 为设定的演化时间。

PyQuantumKit目前支持以Pauli算子的线性组合形式表示哈密顿量：

$$H=\sum_{i_1,i_2,\dots,i_n\in\{0,1,2,3\}} k_{i_1,i_2,\dots i_n} \sigma_{i_1}\otimes\sigma_{i_2}\otimes \dots \otimes\sigma_{i_n}$$

每一项对应一个 $n$ 比特Pauli算子，它是单比特Pauli算子的张量积， $k_{i_1,i_2,\dots i_n} \in \mathbb{R}$ 为该Pauli算子对应的线性组合系数，求和至多 $4^n$ 项。有4个单比特Pauli算子：

$$\sigma_0 = \left[\begin{array}{cc}1&0\\0&1\end{array}\right], \sigma_1 = \left[\begin{array}{cc}0&1\\1&0\end{array}\right], \sigma_2 = \left[\begin{array}{cc}0&-i\\i&0\end{array}\right], \sigma_3 = \left[\begin{array}{cc}1&0\\0&-1\end{array}\right]$$

实际的哈密顿量往往具有稀疏性，即 $4^n$ 个组合系数中只有 $O(n)$ 个不为0，因此对哈密顿量的模拟可以分解为对各Pauli矩阵形式的模拟的组合。

设总哈密顿量可以写成 $m$ 个局部哈密顿量之和 $H=H_1+H_2+\dots+H_m$ ，若这 $m$ 个局部哈密顿量两两对易（即乘法可交换： $\forall i\neq j, H_iH_j=H_jH_i$ ），则对总哈密顿量的模拟可以严格分解为对各局部哈密顿量的依次模拟：

$$ e^{-i(H_1+H_2+\dots+H_m)t} = e^{-iH_1t}e^{-iH_2t} \dots e^{-iH_mt} $$

然而在实际中，各局部哈密顿量往往不具有对易性质，因此需要使用一定的近似公式来进行模拟。有两种常用的近似方式：Lie-Trotter和2阶Suzuki，它们分别可以近似到时间步长 $\Delta t$ 的平方和三次方。
Lie-Trotter公式：

$$e^{-i(H_1+H_2+\dots+H_m)\Delta t} = e^{-iH_1 \Delta t}e^{-iH_2 \Delta t} \dots e^{-iH_m \Delta t} + O(\Delta t^2)$$

2阶Suzuki公式：

$$e^{-i(H_1+H_2+\dots+H_m)\Delta t} = e^{-iH_1 \Delta t/2}e^{-iH_2 \Delta t/2} \dots e^{-iH_m \Delta t/2}e^{-iH_m \Delta t/2}e^{-iH_{m-1} \Delta t/2} \dots e^{-iH_1 \Delta t/2} + O(\Delta t^3)$$

因此在实践中，可以选定一个重复次数 $n$ ，并取时间步长 $\Delta t=t/n$ ，于是总的哈密顿量模拟可以分解为 $n$ 次重复：

$$e^{-i(H_1+H_2+\dots+H_m)t} \sim \left( e^{-iH_1 t/n}e^{-iH_2 t/n} \dots e^{-iH_m t/n} \right)^n$$

$$e^{-i(H_1+H_2+\dots+H_m)t} \sim \left( e^{-iH_1 t/2n}e^{-iH_2 t/2n} \dots e^{-iH_m t/2n}e^{-iH_m t/2n}e^{-iH_{m-1} t/2n} \dots e^{-iH_1 t/2n} \right)^n$$

PyQuantumKit提供了基于上述两种分解方式的量子哈密顿量模拟算法，函数原型为：

```python
def pqk_hsim_paulis_trotter(q_circuit, hamiltonian : PauliHamiltonian, t : float, n : int, qindex : list[int]):
def pqk_hsim_paulis_suzuki2(q_circuit, hamiltonian : PauliHamiltonian, t : float, n : int, qindex : list[int]):
```

- 参数`q_circuit`指定目标量子线路。
- 参数`hamiltonian`是一个`PauliHamiltonian`类，用于指定目标哈密顿量 $H$ ；
- 参数`t`指定演化时间；
- 参数`n`指定分解的重复次数；
- 参数`qindex`是一个整数列表，指定要应用哈密顿模拟的量子比特下标。

函数中使用了`PauliHamiltonian`类来表示哈密顿量，成员函数`append_pauli`用于在`PauliHamiltonian`类中添加一个哈密顿量的Pauli因子，原型为：

```python
class PauliHamiltonian:
    def append_pauli(self, paulistr : str, factor : float, focus : int = 0) -> None:
```

- 参数`paulistr`是一个由`'I'`,`'X'`,`'Y'`,`'Z'`组成的字符串，用于指定对应的Pauli算子，字符串长度应与`PauliHamiltonian`对象构造时指定的量子比特数目匹配。
- 参数`factor`是一个浮点数，指定该因子的系数；
- 参数`focus`是一个可选参数，用于控制量子线路生成的方式，默认为0。

以下示例展示了如何使用PyQuantumKit构造量子哈密顿量模拟线路。考虑横场伊辛模型，每个粒子用一个量子比特表示，哈密顿量为：

$$H=-J\sum_{\langle i,j \rangle}\sigma_3^{(i)}\sigma_3^{(j)} - B\sum_{i}\sigma_1^{(i)} $$

其中 $\sigma_3^{(i)}\sigma_3^{(j)}$ 表示在第 $i,j$ 个量子比特上的Pauli算子为 $\sigma_3$ ，其余量子比特上为 $\sigma_0$ ； $\sigma_1^{(i)}$ 表示在第 $i$ 个量子比特上的Pauli算子为 $\sigma_1$ ，其余量子比特上为 $\sigma_0$ 。求和下标 $\langle i,j \rangle$ 表示对近邻粒子求和。

这里我们考虑一个具体的案例。一共 $N=5$ 个粒子，排成环状，在环上相邻的粒子之间有相互作用。设定相互作用强度 $J=1.0$ ，外加磁场的强度 $B=1.0$ ，演化时间 $t=1.0$ 。采用Lie-Trotter分解方案，重复次数设为 $n=20$ 次。利用PyQuantumKit在QPanda3和Qiskit上构建量子线路的代码如下：

```python
import pyqpanda3.core as qpanda
import qiskit, qiskit_aer
import pyquantumkit as PQK
import pyquantumkit.library.hamiltonian as PQKHami

N = 5           # number of particles
J = 1.0         # interaction
B = 1.0         # magnatic field
t = 1.0         # evolution time
n = 20          # rounds of decomposition

# ----- Build the Hamiltonian -----
# construct a PauliHamiltonian object, the parameter is the number of qubits
TFIsing = PQKHami.PauliHamiltonian(N)
# interaction terms
TFIsing.append_pauli('ZZIII', -J)
TFIsing.append_pauli('IZZII', -J)
TFIsing.append_pauli('IIZZI', -J)
TFIsing.append_pauli('IIIZZ', -J)
TFIsing.append_pauli('ZIIIZ', -J)
# magnatic field terms
TFIsing.append_pauli('XIIII', -B)
TFIsing.append_pauli('IXIII', -B)
TFIsing.append_pauli('IIXII', -B)
TFIsing.append_pauli('IIIXI', -B)
TFIsing.append_pauli('IIIIX', -B)

# construct circuit on qpanda
qpanda_circuit = qpanda.QCircuit(N)
PQKHami.pqk_hsim_paulis_trotter(qpanda_circuit, TFIsing, t, n, range(N))
print(qpanda_circuit)

# construct circuit on qiskit
qiskit_circuit = qiskit.QuantumCircuit(N)
PQKHami.pqk_hsim_paulis_trotter(qiskit_circuit, TFIsing, t, n, range(N))
print(qiskit_circuit)
```
