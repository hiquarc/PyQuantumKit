# Quick Reference of Supported Quantum Gates

This page lists the quantum gates supported by PyQuantumKit, along with the corresponding call strings for the `apply_gate` function and the SymPy matrix names in `pyquantumkit.symbol.gate` for user reference.

**The call strings for the `apply_gate` function are case-insensitive**. If multiple strings are listed for a gate, any of them can be used. For example, `'CCNOT'`, `'ccx'`, `'Toffoli'`, `'toFFoLi'` are all valid call strings representing the Toffoli gate. For parameterized quantum gates, an array must be assigned as the `paras` parameter. **Note: Even if there is only one parameter, it must be assigned in the form of an array**.

Since the SymPy matrices provided by `pyquantumkit.symbol.gate` are Python objects or functions that return Python objects, **the SymPy matrix names are case-sensitive**. In addition, the `symbol_gate_matrix` function can be used to convert a call string to a SymPy matrix object, and the call strings for this function are the same as those for the `apply_gate` function (case-insensitive).

## 1. Single-Qubit Gates

### Identity
- Matrix:

$$ \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}  $$

- Call strings for the `apply_gate` function (case-insensitive, the same below): `'i'`, `'id'`
- SymPy matrix name in `pyquantumkit.symbol.gate` (case-sensitive, the same below): `Id`

### X Gate
- Matrix:

$$ \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix} $$

- Call strings for the `apply_gate` function: `'x'`
- SymPy matrix name in `pyquantumkit.symbol.gate`: `X`

### Y Gate
- Matrix:

$$ \begin{bmatrix} 0 & -i \\ i & 0 \end{bmatrix} $$

- Call strings for the `apply_gate` function: `'y'`
- SymPy matrix name in `pyquantumkit.symbol.gate`: `Y`

### Z Gate
- Matrix:

$$ \begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix} $$

- Call strings for the `apply_gate` function: `'z'`
- SymPy matrix name in `pyquantumkit.symbol.gate`: `Z`

### S Gate
- Matrix:

$$ \begin{bmatrix} 1 & 0 \\ 0 & i \end{bmatrix} $$

- Call strings for the `apply_gate` function: `'s'`
- SymPy matrix name in `pyquantumkit.symbol.gate`: `S`

### T Gate
- Matrix:

$$ \begin{bmatrix} 1 & 0 \\ 0 & e^{\frac{\pi}{4}i} \end{bmatrix} $$

- Call strings for the `apply_gate` function: `'t'`
- SymPy matrix name in `pyquantumkit.symbol.gate`: `T`

### Hadamard Gate
- Matrix:

$$ \frac{1}{\sqrt 2}\begin{bmatrix} 1 & 1 \\ 1 & -1 \end{bmatrix} $$

- Call strings for the `apply_gate` function: `'h'`
- SymPy matrix name in `pyquantumkit.symbol.gate`: `H`

### $S^{\dagger}$ Gate
- Matrix:

$$ \begin{bmatrix} 1 & 0 \\ 0 & -i \end{bmatrix} $$

- Call strings for the `apply_gate` function: `'sd'`, `'sdg'`, `'sdag'`, `'sdagger'`
- SymPy matrix name in `pyquantumkit.symbol.gate`: `Sdag`

### $T^{\dagger}$ Gate
- Matrix:

$$ \begin{bmatrix} 1 & 0 \\ 0 & e^{-\frac{\pi}{4}i} \end{bmatrix} $$

- Call strings for the `apply_gate` function: `'td'`, `'tdg'`, `'tdag'`, `'tdagger'`
- SymPy matrix name in `pyquantumkit.symbol.gate`: `Tdag`

### $\sqrt{X}$ Gate
- Matrix:

$$ \begin{bmatrix} 1+i & 1-i \\ 1-i & 1+i \end{bmatrix} $$

- Call strings for the `apply_gate` function: `'sx'`, `'sqrtx'`
- SymPy matrix name in `pyquantumkit.symbol.gate`: `SqrtX`

### $\sqrt{X}^{\dagger}$ Gate
- Matrix:

$$ \begin{bmatrix} 1-i & 1+i \\ 1+i & 1-i \end{bmatrix} $$

- Call strings for the `apply_gate` function: `'sxd'`, `'sxdg'`, `'sxdag'`, `'sxdagger'`, `'sqrtxdg'`, `'sqrtxdag'`, `'sqrtxdag'`
- SymPy matrix name in `pyquantumkit.symbol.gate`: `SqrtXdag`

## 2. Two-Qubit Gates
### CNOT Gate (Controlled-X Gate)
- Matrix:

$$ \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & 1 & 0 \end{bmatrix} $$

- Call strings for the `apply_gate` function: `'cx'`, `'cnot'`
- SymPy matrix name in `pyquantumkit.symbol.gate`: `CNOT`

### Controlled-Y Gate
- Matrix:

