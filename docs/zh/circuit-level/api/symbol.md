# pyquantumkit.symbol模块

## 一、pyquantumkit.symbol.gate模块
`pyquantumkit.symbol.gate`模块提供了基本门的矩阵表示（基于`sympy.Matrix`类实现）。

### 量子门矩阵对象
模块中预置了受支持量子门对应的SymPy矩阵对象或生成矩阵对象的函数（对于带参数量子门），可以直接使用具体的对象名（[查看详情](./supported-gates.md)）来引用。

**注意：本模块提供的矩阵按照符合人类阅读的形式，即量子计算教科书中的使用的形式，这可能与诸如Qiskit中的约定不同。** 例如，以第一个量子比特作为控制位，第二个量子比特作为受控位的CNOT门对应的矩阵为：

$$ \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & 1 & 0 \end{bmatrix} $$

该矩阵在模块中对应的对象为`pyquantumkit.symbol.gate.CNOT`。

### symbol_gate_matrix函数
`symbol_gate_matrix`函数可将代表量子门的字符串转换为具体的矩阵对象，函数原型为：

```python
def symbol_gate_matrix(gate_str : str, paras : list = None) -> sympy.Matrix
```
- 参数`gate_str`是一个指示量子门的字符串，与`apply_gate`函数中的相同（[查看详情](./supported-gates.md)）。
- 参数`paras`是一个列表，用于为含参数门指派参数，与`apply_gate`函数中的相同；对于无参数门，不用指派此参数。

例如：`symbol_gate_matrix('CNOT')`将返回表示CNOT门的sympy.Matrix对象。

### symbol_inverse_gate函数
`symbol_inverse_gate`函数输入一个代表量子门的sympy.Matrix矩阵，返回它的逆矩阵（即共轭转置），函数原型为：

```python
def symbol_inverse_gate(mat : sympy.MatrixBase) -> sympy.Matrix
```
- 参数`mat`是一个代表酉矩阵的sympy.Matrix对象。该函数仅仅简单取`mat`的共轭转置，不检验`mat`的幺正性（酉性）。

### is_legal_gate_matrix函数
`is_legal_gate_matrix`函数输入一个代表量子门的sympy.Matrix矩阵，判断该矩阵是否为合法的量子门矩阵，函数原型为：

```python
def is_legal_gate_matrix(mat : sympy.MatrixBase) -> bool
```
- 参数`mat`是一个sympy.Matrix对象。

函数返回True当且仅当`mat`是方阵且为酉矩阵。

### reverse_matrix_endianness函数
本模块提供的矩阵按照符合人类阅读的形式，即量子计算教科书中的使用的形式。一些量子开发框架可能会使用反转量子比特顺序的约定（例如Qiskit）。`reverse_matrix_endianness`提供了在这两种表示形式之间的转换，函数原型为：

```python
def reverse_matrix_endianness(mat : sympy.MatrixBase) -> sympy.Matrix
```
- 参数`mat`是一个sympy.Matrix对象。

函数返回反转`mat`矩阵端序模式的矩阵。例如，如果输入

$$ \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & 1 & 0 \end{bmatrix} $$

则函数返回

$$ \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & 1 & 0 \\ 0 & 1 & 0 & 0 \end{bmatrix} $$

## 二、pyquantumkit.symbol.circuit模块
`pyquantumkit.symbol.circuit`模块提供了若干由基本量子门构造量子线路矩阵表示的函数。

### symbol_apply_gate函数

`symbol_apply_gate`函数在指定下标的量子比特上应用指定的量子门，返回对应的矩阵表示。函数原型为：

```python
def symbol_apply_gate(gate : sympy.Matrix, nqbits : int, indexlist : list[int]) -> sympy.Matrix:
```

