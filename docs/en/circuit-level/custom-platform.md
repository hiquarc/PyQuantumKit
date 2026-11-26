# Custom Quantum Development Framework Support
PyQuantumKit uses the "code translation" approach to translate unified quantum circuit construction code into corresponding code on different quantum development platforms, in order to achieve cross-platform support. Starting from PyQuantumKit v.0.2.1, users are allowed to add custom code translation scripts to add support for more quantum development frameworks and quantum programming languages.

Here it is necessary to distinguish the terms "**quantum development framework**" and "**quantum programming language**", because PyQuantumKit provides different degrees of support for the two.

In this document, a **quantum development framework** refers to a **third-party Python package used to support the writing of quantum circuits**, such as qiskit, pyqpanda3, cqlib, etc. Since PyQuantumKit is implemented based on Python, for these Python packages, PyQuantumKit provides relatively complete translation process support, supporting both the generation of textual code and direct operation on the quantum circuit objects in these development packages.

Correspondingly, a **quantum programming language** refers to an **independent third-party quantum programming language**, such as Q\#, OpenQASM 2.0, etc. PyQuantumKit's translation process only supports generating textual code, and does not provide further operations on the specific code of these languages.

## 1. Writing a script for translation to a quantum programming language
This document first introduces how to write a script for translation to a quantum programming language, because it is relatively simple.

### Actions and constants in the translation script
The essence of the code translation process is: given the code written in PyQuantumKit to construct a quantum circuit, translate each step of the construction process into the corresponding code that implements the corresponding function in the target quantum programming language. Each "step" here is called an **action** (Action), for example declaring a quantum circuit, applying a quantum gate (calling the `apply_gate()` function), applying a measurement operation, etc. are all actions. The translation script gives how various actions are translated. In addition, the translation script also needs to contain some **constants** (Constant) used during the code translation process, such as the name of the standard library, the supported quantum subroutines and the names of their corresponding libraries, etc.

In PyQuantumKit, a code translation script is usually written as a Python file (.py), in which a series of **constants** and **actions** required to express the translation process are defined. Among them, "constants" are implemented as Python global variables, while "actions" are implemented as Python functions.

Specifically, a script for translation to a quantum programming language needs to contain the following 3 actions: `IMPORT`, `DECLARE`, `APPLY`; and also needs to contain the definitions of the following 2 constants: `SUPPORT_SUBROUTINES`, `EXPORT_CONSTANTS`. For emphasis, PyQuantumKit agrees that the naming of all constants and actions uses all uppercase. The specific information of each action and constant is introduced below.

### Action: IMPORT
In PyQuantumKit, **a specific action needs to be implemented as a function with a specific formal parameter type, whose return value is a string representing the translation result, and whose function body describes how the specific action is implemented.** Specifically, the `IMPORT` action gives how the process of "**importing a package**" is translated to the target quantum programming language. The function prototype it requires is:

```python
def IMPORT(module_name : str) -> str:
    # Translation process
    # Return the translation result string
```

The `IMPORT` action needs to accept one parameter `module_name`, indicating the name of the package to import.

Here we use the Python language to illustrate the writing of the function body. The syntax used by the Python language to import a package is `import xxx`, so the corresponding function body can be written as:

```python
# Example: write the function body that translates the "import package" action to Python syntax
def IMPORT(module_name : str) -> str:
    return "import " + module_name
```

### Action: DECLARE
The `DECLARE` action gives how the process of "**declaring an entity on which quantum operations can be applied**" is translated to the target quantum programming language. Here, an "entity on which quantum operations can be applied" refers to a quantum circuit, qubit register, etc., usually the object acted on by quantum gates. The function prototype required by the `DECLARE` action is:

```python
def DECLARE(cir_name : str, module_name : str,
            mixed : bool, nqbits : int, ncbits : int) -> str:
```

