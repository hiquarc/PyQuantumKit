## 二、模块化构建
**注意：此功能为实验性功能，未经过系统性的测试，且接口在未来可能改变，请谨慎使用。**

区分circuit和program

### append_circuit

```python
def append_circuit(dest_qcir, src_qcir, remap = None, inverse : bool = False)
```

### copy_circuit

```python
def copy_circuit(src_qcir, remap = None, inverse : bool = False)
```

### append_program

```python
def append_program(dest_qp, src_qp, qbits_remap = None, cbits_remap = None)
```

### copy_program

```python
def copy_program(src_qp, qbits_remap = None, cbits_remap = None)
```

### new_circuit

```python
def new_circuit(framework, nqbits : int):
```

### new_program

```python
def new_program(framework, nqbits : int, ncbits : int = 0):
```

## 三、获取比特数目
