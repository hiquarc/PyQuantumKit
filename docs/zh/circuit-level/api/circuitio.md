# CircuitIO类成员函数速查
本页给出CircuitIO类的各成员函数，供用户查阅。

## 1. 初始化与比特数
### 初始化__init__
定义一个CircuitIO对象时，会调用它的初始化方法（构造函数）`__init__`，函数原型为：

```python
def __init__(self, nqbits : int = 0, ncbits : int = 0) -> None
```
- 参数`nqbits`指定CircuitIO对象包含的量子比特数，默认为0。
- 参数`ncbits`指定CircuitIO对象包含的经典比特数，默认为0。

**注：CircuitIO类的“量子比特数”和“经典比特数”两个参数仅仅用作提示（例如并联两个量子线路时），在应用量子门时不会对下标是否溢出进行检查。**

### set_nqbits
`set_nqbits`函数设置CircuitIO对象的量子比特数，函数原型为：

```python
def set_nqbits(self, nqbits) -> None
```
- 参数`nqbits`指定要设置的量子比特数。

### set_ncbits
`set_ncbits`函数设置CircuitIO对象的经典比特数，函数原型为：

```python
def set_ncbits(self, ncbits) -> None
```
- 参数`ncbits`指定要设置的量子比特数。

### get_nqbits
`get_nqbits`函数返回CircuitIO对象的量子比特数，函数原型为：

```python
def get_nqbits(self) -> int
```

### get_ncbits
`get_ncbits`函数返回CircuitIO对象的经典比特数，函数原型为：

```python
def get_ncbits(self) -> int
```

## 2. 应用量子门
### apply_gate
CircuitIO类的`apply_gate`成员函数与全局的`apply_gate`函数类似，可以在CircuitIO对象的量子线路上应用量子门。

```python
def apply_gate(self, gatestr : str, qbits : list[int], paras : list = None) -> None
```
- 参数`gate_str`是一个字符串，用于指示需要应用的门。考虑到同一个门可能有多个不同的名称（例如Toffoli,CCNOT,CCX都表示同一个门），PyQuantumKit允许以不同的名字字符串来表示同一个门，且不区分大小写。[点此查看](supported-gates.md)具体支持的量子门及其对应的字符串。
- 参数`qbits`是一个整数列表，指定门要应用的量子比特下标列表。注意无论量子门是单比特还是多比特，都需要**以列表的方式指派此参数**。
- 参数`paras`是一个列表，用于为含参数门指派参数；对于无参数门，不用指派此参数。

对CircuitIO对象`CircuitIO_Obj`使用`apply_gate`成员函数：
```python
CircuitIO_Obj.apply_gate('H', [2])
```
可以等价替换为全局的`apply_gate`函数，只要将CircuitIO对象作为代表量子线路的参数传入：
```python
apply_gate(CircuitIO_Obj, 'H', [2])
```

### apply_measure
CircuitIO类的`apply_measure`成员函数与全局的`apply_measure`函数类似，可以在CircuitIO对象的量子线路上应用量子测量操作。

```python
def apply_measure(self, qindex : list[int], cindex : list[int]) -> None
```
- 参数`qindex`是一个整数列表，指定要测量的量子比特下标。
- 参数`cindex`是一个整数列表，指定测量结果存放的经典比特下标。`qindex`和`cindex`各分量分别对应，因此`qindex`和`cindex`长度应相同。

对CircuitIO对象`CircuitIO_Obj`使用`apply_measure`成员函数：
```python
CircuitIO_Obj.apply_measure([0, 1, 2], [0, 1, 2])
```
可以等价替换为全局的`apply_measure`函数，只要将CircuitIO对象作为代表量子线路的参数传入：
```python
apply_measure(CircuitIO_Obj, [0, 1, 2], [0, 1, 2])
```

## 3. 模块化构建
### inverse
`inverse`函数将当前CircuitIO对象中的量子线路反转为逆线路（就地操作）。

```python
def inverse(self)
```

### remap_qbits
`remap_qbits`函数对当前CircuitIO对象中的量子比特的下标进行重映射（就地操作）。

```python
def remap_qbits(self, remap : int|list|range)
```
- 参数`remap`指派量子比特的重映射方式，传入类型可以为`int`或`list[int]`，默认为`None`，表示不进行重映射。当传入`int`类型时，源量子线路的每个量子比特的下标在串联时会增加此整数值；当传入`list[int]`类型时，串联时按照此数组的指示进行重映射。

### remap_cbits
`remap_cbits`函数对当前CircuitIO对象中的经典比特的下标进行重映射（就地操作）。

```python
def remap_cbits(self, remap : int|list|range)
```
- 参数`remap`指派经典比特的重映射方式，传入类型可以为`int`或`list[int]`，默认为`None`，表示不进行重映射。当传入`int`类型时，源量子线路的每个经典比特的下标在串联时会增加此整数值；当传入`list[int]`类型时，串联时按照此数组的指示进行重映射。

### append_circuit_io
`append_circuit_io`函数将另一个CircuitIO对象的量子线路串联到本对象的量子线路末尾。

```python
def append_circuit_io(self, cir_io_obj)
```
- 参数`cir_io_obj`指派源量子线路。

### << 运算符
`append_circuit_io`函数可用`<<`运算符替换。

