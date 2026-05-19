# Changelog

**2026/4/15 v.0.1.6**

- Add documents

**2026/3/27 v.0.1.5**

- Add a new supported quantum framework: cqlib
- `CircuiIO` class now is able to export the code of QSharp and isQ languages
- Add new circuit equivalence and identity verification function based on quantum circuit matrix representation

**2026/1/20 v.0.1.4**

- Add a new library (/symbol) to construct the matrix representation of quantum circuits
- `CircuitIO` class now supports the use of SymPy symbols as the parameters of quantum gates
- Add the support of $CS$ , $CS^{\dagger}$ , $\sqrt{X}$ and $\sqrt{X}^{\dagger}$ gates

**2025/12/04 v.0.1.3**

- Add a new function `apply_exp_pauli` to support quantum Hamiltonian simulation (experimental)
- Add a library for quantum Hamiltonian simulation (experimental) (/library/hamiltonian.py)

**2025/7/25 v.0.1.2**

- Add a new class `CircuitIO` to format the quantum circuits
- Change the translation of applying gates to generate human-readable code

**2025/7/10 v.0.1.1**

- The first preview version v.0.1.1