$$ \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & -i \\ 0 & 0 & i & 0 \end{bmatrix} $$

- Call strings for the `apply_gate` function: `'cy'`
- SymPy matrix name in `pyquantumkit.symbol.gate`: `CY`

### Controlled-Z Gate
- Matrix:

$$ \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & -1 \end{bmatrix} $$

- Call strings for the `apply_gate` function: `'cz'`
- SymPy matrix name in `pyquantumkit.symbol.gate`: `CZ`

### Controlled-S Gate
- Matrix:

$$ \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & i \end{bmatrix} $$

- Call strings for the `apply_gate` function: `'cs'`
- SymPy matrix name in `pyquantumkit.symbol.gate`: `CS`

### Controlled $S^{\dagger}$ Gate
- Matrix:

$$ \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & -i \end{bmatrix} $$

- Call strings for the `apply_gate` function: `'csd'`, `'csdg'`, `'csdag'`, `'csdagger'`
- SymPy matrix name in `pyquantumkit.symbol.gate`: `CSdag`

### Controlled-Hadamard Gate
- Matrix:

$$ \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & \frac{1}{\sqrt 2} & \frac{1}{\sqrt 2} \\ 0 & 0 & \frac{1}{\sqrt 2} & -\frac{1}{\sqrt 2} \end{bmatrix} $$

- Call strings for the `apply_gate` function: `'ch'`
- SymPy matrix name in `pyquantumkit.symbol.gate`: `CH`

### SWAP Gate
- Matrix:

$$ \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix} $$

- Call strings for the `apply_gate` function: `'sw'`, `'swap'`
- SymPy matrix name in `pyquantumkit.symbol.gate`: `SWAP`

### iSWAP Gate
- Matrix:

$$ \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 0 & i & 0 \\ 0 & i & 0 & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix} $$

- Call strings for the `apply_gate` function: `'isw'`, `'iswap'`
- SymPy matrix name in `pyquantumkit.symbol.gate`: `iSWAP`

## 3. Three-Qubit Gates
### Toffoli Gate (CCNOT Gate)
- Matrix:

$$ \begin{bmatrix} 1 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 1 \\ 0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 \end{bmatrix} $$

- Call strings for the `apply_gate` function: `'ccx'`, `'ccnot'`, `'toffoli'`
- SymPy matrix name in `pyquantumkit.symbol.gate`: `Toffoli`

### Fredkin Gate (Controlled-SWAP Gate)
- Matrix:

$$ \begin{bmatrix} 1 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 1 \end{bmatrix} $$

- Call strings for the `apply_gate` function: `'csw'`, `'cswap'`, `'fredkin'`
- SymPy matrix name in `pyquantumkit.symbol.gate`: `Fredkin`

### CCZ Gate
- Matrix:

$$ \begin{bmatrix} 1 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & -1 \end{bmatrix} $$

- Call strings for the `apply_gate` function: `'ccz'`
- SymPy matrix name in `pyquantumkit.symbol.gate`: `CCZ`

## 4. Single-Qubit Parameterized Gates
### $R_x(\theta)$ Gate
- Matrix:

$$ \begin{bmatrix} \cos\frac{\theta}{2} & -i\sin\frac{\theta}{2} \\ -i\sin\frac{\theta}{2} & \cos\frac{\theta}{2} \end{bmatrix} $$

- Call strings for the `apply_gate` function: `'rx'`
- `paras` parameter for the `apply_gate` function: `[theta_]`
- SymPy matrix name in `pyquantumkit.symbol.gate`: `Rx(theta_)`

### $R_y(\theta)$ Gate
- Matrix:

$$ \begin{bmatrix} \cos\frac{\theta}{2} & -\sin\frac{\theta}{2} \\ \sin\frac{\theta}{2} & \cos\frac{\theta}{2} \end{bmatrix} $$

- Call strings for the `apply_gate` function: `'ry'`
- `paras` parameter for the `apply_gate` function: `[theta_]`
- SymPy matrix name in `pyquantumkit.symbol.gate`: `Ry(theta_)`

### $R_z(\theta)$ Gate
- Matrix:

$$ \begin{bmatrix} e^{-i\frac{\theta}{2}} & 0 \\ 0 & e^{i\frac{\theta}{2}} \end{bmatrix} $$

- Call strings for the `apply_gate` function: `'rz'`
- `paras` parameter for the `apply_gate` function: `[theta_]`
- SymPy matrix name in `pyquantumkit.symbol.gate`: `Rz(theta_)`

### $P(\theta)$ Gate ( $U1(\theta)$ Gate)
- Matrix:

$$ \begin{bmatrix} 1 & 0 \\ 0 & e^{i\theta} \end{bmatrix} $$

- Call strings for the `apply_gate` function: `'p'`, `'u1'`, `'r1'`
- `paras` parameter for the `apply_gate` function: `[theta_]`
- SymPy matrix name in `pyquantumkit.symbol.gate`: `U1(theta_)`