- 参数`gate`是一个 $2^k\times 2^k$ 矩阵，其中 $k$ 代表了量子门的比特数，例如单比特量子门（ $k=1$ ）是 $2\times 2$ 矩阵，双比特量子门（ $k=2$ ）是 $4\times 4$ 矩阵。
- 参数`nqbits`是一个正整数，指定总量子比特数 $n$ ，该参数不能小于 $k$ 。
- 参数`indexlist`是一个列表，按顺序指定要作用量子门的比特的下标，**注意下标从0开始，这和Mathematica的约定不同**。列表长度必须为 $k$ ，即与参数`gate`的维数匹配。
- 该函数的返回值为一个 $2^n\times 2^n$ 维矩阵。

**例1**. 设总共有5个量子比特，以下标为3的量子比特为控制位，下标为1的量子比特为目标位应用一个CNOT门，如下图所示：
<div align="left">
<img src=../../../imgs/5cnot31.jpg width=20% />
</div>

可用如下方式使用该函数生成对应的矩阵表示：

```python
from pyquantumkit.symbol.gate import *
from pyquantumkit.symbol.circuit import *

Mat1 = symbol_apply_gate(CNOT, 5, [3, 1])
print(Mat1)
```

返回结果为一个 $32\times 32$（即 $2^5\times 2^5$）维矩阵。

```
Matrix([[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]])
```

### symbol_controlled_gate函数

`symbol_controlled_gate`函数返回一个指定量子门的受控形式的矩阵表示。函数原型为：

```python
def symbol_controlled_gate(gate : sympy.Matrix, nctrlbits : int) -> sympy.BlockDiagMatrix
```

- 参数`gate`是一个 $2^k\times 2^k$ 矩阵，其中 $k$ 代表了量子门的比特数。
- 参数`nctrlbits`是一个正整数，指定控制量子比特个数 $n$ 。

该函数的返回值为一个 $2^{n+k}\times 2^{n+k}$ 维分块对角矩阵（`sympy.BlockDiagMatrix`类对象），**其中对应的前 $n$ 个量子比特为控制位， 后 $k$ 个量子比特为目标位。** 具体而言，设 $U$ 为`gate`参数对应的矩阵，则该函数返回如下形式的分块对角矩阵：

$$
CU = \begin{bmatrix} I_{2^k\times 2^k} & 0 & \cdots & 0 & 0 \\ 0 & I_{2^k\times 2^k} & \cdots & 0 & 0 \\ \vdots & \vdots & \ddots & \vdots & \vdots \\ 0 & 0 & \cdots & I_{2^k\times 2^k} & 0 \\ 0 & 0 & \cdots & 0 & U \end{bmatrix}_{2^{n+k}\times 2^{n+k}}
$$

其中 $I_{2^k\times 2^k}$ 为单位矩阵，这样的单位矩阵块一共有 $2^n-1$ 块。加上最后一个 $U$ 块，一共有 $2^n$ 块。

联合使用`symbol_controlled_gate`和`symbol_apply_gate`函数，可以生成以其中一些量子比特为控制位，其他一些量子比特为目标位的受控门的矩阵表示。

**例2**. 首先生成由3个比特控制的X门（即CCCNOT）门，可如下实现：
```python
cccnot = symbol_controlled_gate(X, 3)
```

然后将上述量子门以下标为2的量子比特为目标位，其余为控制位构造量子线路，如下图所示：
<div align="left">
<img src=../../../imgs/cccx.jpg width=20% />
</div>

实现代码为：
```python
Mat = symbol_apply_gate(cccnot, 4, [0, 1, 3, 2])
```

这里指派的数组`[0, 1, 3, 2]`可以这样理解：由于`cccnot`对应的下标0,1,2为控制，下标3为目标，而我们需要以2号量子比特作为目标位，因此数组的2号位置（从0开始数）指派为3，其余0,1,3号位置按照顺序指派为0,1,2。

### symbol_multi_apply_sqgate函数

