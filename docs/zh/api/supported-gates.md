# PyQuantumKit支持的量子门

本页给出了PyQuantumKit支持的量子门及其对应的apply_gate函数的调用字符串及pyquantumkit.symbol.gate中的SymPy矩阵名，供用户查阅。

**apply_gate函数的调用字符串不区分大小写**，且若一个门列出多个字符串，采用其中的任意一个均可。例如，`'CCNOT'`, `'ccx'`, `'Toffoli'`, `'toFFoLi'`均为合法的代表Toffoli门的调用字符串。对于带参数量子门，需要指派一个数组作为`paras`参数，**注：即使只有一个参数也需要以数组形式指派**。

由于pyquantumkit.symbol.gate提供的SymPy矩阵为Python对象或返回Python对象的函数，因而**SymPy矩阵名区分大小写**。此外，也可以使用`symbol_gate_matrix`函数将调用字符串转换为SymPy矩阵对象，此函数对应的调用字符串与apply_gate函数相同，不区分大小写。

## 1. 单比特门

### 恒等变换（Identity）
- 矩阵：

$$ \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}  $$

- apply_gate函数的调用字符串（不区分大小写，下同）： `'i'`, `'id'`
- pyquantumkit.symbol.gate中的SymPy矩阵名（区分大小写，下同）： `Id`

### X门
- 矩阵：

$$ \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix} $$

- apply_gate函数的调用字符串： `'x'`
- pyquantumkit.symbol.gate中的SymPy矩阵名： `X`

### Y门
- 矩阵：

$$ \begin{bmatrix} 0 & -i \\ i & 0 \end{bmatrix} $$

- apply_gate函数的调用字符串： `'y'`
- pyquantumkit.symbol.gate中的SymPy矩阵名： `Y`

### Z门
- 矩阵：

$$ \begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix} $$

- apply_gate函数的调用字符串： `'z'`
- pyquantumkit.symbol.gate中的SymPy矩阵名： `Z`

### S门
- 矩阵：

$$ \begin{bmatrix} 1 & 0 \\ 0 & i \end{bmatrix} $$

- apply_gate函数的调用字符串： `'s'`
- pyquantumkit.symbol.gate中的SymPy矩阵名： `S`

### T门
- 矩阵：

$$ \begin{bmatrix} 1 & 0 \\ 0 & e^{\frac{\pi}{4}i} \end{bmatrix} $$

- apply_gate函数的调用字符串： `'t'`
- pyquantumkit.symbol.gate中的SymPy矩阵名： `T`

### Hardmard门
- 矩阵：

$$ \frac{1}{\sqrt 2}\begin{bmatrix} 1 & 1 \\ 1 & -1 \end{bmatrix} $$

- apply_gate函数的调用字符串： `'h'`
- pyquantumkit.symbol.gate中的SymPy矩阵名： `H`

### $S^{\dagger}$ 门
- 矩阵：

$$ \begin{bmatrix} 1 & 0 \\ 0 & -i \end{bmatrix} $$

- apply_gate函数的调用字符串： `'sd'`, `'sdg'`, `'sdag'`, `'sdagger'`
- pyquantumkit.symbol.gate中的SymPy矩阵名： `Sdag`

### $T^{\dagger}$ 门
- 矩阵：

$$ \begin{bmatrix} 1 & 0 \\ 0 & e^{-\frac{\pi}{4}i} \end{bmatrix} $$

- apply_gate函数的调用字符串： `'td'`, `'tdg'`, `'tdag'`, `'tdagger'`
- pyquantumkit.symbol.gate中的SymPy矩阵名： `Tdag`

### $\sqrt{X}$ 门
- 矩阵：

$$ \begin{bmatrix} 1+i & 1-i \\ 1-i & 1+i \end{bmatrix} $$

- apply_gate函数的调用字符串： `'sx'`, `'sqrtx'`
- pyquantumkit.symbol.gate中的SymPy矩阵名： `SqrtX`

### $\sqrt{X}^{\dagger}$ 门
- 矩阵：

$$ \begin{bmatrix} 1-i & 1+i \\ 1+i & 1-i \end{bmatrix} $$

- apply_gate函数的调用字符串： `'sxd'`, `'sxdg'`, `'sxdag'`, `'sxdagger'`, `'sqrtxdg'`, `'sqrtxdag'`, `'sqrtxdag'`
- pyquantumkit.symbol.gate中的SymPy矩阵名： `SqrtXdag`

## 2. 双比特门
### CNOT门（受控X门）
- 矩阵：

$$ \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & 1 & 0 \end{bmatrix} $$

- apply_gate函数的调用字符串： `'cx'`, `'cnot'`
- pyquantumkit.symbol.gate中的SymPy矩阵名： `CNOT`

