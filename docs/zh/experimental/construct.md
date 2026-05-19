# 量子线路的模块化构建
**注意：此功能为实验性功能，未经过系统性的测试，且接口在未来可能改变，请谨慎使用。**

PyQuantumKit提供了量子线路的模块化构建函数，实现量子线路的串联、并联、反转、比特重映射等功能。这些函数在具体的量子开发框架上将被翻译为对应框架的量子线路对象的串联、并联、反转、比特重映射。**因此这些功能需要目标量子框架支持才能实现。对于不受支持的框架，推荐使用CircuitIO类来间接实现，[点此查看](../stable/circuit.md#circuitio)详情。**

PyQuantumKit区分两类量子线路：其一称为Circuit，仅包含量子门，不包含测量；其二称为Program，除了量子门外还可包含测量及存储测量结果的经典比特。以`circuit`结尾的函数适用于Circuit，以`program`结尾的函数适用于Program。

## 一、量子线路操作
### new_circuit
`new_circuit`函数新建一个目标量子开发框架上的量子线路对象。

```python
def new_circuit(framework : str, nqbits : int)
```
- 字符串参数`framework`指示具体的框架名（例如`'qiskit'`、`'pyqpanda3'`）。
- 整数参数`nqbits`指派量子线路包含的量子比特数。

函数返回具体量子开发框架的量子线路对象（例如Qiskit的`QuantumCircuit`对象或QPanda3的`QCircuit`对象）。

### new_program
`new_program`函数新建一个目标量子开发框架上的量子线路对象。

```python
def new_program(framework : str, nqbits : int, ncbits : int = 0)
```
- 字符串参数`framework`指示具体的框架名（例如`'qiskit'`、`'pyqpanda3'`）。
- 整数参数`nqbits`指派量子线路包含的量子比特数。
- 整数参数`ncbits`指派量子线路包含的经典比特数。

函数返回具体量子开发框架的量子线路对象（例如Qiskit的`QuantumCircuit`对象或QPanda3的`QProg`对象）。

### copy_circuit
`copy_circuit`函数复制源量子比特，返回它的一个额外的独立副本，复制过程中可进行反转和比特重映射操作。

```python
def copy_circuit(src_qcir, remap : int|list|range = None, inverse : bool = False)
```
- 参数`src_qcir`指派源量子线路。
- 参数`qbits_remap`指派量子比特的重映射方式，传入类型可以为`int`或`list[int]`，默认为`None`，表示不进行重映射。当传入`int`类型时，源量子线路的每个量子比特的下标在串联时会增加此整数值；当传入`list[int]`类型时，串联时按照此数组的指示进行重映射。
- 参数`cbits_remap`指派经典比特的重映射方式，传入类型可以为`int`或`list[int]`，默认为`None`，表示不进行重映射。当传入`int`类型时，源量子线路的每个经典比特的下标在串联时会增加此整数值；当传入`list[int]`类型时，串联时按照此数组的指示进行重映射。

函数返回一个新的Circuit对象。

### copy_program
`copy_program`函数复制源量子比特，返回它的一个额外的独立副本，复制过程中可进行反转和比特重映射操作。

```python
def copy_program(src_qp, qbits_remap : int|list|range = None, cbits_remap : int|list|range = None)
```
- 参数`src_qcir`指派源量子线路。
- 参数`qbits_remap`指派量子比特的重映射方式，传入类型可以为`int`或`list[int]`，默认为`None`，表示不进行重映射。当传入`int`类型时，源量子线路的每个量子比特的下标在串联时会增加此整数值；当传入`list[int]`类型时，串联时按照此数组的指示进行重映射。
- 参数`cbits_remap`指派经典比特的重映射方式，传入类型可以为`int`或`list[int]`，默认为`None`，表示不进行重映射。当传入`int`类型时，源量子线路的每个经典比特的下标在串联时会增加此整数值；当传入`list[int]`类型时，串联时按照此数组的指示进行重映射。

函数返回一个新的Program对象。

### append_circuit
`append_circuit`函数将一个源量子线路串联到目标量子线路末尾，串联过程中可进行反转和比特重映射操作。

```python
def append_circuit(dest_qcir, src_qcir, remap : int|list|range = None, inverse : bool = False)
```
- 参数`dest_qcir`指派目标量子线路。
- 参数`src_qcir`指派源量子线路。
- 参数`remap`指派量子比特的重映射方式，传入类型可以为`int`或`list[int]`，默认为`None`，表示不进行重映射。当传入`int`类型时，源量子线路的每个量子比特的下标在串联时会增加此整数值；当传入`list[int]`类型时，串联时按照此数组的指示进行重映射。
- 参数`inverse`指派在串联时是否反转源量子线路，默认为`False`。

函数返回`dest_qcir`。

### append_program
`append_program`函数将一个源量子线路串联到目标量子线路末尾，串联过程中可进行反转和比特重映射操作。

```python
def append_program(dest_qp, src_qp, qbits_remap : int|list|range = None, cbits_remap : int|list|range = None)
```
- 参数`dest_qcir`指派目标量子线路。
- 参数`src_qcir`指派源量子线路。
- 参数`qbits_remap`指派量子比特的重映射方式，传入类型可以为`int`或`list[int]`，默认为`None`，表示不进行重映射。当传入`int`类型时，源量子线路的每个量子比特的下标在串联时会增加此整数值；当传入`list[int]`类型时，串联时按照此数组的指示进行重映射。
- 参数`cbits_remap`指派经典比特的重映射方式，传入类型可以为`int`或`list[int]`，默认为`None`，表示不进行重映射。当传入`int`类型时，源量子线路的每个经典比特的下标在串联时会增加此整数值；当传入`list[int]`类型时，串联时按照此数组的指示进行重映射。

函数返回`dest_qcir`。

### parallel_circuits
`parallel_circuits`函数并联若干个源量子线路，并联过程中将按顺序对源量子线路进行量子比特重映射。

```python
def parallel_circuits(*args)
```

示例：如下代码
```python
import pyquantumkit
qc1 = pyquantumkit.new_circuit('qiskit', 2)
qc2 = pyquantumkit.new_circuit('qiskit', 5)
qc3 = pyquantumkit.new_circuit('qiskit', 3)
parallel_qc = pyquantumkit.parallel_circuits(qc1, qc2, qc3)
```
返回的`parallel_qc`将包含2+5+3=10个量子比特，其中`qc1`作用于下标为0, 1的量子比特，`qc2`作用于下标为2, 3, 4, 5, 6的量子比特，`qc3`作用于下标为7, 8, 9的量子比特。

### parallel_programs
`parallel_programs`函数并联若干个源量子线路，并联过程中将按顺序对源量子线路进行量子比特和经典比特重映射。

```python
def parallel_programs(*args)
```

## 二、获取比特数目
### get_n_qubits
`get_n_qubits`函数返回量子线路的量子比特数。
```python
def get_n_qubits(q_prog) -> int
```

### get_qubit_list
`get_qubit_list`函数返回量子线路使用的量子比特下标数组。
```python
def get_qubit_list(q_prog) -> list[int]
```

### get_n_cbits
`get_n_cbits`函数返回量子线路的经典比特数。
```python
def get_n_cbits(q_prog) -> int
```

### get_cbit_list
`get_cbit_list`函数返回量子线路使用的经典比特下标数组。
```python
def get_cbit_list(q_prog) -> list[int]
```