`symbol_multi_apply_sqgate`函数生成在每个量子比特上分别应用一个单比特量子门的矩阵表示，即给定 $2\times 2$ 矩阵 $U$ 和总量子比特数 $n$ ，函数生成矩阵 $U^{\otimes n}$ 。函数原型为：

```python
def symbol_multi_apply_sqgate(sqgate : sympy.Matrix, nqbits : int) -> sympy.Matrix:
```

- 参数`sqgate`是个一个 $2\times 2$ 矩阵，表示单比特量子门。
- 参数`nqbits`是一个正整数，表示总量子比特数 $n$ 。
- 函数返回一个 $2^n\times 2^n$ 维矩阵。

`symbol_multi_apply_sqgate(U, 2)`等价于`sympy.KroneckerProduct(U, U)`；
`symbol_multi_apply_sqgate(U, 3)`等价于`sympy.KroneckerProduct(U, U, U)`。

## 三、pyquantumkit.symbol.qstate模块
`pyquantumkit.symbol.qstate`模块提供了基本量子态向量表示SymPy矩阵对象，包括ket表示（列向量）、bra表示（行向量）和密度矩阵表示。

### 单比特0态
- Ket表示: `Ket0`

$$\ket{0} = \begin{bmatrix} 1 \\ 0 \end{bmatrix}$$

- Bra表示: `Bra0`

$$\bra{0} = \begin{bmatrix} 1 & 0 \end{bmatrix}$$

- 密度矩阵: `Rho0`

$$\rho_0 = \ket{0}\bra{0} = \begin{bmatrix} 1 & 0 \\ 0 & 0 \end{bmatrix}$$

### 单比特1态
- Ket表示: `Ket1`

$$\ket{1} = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$$

- Bra表示: `Bra1`

$$\bra{1} = \begin{bmatrix} 0 & 1 \end{bmatrix}$$

- 密度矩阵: `Rho1`

$$\rho_1 = \ket{1}\bra{1} = \begin{bmatrix} 0 & 0 \\ 0 & 1 \end{bmatrix}$$

### 单比特+态
- Ket表示: `KetPlus`

$$\ket{+} = \frac{1}{\sqrt 2}\left(\ket{0}+\ket{1}\right) = \begin{bmatrix} \frac{1}{\sqrt 2} \\ \frac{1}{\sqrt 2} \end{bmatrix}$$

- Bra表示: `BraPlus`

$$\bra{+} = \begin{bmatrix} \frac{1}{\sqrt 2} & \frac{1}{\sqrt 2} \end{bmatrix}$$

- 密度矩阵: `RhoPlus`

$$\rho_+ = \ket{+}\bra{+} = \begin{bmatrix} \frac{1}{2} & \frac{1}{2} \\ \frac{1}{2} & \frac{1}{2} \end{bmatrix}$$

### 单比特-态
- Ket表示: `KetMinus`

$$\ket{-} = \frac{1}{\sqrt 2}\left(\ket{0}-\ket{1}\right) = \begin{bmatrix} \frac{1}{\sqrt 2} \\ -\frac{1}{\sqrt 2} \end{bmatrix}$$

- Bra表示: `BraMinus`

$$\bra{-} = \begin{bmatrix} \frac{1}{\sqrt 2} & -\frac{1}{\sqrt 2} \end{bmatrix}$$

- 密度矩阵: `RhoMinus`

$$\rho_- = \ket{-}\bra{-} = \begin{bmatrix} \frac{1}{2} & -\frac{1}{2} \\ -\frac{1}{2} & \frac{1}{2} \end{bmatrix}$$

### Bloch球上的状态
- Ket表示: `KetBloch(theta_, phi_, gamma_)`

$$\ket{\psi} = e^{i\gamma}\left( \cos\frac{\theta}{2}\ket{0} + e^{i\phi}\sin\frac{\theta}{2}\ket{1} \right) = \begin{bmatrix} e^{i\gamma}\cos\frac{\theta}{2} \\ e^{i(\gamma+\phi)}\sin\frac{\theta}{2} \end{bmatrix}$$