- `cir_name` indicates the name of the declared object (variable name).
- `module_name` indicates the package name that needs to be referenced when declaring the object.
- `mixed` indicates whether the declared object contains only qubits (`False`) or is allowed to contain both qubits and classical bits (`True`). The reason for introducing this parameter is that some development frameworks make such a distinction.
- `nqbits` indicates the number of qubits contained in the declared object.
- `ncbits` indicates the number of classical bits contained in the declared object (this is ignored when `mixed=False`).

### Action: APPLY
The `APPLY` action gives how the process of "**applying a quantum operation (gate, measurement, subroutine)**" is translated to the target quantum programming language. The function prototype required by the `APPLY` action is:

```python
def APPLY(cir_name : str, module_name : str,
          op_name : str, qbits : list[int], paras : list,
          is_qsub : bool = False) -> str:
```

- `cir_name` indicates the entity (quantum circuit, qubit register object) on which the quantum operation is to be applied.
- `module_name` indicates the package name required by the quantum operation.
- `op_name` indicates the name of the quantum operation to be applied.
- `qbits` indicates the array of qubit indices to be applied.
- `paras` indicates the classical parameters corresponding to the quantum operation.
- `is_qsub` indicates whether the applied operation is a quantum subroutine.

**The `APPLY` action is the core of the translation script, usually requires a large amount of writing, and needs to be written carefully.** For the specific writing method, please refer to the [built-in translation scripts](./api/scripts.md).

PyQuantumKit supports using different strings to apply the same gate (for example `'CCX'`, `'CCNOT'`, `'Toffoli'`), so this function usually needs to first convert `'op_name'` into a unified standard form in PyQuantumKit, and then proceed to the next step. The `pyquantumkit.translate.common` package provides the `get_standard_gatename()` function, which is used to convert non-standard quantum gate name strings into standard form. The constant `Standard_Gate_Name` of `pyquantumkit.translate.common` gives the standard forms of all supported quantum gates:

```python
Standard_Gate_Name = {
    'I', 'X', 'Y', 'Z', 'S', 'T', 'H', 'M',
    'CX', 'CY', 'CZ', 'CH', 'RX', 'RY', 'RZ', 'SW', 'ISW',
    'CRX', 'CRY', 'CRZ', 'RXX', 'RYY', 'RZZ', 'CSW',
    'CCX', 'CCZ', 'SD', 'TD', 'U1', 'CU1', 'U3',
    'SX', 'SXD', 'CS', 'CSD',
}
```

The written translation code should be able to handle the translation of all the above gates ([click here](./api/supported-gates.md) for the specific definitions of each quantum gate). If the target platform does not directly support a certain gate, it should be translated into an equivalent combination of other supported gates.

The measurement operation is implemented by specifying the quantum gate name as `'M'`, in which case the parameter `paras` is the array of classical bits for storing the measurement result.

### Constant: SUPPORT_SUBROUTINES
The constant `SUPPORT_SUBROUTINES` is a dictionary with strings as keys and strings as values, used to indicate the subroutines supported by the target quantum programming language and the corresponding library names, to support the translation of applying quantum subroutines in the `APPLY` action. Note that the keys of the dictionary correspond to the name passed by the `op_name` parameter of the `APPLY` action, not the name in the target quantum programming language.

For example, it is known that the standard library of the Q\# language provides the quantum Fourier transform function `ApplyQFT()`, which is located in the `Microsoft.Quantum.Canon` package. Suppose that in PyQuantumKit, the string for applying the quantum Fourier transform subroutine is `'QFT'`. Then to support the translation of applying the quantum operation `'QFT'`, `SUPPORT_SUBROUTINES` needs to contain one entry:

```
'QFT' : "Microsoft.Quantum.Canon"
```

### Constant: EXPORT_CONSTANTS
The constant `EXPORT_CONSTANTS` is a dictionary indicating a series of constants and their corresponding values needed in the process of exporting to code. For a script for translation to a quantum programming language, in order to translate to complete, standalone code of the target quantum programming language, the values of the following constants need to be specified:

