# Experimental Features: Overview and Explanation
**This section explains some experimental features of PyQuantumKit. These features are still in the experimental stage, have not undergone systematic testing, and their interfaces may change in the future. Please use them with caution.**

## Modular Quantum Circuit Construction

Creation, copying, concatenation, and parallelization of quantum circuits/programs: `new_circuit`, `new_program`, `copy_circuit`, `copy_program`, `append_circuit`, `append_program`, `parallel_circuits`, `parallel_programs`

Get the number of classical/quantum bits of a quantum circuit: `get_n_qubits`, `get_n_cbits`, `get_qubit_list`, `get_cbit_list`

Generate an inverse version or a qubit-reordered version of a quantum circuit: `derivative`

Pauli measurement: `apply_measure_x`, `apply_measure_y`, `apply_measure_z`, `apply_pauli_measure`

Run quantum circuits in a unified manner: `run_and_get_counts`

## pyquantumkit.classical.run_result module: Run Result Analysis

Extract a dictionary of results for a subset of qubits from the run result dictionary: `count_subset_of_result_dict`, `count_first_bits_of_result_dict`, `count_last_bits_of_result_dict`

Extract the set of occurring run results: `get_result_str_set`

## pyquantumkit.state_prepare module: Provides some quantum state preparation algorithms

Prepare states from a string: `create_state_by_01pm`, `uncompute_state_by_01pm`, `create_state_by_sqgate_str`, `uncompute_state_by_sqgate_str`

Compute the basis state $\ket{x}$: `create_ket_int_le`, `create_ket_int_be`, `uncompute_ket_int_le`, `uncompute_ket_int_be`

Complementary superposition state $\frac{1}{\sqrt2}(\ket{x}+e^{i\phi}\ket{\bar{x}})$, where $\bar{x}$ is the bitwise negation of $x$, and $e^{i\phi}$ is the relative phase: `create_ket_int_plus_eiphi_neg_le`, `create_ket_int_plus_eiphi_neg_be`, `uncompute_ket_int_plus_eiphi_neg_le`, `uncompute_ket_int_plus_eiphi_neg_be`

Binary superposition state $\frac{1}{\sqrt2}(\ket{x}+e^{i\phi}\ket{y})$: `create_ket_int1_plus_eiphi_ket_int2_le`, `create_ket_int1_plus_eiphi_ket_int2_be`, `uncompute_ket_int1_plus_eiphi_ket_int2_le`, `uncompute_ket_int1_plus_eiphi_ket_int2_be`

Eigenstates of Pauli operators: `create_pauli_eigenstate`, `uncompute_pauli_eigenstate`

## pyquantumkit.library module: Provides some commonly used quantum algorithms

Swap Test, Quantum State Tomography, Quantum Fourier Transform (QFT), Quantum Hamiltonian Simulation

## pyquantumkit.program_check.program_relation module: Provides quantum program property verification algorithms

This module is implemented based on the paper https://arxiv.org/abs/2307.01481.

Equivalence check: `run_equivalence_check`
Identity check: `run_identity_check`
Unitarity check: `run_unitarity_check`
Purity preservation check: `run_keep_purity_check`
Computational basis preservation check: `run_keep_basis_check`