```python
def __lshift__(self, cir_io_obj)
```

例如，以下代码
```python
import pyquantumkit
cio1 = pyquantumkit.CircuitIO(3)
cio2 = pyquantumkit.CircuitIO(3)
# ... construct circuit code ...
cio1.append_circuit_io(cio2)
```
中，最后一行

`cio1.append_circuit_io(cio2)`

将`cio2`中的量子线路串联到`cio1`的末尾。这行可以等价替换为：

`cio1 << cio2`


## 4. 属性检验
### contains_measure
`contains_measure`检查CircuitIO对象中是否包含测量操作，若包含则返回`True`。

```python
def contains_measure(self) -> bool
```

### check_nqbits
`check_nqbits`函数检查CircuitIO对象中的各量子门操作是否出现下标越界，即使用了超出量子比特数目的量子比特下标。

```python
def check_nqbits(self, adjust : bool = False) -> bool
```
- 参数`adjust`指定当检验出现下标越界时，是否自动调整量子比特数目以适应其中的量子门操作的下标。默认为`False`，即从不调整。

若无下标越界，返回`True`；否则返回`False`，并且若`adjust`参数为`True`时，自动调整量子比特数目。

### check_ncbits
`check_ncbits`函数检查CircuitIO对象中的测量操作的经典比特是否出现下标越界，即使用了超出经典比特数目的经典比特下标。

```python
def check_ncbits(self, adjust : bool = False) -> bool
```

- 参数`adjust`指定当检验出现下标越界时，是否自动调整经典比特数目以适应其中的测量操作的下标。默认为`False`，即从不调整。

若无下标越界，返回`True`；否则返回`False`，并且若`adjust`参数为`True`时，自动调整经典比特数目。

## 5. 矩阵符号表示
### get_sympy_matrix
`get_sympy_matrix`函数计算CircuitIO对象中量子线路对应的矩阵表示，返回SymPy矩阵对象。

```python
def get_sympy_matrix(self, subsdict : dict = None, simplify : bool = True) -> sympy.Matrix
```
- 可选参数`subsdict`是一个字典，用于指定SymPy符号代入规则。默认为None，即不进行任何符号代换。**注：只有当使用了SymPy符号作为量子门参数时才需要指定此参数。** 例如，传入`{t : 3, x : 4}`表示用数字3代入符号`t`，用数字4代入符号`x`。
- 可选参数`simplify`指定是否在计算矩阵表示的过程中进行化简（即SymPy的simplify操作），默认为`True`。

函数返回SymPy矩阵对象。

### get_numpy_matrix
`get_numpy_matrix`函数计算CircuitIO对象中量子线路对应的矩阵表示，返回NumPy矩阵对象。

```python
def get_numpy_matrix(self, subsdict : dict = None) -> numpy.array
```
- 参数`subsdict`是一个字典，指定在计算时是否需要对其中的符号进行代换，以及代换方式。默认为`None`，即不进行代换。

函数返回NumPy矩阵对象。

### symbol_subs
`symbol_subs`函数对CircuitIO对象中的SymPy符号进行代换（就地操作）。

```python
def symbol_subs(self, subsdict : dict)
```
- 参数`subsdict`是一个字典，指定代换方式。

## 6. 导出线路
### get_circuit_code
`get_circuit_code`函数将CircuitIO对象中的量子线路导出到受支持的编程语言的代码。

```python
def get_circuit_code(self, language : str, circuit_name : str,
                     gate_lib_name : str = None, linebreak : str = '\n',
                     subsdict : dict = None) -> str
```
- 参数`language`是一个字符串，指定导出的语言（[点此查看](./supported-platforms.md)）。
- 参数`circuit_name`是一个字符串，指定导出代码中，量子线路对象名称。
- 参数`gate_lib_name`是一个字符串，指定导出代码中，量子线路对象名称的包前缀，默认为`None`，即无前缀。**注：无前缀请指定为`None`，不要指定为空字符串`''`。**
- 参数`linebreak`是一个字符串，指定导出代码中各语句之间的分隔符，默认为换行符`'\n'`。
- 参数`subsdict`是一个字典，指定在导出代码时是否需要对其中的符号进行代换，以及代换方式。默认为`None`，即不进行代换。

函数返回包含导出代码的字符串。

### append_into_actual_circuit
`append_into_actual_circuit`函数将CircuitIO对象中的量子线路插入到具体的量子开发框架的量子线路对象中。

```python
def append_into_actual_circuit(self, dest_qcir, subsdict : dict = None)
```

**注：当需要在插入到具体的量子开发框架的量子线路的过程中进行符号代入时，不能使用`>>`运算符，必须显式使用`append_into_actual_circuit`成员函数。**

### >> 运算符
在不使用符号替换的情况下，`append_into_actual_circuit`函数可用`>>`运算符替换。

```python
def __rshift__(self, dest_qcir)
```

例如，以下代码
```python
import qiskit
import pyquantumkit
qc = qiskit.QuantumCircuit(3)
cio = pyquantumkit.CircuitIO(3)
# ... construct circuit code ...
cio.append_into_actual_circuit(qc)
```
中，最后一行

`cio.append_into_actual_circuit(qc)`

可等价替换为

`cio >> qc`
