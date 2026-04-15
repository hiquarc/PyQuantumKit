# PyQuantumKit简介

PyQuantumKit是一个基于Python的量子软件开发辅助工具，设计目标包括：

- 提供统一的方式在不同的基于Python的量子开发框架上构建量子线路，实现代码复用；
- 提供常用的量子算法和开发辅助功能，提升量子软件开发效率和正确性；
- 软件架构具有扩展性，未来可方便地添加更多的功能和量子开发框架的支持。

# 安装和使用

使用`pip install`命令可安装PyQuantumKit

```sh
pip install pyquantumkit
```

PyQuantumKit要求Python版本>=3.8，且依赖如下Python包：

- sympy >= 1.8
- numpy >= 1.22.0

通常，PyQuantumKit需要与受支持的基于Python的量子开发框架（例如qiskit或pyqpanda3等）联合使用。可以在安装PyQuantumKit的同时安装受支持的量子开发框架，例如，使用如下命令在安装PyQuantumKit的同时安装qiskit：

```sh
pip install pyquantumkit[qiskit]
```

使用`git clone`命令将PyQuantumKit仓库复制到本地：

```sh
git clone https://github.com/hiquarc/PyQuantumKit.git
```

用户文档参见：[https://pyquantumkit.readthedocs.io/](https://pyquantumkit.readthedocs.io/)

# 联系我们

PyQuantumKit由中国科学院高能物理研究所计算中心研发，得到了国家高能物理科学数据中心的支持。

项目负责人：龙沛洵
longpx@ihep.ac.cn

# 版本历史

2026/4/15 v.0.1.6
- 为项目添加说明文档

2026/3/27 v.0.1.5
- 新增一个支持的量子开发框架：cqlib
- CircuitIO类现在可以将线路导出为QSharp和isQ语言的代码
- 新增基于量子线路矩阵表示的线路等价性和恒等性检验函数

2026/1/20 v.0.1.4
- 新增符号运算库 (/symbol) ，用于构建量子线路的矩阵表示
- CircuitIO类现在能支持以sympy符号作为门的参数来构建量子线路
- 增加支持 $CS$ 、$CS^{\dagger}$ 、 $\sqrt{X}$ 和 $\sqrt{X}^{\dagger}$ 门

2025/12/04 v.0.1.3
- 新增apply_exp_pauli函数用于支持量子哈密顿模拟算法
- 新增量子哈密顿模拟算法库（实验性） (/library/hamiltonian.py)

2025/7/25 v.0.1.2
- 新增CircuitIO类，用于量子线路的格式化操作
- 修改了应用门的代码的翻译方式，以适应CircuitIO类输出为用户可读代码的功能

2025/7/10 v.0.1.1
- 首个预览版本 (v.0.1.1) 发布
