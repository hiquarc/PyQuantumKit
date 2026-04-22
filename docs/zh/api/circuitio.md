# CircuitIO类成员函数速查
本页给出CircuitIO类的各成员函数，供用户查阅。

## 1. 基本操作
### 初始化__init__
定义一个CircuitIO对象时，会调用它的初始化方法（构造函数）`__init__`，函数原型为：

```python
def __init__(self, nqbits : int = 0, ncbits : int = 0) -> None
```
- 参数`nqbits`指定CircuitIO对象包含的量子比特数，默认为0。
- 参数`ncbits`指定CircuitIO对象包含的经典比特数，默认为0。

**注：CircuitIO类的“量子比特数”和“经典比特数”两个参数仅仅用作提示，在应用量子门时不会对下标是否溢出进行检查。**

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

```python
def apply_gate(self, gatestr : str, qbits : list[int], paras : list = None) -> None
```

### apply_measure

```python
def apply_measure(self, qindex : list[int], cindex : list[int]) -> None
```

## 3. 模块化构建
### inverse
`inverse`函数将当前CircuitIO对象中的量子线路反转为逆线路（就地操作）。

```python
def inverse(self)
```

### remap_qbits

```python
def remap_qbits(self, remap : int|list|range)
```

### remap_cbits

```python
def remap_cbits(self, remap : int|list|range)
```

### append_circuit_io
`append_circuit_io`函数将另一个CircuitIO对象的量子线路串联到本对象的量子线路末尾。

```python
def append_circuit_io(self, cir_io_obj)
```

### << 运算符
`append_circuit_io`函数可用`<<`运算符替换。

```python
def __lshift__(self, cir_io_obj)
```


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

```python
def get_sympy_matrix(self, subsdict : dict = None, simplify : bool = True) -> sympy.Matrix
```

### get_numpy_matrix

```python
def get_numpy_matrix(self, subsdict : dict = None) -> numpy.array
```

### symbol_subs

```python
def symbol_subs(self, subsdict : dict)
```

## 6. 导出线路
### get_circuit_code
`get_circuit_code`函数将CircuitIO对象中的量子线路导出到受支持的编程语言的代码。

```python
def get_circuit_code(self, language : str, circuit_name : str,
                     gate_lib_name : str = None, linebreak : str = '\n',
                     subsdict : dict = None) -> str
```
- 参数`language`

### append_into_actual_circuit
`append_into_actual_circuit`函数将CircuitIO对象中的量子线路插入到具体的量子开发框架的量子线路对象中。

```python
def append_into_actual_circuit(self, dest_qcir, subsdict : dict = None)
```

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