### 受控Y门
- 矩阵：

$$ \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & -i \\ 0 & 0 & i & 0 \end{bmatrix} $$

- apply_gate函数的调用字符串： `'cy'`
- pyquantumkit.symbol.gate中的SymPy矩阵名： `CY`

### 受控Z门
- 矩阵：

$$ \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & -1 \end{bmatrix} $$

- apply_gate函数的调用字符串： `'cz'`
- pyquantumkit.symbol.gate中的SymPy矩阵名： `CZ`

### 受控S门
- 矩阵：

$$ \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & i \end{bmatrix} $$

- apply_gate函数的调用字符串： `'cs'`
- pyquantumkit.symbol.gate中的SymPy矩阵名： `CS`

### 受控 $S^{\dagger}$ 门
- 矩阵：

$$ \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & -i \end{bmatrix} $$

- apply_gate函数的调用字符串： `'csd'`, `'csdg'`, `'csdag'`, `'csdagger'`
- pyquantumkit.symbol.gate中的SymPy矩阵名： `CSdag`

### 受控Hardmard门
- 矩阵：

$$ \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & \frac{1}{\sqrt 2} & \frac{1}{\sqrt 2} \\ 0 & 0 & \frac{1}{\sqrt 2} & -\frac{1}{\sqrt 2} \end{bmatrix} $$

- apply_gate函数的调用字符串： `'ch'`
- pyquantumkit.symbol.gate中的SymPy矩阵名： `CH`

### SWAP门（交换门）
- 矩阵：

$$ \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix} $$

- apply_gate函数的调用字符串： `'sw'`, `'swap'`
- pyquantumkit.symbol.gate中的SymPy矩阵名： `SWAP`

### iSWAP门
- 矩阵：

$$ \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 0 & i & 0 \\ 0 & i & 0 & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix} $$

- apply_gate函数的调用字符串： `'isw'`, `'iswap'`
- pyquantumkit.symbol.gate中的SymPy矩阵名： `iSWAP`

## 3. 三比特门
### Toffoli门（CCNOT门）
- 矩阵：

$$ \begin{bmatrix} 1 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 1 \\ 0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 \end{bmatrix} $$

- apply_gate函数的调用字符串： `'ccx'`, `'ccnot'`, `'toffoli'`
- pyquantumkit.symbol.gate中的SymPy矩阵名： `Toffoli`

### Fredkin门（受控交换门）
- 矩阵：

$$ \begin{bmatrix} 1 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 1 \end{bmatrix} $$

- apply_gate函数的调用字符串： `'csw'`, `'cswap'`, `'fredkin'`
- pyquantumkit.symbol.gate中的SymPy矩阵名： `Fredkin`

### CCZ门
- 矩阵：

$$ \begin{bmatrix} 1 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & -1 \end{bmatrix} $$

- apply_gate函数的调用字符串： `'ccz'`
- pyquantumkit.symbol.gate中的SymPy矩阵名： `CCZ`

## 4. 单比特带参数门
### $R_x(\theta)$ 门
- 矩阵：

$$ \begin{bmatrix} \cos\frac{\theta}{2} & -i\sin\frac{\theta}{2} \\ -i\sin\frac{\theta}{2} & \cos\frac{\theta}{2} \end{bmatrix} $$

- apply_gate函数的调用字符串： `'rx'`
- apply_gate函数的paras参数：`[theta_]`
- pyquantumkit.symbol.gate中的SymPy矩阵名： `Rx(theta_)`

### $R_y(\theta)$ 门
- 矩阵：

$$ \begin{bmatrix} \cos\frac{\theta}{2} & -\sin\frac{\theta}{2} \\ \sin\frac{\theta}{2} & \cos\frac{\theta}{2} \end{bmatrix} $$

- apply_gate函数的调用字符串： `'ry'`
- apply_gate函数的paras参数：`[theta_]`
- pyquantumkit.symbol.gate中的SymPy矩阵名： `Ry(theta_)`

### $R_z(\theta)$ 门
- 矩阵：

$$ \begin{bmatrix} e^{-i\frac{\theta}{2}} & 0 \\ 0 & e^{i\frac{\theta}{2}} \end{bmatrix} $$

- apply_gate函数的调用字符串： `'rz'`
- apply_gate函数的paras参数：`[theta_]`
- pyquantumkit.symbol.gate中的SymPy矩阵名： `Rz(theta_)`

### $P(\theta)$ 门 （ $U1(\theta)$ 门）
- 矩阵：

$$ \begin{bmatrix} 1 & 0 \\ 0 & e^{i\theta} \end{bmatrix} $$

- apply_gate函数的调用字符串： `'p'`, `'u1'`, `'r1'`
- apply_gate函数的paras参数：`[theta_]`
- pyquantumkit.symbol.gate中的SymPy矩阵名： `U1(theta_)`

