# Overview of High-Level-Language-Level Quantum Program Development

The development of programming languages has gone through the process from machine language and assembly language to high-level languages. In particular, the emergence of high-level languages has greatly lowered the threshold for writing computer programs and improved development efficiency.

Compared with the programming paradigms and programming languages of mature classical (traditional) programs, quantum programming languages are still in an early stage of development, and current quantum programming is still at a relatively low level. For example, developers need to manage the allocation of qubits themselves, need to directly operate on individual qubits (apply quantum gates), and need to convert the measurement results of each qubit into the required format themselves. This is illustrated below with a piece of quantum program code written based on Qiskit.
```python
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from math import pi

qc = QuantumCircuit(6, 6)
qc.h(1)
qc.p(pi / 3, 1)
qc.x(2)
qc.x(3)
qc.x(5)
qc.cx(1, 2)
qc.cx(1, 4)
qc.measure(0, 0)
qc.measure(1, 1)
qc.measure(2, 2)
qc.measure(3, 3)
qc.measure(4, 4)
qc.measure(5, 5)

sim = AerSimulator()
result = sim.run(qc, shots = 1000).result()
print(result.get_counts())
```
This program declares a quantum circuit containing 6 qubits, and then constructs a quantum program by applying gates and measurement operations on these qubits. This programming style is similar to writing assembly language code: specifying that a certain basic instruction is to be executed on register number such-and-such, and the sequence of instructions constitutes the assembly language code. In fact, the functionality executed by the above code has its own logical meaning; however, it is difficult for developers to intuitively see the specific function of the code from this series of assembly-like instructions (just as the difficulty of decompilation).

The (one) running result of the above program is:
```
{'101100': 511, '111010': 489}
```
As can be seen, the running result of the program is a series of `'0'`/`'1'` strings together with their corresponding occurrence counts (forming a dictionary). However, in the logic of the original program, the `'0'`/`'1'` strings have their corresponding specific information, and the user also needs to write an interpretation program to extract the corresponding information from the result `'0'`/`'1'` strings. In the process of writing the result interpretation program, there is an issue that needs special attention: should the result `'0'`/`'1'` string be read starting from the left or from the right? In other words, does the result of the first qubit (with index 0) correspond to the leftmost character or the rightmost character? In fact, the order of the result string has different conventions in different frameworks; for example, Qiskit and QPanda3 use the convention of reading from the right, while Quafu uses the convention of reading from the left. However, the documentation of these frameworks does not emphasize the order of the result string (or does not mention it at all), making it easy for users to interpret wrong results.

In fact, the functionality executed by the above program is: preparing and measuring the binary superposition quantum state $\frac{1}{\sqrt{2}}\left(\ket{44} + e^{i\pi/3}\ket{58}\right)$ composed of the integers 44 and 58 and the relative phase angle $\pi/3$. Here, the decimal integers 44 and 58 are stored in little-endian binary encoding (that is, the low-order bits of the integer are stored at the low indices of the qubit array) into a qubit array composed of 6 qubits, that is, the actually prepared quantum state is: $\frac{1}{\sqrt{2}}\left(\ket{0}\ket{1}\ket{0}\ket{1}\ket{1}\ket{1} + e^{i\pi / 3}\ket{0}\ket{0}\ket{1}\ket{1}\ket{0}\ket{1}\right)$. When interpreting the result, since Qiskit's convention is to read from the right, the result string is exactly the big-endian binary representation of the integer, so `'111010'` corresponds to the decimal integer 58 and `'101100'` corresponds to the decimal integer 44.

## Quantum Programming: From "Assembly Language" to "High-Level Language"

From the above code example, it can be seen that quantum programming at the current stage is similar to assembly language. If the functionality of the above code were described in a high-level language, it should be similar to the following form:
```python
# Define a quantum integer (let's call it QuInt) variable qnum, which contains 6 qubits
qnum = QuInt(6)

# Directly call the methods of the QuInt type to generate a binary superposition quantum state
qnum.create_two_value_superposition(44, 58, pi / 3)

# Measure qnum
measure(qnum)
```
Moreover, the measurement result of the quantum integer variable should be directly output in integer form (rather than the raw `'0'`/`'1'` strings), for example in the following form:
```
[({'qnum' : 44}, 511),
 ({'qnum' : 58}, 489)]
```
That is, among the measurement results of the quantum integer variable `qnum`, 511 times the result is 44 and 489 times the result is 58. In this way, developers do not need to care about the specific storage of quantum integers and the details of recovering information from the result string (for example, whether it is big-endian or little-endian), and the readability of the entire quantum program and the measurement results is greatly improved.

In the NISQ era, the number of qubits available on quantum hardware is small (a few dozen), and the programming style of directly manipulating individual qubits like assembly language may still be sufficient. However, in the future, as the number of qubits further increases, the programming paradigm of directly manipulating qubits will face a bottleneck, and quantum programming needs a leap from "assembly language" to "high-level language".

## Using PyQuantumKit for High-Level-Language-Level Quantum Programming

PyQuantumKit v.0.2 newly introduces the high-level-language-level quantum programming feature (the `pyquantumkit.program` module). Users can:

- Use Python syntax to write high-level-language-level quantum programs, including defining quantum variables and using functions, etc.;
- Define custom quantum data types based on Python syntax, and customize their operations and the way measurement results are interpreted;
- Use data organization forms such as arrays (QArray), tuples (QTuple), structs (QStruct) and unions (QUnion) to build complex quantum data types;
- Compile high-level-language-level quantum programs into quantum circuits on different quantum development frameworks, and run them on simulators or real quantum hardware.
- Interpret the `'0'`/`'1'` strings or dictionaries of the running results and recover them into the information carried by the corresponding data types.
- Seamlessly connect with existing classical algorithms in classical-quantum hybrid programming.
