# 量子线路矩阵的符号表示

PyQuantumKit提供了symbol库 (pyquantumkit.symbol) ，此模块基于sympy库实现，用于构造量子线路的矩阵表示。

<!--*hiquarc仓库中还有另一个基于Mathematica的构造量子线路的矩阵表示库QCirMat（见[https://github.com/hiquarc/QCirMat](https://github.com/hiquarc/QCirMat)），此symbol库可以视为基于Python和sympy版本的QCirMat，方便没有Mathematica的用户使用。*-->

- `pyquantumkit.symbol.gate`模块提供了基本门的矩阵表示（基于`sympy.Matrix`类）
- `pyquantumkit.symbol.qstate`模块提供了基本量子态向量表示（包括ket表示、bra表示和密度矩阵表示）
- `pyquantumkit.symbol.circuit`模块提供了若干用于构造量子线路的矩阵表示的函数

**注意：由于Python对于下标的约定是从0开始，pyquantumkit.symbol库涉及下标的参数均按照Python的约定从0开始，这与Mathematica的从1开始的约定不同。**

## 一、使用量子门对应的矩阵
`pyquantumkit.symbol.gate`模块中预置了受支持量子门对应的SymPy矩阵对象或生成矩阵对象的函数（对于带参数量子门）。可以直接使用具体的对象名（[查看详情](../api/supported-gates.md)）来引用：

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

也可以使用`symbol_gate_matrix`函数，传入一个指示门的字符串来引用，该字符串与`apply_gate`函数中的相同（[查看详情](../api/supported-gates.md)）。上述示例中的代码还可以等价地写为：

```python
import pyquantumkit.symbol.gate as PQK_S_GATE

print(PQK_S_GATE.symbol_gate_matrix('y'))
print(PQK_S_GATE.symbol_gate_matrix('sxdg'))
print(PQK_S_GATE.symbol_gate_matrix('rxx', [0.5]))
```

## 二、量子态向量

## 三、构造量子线路对应的矩阵

## CircuitIO类与符号表示

CircuitIO类对象支持以sympy符号作为含参量子门（例如Rx门）的参数，并可根据对象内已包含的量子门序列计算出整个量子线路的矩阵表示。

利用`get_sympy_matrix`成员函数可以计算CircuitIO对象的量子线路的矩阵表示，函数原型为：

```python
def get_sympy_matrix(self, subsdict : dict = None, simplify : bool = True) -> sympy.Matrix:
```

- 可选参数`subsdict`是一个字典，用于指定sympy符号代入规则。默认为None，即不进行任何符号代换。**注：只有当使用了sympy符号作为量子门参数时才需要指定此参数。**
- 可选参数`simplify`指定是否在计算矩阵表示的过程中进行化简（即sympy的simplify操作），默认为True。
- 函数返回量子线路对应的矩阵表示。

在将CircuitIO对象的量子线路转换为具体量子开发框架的量子线路对象时，可以将具体的数值代入这些sympy符号中。`append_into_actual_circuit`成员函数有一个额外可选参数`subsdict`，用于指定sympy符号代入规则。**注：当需要在插入到具体的量子开发框架的量子线路的过程中进行符号代入时，不能使用`>>`运算符，必须显式使用`append_into_actual_circuit`成员函数。**

```python
def append_into_actual_circuit(self, dest_qcir, subsdict : dict = None):
```