### $U3(\theta,\phi,\lambda)$ Gate (General Single-Qubit Gate)
- Matrix:

$$ \begin{bmatrix} \cos\frac{\theta}{2} & -e^{i\lambda}\sin\frac{\theta}{2} \\ e^{i\phi}\sin\frac{\theta}{2} & e^{i(\phi+\lambda)}\cos\frac{\theta}{2} \end{bmatrix} $$

- Call strings for the `apply_gate` function: `'u'`, `'u3'`
- `paras` parameter for the `apply_gate` function: `[theta_, phi_, lambda_]`
- SymPy matrix name in `pyquantumkit.symbol.gate`: `U3(theta_, phi_, lambda_)`

## 5. Two-Qubit Parameterized Gates
### Controlled $R_x(\theta)$ Gate
- Matrix:

$$ \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & \cos\frac{\theta}{2} & -i\sin\frac{\theta}{2} \\ 0 & 0 & -i\sin\frac{\theta}{2} & \cos\frac{\theta}{2} \end{bmatrix} $$

- Call strings for the `apply_gate` function: `'crx'`
- `paras` parameter for the `apply_gate` function: `[theta_]`
- SymPy matrix name in `pyquantumkit.symbol.gate`: `CRx(theta_)`

### Controlled $R_y(\theta)$ Gate
- Matrix:

$$ \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & \cos\frac{\theta}{2} & -\sin\frac{\theta}{2} \\ 0 & 0 & \sin\frac{\theta}{2} & \cos\frac{\theta}{2} \end{bmatrix} $$

- Call strings for the `apply_gate` function: `'cry'`
- `paras` parameter for the `apply_gate` function: `[theta_]`
- SymPy matrix name in `pyquantumkit.symbol.gate`: `CRy(theta_)`

### Controlled $R_z(\theta)$ Gate
- Matrix:

$$ \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & e^{-i\frac{\theta}{2}} & 0 \\ 0 & 0 & 0 & e^{i\frac{\theta}{2}} \end{bmatrix} $$

- Call strings for the `apply_gate` function: `'crz'`
- `paras` parameter for the `apply_gate` function: `[theta_]`
- SymPy matrix name in `pyquantumkit.symbol.gate`: `CRz(theta_)`

### Controlled $P(\theta)$ Gate
- Matrix:

$$ \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & e^{i\theta} \end{bmatrix} $$

- Call strings for the `apply_gate` function: `'cp'`, `'cu1'`, `'cr1'`
- `paras` parameter for the `apply_gate` function: `[theta_]`
- SymPy matrix name in `pyquantumkit.symbol.gate`: `CU1(theta_)`

### $R_{xx}(\theta)$ Gate
- Matrix:

$$ \begin{bmatrix} \cos\frac{\theta}{2} & 0 & 0 & -i\sin\frac{\theta}{2} \\ 0 & \cos\frac{\theta}{2} & -i\sin\frac{\theta}{2} & 0 \\ 0 & -i\sin\frac{\theta}{2} & \cos\frac{\theta}{2} & 0 \\ -i\sin\frac{\theta}{2} & 0 & 0 & \cos\frac{\theta}{2} \end{bmatrix} $$

- Call strings for the `apply_gate` function: `'rxx'`
- `paras` parameter for the `apply_gate` function: `[theta_]`
- SymPy matrix name in `pyquantumkit.symbol.gate`: `Rxx(theta_)`

### $R_{yy}(\theta)$ Gate
- Matrix:

$$ \begin{bmatrix} \cos\frac{\theta}{2} & 0 & 0 & i\sin\frac{\theta}{2} \\ 0 & \cos\frac{\theta}{2} & -i\sin\frac{\theta}{2} & 0 \\ 0 & -i\sin\frac{\theta}{2} & \cos\frac{\theta}{2} & 0 \\ i\sin\frac{\theta}{2} & 0 & 0 & \cos\frac{\theta}{2} \end{bmatrix} $$

- Call strings for the `apply_gate` function: `'Ryy'`
- `paras` parameter for the `apply_gate` function: `[theta_]`
- SymPy matrix name in `pyquantumkit.symbol.gate`: `Ryy(theta_)`

### $R_{zz}(\theta)$ Gate
- Matrix:

$$ \begin{bmatrix} e^{-i\frac{\theta}{2}} & 0 & 0 & 0 \\ 0 & e^{i\frac{\theta}{2}} & 0 & 0 \\ 0 & 0 & e^{i\frac{\theta}{2}} & 0 \\ 0 & 0 & 0 & e^{-i\frac{\theta}{2}} \end{bmatrix} $$

- Call strings for the `apply_gate` function: `'rzz'`
- `paras` parameter for the `apply_gate` function: `[theta_]`
- SymPy matrix name in `pyquantumkit.symbol.gate`: `Rzz(theta_)`