### $U3(\theta,\phi,\lambda)$ 门（一般单比特门）
- 矩阵：

$$ \begin{bmatrix} \cos\frac{\theta}{2} & -e^{i\lambda}\sin\frac{\theta}{2} \\ e^{i\phi}\sin\frac{\theta}{2} & e^{i(\phi+\lambda)}\cos\frac{\theta}{2} \end{bmatrix} $$

- apply_gate函数的调用字符串： `'u'`, `'u3'`
- apply_gate函数的paras参数：`[theta_, phi_, lambda_]`
- pyquantumkit.symbol.gate中的SymPy矩阵名： `U3(theta_, phi_, lambda_)`

## 5. 双比特带参数门
### 受控 $R_x(\theta)$ 门
- 矩阵：

$$ \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & \cos\frac{\theta}{2} & -i\sin\frac{\theta}{2} \\ 0 & 0 & -i\sin\frac{\theta}{2} & \cos\frac{\theta}{2} \end{bmatrix} $$

- apply_gate函数的调用字符串： `'crx'`
- apply_gate函数的paras参数：`[theta_]`
- pyquantumkit.symbol.gate中的SymPy矩阵名： `CRx(theta_)`

### 受控 $R_y(\theta)$ 门
- 矩阵：

$$ \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & \cos\frac{\theta}{2} & -\sin\frac{\theta}{2} \\ 0 & 0 & \sin\frac{\theta}{2} & \cos\frac{\theta}{2} \end{bmatrix} $$

- apply_gate函数的调用字符串： `'cry'`
- apply_gate函数的paras参数：`[theta_]`
- pyquantumkit.symbol.gate中的SymPy矩阵名： `CRy(theta_)`

### 受控 $R_z(\theta)$ 门
- 矩阵：

$$ \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & e^{-i\frac{\theta}{2}} & 0 \\ 0 & 0 & 0 & e^{i\frac{\theta}{2}} \end{bmatrix} $$

- apply_gate函数的调用字符串： `'crz'`
- apply_gate函数的paras参数：`[theta_]`
- pyquantumkit.symbol.gate中的SymPy矩阵名： `CRz(theta_)`

### 受控 $P(\theta)$ 门
- 矩阵：

$$ \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & e^{i\theta} \end{bmatrix} $$

- apply_gate函数的调用字符串： `'cp'`, `'cu1'`, `'cr1'`
- apply_gate函数的paras参数：`[theta_]`
- pyquantumkit.symbol.gate中的SymPy矩阵名： `CU1(theta_)`

### $R_{xx}(\theta)$ 门
- 矩阵：

$$ \begin{bmatrix} \cos\frac{\theta}{2} & 0 & 0 & -i\sin\frac{\theta}{2} \\ 0 & \cos\frac{\theta}{2} & -i\sin\frac{\theta}{2} & 0 \\ 0 & -i\sin\frac{\theta}{2} & \cos\frac{\theta}{2} & 0 \\ -i\sin\frac{\theta}{2} & 0 & 0 & \cos\frac{\theta}{2} \end{bmatrix} $$

- apply_gate函数的调用字符串： `'rxx'`
- apply_gate函数的paras参数：`[theta_]`
- pyquantumkit.symbol.gate中的SymPy矩阵名： `Rxx(theta_)`

### $R_{yy}(\theta)$ 门
- 矩阵：

$$ \begin{bmatrix} \cos\frac{\theta}{2} & 0 & 0 & i\sin\frac{\theta}{2} \\ 0 & \cos\frac{\theta}{2} & -i\sin\frac{\theta}{2} & 0 \\ 0 & -i\sin\frac{\theta}{2} & \cos\frac{\theta}{2} & 0 \\ i\sin\frac{\theta}{2} & 0 & 0 & \cos\frac{\theta}{2} \end{bmatrix} $$

- apply_gate函数的调用字符串： `'Ryy'`
- apply_gate函数的paras参数：`[theta_]`
- pyquantumkit.symbol.gate中的SymPy矩阵名： `Ryy(theta_)`

### $R_{zz}(\theta)$ 门
- 矩阵：

$$ \begin{bmatrix} e^{-i\frac{\theta}{2}} & 0 & 0 & 0 \\ 0 & e^{i\frac{\theta}{2}} & 0 & 0 \\ 0 & 0 & e^{i\frac{\theta}{2}} & 0 \\ 0 & 0 & 0 & e^{-i\frac{\theta}{2}} \end{bmatrix} $$

- apply_gate函数的调用字符串： `'rzz'`
- apply_gate函数的paras参数：`[theta_]`
- pyquantumkit.symbol.gate中的SymPy矩阵名： `Rzz(theta_)`