- `'comment'`: the comment at the beginning of the exported code;
- `'prefix'`: the code block before the code that applies specific quantum gates;
- `'suffix'`: the code block after the code that applies specific quantum gates;
- `'stdlib_name'`: the name of the target language's standard library (usually the library containing quantum gates).

## 2. Writing a script for translation to a quantum development framework
For a script for translation to a quantum development framework, in addition to the above string-generating actions and constants `IMPORT`, `DECLARE`, `APPLY`, `SUPPORT_SUBROUTINES`, `EXPORT_CONSTANTS`, an additional set of actions and constants is required, which are used for operations on the objects in the corresponding quantum development framework.

### Action: NEW
The `NEW` action performs an action semantically similar to "creating a new quantum circuit", which corresponds to the concrete execution of the `DECLARE` action and can reuse the return value of the `DECLARE` action. The function prototype required by the `NEW` action is:

```python
def NEW(mixed_circuit : bool, nqbits : int, ncbits : int) -> str:
```

Here we use the `NEW` action of the script for translation to Qiskit as an illustration. For convenience of explanation, the `EXPORT_CONSTANTS` constant and the `DECLARE` and `NEW` actions of the script are listed together:

```python
# Selected from translate script qiskit.py
EXPORT_CONSTANTS = {
    'comment' : "# Qiskit code exported from PyQuantumKit",
    'prefix' : "",
    'suffix' : "",
    'stdlib_name' : 'qiskit',
}

def DECLARE(cir_name : str, module_name : str,
            mixed : bool, nqbits : int, ncbits : int) -> str:
    circuit_type = "QuantumCircuit"
    declare_str = "" if cir_name is None else cir_name + " = "
    module_str = "" if module_name is None else module_name + "."
    if mixed:
        return f"{declare_str}{module_str}{circuit_type}({nqbits}, {ncbits})"
    else:
        return f"{declare_str}{module_str}{circuit_type}({nqbits})"

def NEW(mixed_circuit : bool, nqbits : int, ncbits : int) -> str:
    std = EXPORT_CONSTANTS['stdlib_name']
    return DECLARE(None, f"framework_modules('qiskit', '{std}')", mixed_circuit, nqbits, ncbits)
```

The `NEW` action reuses the return value of the `DECLARE` action, but fixes the first two parameters `cir_name` and `module_name`. When the passed parameters are `mixed_circuit=True`, `nqbits=3`, `ncbits=3`, the return value of the `NEW` action function is the following string:
```
"framework_modules('qiskit', 'qiskit').QuantumCircuit(3, 3)"
```

Here let's briefly explain why `cir_name` and `module_name` are chosen in this way in the `NEW` action. In fact, the syntax for declaring a quantum circuit variable in qiskit is exactly
```python
qc = qiskit.QuantumCircuit(3, 3)
```

In order to support the execution of code in different quantum development frameworks, PyQuantumKit maintains a data structure for storing and querying imported Python packages, used to manage the package imports of quantum development frameworks. The imported package can be obtained using the function `framework_modules(framework name, package name)`.

In summary, **these additional actions of the script for translation to a quantum development framework (such as `NEW`, `GATE`, `SUBROUTINE`, `BITS`, etc.) can be viewed as the case of fixing specific parameters of the code-generating actions (`IMPORT`, `DECLARE`, `APPLY`, etc.), and the fixed parameters allow the code to be executed in the environment where these actions are called during the translation process.**

### Actions: GATE and SUBROUTINE
The `GATE` action and the `SUBROUTINE` action perform actions semantically similar to "applying a quantum operation", which correspond to the concrete execution of the `APPLY` action and can reuse the return value of the `APPLY` action. Among them, the `GATE` action fixes `is_qsub=False`, and the `SUBROUTINE` action fixes `is_qsub=True`. The function prototypes they require are:

