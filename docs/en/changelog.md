# Changelog

**2026/11/12 v.0.2.1**

- Adjusted the writing rules of the code translation module to accommodate user-defined translation scripts;
- Allowed users to write custom translation scripts to support translating quantum circuits to more quantum programming languages or Python-based quantum development frameworks, and to modify the built-in translation scripts;
- Added support for the OpenQASM 2.0 language to the built-in translation scripts;
- Experimentally introduced the concept of quantum subroutines.

**2026/9/15 v.0.2.0**

- **Major update: high-level-language quantum programming (pyquantumkit.program module)**
- Modified the software architecture to support high-level-language quantum programming. Code previously written with PyQuantumKit v.0.1.* may need its module names and function names adjusted.

    - Adjusted the directory structure and retrieval method of the code translation module;
    - The function naming related to circuits containing measurements was changed to mixed_circuit (replacing the original program, because program is now used for high-level-language quantum programming);
    - The program_check, program_relation modules were renamed to circuit_check, circuit_relation;

**2026/4/15 v.0.1.6**

- Added documentation for the project.

**2026/3/27 v.0.1.5**

- Added a new supported quantum development framework: cqlib
- The CircuitIO class can now export circuits as QSharp and isQ language code
- Added new circuit equivalence and identity checking functions based on the matrix representation of quantum circuits

**2026/1/20 v.0.1.4**

- Added a symbolic computation library (pyquantumkit.symbol) for constructing the matrix representation of quantum circuits
- The CircuitIO class can now use sympy symbols as gate parameters to build quantum circuits
- Added support for the $CS$, $CS^{\dagger}$, $\sqrt{X}$, and $\sqrt{X}^{\dagger}$ gates

**2025/12/4 v.0.1.3**

- Added the `apply_exp_pauli` function to support quantum Hamiltonian simulation algorithms (experimental)
- Added a quantum Hamiltonian simulation algorithm library (experimental) (pyquantumkit.library.hamiltonian)

**2025/7/25 v.0.1.2**

- Added the CircuitIO class for formatting operations on quantum circuits
- Modified the translation method of gate-application code to accommodate the feature of exporting human-readable code through the CircuitIO class

**2025/7/10 v.0.1.1**

- Released the first preview version (v.0.1.1)