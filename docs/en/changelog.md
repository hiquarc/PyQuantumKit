# Changelog

**2026/9/15 v.0.2.0**

- **Major update: high-level-language-level quantum programming (pyquantumkit.program module)**
- The software architecture was changed to support high-level-language-level quantum programming. Code previously written with PyQuantumKit v.0.1.* may need adjustments to module names and function names.

    - Adjusted the directory structure and retrieval method of the code translation module;
    - Functions related to quantum circuits containing measurement were renamed to mixed_circuit (replacing the original program, since program is now used for high-level-language-level quantum programming);
    - The program_check and program_relation modules were renamed to circuit_check and circuit_relation;

**2026/4/15 v.0.1.6**

- Added documentation for the project

**2026/3/27 v.0.1.5**

- Added one more supported quantum development framework: cqlib
- The CircuitIO class can now export circuits as QSharp and isQ language code
- Added functions for checking circuit equivalence and identity based on the matrix representation of quantum circuits

**2026/1/20 v.0.1.4**

- Added a symbolic computation library (pyquantumkit.symbol) for building matrix representations of quantum circuits
- The CircuitIO class can now support building quantum circuits with sympy symbols as gate parameters
- Added support for the $CS$, $CS^{\dagger}$, $\sqrt{X}$ and $\sqrt{X}^{\dagger}$ gates

**2025/12/4 v.0.1.3**

- Added the `apply_exp_pauli` function to support quantum Hamiltonian simulation algorithms (experimental)
- Added a quantum Hamiltonian simulation algorithm library (experimental) (pyquantumkit.library.hamiltonian)

**2025/7/25 v.0.1.2**

- Added the CircuitIO class for formatting operations on quantum circuits
- Changed the translation method of the gate-application code to accommodate the CircuitIO class outputting user-readable code

**2025/7/10 v.0.1.1**

- First preview version (v.0.1.1) released
