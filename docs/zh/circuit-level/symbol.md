# 量子线路矩阵的符号表示

PyQuantumKit提供了symbol模块 (`pyquantumkit.symbol`) ，此模块基于SymPy库实现，用于构造量子线路的矩阵表示。

<!--*hiquarc仓库中还有另一个基于Mathematica的构造量子线路的矩阵表示库QCirMat（见[https://github.com/hiquarc/QCirMat](https://github.com/hiquarc/QCirMat)），此symbol库可以视为基于Python和sympy版本的QCirMat，方便没有Mathematica的用户使用。*-->

- `pyquantumkit.symbol.gate`模块提供了基本门的矩阵表示（基于`sympy.Matrix`类）。
- `pyquantumkit.symbol.qstate`模块提供了基本量子态向量表示（包括ket表示、bra表示和密度矩阵表示）。
- `pyquantumkit.symbol.circuit`模块提供了若干用于构造量子线路的矩阵表示的函数。

**pyquantumkit.symbol模块的详细内容请[点此查看](./api/symbol.md)。**

**注意：由于Python对于下标的约定是从0开始，pyquantumkit.symbol库涉及下标的参数均按照Python的约定从0开始，这与Mathematica的从1开始的约定不同。**

## 一、使用量子门对应的矩阵
`pyquantumkit.symbol.gate`模块中预置了受支持量子门对应的SymPy矩阵对象或生成矩阵对象的函数（对于带参数量子门）。可以直接使用具体的对象名（[查看详情](./api/supported-gates.md)）来引用：

```python
import pyquantumkit.symbol.gate as PQK_S_GATE

print(PQK_S_GATE.Y)             # Y gate
print(PQK_S_GATE.SqrtXdag)      # √X gate
print(PQK_S_GATE.Rxx(0.5))      # Rxx gate with theta=0.5
```
输出为
```
Matrix([[0, -I], [I, 0]])
Matrix([[1/2 - I/2, 1/2 + I/2], [1/2 + I/2, 1/2 - I/2]])
Matrix([[0.968912421710645, 0, 0, -0.247403959254523*I], [0, 0.968912421710645, -0.247403959254523*I, 0], [0, -0.247403959254523*I, 0.968912421710645, 0], [-0.247403959254523*I, 0, 0, 0.968912421710645]])
```

也可以使用`symbol_gate_matrix`函数，传入一个指示门的字符串来引用，该字符串与`apply_gate`函数中的相同（[查看详情](./api/supported-gates.md)）。上述示例中的代码还可以等价地写为：

```python
import pyquantumkit.symbol.gate as PQK_S_GATE

print(PQK_S_GATE.symbol_gate_matrix('Y'))           # Y gate
print(PQK_S_GATE.symbol_gate_matrix('sxdg'))        # √X gate
print(PQK_S_GATE.symbol_gate_matrix('Rxx', [0.5]))  # Rxx gate with theta=0.5
```

## 二、使用量子态向量
`pyquantumkit.symbol.qstate`模块中预置了常见量子态的态向量或矩阵表示，例如ket表示 $\ket{0}$ 、bra表示 $\bra{+}$ 、贝尔态的密度矩阵表示 $\ket{\beta_{00}}\bra{\beta_{00}}$ 等。可以直接使用具体的对象名（[查看详情](./api/symbol.md#pyquantumkitsymbolqstate)）来引用：

```python
import pyquantumkit.symbol.qstate as PQK_S_STATE

print(PQK_S_STATE.Ket0)
print(PQK_S_STATE.BraPlus)
print(PQK_S_STATE.RhoBell)
```

输出为
```
Matrix([[1], [0]])
Matrix([[sqrt(2)/2, sqrt(2)/2]])
Matrix([[1/2, 0, 0, 1/2], [0, 0, 0, 0], [0, 0, 0, 0], [1/2, 0, 0, 1/2]])
```

## 三、构造量子线路对应的矩阵
### 方法1：直接利用SymPy矩阵运算
利用量子门的矩阵构造量子线路对应的矩阵，一种方法是直接使用SymPy提供的矩阵运算：量子门的顺序应用对应矩阵连乘，量子门的并行应用对应矩阵。

**例1**. 考虑如下制备Bell态的量子线路：
<div align="left">
<img src=../../../imgs/bell.jpg width=50% />
</div>

它包含一个作用于第一个量子比特的H门和一个作用于两个量子比特的CNOT门。第一个量子比特作用H门可用张量积（Kronecker积）形式表示为 $H\otimes I$ ，而总的矩阵表示为两个量子门的矩阵表示的乘积：

$$CNOT \cdot (H\otimes I) = \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & 1 & 0 \end{bmatrix} \cdot \left( \frac{1}{\sqrt 2}\begin{bmatrix} 1 & 1 \\ 1 & -1 \end{bmatrix} \otimes \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix} \right) = \frac{1}{\sqrt 2}\begin{bmatrix} 1 & 0 & 1 & 0 \\ 0 & 1 & 0 & 1 \\ 0 & 1 & 0 & -1 \\ 1 & 0 & -1 & 0 \end{bmatrix}$$

**注意：矩阵乘法的顺序与量子门作用的顺序相反！**

以下代码基于`pyquantumkit.symbol.gate`中预置的量子门矩阵，利用SymPy库提供的矩阵乘法和Kronecker积，计算上述量子线路的矩阵表示：
```python
import sympy
import pyquantumkit.symbol.gate as PQK_S_GATE

Circuit_Matrix =  PQK_S_GATE.CNOT * \
                  sympy.KroneckerProduct(PQK_S_GATE.H, PQK_S_GATE.Id)
print(Circuit_Matrix)
```
运行结果为：
```
Matrix([[sqrt(2)/2, 0, sqrt(2)/2, 0], [0, sqrt(2)/2, 0, sqrt(2)/2], [0, sqrt(2)/2, 0, -sqrt(2)/2], [sqrt(2)/2, 0, -sqrt(2)/2, 0]])
```

### 方法2：利用CircuitIO类导出量子线路的矩阵
CircuitIO类对象支持以SymPy符号作为含参量子门（例如Rx门）的参数，并可根据对象内已包含的量子门序列计算出整个量子线路的矩阵表示。CircuitIO类对象导出量子线路的矩阵表示的函数为`get_sympy_matrix`（返回SymPy矩阵）和`get_numpy_matrix`（返回NumPy矩阵），函数的具体细节请[点此查看](./api/circuitio.md#get_sympy_matrix)。

**例1'**. 利用CircuitIO类计算例1中量子线路的矩阵表示

```python
import pyquantumkit

cio = pyquantumkit.CircuitIO(2)
cio.apply_gate('H', [0])
cio.apply_gate('CNOT', [0, 1])
Circuit_Matrix = cio.get_sympy_matrix()     # calculate the matrix of whole circuit
print(Circuit_Matrix)
```
运行结果与例1相同：
```
Matrix([[sqrt(2)/2, 0, sqrt(2)/2, 0], [0, sqrt(2)/2, 0, sqrt(2)/2], [0, sqrt(2)/2, 0, -sqrt(2)/2], [sqrt(2)/2, 0, -sqrt(2)/2, 0]])
```