- Bra表示: `BraBloch(theta_, phi_, gamma_)`

$$\bra{\psi} = e^{-i\gamma}\left( \cos\frac{\theta}{2}\bra{0} + e^{-i\phi}\sin\frac{\theta}{2}\bra{1} \right) = \begin{bmatrix} e^{-i\gamma}\cos\frac{\theta}{2} & e^{-i(\gamma+\phi)}\sin\frac{\theta}{2} \end{bmatrix}$$

- 密度矩阵: `BraBloch(theta_, phi_, gamma_)`

$$\rho=\ket{\psi}\bra{\psi} = \begin{bmatrix} \cos^2(\frac{\theta}{2}) & e^{-i\phi}\cos\frac{\theta}{2}\sin\frac{\theta}{2} \\ e^{i\phi}\cos\frac{\theta}{2}\sin\frac{\theta}{2} & \sin^2(\frac{\theta}{2}) \end{bmatrix}$$

### Bell 00态（ $\Phi^+$ 态）
- Ket表示: `KetBell`

$$\ket{\beta_{00}} = \ket{\Phi^+} = \frac{1}{\sqrt 2}\left(\ket{00}+\ket{11}\right) = \begin{bmatrix} \frac{1}{\sqrt 2} \\ 0 \\ 0 \\ \frac{1}{\sqrt 2} \end{bmatrix}$$

- Bra表示: `BraBell`

$$\bra{\beta_{00}} = \frac{1}{\sqrt 2}\left(\bra{00}+\bra{11}\right) = \begin{bmatrix} \frac{1}{\sqrt 2} & 0 & 0 & \frac{1}{\sqrt 2} \end{bmatrix}$$

- 密度矩阵: `RhoBell`

$$\rho = \ket{\beta_{00}}\bra{\beta_{00}} = \begin{bmatrix} \frac{1}{2} & 0 & 0 & \frac{1}{2} \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ \frac{1}{2} & 0 & 0 & \frac{1}{2} \end{bmatrix}$$

### Bell 01态（ $\Psi^+$ 态）
- Ket表示: `KetBell01`

$$\ket{\beta_{01}} = \ket{\Psi^+} = \frac{1}{\sqrt 2}\left(\ket{01}+\ket{10}\right) = \begin{bmatrix} 0 \\ \frac{1}{\sqrt 2} \\ \frac{1}{\sqrt 2} \\ 0 \end{bmatrix}$$

- Bra表示: `BraBell01`

$$\bra{\beta_{01}} = \frac{1}{\sqrt 2}\left(\bra{01}+\bra{10}\right) = \begin{bmatrix} 0 & \frac{1}{\sqrt 2} & \frac{1}{\sqrt 2} & 0 \end{bmatrix}$$

- 密度矩阵: `RhoBell01`

$$\rho = \ket{\beta_{01}}\bra{\beta_{01}} = \begin{bmatrix} 0 & 0 & 0 & 0 \\ 0 & \frac{1}{2} & \frac{1}{2} & 0 \\ 0 & \frac{1}{2} & \frac{1}{2} & 0 \\ 0 & 0 & 0 & 0 \end{bmatrix}$$

### Bell 10态（ $\Phi^-$ 态）
- Ket表示: `KetBell10`

$$\ket{\beta_{10}} = \ket{\Phi^-} = \frac{1}{\sqrt 2}\left(\ket{00}-\ket{11}\right) = \begin{bmatrix} \frac{1}{\sqrt 2} \\ 0 \\ 0 \\ -\frac{1}{\sqrt 2} \end{bmatrix}$$

- Bra表示: `BraBell10`

$$\bra{\beta_{10}} = \frac{1}{\sqrt 2}\left(\bra{00}-\bra{11}\right) = \begin{bmatrix} \frac{1}{\sqrt 2} & 0 & 0 & -\frac{1}{\sqrt 2} \end{bmatrix}$$

