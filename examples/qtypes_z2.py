import pyqpanda3.core as qpanda
from pyquantumkit import QProgramBuilder
from pyquantumkit.program.std import *
from pyquantumkit.library.hamiltonian import PauliHamiltonian, pqk_hsim_paulis_trotter


# 代表正电子的类型
class Positron(QStruct):
    _mass = 1.0          # 正电子质量
    def __init__(self, varname=None):
        super().__init__(varname)
        self._state = Qubit()       # 用一个量子比特存储状态
        self.init_qstruct(self._state)
    def _gate_(self, *args):
        return self
    # 正电子的哈密顿量动能项
    def guage_kinetic(self, epsilon):
        gate('rz', [self._state], [Positron._mass * epsilon])

# 代表电子的类型
class Electron(QStruct):
    _mass = 1.0          # 电子质量
    def __init__(self, varname=None):
        super().__init__(varname)
        self._state = Qubit()       # 用一个量子比特存储状态
        self.init_qstruct(self._state)
    def _gate_(self, *args):
        return self
    # 电子的哈密顿量动能项
    def guage_kinetic(self, epsilon):
        gate('rz', [self._state], [-Electron._mass * epsilon])

# 代表光子的类型
class Photon(QStruct):
    def __init__(self, varname=None):
        super().__init__(varname)
        self._state = Qubit()       # 用一个量子比特存储状态
        self.init_qstruct(self._state)
    def _gate_(self, *args):
        return self
    # 光子的哈密顿量动能项
    def guage_kinetic(self, epsilon):
        gate('rx', [self._state], [epsilon])


# Z2格点模型
class Z2Lattice(QStruct):
    def __init__(self, Ns : int, varname=None):
        super().__init__(varname)
        if Ns < 2:
            raise ValueError("Ns must >= 2.")
        
        # 模型的经典参数
        self.__n_sites = Ns
        self.__eta = 1.0
        self.__epsilon = 1.0

        # ----- 初始化存储粒子状态的量子比特区域 -----
        nqs = 2 * Ns - 1
        # 排列循环：正电子, 光子, 电子, 光子 ...
        cycle = (Positron, Photon, Electron, Photon)
        # 生成完整粒子排列，用一个QTuple结构依次存放
        types = tuple(cycle[i % 4] for i in range(nqs))
        self.__qubit_field = make_qtuple(types)
        self.init_qstruct(self.__qubit_field)

    # 设置模型的经典参数
    def set_mass(self, mass : float):
        # 设置电子和正电子的质量 m
        Positron.mass = mass
        Electron.mass = mass
    def set_eta(self, eta : float):
        # 设置相互作用强度参数 η
        self.__eta = eta
    def set_epsilon(self, epsilon : float):
        # 设置步长参数 ε
        self.__epsilon = epsilon

    # 根据下标获取格点粒子（电子和正电子）
    def get_site(self, index : int):
        return self.__qubit_field[index * 2]
    # 根据下标获取光子
    def get_photon(self, index : int):
        return self.__qubit_field[index * 2 + 1]
    # 获取格点数
    def n_sites(self):
        return self.__n_sites
    # 获取粒子数目
    def n_particals(self):
        return len(self.__qubit_field)
    # 获取量子比特数
    def n_qubits(self):
        return self.__qubit_field.n_qubits()

    # 哈密顿量模拟动能项
    def guage_kinetic(self):
        # 依次调用每个粒子的哈密顿量模拟动能项
        for i in range(len(self.__qubit_field)):
            self.__qubit_field[i].guage_kinetic(self.__epsilon)

    # ----- 哈密顿量模拟势能项 -----
    # 局部势能项
    def _local_potential(self, index, focus_qubit):
        lp = PauliHamiltonian(3)
        t = self.__epsilon
        lp.append_pauli('XZX', self.__eta / 4, focus_qubit)
        lp.append_pauli('YZY', self.__eta / 4, focus_qubit)
        tempcir = CircuitIO(3)
        pqk_hsim_paulis_trotter(tempcir, lp, t, 1, range(3))
        qlist = [self.get_site(index), self.get_photon(index), self.get_site(index + 1)]
        circuit(tempcir, qlist)

    # 总势能项
    def guage_potential(self):
        for i in range(self.n_sites() - 1):
            self._local_potential(i, (i + 1) % 2)


def qmain(builder : QProgramBuilder):
    z2 = Z2Lattice(3, 'z2')
    builder.declare_qvars(z2)

    z2.set_mass(1.0)
    z2.set_eta(0.5)
    z2.set_epsilon(0.1)
    z2.guage_kinetic()
    z2.guage_potential()


qpbuilder = QProgramBuilder()
qpbuilder.build(qmain)
print(qpbuilder.n_qvars_qubits())
print(qpbuilder.n_measure_cbits())

qpanda_cir = qpanda.QProg()
qpbuilder.get_built_circuit() >> qpanda_cir
print(qpanda_cir)
