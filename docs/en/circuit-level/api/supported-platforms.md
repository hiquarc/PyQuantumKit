# Quick Reference of Quantum Development Framework
## Supported Python-based Quantum Development Frameworks

This page lists the quantum development frameworks supported by PyQuantumKit.

PyQuantumKit supports multiple quantum development frameworks through a "code translation" approach. It identifies the type of quantum circuit in function parameters and its associated quantum development framework, then translates the function call into the corresponding call code for that quantum development framework. The currently supported quantum development frameworks and their corresponding framework name strings (case-sensitive) are as follows:

- **IBM Qiskit** : `'qiskit'`
- **Origin Quantum QPanda3** : `'pyqpanda3'`
- **Beijing Academy of Quantum Information Sciences Quafu** : `'quafu'`
- **Cqlib** : `'cqlib'`

Due to the varying functionality supported by different quantum development frameworks, PyQuantumKit may not be able to translate some unified code into call code for the corresponding quantum development framework. If you need to use these functions on an unsupported quantum development framework, you can consider implementing them indirectly based on the CircuitIO class ([see details](../stable/circuit.md#iii-circuitio-class)). The table below shows the functional support of each quantum development framework:

| | qiskit | pyqpanda3 | quafu | cqlib |  
| --- |:---:|:---:|:---:|:---:| 
| Create new quantum circuit | &#10003; | &#10003; | &#10003; | &#10003; |
| Apply quantum gate | &#10003; | &#10003; | &#10003; | &#10003; |
| Apply measurement | &#10003; | &#10003; | &#10003; | &#10003; |
| Support classical bits | &#10003; | &#10003; | &#10003; |  |
| Combination between quantum circuits | &#10003; | &#10003; |  |  |
| Qubit remapping | &#10003; | &#10003; |  |  |
| Generate inverse circuit | &#10003; | &#10003; |  |  |
| Local quantum simulator | &#10003; | &#10003; | &#10003; |  |

## Additional Quantum Programming Languages Supported for Code Export

PyQuantumKit can export code from the quantum circuit of a CircuitIO object. In addition to the above Python-based quantum development frameworks, it also supports exporting code to the following programming languages (name strings are case-sensitive):

- **Microsoft Q\#** : `'QSharp'` or `'Q#'`
- **isQ** : `'isQ'`
