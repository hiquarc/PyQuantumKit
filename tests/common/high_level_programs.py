# test: common/high_level_programs.py
#    2026/9/8
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from pyquantumkit import QProgramBuilder, CircuitIO
from pyquantumkit.program.std import *
from pyquantumkit.program.quint import *
import math

# -------- test cases for program structure ----------
# PASS
def empty_qmain(builder : QProgramBuilder):
    pass
# PASS
def empty_declare(builder : QProgramBuilder):
    builder.declare_qvars()
# PASS
def empty_declare_measure(builder : QProgramBuilder):
    builder.declare_qvars()
    builder.measure_all()
# PASS
def no_measure(builder : QProgramBuilder):
    q = Qubit('q')
    builder.declare_qvars(q)
    gate('H', [q])
# PASS
def empty_measure(builder : QProgramBuilder):
    q = Qubit('q')
    builder.declare_qvars(q)
    gate('H', [q])
    builder.measure()
# PASS
def only_measure(builder : QProgramBuilder):
    builder.measure_all()

# FAIL
def forget_builder():
    pass
# FAIL
def forget_declare(builder : QProgramBuilder):
    q = Qubit('q')
    gate('H', [q])
# FAIL
def measure_undeclare(builder : QProgramBuilder):
    decq = Qubit('decq')
    undecq = Qubit('undecq')
    builder.declare_qvars(decq)
    builder.measure(undecq)
# FAIL
def operate_after_measure(builder : QProgramBuilder):
    q = Qubit('q')
    builder.declare_qvars(q)
    gate('X', [q])
    builder.measure(q)
    gate('H', [q])
# FAIL
def declare_twice(builder : QProgramBuilder):
    q1 = Qubit('q1')
    q2 = Qubit('q2')
    builder.declare_qvars(q1)
    builder.declare_qvars(q2)
    builder.measure_all()
# FAIL
def measure_twice(builder : QProgramBuilder):
    q1 = Qubit('q1')
    q2 = Qubit('q2')
    builder.declare_qvars(q1, q2)
    builder.measure(q1)
    builder.measure(q2)
# FAIL
def declare_anonymous(builder : QProgramBuilder):
    q1 = Qubit()
    q2 = Qubit('q2')
    builder.declare_qvars(q1, q2)
    builder.measure_all()
# FAIL
def declare_same_name(builder : QProgramBuilder):
    q1 = QubitArray(5, 'name')
    q2 = QuInt(6, 'name')
    builder.declare_qvars(q1, q2)
    builder.measure_all()


# ---------- test cases for the compilation result ----------
# Basic Circuit Compile
def prog_EmptyCir(builder : QProgramBuilder):
    qarr = QubitArray(4, 'qarr')
    builder.declare_qvars(qarr)
def prog_OnlyGlobalPhase(builder : QProgramBuilder):
    qb = Qubit('qb')
    qarr = QubitArray(3, 'qarr')
    builder.declare_qvars(qb, qarr)
    gate('Z', [qb])
    gate('Rz', [qb], [math.pi])
def prog_Cir1A(builder : QProgramBuilder):
    q0 = Qubit('q0')
    q1 = Qubit('q1')
    builder.declare_qvars(q0, q1)
    gate('H', [q1])
    gate('CX', [q0, q1])
    gate('Z', [q0])
    gate('Z', [q1])
    gate('CX', [q0, q1])
    gate('H', [q1])

# Compile QubitArray
def Create01pm0(*args) -> CircuitIO:
    qc = CircuitIO(5, 5)
    qc.apply_gate('X', [1])
    qc.apply_gate('H', [2])
    qc.apply_gate('X', [3])
    qc.apply_gate('H', [3])
    return qc
def prog_Create01pm0(builder : QProgramBuilder):
    qarr = QubitArray(5, 'qarr')
    builder.declare_qvars(qarr)
    qarr.create_state_by_01pm_str('01+-0')

# Compile QuInt and two-value superposition
def Create44plus58(*args) -> CircuitIO:
    qc = CircuitIO(6, 6)
    qc.apply_gate('H', [1])
    qc.apply_gate('U1', [1], [math.pi / 3])
    qc.apply_gate('X', [2])
    qc.apply_gate('x', [3])
    qc.apply_gate('X', [5])
    qc.apply_gate('CX', [1, 2])
    qc.apply_gate('CNOT', [1, 4])
    return qc
def prog_Create44plus58(builder : QProgramBuilder):
    qnum = QuInt(6, 'qnum')
    builder.declare_qvars(qnum)
    qnum.create_two_value_superposition(44, 58, math.pi / 3)


# Compile QStruct, QTuple and QUnion
class MyStruct(QStruct):
    def __init__(self, varname=None):
        super().__init__(varname)
        self.x = QubitArray(3, 'x')
        self.y = make_qarray(QubitArray(2), 2, 'y')
        self.z = Qubit('z')
        self.init_qstruct(self.x, self.y, self.z)
class MyUnion(QUnion):
    def __init__(self, varname=None):
        super().__init__(varname)
        self.x = QubitArray(3, 'x')
        self.y = make_qarray(QubitArray(2), 2, 'y')
        self.z = Qubit('z')
        self.init_qunion(self.x, self.y, self.z)

# Compile QArray
