# Experimental Features: Overview and Notes
**This section explains some experimental features of PyQuantumKit. These features are still in the experimental stage, have not been systematically tested, and their interfaces may change in the future. Please use them with caution.**

## Modular Quantum Circuit Construction
**Warning: With the introduction of high-level-language-level quantum program development features, this module will in the future be for internal use only, and users are not advised to use this module directly.**

**Alternative:** It is recommended to use high-level-language-level quantum program design.

Creating, copying, concatenating and combining in parallel quantum circuits/programs: `new_circuit`, `new_program`, `copy_circuit`, `copy_program`, `append_circuit`, `append_program`, `parallel_circuits`, `parallel_programs`

Obtaining the number of classical bits/qubits of a quantum circuit: `get_n_qubits`, `get_n_cbits`, `get_qubit_list`, `get_cbit_list`

Generating the inverse version of a quantum circuit or a version with qubits rearranged: `derivative`

Pauli measurement: `apply_measure_x`, `apply_measure_y`, `apply_measure_z`, `apply_pauli_measure`

Running a quantum circuit in a unified way: `run_and_get_counts`

## pyquantumkit.classical.run_result module: Running Result Analysis

Extracting a dictionary of the results for a subset of qubits from the running result dictionary: `count_subset_of_result_dict`, `count_first_bits_of_result_dict`, `count_last_bits_of_result_dict`

Extracting the set of running results that appear: `get_result_str_set`

## pyquantumkit.state_prepare module: Provides some quantum state preparation algorithms
**Warning: With the introduction of high-level-language-level quantum program development features, this module will be deprecated in the future.**

**Alternative:** The `QubitArray` type in `pyquantumkit.program.std` and the `QuInt` type in `pyquantumkit.program.quint`, which provide similar methods.

*Preparing a state from a string: `create_state_by_01pm`, `uncompute_state_by_01pm`, `create_state_by_sqgate_str`, `uncompute_state_by_sqgate_str`*

*Computational basis state $\ket{x}$: `create_ket_int_le`, `create_ket_int_be`, `uncompute_ket_int_le`, `uncompute_ket_int_be`*

*Complementary superposition state $\frac{1}{\sqrt2}(\ket{x}+e^{i\phi}\ket{\bar{x}})$, where $\bar{x}$ is the bitwise negation of $x$ and $e^{i\phi}$ is the relative phase: `create_ket_int_plus_eiphi_neg_le`, `create_ket_int_plus_eiphi_neg_be`, `uncompute_ket_int_plus_eiphi_neg_le`, `uncompute_ket_int_plus_eiphi_neg_be`*

*Binary superposition state $\frac{1}{\sqrt2}(\ket{x}+e^{i\phi}\ket{y})$: `create_ket_int1_plus_eiphi_ket_int2_le`, `create_ket_int1_plus_eiphi_ket_int2_be`, `uncompute_ket_int1_plus_eiphi_ket_int2_le`, `uncompute_ket_int1_plus_eiphi_ket_int2_be`*

*Eigenstates of the Pauli operator: `create_pauli_eigenstate`, `uncompute_pauli_eigenstate`*

## pyquantumkit.library module: Provides some commonly used quantum algorithms
**Warning: With the introduction of high-level-language-level quantum program development features, this module will gradually migrate to the high-level language in the future, and users are not advised to use this module directly.**

Swap Test, quantum state Tomography, quantum Fourier transform (QFT), quantum Hamiltonian simulation

## pyquantumkit.circuit_check.circuit_relation module: Provides algorithms for checking quantum program properties
**Warning: With the introduction of high-level-language-level quantum program development features, this module will in the future be for internal use only, and users are not advised to use this module directly.**

This module is implemented based on the paper https://arxiv.org/abs/2307.01481.

Equivalence check: `run_equivalence_check`
Identity check: `run_identity_check`
Unitarity check: `run_unitarity_check`
Purity-preserving check: `run_keep_purity_check`
Computational-basis-state-preserving check: `run_keep_basis_check`
