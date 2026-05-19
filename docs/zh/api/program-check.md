# pyquantumkit.program_check模块
program_check模块提供了用于检验量子线路和量子程序的函数。

## pyquantumkit.program_check.matrix_based模块
`pyquantumkit.program_check.matrix_based`提供了基于矩阵表示的量子线路检验方法。

### numeric_equivalence_check函数
`numeric_equivalence_check`函数输入代表两个量子线路的NumPy矩阵，利用矩阵范数检验它们是否等价。函数原型为：

```python
def numeric_equivalence_check(cirmat1 : numpy.array, cirmat2 : numpy.array,
                              ignore_global_phase : bool = True,
                              tolerance : float = DEFAULT_TOLERANCE,
                              norm = numpy_2_norm) -> bool:
```
- 参数`cirmat1`为代表第一个量子线路的NumPy矩阵（可以利用CircuitIO类的`get_numpy_matrix`函数获取，[点此查看](./circuitio.md#get_numpy_matrix)）。
- 参数`cirmat2`为代表第二个量子线路的NumPy矩阵。
- 参数`ignore_global_phase`指定在检验等价时，是否忽略全局相位。如果设置为`False`，则只有当两个量子线路对应的矩阵在误差范围内相等时才判定为等价；如果设置为`True`，则只要两个量子线路对应的矩阵只相差一个全局相位时就判定为等价。默认为`True`。
- 参数`tolerance`指定在判定相等时的误差容许度，默认为`DEFAULT_TOLERANCE = 0.001`。
- 参数`norm`指定计算时采用的矩阵范数函数，范数函数应以`numpy.array`类型作为唯一参数，以`float`类型作为返回值。用户可以自定义的范数函数，也可使用如下预置的范数函数（默认为`numpy_2_norm`）：
    - `numpy_1_norm`: 1-范数 $\|A\|_1 = \max_{1\leq j \leq n}\sum_{i=1}^n a_{ij}$
    - `numpy_2_norm`: 2-范数（谱范数）， $A^T A$ 的最大特征值的平方根。
    - `numpy_inf_norm`: $\infty$-范数 $\|A\|_{\infty} = \max_{1\leq i \leq n}\sum_{j=1}^n a_{ij}$
    - `numpy_frobenius_norm`: Frobenius范数 $\|A\|_F = \sqrt{\sum_{i=1}^n \sum_{j=1}^n |a_{ij}|^2}$

若两个量子线路判定为相等，则返回`True`；否则返回`False`。

该函数的具体执行流程为：设两个量子线路对应的矩阵分别为 $A$, $B$ ，传入的`tolerance`参数记为 $\epsilon$ ，
- 若`ignore_global_phase`设置为`False`，则函数按照给定的范数函数`norm`计算两矩阵差值的范数 $\|A-B\|$ 并与 $\epsilon$ 进行比较，函数返回`True`当且仅当 $\|A-B\| \leq \epsilon$ 。
- 若`ignore_global_phase`设置为`True`，则函数首先寻找 $B$ 中模最大的元素，假设其下标为 $i',j'$ ；然后函数通过该元素下标计算 $A$ 与 $B$ 之间的可能存在的相位差： $\kappa=a_{i'j'}/b_{i'j'}$ ；最后函数按照给定的范数函数`norm`计算范数 $\|A-\kappa B\|$ 并与 $\epsilon$ 进行比较，函数返回`True`当且仅当 $\|A-\kappa B\| \leq \epsilon$ 。

### numeric_identity_check函数
`numeric_equivalence_check`函数输入一个代表量子线路的NumPy矩阵，利用矩阵范数检验它是否为恒等变换（Identity）。函数原型为：

```python
def numeric_identity_check(cirmat : numpy.array,
                           ignore_global_phase : bool = True,
                           tolerance : float = DEFAULT_TOLERANCE,
                           norm = numpy_2_norm) -> bool:
```
- 参数`cirmat`为代表待检验量子线路的NumPy矩阵。
- 参数`ignore_global_phase`指定在检验等价时，是否忽略全局相位。如果设置为`False`，则只有当两个量子线路对应的矩阵在误差范围内相等时才判定为等价；如果设置为`True`，则只要两个量子线路对应的矩阵只相差一个全局相位时就判定为等价。默认为`True`。
- 参数`tolerance`指定在判定相等时的误差容许度，默认为`DEFAULT_TOLERANCE = 0.001`。
- 参数`norm`指定计算时采用的矩阵范数函数（与`numeric_equivalence_check`函数的同名参数相同），默认为`numpy_2_norm`。

若量子线路判定为恒等变换，则返回`True`；否则返回`False`。

该函数等价于对`cirmat`和与它同阶数的单位矩阵调用`numeric_equivalence_check`函数。
