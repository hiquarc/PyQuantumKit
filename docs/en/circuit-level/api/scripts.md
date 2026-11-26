# Built-in Translation Script Reference
This document lists the translation scripts for the quantum development frameworks and quantum programming languages built into PyQuantumKit, for users to reference when writing their own translation scripts.

## Python-based quantum development frameworks
### qiskit
Qiskit is an open-source quantum computing software stack led by IBM, built on Python. Its core function is to provide stable tools for building, optimizing, compiling, and executing quantum circuits, supporting work at the level of extended quantum circuits, operators, and primitives. Qiskit's compiler can adapt to various quantum hardware backends such as IBM, IonQ, and Azure Quantum. This software has a large user base in the field of quantum computing and is used in education, research, and industry.

```python title="qiskit.py"
--8<-- "pyquantumkit/translate/translate_scripts/qiskit.py"
```

### pyqpanda3
pyqpanda3 is the Python SDK of QPanda3 (Origin Quantum's high-performance quantum computing framework). It provides a comprehensive set of tools for building, optimizing, and running quantum circuits, as well as connecting to real quantum hardware through Origin Quantum's cloud service.

```python title="pyqpanda3.py"
--8<-- "pyquantumkit/translate/translate_scripts/pyqpanda3.py"
```

### pyquafu

Note: the pyquafu here corresponds to the **old PyQuafu platform**, whose documentation website is: [https://scq-cloud.github.io/](https://scq-cloud.github.io/)

In October 2026, the Quafu platform underwent an update and no longer uses the old pyquafu to submit quantum circuits, but instead uses OpenQASM 2.0 syntax to submit quantum circuits. See the new Quafu platform website for details: [https://quafu.com.cn/](https://quafu.com.cn/)

```python title="pyquafu.py"
--8<-- "pyquantumkit/translate/translate_scripts/pyquafu.py"
```

### cqlib
Cqlib is an open-source quantum programming framework independently developed by China Telecom Quantum Group, a subsidiary of China Telecom. As the supporting software development tool of the Tianyan quantum computing cloud platform, it provides full-chain capabilities from quantum circuit design and compilation optimization to real hardware invocation.

```python title="cqlib.py"
--8<-- "pyquantumkit/translate/translate_scripts/cqlib.py"
```

## Other quantum programming languages
### OpenQASM 2.0
OpenQASM 2.0 is an open quantum assembly language for describing quantum circuits, launched by IBM in 2017, and is still the basic format for interaction between many quantum programming frameworks and hardware.

```python title="openqasm2.py"
--8<-- "pyquantumkit/translate/extra/openqasm2.py"
```

### Q\#
Q# is an open-source quantum programming language developed by Microsoft, specifically designed for writing quantum programs, and is included in the Microsoft Quantum Development Kit (QDK).

```python title="qsharp.py"
--8<-- "pyquantumkit/translate/extra/qsharp.py"
```

### isQ
isQ is part of the quantum software toolkit of the Institute of Software, Chinese Academy of Sciences. The isQ compiler takes an isQ program as input and generates low-level code written in various intermediate representations or instruction sets (depending on the compiler options).

```python title="isq.py"
--8<-- "pyquantumkit/translate/extra/isq.py"
```