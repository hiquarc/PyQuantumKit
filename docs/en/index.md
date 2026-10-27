# Welcome to PyQuantumKit

As a developer who wants to use quantum computing technology, are you facing the following problems?

- The internationally common IBM quantum hardware platform cannot be used domestically.
- You want to use domestic quantum hardware platforms, but different platforms have their own independent software packages and frameworks. When switching to another platform, you have to rewrite your code. In addition, the quantum gates supported and the APIs provided differ between quantum platforms, so converting code between platforms requires extra effort for adaptation.
- **Currently the level of quantum programming is rather low: you need to operate individual qubits just like writing assembly language to manipulate registers, and the running results are 0/1 strings that the user has to interpret on their own.**
- There is a lack of tools for verifying the correctness of quantum circuit construction.


## Design Goals

To solve the above problems and realize high-level-language-level quantum programming and cross-(quantum-hardware)-platform development of quantum computing applications, we designed PyQuantumKit. It is a Python-based cross-platform quantum program development tool that can also serve as middleware for building cross-platform quantum applications. The design goals of PyQuantumKit include:

- **Provide high-level-language-level quantum programming capability, so that users can write high-level-language-level quantum programs using Python syntax;**
- **Provide a variety of quantum data types, and support users in defining custom quantum data types based on Python syntax;**
- High-level-language-level quantum programs can be compiled into quantum circuits on different quantum development frameworks, achieving **cross-platform development**;
- The software architecture is **extensible**, so that more features and support for more quantum development frameworks can be easily added in the future;
- The source code is fully open source, providing an experimental platform for research on new quantum software technologies.

### Key Features

- **High-level-language-level quantum programming:** (new feature in v.0.2) Provides Python-based high-level-language-level quantum program design, with quantum data type support (arrays, structs, tuples, unions, etc.), enabling interpretation of 0/1 strings in running results;
- **Cross-platform development:** Write the code once and compile it into quantum circuits on different quantum development frameworks, thereby running on different quantum platforms;
- **Symbolic representation:** Generate a matrix symbolic representation of quantum circuits (based on sympy).

## Currently Supported Frameworks
PyQuantumKit v.0.2.0 currently supports the following quantum development frameworks:

- **IBM Qiskit**
- **Origin Quantum QPanda3**
- **Beijing Academy of Quantum Quafu**
- **Cqlib**

## Contact Us
PyQuantumKit is developed by the Computing Center of the Institute of High Energy Physics, Chinese Academy of Sciences, with support from the National High Energy Physics Science Data Center.

Project lead: Peixun Long [longpx@ihep.ac.cn](mailto:longpx@ihep.ac.cn)
