# Quantum Development Frameworks Quick Reference
## Supported Python-based Quantum Development Frameworks

This page gives the quantum development frameworks supported by PyQuantumKit.

PyQuantumKit adopts a "code translation" approach to support multiple quantum development frameworks: by identifying the type of the quantum circuit in the function parameters and the quantum development framework to which it belongs, it translates the function call into the call code of the corresponding quantum development framework. The currently supported quantum development frameworks and their corresponding framework name strings (case-sensitive) are as follows:

- **IBM Qiskit** : `'qiskit'`
- **Origin Quantum QPanda3** : `'pyqpanda3'`
- **Beijing Academy of Quantum Quafu** : `'quafu'`
- **Cqlib** : `'cqlib'`

Since different quantum development frameworks support different features, PyQuantumKit may not be able to translate some unified code into the call code of the corresponding quantum development framework. If you need to use these features on an unsupported quantum development framework, you can consider implementing them indirectly based on the CircuitIO class ([see details](../circuit.md#circuitio)). The table below gives the feature support of each quantum development framework:

| | qiskit | pyqpanda3 | quafu | cqlib |  
| --- |:---:|:---:|:---:|:---:| 
| Create a new quantum circuit | &#10003; | &#10003; | &#10003; | &#10003; |
| Apply quantum gates | &#10003; | &#10003; | &#10003; | &#10003; |
| Apply measurement | &#10003; | &#10003; | &#10003; | &#10003; |
| Support classical bits | &#10003; | &#10003; | &#10003; |  |
| Combination between quantum circuits | &#10003; | &#10003; |  |  |
| Qubit remapping | &#10003; | &#10003; |  |  |
| Generate inverse circuits | &#10003; | &#10003; |  |  |
| Local quantum simulator | &#10003; | &#10003; | &#10003; |  |

## Quantum Programming Languages Additionally Supported for Code Export

PyQuantumKit can export code from the quantum circuit of a CircuitIO object. Besides the Python-based quantum development frameworks above, it additionally supports exporting code for the following programming languages (the name strings are case-sensitive):

- **Microsoft Q\#** : `'QSharp'` or `'Q#'`
- **isQ** : `'isQ'`