```python
def GATE(gate_name : str, qbits : list[int], paras : list) -> str:
def SUBROUTINE(qsub_name : str, qbits : list[int], paras : list) -> str:
```

Taking the qiskit translation script as an example, their concrete implementations are:

```python
def GATE(gate_name : str, qbits : list[int], paras : list) -> str:
    return APPLY("qc", None, gate_name, qbits, paras, False)

def SUBROUTINE(qsub_name : str, qbits : list[int], paras : list) -> str:
    return APPLY("qc", None, qsub_name, qbits, paras, True)
```

PyQuantumKit agrees that the `cir_name` parameter here must be fixed to `"qc"`.

### Action: BITS
The `BITS` action performs an action semantically similar to "obtaining the number of bits", and the function prototype it requires is:

```python
def BITS(ret_cbit : bool, ret_list : bool) -> str:
```

- The `ret_cbit` parameter specifies whether the return value is the number of classical bits (`True`) or the number of qubits (`False`).
- The `ret_list` parameter specifies whether the return value is a number (for example: 4) or an index list (for example: `[0, 1, 2, 3]`).

### Internally reserved actions
PyQuantumKit also provides several internally reserved actions, used for testing during the development of PyQuantumKit; for user-defined translation scripts, these actions usually do not need to be specified. They include `CIRCUIT`, `MIXED_CIRCUIT`, and `RUN`.

