# Welcome to PyQuantumKit

As a developer who wants to use quantum computing technology, are you facing the following problems?

- The internationally-used IBM quantum hardware platform cannot be used in China.
- You want to use domestic quantum hardware platforms, but different platforms have their own independent software packages and frameworks, so switching to another platform forces you to rewrite the code. In addition, the quantum gates supported and the APIs provided by different quantum platforms differ, so converting code between platforms requires extra effort for adaptation.
- **The current level of quantum programming is low, requiring you to manipulate individual qubits as if writing assembly language to operate registers, and the running results are 0/1 strings that users must interpret themselves.**
- There is a lack of tools for verifying the correctness of quantum circuits.


## Design Goals

To solve the above problems and realize high-level-language quantum programming and cross-(quantum hardware)-platform development of quantum computing applications, we designed PyQuantumKit. It is a Python-based cross-platform quantum program development tool, and can also be used as middleware for building cross-platform quantum applications. The design goals of PyQuantumKit include:

- **Provide high-level-language quantum programming capabilities, allowing users to use Python syntax to write high-level-language quantum programs;**
- **Provide multiple quantum data types, and support users in defining custom quantum data types based on Python syntax;**
- High-level-language quantum programs can be compiled into quantum circuits on different quantum development frameworks, achieving **cross-platform development**;
- The software architecture is **extensible**, making it convenient to add more features and support for more quantum development frameworks in the future;
- The source code is **fully open source**, providing an experimental platform for research on new quantum software technologies.

### Featured Functions

- **High-level-language quantum programming:** Provides Python-based high-level-language quantum program design, with support for quantum data types (arrays, structs, tuples, unions, etc.), and enables interpretation of the 0/1 string running results;
- **Cross-platform development:** Write code once and compile it into quantum circuits on different quantum development frameworks, enabling execution on different quantum platforms;
- **Platform extensibility:** Provides several built-in quantum development framework supports, and (new in v.0.2.1) also supports users in adding additional quantum development framework support;
- **Symbolic representation:** Generates the symbolic matrix representation of quantum circuits (based on sympy).

## Built-in Quantum Development Framework / Programming Language Support
PyQuantumKit has built-in support for the following quantum development frameworks:

`qiskit`, `pyqpanda3`, `pyquafu`, `cqlib`

PyQuantumKit has built-in translation to the following quantum programming languages:

`OpenQASM2.0`, `Q#`, `isQ`

In addition, starting from PyQuantumKit v.0.2.1, users are allowed to add additional quantum development framework/language support.

## Contact Us
PyQuantumKit is developed by the Computing Center of the Institute of High Energy Physics, Chinese Academy of Sciences, with support from the National High Energy Physics Science Data Center.

Project leader: Long Peixun [longpx@ihep.ac.cn](mailto:longpx@ihep.ac.cn)