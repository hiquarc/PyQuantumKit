# 内置翻译脚本参考
本文列出PyQuantumKit内置支持的量子开发框架和量子编程语言的翻译脚本，供用户自己编写翻译脚本时参考。

## 基于Python的量子开发框架
### qiskit
Qiskit是一个由IBM主导开发的开源量子计算软件栈，基于Python构建。其核心功能是提供构建、优化、编译和执行量子电路的稳定工具，支持在扩展量子电路、算子和原语级别上工作。Qiskit的编译器能适配IBM、IonQ、Azure Quantum等多种量子硬件后端。该软件在量子计算领域拥有较大的用户群体，被应用于教育、研究和产业中。

```python title="qiskit.py"
--8<-- "pyquantumkit/translate/translate_scripts/qiskit.py"
```

### pyqpanda3
pyqpanda3 是 QPanda3（本源量子的高性能量子计算框架）的 Python SDK。它提供了一套全面的工具，用于构建、优化和允许量子线路，以及通过本源量子云服务连接到真实量子硬件。

```python title="pyqpanda3.py"
--8<-- "pyquantumkit/translate/translate_scripts/pyqpanda3.py"
```

### pyquafu

注：这里的pyquafu对应的是**旧版PyQuafu平台**，文档网址：[https://scq-cloud.github.io/](https://scq-cloud.github.io/)

2026年10月Quafu平台进行了一次更新，不再使用旧版pyquafu提交量子线路，而是使用OpenQASM 2.0语法提交量子线路。详见新版Quafu平台网址：[https://quafu.com.cn/](https://quafu.com.cn/)

```python title="pyquafu.py"
--8<-- "pyquantumkit/translate/translate_scripts/pyquafu.py"
```

### cqlib
‌Cqlib 是中国电信旗下中电信量子集团自主研发的开源量子编程框架‌，作为天衍量子计算云平台的配套软件开发工具，提供从量子电路设计、编译优化到真实硬件调用的全链条能力 。‌‌

```python title="cqlib.py"
--8<-- "pyquantumkit/translate/translate_scripts/cqlib.py"
```

## 其他量子编程语言
### OpenQASM 2.0
‌OpenQASM 2.0 是一种用于描述量子电路的开放量子汇编语言‌，由 IBM 于 2017 年推出，目前仍是许多量子编程框架和硬件交互的基础格式。‌‌

```python title="openqasm2.py"
--8<-- "pyquantumkit/translate/extra/openqasm2.py"
```

### Q\#
Q# 是由‌微软开发的开源量子编程语言‌，专门用于编写量子程序，包含在 Microsoft Quantum 开发工具包（QDK）中 。‌‌

```python title="qsharp.py"
--8<-- "pyquantumkit/translate/extra/qsharp.py"
```

### isQ
isQ是中国科学院软件研究所量子软件工具包的一部分。isQ编译器接收isQ程序作为输入，并生成以多种中间表示或指令集（具体取决于编译器选项）编写的低级代码。

```python title="isq.py"
--8<-- "pyquantumkit/translate/extra/isq.py"
```
