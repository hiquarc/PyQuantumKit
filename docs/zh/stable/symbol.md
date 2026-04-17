# 量子线路矩阵的符号表示

PyQuantumKit提供了symbol库 (pyquantumkit.symbol) ，此模块基于sympy库实现，用于构造量子线路的矩阵表示。

<!--*hiquarc仓库中还有另一个基于Mathematica的构造量子线路的矩阵表示库QCirMat（见[https://github.com/hiquarc/QCirMat](https://github.com/hiquarc/QCirMat)），此symbol库可以视为基于Python和sympy版本的QCirMat，方便没有Mathematica的用户使用。*-->

- `pyquantumkit.symbol.gate`模块提供了基本门的矩阵表示（基于`sympy.Matrix`类）
- `pyquantumkit.symbol.qstate`模块提供了基本量子态向量表示（包括ket表示、bra表示和密度矩阵表示）
- `pyquantumkit.symbol.circuit`模块提供了若干用于构造量子线路的矩阵表示的函数

**注意：由于Python对于下标的约定是从0开始，pyquantumkit.symbol库涉及下标的参数均按照Python的约定从0开始，这与Mathematica的从1开始的约定不同。**

## 使用量子门的矩阵
`pyquantumkit.symbol.gate`模块中预置了受支持量子门对应的SymPy矩阵对象或生成矩阵对象的函数（对于带参数量子门）。可以直接使用具体的对象名（[查看详情](../api/supported-gates.md)）来引用：

```python
import pyquantumkit.symbol.gate as PQK_S_GATE

print(PQK_S_GATE.Y)
print(PQK_S_GATE.SqrtXdag)
print(PQK_S_GATE.Rxx(0.5))
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