- 密度矩阵: `RhoBell10`

$$\rho = \ket{\beta_{10}}\bra{\beta_{10}} = \begin{bmatrix} \frac{1}{2} & 0 & 0 & -\frac{1}{2} \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ -\frac{1}{2} & 0 & 0 & \frac{1}{2} \end{bmatrix}$$

### Bell 11态（ $\Psi^-$ 态）
- Ket表示: `KetBell11`

$$\ket{\beta_{11}} = \ket{\Psi^+} = \frac{1}{\sqrt 2}\left(\ket{01}-\ket{10}\right) = \begin{bmatrix} 0 \\ \frac{1}{\sqrt 2} \\ -\frac{1}{\sqrt 2} \\ 0 \end{bmatrix}$$

- Bra表示: `BraBell11`

$$\bra{\beta_{11}} = \frac{1}{\sqrt 2}\left(\bra{01}-\bra{10}\right) = \begin{bmatrix} 0 & \frac{1}{\sqrt 2} & -\frac{1}{\sqrt 2} & 0 \end{bmatrix}$$

- 密度矩阵: `RhoBell11`

$$\rho = \ket{\beta_{11}}\bra{\beta_{11}} = \begin{bmatrix} 0 & 0 & 0 & 0 \\ 0 & \frac{1}{2} & -\frac{1}{2} & 0 \\ 0 & -\frac{1}{2} & \frac{1}{2} & 0 \\ 0 & 0 & 0 & 0 \end{bmatrix}$$

### n比特全0态
- Ket表示: `KetAllZero(nqbits)`，其中参数`nqbits`指定量子比特数 $n$

$$\ket{0\dots 0} = \begin{bmatrix} 1 \\ 0 \\ \vdots \\ 0 \end{bmatrix}_{2^n\times 1}$$

- Bra表示: `BraAllZero(nqbits)`，其中参数`nqbits`指定量子比特数 $n$

$$\bra{0\dots 0} = \begin{bmatrix} 1 & 0 & \cdots & 0 \end{bmatrix}_{1\times 2^n}$$

- 密度矩阵: `RhoAllZero(nqbits)`，其中参数`nqbits`指定量子比特数 $n$

$$\ket{0\dots 0}\bra{0\dots 0} = \begin{bmatrix} 1 & 0 & \cdots & 0 \\ 0 & 0 & \cdots & 0 \\ \vdots & \vdots & \ddots & \vdots \\ 0 & 0 & \cdots & 0 \end{bmatrix}_{2^n\times 2^n}$$

### n比特均匀叠加态
- Ket表示: `KetUniformSuperposition(nqbits)`，其中参数`nqbits`指定量子比特数 $n$

$$\ket{\psi} = \frac{1}{\sqrt{2^n}}\sum_{x\in \{0,1\}^n}\ket{x} = \frac{1}{\sqrt{2^n}} \begin{bmatrix} 1 \\ 1 \\ \vdots \\ 1 \end{bmatrix}_{2^n\times 1}$$

- Bra表示: `BraUniformSuperposition(nqbits)`，其中参数`nqbits`指定量子比特数 $n$

$$\bra{\psi} = \frac{1}{\sqrt{2^n}}\sum_{x\in \{0,1\}^n}\bra{x} = \frac{1}{\sqrt{2^n}} \begin{bmatrix} 1 & 1 & \cdots & 1 \end{bmatrix}_{1\times 2^n}$$

- 密度矩阵: `RhoUniformSuperposition(nqbits)`，其中参数`nqbits`指定量子比特数 $n$

$$\rho = \ket{\psi}\bra{\psi} = \frac{1}{2^n} \begin{bmatrix} 1 & 1 & \cdots & 1 \\ 1 & 1 & \cdots & 1 \\ \vdots & \vdots & \ddots & \vdots \\ 1 & 1 & \cdots & 1 \end{bmatrix}_{2^n\times 2^n}$$