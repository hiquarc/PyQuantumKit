# Built-in Quantum Development Framework / Language Support Quick Reference
## Built-in supported Python-based quantum development frameworks

This page gives the quantum development frameworks supported by PyQuantumKit.

PyQuantumKit uses the "code translation" approach to implement support for multiple quantum development frameworks. By identifying the type of the quantum circuit in the function parameters and the quantum development framework it belongs to, it translates the function call into the corresponding call code of that quantum development framework. The currently supported quantum development frameworks and their corresponding framework name strings (case-sensitive) are as follows:

- **IBM Qiskit** : `'qiskit'`
- **Origin Quantum PyQPanda3** : `'pyqpanda3'`
- **Beijing Academy of Quantum Information Sciences PyQuafu** (old version) : `'quafu'`
- **China Telecom Quantum Cqlib** : `'cqlib'`

Note: The new version of the Quafu platform of the Beijing Academy of Quantum Information Sciences has switched to submitting quantum circuits in the OpenQASM 2.0 format, and no longer uses the old PyQuafu framework. See the new Quafu platform website for details: [https://quafu.com.cn/](https://quafu.com.cn/)

Since different quantum development frameworks support different functions, PyQuantumKit may not be able to translate some unified code into the corresponding call code of a quantum development framework. If these functions need to be used on an unsupported quantum development framework, consider implementing them indirectly based on the CircuitIO class ([view details](../circuit.md#circuitio)). The following table gives the function support of each quantum development framework:

| | qiskit | pyqpanda3 | pyquafu | cqlib |  
| --- |:---:|:---:|:---:|:---:| 
| Create a new quantum circuit | &#10003; | &#10003; | &#10003; | &#10003; |
| Apply quantum gates | &#10003; | &#10003; | &#10003; | &#10003; |
| Apply measurements | &#10003; | &#10003; | &#10003; | &#10003; |
| Support classical bits | &#10003; | &#10003; | &#10003; |  |
| Composition between quantum circuits | &#10003; | &#10003; |  |  |
| Qubit remapping | &#10003; | &#10003; |  |  |
| Generate inverse circuit | &#10003; | &#10003; |  |  |
| Local quantum simulator | &#10003; | &#10003; | &#10003; |  |

## Built-in supported quantum programming languages to which code can be exported

PyQuantumKit can export code from the quantum circuit of a CircuitIO object. In addition to supporting the Python-based quantum development frameworks above, it additionally supports exporting code to the following programming languages (name strings are case-sensitive):

- **OpenQASM 2.0** : `'OpenQASM2.0'` (newly supported in PyQuantumKit v.0.2.1)
- **Microsoft Q\#** : `'Q#'`
- **isQ** : `'isQ'`

## Support status of quantum subroutines
Here we list the names of the quantum subroutines supported by each quantum development framework; if not listed, it means not supported.

- **Qiskit** : `QFT`, `QFT_NS`, `IQFT`, `IQFT_NS`
- **Q#** : `QFT`, `IQFT`
- **isQ** : `QFT`, `IQFT`