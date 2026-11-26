# Overview of High-Level-Language Quantum Program Development

The development of programming languages has gone through a process from machine language, assembly language, to high-level languages. The emergence of high-level languages in particular has greatly lowered the barrier to writing computer programs and improved development efficiency.

Compared to the mature programming paradigms and programming languages of classical (traditional) programs, quantum programming languages are still in their early stage of development, and current quantum programming is still at a relatively low level. For example, developers need to manage the allocation of qubits themselves, need to directly operate on individual qubits (applying quantum gates), and need to convert the measurement results of each qubit into the required format themselves. Let us illustrate this with a quantum program written based on Qiskit.
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
This program declares a quantum circuit containing 6 qubits, and then builds the quantum program by applying gates and measurement operations on these qubits. This style of programming is similar to writing assembly language code: specifying a basic instruction to execute on a certain register, with the sequence of instructions forming the assembly language code. In fact, the function performed by the above code has a logical meaning, yet it is very difficult for developers to intuitively see the specific function of the code from this series of assembly-like instructions (just as decompilation is difficult).

The (one particular) running result of the above program is:
```
{'101100': 511, '111010': 489}
```
As can be seen, the running result of the program is a series of `'0'`/`'1'` strings and their corresponding occurrence counts (forming a dictionary). However, in the logic of the original program, each `'0'`/`'1'` string carries specific information, and the user still needs to write an interpretation program to extract the corresponding information from the resulting `'0'`/`'1'` strings. When writing the result interpretation program, there is one issue that needs special attention: should the resulting `'0'`/`'1'` string be read from the left or from the right? In other words, does the result of the first qubit (with index 0) correspond to the leftmost character or the rightmost character? In fact, the order of the result string has different conventions in different frameworks; for example, Qiskit and QPanda3 use the read-from-the-right convention, while some frameworks use the read-from-the-left convention (for example the old PyQuafu, though the new Quafu platform has changed to read-from-the-right). However, the documentation of these frameworks does not prominently mention the order of the result string (some do not mention it at all), making it easy for users to interpret the wrong result.

In fact, the function performed by the above program is: prepare and measure the two-value superposition quantum state $\frac{1}{\sqrt{2}}\left(\ket{44} + e^{i\pi/3}\ket{58}\right)$ composed of the integers 44 and 58 together with the relative phase angle $\pi/3$. Here, the decimal integers 44 and 58 are stored in little-endian binary encoding (i.e., the low bits of the integer are stored at the low indices of the qubit array) into a qubit array made of 6 qubits, so the actually prepared quantum state is: $\frac{1}{\sqrt{2}}\left(\ket{0}\ket{1}\ket{0}\ket{1}\ket{1}\ket{1} + e^{i\pi / 3}\ket{0}\ket{0}\ket{1}\ket{1}\ket{0}\ket{1}\right)$. When interpreting the result, since Qiskit uses the read-from-the-right convention, the result string is exactly the big-endian binary representation of the integer, so `'111010'` corresponds to the decimal integer 58, and `'101100'` corresponds to the decimal integer 44.

## Quantum Programming: From "Assembly Language" to "High-Level Language"

From the above code example, it can be seen that quantum programming at the current stage is similar to assembly language. If the function of the above code were described in a high-level language, it should look roughly like the following:
```python
# Define a quantum integer (let's call it QuInt) variable qnum, containing 6 qubits
qnum = QuInt(6)

# Directly call a method of the QuInt type to generate a two-value superposition quantum state
qnum.create_two_value_superposition(44, 58, pi / 3)

# Measure qnum
measure(qnum)
```
Moreover, the measurement result of the quantum integer variable should be directly output in integer form (rather than the raw `'0'`/`'1'` string), for example in the following form:
```
[({'qnum' : 44}, 511),
 ({'qnum' : 58}, 489)]
```
That is, in the measurement results of the quantum integer variable `qnum`, there are 511 results equal to 44 and 489 results equal to 58. In this way, developers no longer need to care about the specific storage of quantum integers or the details of recovering information from the result string (for example whether it is big-endian or little-endian), and the readability of the entire quantum program and its measurement results is greatly improved.

In the NISQ era, the number of qubits available on quantum hardware is relatively small (a few dozen), so the programming style of directly manipulating individual qubits like assembly language may still suffice. However, as the number of qubits further increases in the future, the paradigm of directly manipulating qubits will face a bottleneck, and quantum programming needs to make a leap from "assembly language" to "high-level language".

## High-Level-Language Quantum Programming with PyQuantumKit

PyQuantumKit v.0.2 introduces a new high-level-language quantum programming feature (the `pyquantumkit.program` module), with which users can:

- Use Python syntax to write high-level-language quantum programs, including defining quantum variables and using functions;
- Define custom quantum data types based on Python syntax, and customize their operations and measurement result interpretation methods;
- Use data organization forms such as arrays (QArray), tuples (QTuple), structs (QStruct), and unions (QUnion) to build complex quantum data types;
- Compile high-level-language quantum programs into quantum circuits on different quantum development frameworks, and run them on simulators or real quantum hardware.
- Interpret the `'0'`/`'1'` strings or dictionaries of the running results, recovering the information carried by the corresponding data types.
- Seamlessly integrate with existing classical algorithms in classical-quantum hybrid programming.
