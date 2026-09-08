# 实验性功能：总览和说明
**这里对PyQuantumKit的一些实验性功能进行说明，这些功能尚处于实验阶段，未经过系统性的测试，且接口在未来可能改变，请谨慎使用。**

## 模块化量子线路构建
**警告：随着高级语言级量子程序开发功能的引入，此模块在未来将仅作为内部使用，不建议用户直接使用该模块。**

**替代方案：** 建议使用高级语言级量子程序设计。

量子线路/程序的新建、复制、串联、并联： `new_circuit`, `new_program`, `copy_circuit`, `copy_program`, `append_circuit`, `append_program`, `parallel_circuits`, `parallel_programs`

获取量子线路的经典比特/量子比特数目： `get_n_qubits`, `get_n_cbits`, `get_qubit_list`, `get_cbit_list`

生成量子线路的逆版本或重排量子比特的版本： `derivative`

Pauli测量： `apply_measure_x`, `apply_measure_y`, `apply_measure_z`, `apply_pauli_measure`

以统一的方式运行量子线路： `run_and_get_counts`

## pyquantumkit.classical.run_result模块：运行结果分析

从运行结果字典中提取一个量子比特子集的结果的字典：`count_subset_of_result_dict`, `count_first_bits_of_result_dict`, `count_last_bits_of_result_dict`

提取出现的运行结果集合：`get_result_str_set`

## pyquantumkit.state_prepare模块：提供一些量子态制备算法
**警告：随着高级语言级量子程序开发功能的引入，此模块在未来将被废弃。**

**替代方案：** `pyquantumkit.program.std`中的`QubitArray`类型和`pyquantumkit.program.quint`中的`QuInt`类型。

*根据一个字符串制备状态： `create_state_by_01pm`, `uncompute_state_by_01pm`, `create_state_by_sqgate_str`, `uncompute_state_by_sqgate_str`*

*计算基态 $\ket{x}$ ： `create_ket_int_le`, `create_ket_int_be`, `uncompute_ket_int_le`, `uncompute_ket_int_be`*

*互补叠加态 $\frac{1}{\sqrt2}(\ket{x}+e^{i\phi}\ket{\bar{x}})$ ，其中 $\bar{x}$ 是 $x$ 的按位取反， $e^{i\phi}$ 是相对相位： `create_ket_int_plus_eiphi_neg_le`, `create_ket_int_plus_eiphi_neg_be`, `uncompute_ket_int_plus_eiphi_neg_le`, `uncompute_ket_int_plus_eiphi_neg_be`*

*二值叠加态 $\frac{1}{\sqrt2}(\ket{x}+e^{i\phi}\ket{y})$ ： `create_ket_int1_plus_eiphi_ket_int2_le`, `create_ket_int1_plus_eiphi_ket_int2_be`, `uncompute_ket_int1_plus_eiphi_ket_int2_le`, `uncompute_ket_int1_plus_eiphi_ket_int2_be`*

*Pauli算子的本征态： `create_pauli_eigenstate`, `uncompute_pauli_eigenstate`*

## pyquantumkit.library模块：提供一些常用量子算法

交换测试（Swap Test）、量子态层析（Tomography）、量子傅里叶变换（QFT）、量子哈密顿模拟

## pyquantumkit.program_check.program_relation模块：提供量子程序性质检验算法

此模块基于论文 https://arxiv.org/abs/2307.01481 实现。

等价性检验： `run_equivalence_check`
恒同性检验： `run_identity_check`
幺正性检验： `run_unitarity_check`
保持纯态检验： `run_keep_purity_check`
保持计算基态检验： `run_keep_basis_check`
