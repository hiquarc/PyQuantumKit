# example/special_qubit_types.py
#    2026/9/7
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

import pyqpanda3.core as qpanda
from pyquantumkit import QProgramBuilder
from pyquantumkit.program.std import *
from pyquantumkit.program.quint import *

# 量子布尔类型
class QuBool(Qubit):
    def _interpret_(self, output):
        return (True if super()._interpret_(output) == '1' else False)


# 只允许Clifford门的量子比特
class CliffordQubit(Qubit):
    def _gate_(self, gate_name : str, qubit_var_list : list, paras : list) -> Qubit:
        # 调用get_standard_gatename()函数将gate_name转换为PyQuantumKit标准名称
        standard_name = get_standard_gatename(gate_name)

        # 若使用的门不是Clifford门，报错
        if standard_name not in {'I', 'X', 'Y', 'Z', 'S', 'H', 'CX', 'CY', 'CZ', 'SW', 'ISW'}:
            raise QuantumProgramBuildError(f"Cannot apply non-Clifford gate '{gate_name}' on the CliffordQubit '{self.get_varname()}'")
        
        # 若使用的门是Clifford门，返回self作为调用gate()的目标
        return self


# 基于 |+>, |-> 基的量子比特类型
class PMQubit(Qubit):
    # 初始化操作
    def _initialize_(self):
        gate('H', [self])

    # 测量前操作
    def _premeasure_(self):
        gate('H', [self])

    # 解读测量结果
    def _interpret_(self, output : str):
        return ('+' if super()._interpret_(output) == '0' else '-')


# |+>,|->基量子比特数组
class PMQubitArray(QArray):
    def __init__(self, length : int, varname = None):
        super().__init__(varname)
        self._base_obj = PMQubit()
        self._length = length
        self.init_qarray()
    def _interpret_(self, output):
        return ''.join(super()._interpret_(output))


def qmain(builder : QProgramBuilder):
    pmq1 = PMQubit('pmq1')
    pmq2 = PMQubit('pmq2')
    builder.declare_qvars(pmq1, pmq2)

    gate('X', [pmq1])
    gate('Z', [pmq2])

    builder.measure_all()


qpbuilder = QProgramBuilder()
qpbuilder.build(qmain)

qpanda_cir = qpanda.QProg()
qpbuilder.get_built_circuit() >> qpanda_cir
print(qpanda_cir)

qpanda_qvm = qpanda.CPUQVM()
qpanda_qvm.run(qpanda_cir, 1000)
qpanda_result = qpanda_qvm.result().get_counts()

rec_result = qpbuilder.interpret_result_dict(qpanda_result, 'pyqpanda3')
print(rec_result)