### Constant: INTERPRET_PROTOCOL
The constant `INTERPRET_PROTOCOL` specifies whether the output result `'0'/'1'` string of this quantum development framework follows the read-from-the-left convention (`'l'`) or the read-from-the-right convention (`'r'`). This constant is mainly used for the interpretation of the running results of high-level-language quantum programs; [click here](../program-level/guide/measure.md#_5) for details.

## 3. Adding, testing, and replacing translation scripts
Users can call the `update_framework_translation` and `update_language_translation` functions to add or replace translation scripts, where the former is used for scripts for translation to quantum development frameworks (including the execution of code), and the latter is used for scripts for translation to quantum programming languages (only including code generation, not including code execution).

### Scripts for translation to a quantum programming language
The prototype of the function `update_language_translation` is:

```python
def update_language_translation(language_name : str, translate_rule_file : str) -> None:
```

- The parameter `language_name` is the name of the language to add or modify. If the name has not yet been added, the name and the corresponding translation rules are added to PyQuantumKit; otherwise, the translation rules corresponding to the name are replaced (the built-in translation rules of PyQuantumKit can also be replaced).
- The parameter `translate_rule_file` specifies the Python file (with the `.py` omitted) used to describe the translation rules. Usually the translation rule file is placed in the same folder as the source file that calls `update_language_translation`.

For example, let main.py be the written quantum main program, in which the translation script my_language.py needs to be added. Suppose they are placed in the same directory:

```
my_project/
 |--- main.py
 |--- my_language.py
```

Then in main.py, the translation script can be added as follows:

```python title="main.py"
import pyquantumkit as pqk
# Add my_language.py as the translation script corresponding to the name 'My Language'
pqk.update_language_translation('My Language', 'my_language')
```

### Scripts for translation to a quantum development framework
The prototype of the function `update_framework_translation` is:

```python
def update_framework_translation(framework_name : str, translate_rule_file : str, import_packages : list[str]) -> None:
```

- The parameter `framework_name` is the name of the quantum development framework to add or modify. If the name has not yet been added, the name and the corresponding translation rules are added to PyQuantumKit; otherwise, the translation rules corresponding to the name are replaced (the built-in translation rules of PyQuantumKit can also be replaced).
- The parameter `translate_rule_file` specifies the Python file (with the `.py` omitted) used to describe the translation rules. Usually the translation rule file is placed in the same folder as the source file that calls `update_framework_translation`.
- The parameter `import_packages` gives the names of the Python packages that will be used in the translation script; these packages can be referenced in the translation script through `framework_modules(framework name, package name)`.

### Testing translation scripts
PyQuantumKit provides the `test_code_translation` module for testing the writing of translation scripts.

#### Testing the translation of applying a single quantum gate
The `test_apply_gate` function is used to test the code translation of applying a single quantum gate. For example, the following code can be used to test and print the translation result of applying an $R_{xx}(0.123)$ gate to the qubits with indices 0, 2, 4 in qiskit:

```python
from pyquantumkit import *
import pyquantumkit.test_code_translation as TC
TC.test_apply_gate('qiskit', 'qc', 'Rxx', [0, 2, 4], [0.123])
```

The output is:

```
# Qiskit code exported from PyQuantumKit
from qiskit import *

qc = QuantumCircuit(5)
qc.rxx(0.123, 0, 2, 4)
```

Developers can check whether the translation is correct through the output; simply modify the first parameter to the name of the custom quantum development framework to test the custom translation script. The translation result of the `test_apply_gate` function contains the prefix and suffix, and in principle should be code that can run independently.

#### Testing the translation of applying a measurement operation
The `test_apply_measure` function is used to test the code translation of applying a quantum operation.

```python
from pyquantumkit import *
import pyquantumkit.test_code_translation as TC
TC.test_apply_measure('qsharp', 'qs', [0, 1, 2, 3, 4], [0, 1, 2, 3, 4])
```

The output is:

```
// Q# Code exported from PyQuantumKit
open Microsoft.Quantum.Core;
operation Main() : Unit
{
use qs = Qubit[5];
let c_0 = M(qs[0]); let c_1 = M(qs[1]); let c_2 = M(qs[2]); let c_3 = M(qs[3]); let c_4 = M(qs[4]); 
}
```

#### Testing the validity of the translation of all quantum gates
The `test_apply_gate_all` function is used to test the translation of all quantum gates supported by PyQuantumKit. For example, the following code tests and prints the result of applying all quantum gates in the `pyqpanda3` framework.

```python
from pyquantumkit import *
import pyquantumkit.test_code_translation as TC
TC.test_apply_gate_all('pyqpanda3', 'qc')
```

The output is:

```
# PyQPanda3 code exported from PyQuantumKit
from pyqpanda3.core import *

qc = QProg(5)
qc << I(0)
qc << X(0)
qc << Y(1)
qc << Z(2)
qc << S(3)
qc << T(4)
qc << H(0)
qc << CNOT(1, 2)
qc << Y(4).control(3)
qc << CZ(0, 1)
qc << H(3).control(2)
qc << RX(4, 1.1)
qc << RY(0, 2.2)
qc << RZ(1, 3.3)
qc << SWAP(2, 3)
qc << ISWAP(4, 0)
qc << CRX(1, 3, 0.123)
qc << CRY(2, 4, 0.456)
qc << CRZ(0, 2, 0.789)
qc << RXX(1, 4, 3)
qc << RYY(0, 3, 2)
qc << RZZ(2, 1, 1)
qc << SWAP(1, 2).control(0)
qc << TOFFOLI(1, 2, 3)
qc << Z(4).control([2, 3])
qc << S(0).dagger()
qc << T(4).dagger()
qc << U1(1, -1)
qc << CR(2, 3, -2)
qc << U3(4, -3, 10.0, -0.002)
qc << H(0) << S(0) << H(0)
qc << H(1) << S(1).dagger() << H(1)
qc << S(3).control(2)
qc << S(4).dagger().control(2)
qc << measure(0, 0) << measure(1, 1) << measure(2, 2) << measure(3, 3) << measure(4, 4)
```

The `test_apply_gate_all` function tests the quantum gates that are supported by PyQuantumKit but not supported by the target quantum development framework/language. The translation script should be able to correctly translate such gates into equivalent combinations of gates supported by the target framework, and no exceptions should occur.