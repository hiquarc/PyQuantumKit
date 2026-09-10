# test: common/high_level_programs.py
#    2026/9/8
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from pyquantumkit import QProgramBuilder, CircuitIO, parallel_circuits
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

# Measure a QUnion without activity item
# FAIL
class NoactQUnion(QUnion):
    def __init__(self, varname=None):
        super().__init__(varname)
        self.x = QubitArray(4, 'x')
        self.y = QuInt(5, 'y')
        self.init_qunion(self.x, self.y)
def measure_no_act_qunion(builder : QProgramBuilder):
    qu = NoactQUnion('qu')
    builder.declare_qvars(qu)
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
    builder.measure_all()

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
    builder.measure_all()


# The QStruct and QUnion to be tested
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

# Test compile QStruct
def cir_TestQStruct(*args) -> CircuitIO:
    qc = CircuitIO(8, 8)
    qc.apply_gate('T', [7])
    qc.apply_gate('SWAP', [5, 6])
    qc.apply_gate('H', [3])
    qc.apply_gate('CNOT', [3, 4])
    qc.apply_gate('H', [0])
    qc.apply_gate('X', [1])
    qc.apply_gate('X', [2])
    qc.apply_gate('H', [2])
    return qc

def apply_on_mydata(qvar : MyStruct|MyUnion):
    qvar.x.create_state_by_01pm_str('+1-')
    qvar.y[0].create_complementary_superposition('00')
    gate('SWAP', [qvar.y[1][0], qvar.y[1][1]])
    gate('T', [qvar.z])
def prog_TestQStruct(builder : QProgramBuilder):
    mystruct = MyStruct('mystruct')
    builder.declare_qvars(mystruct)
    apply_on_mydata(mystruct)
    builder.measure_all()

# Test compile QTuple
def prog_TestQTuple(builder : QProgramBuilder):
    mytuple = make_qtuple(( QubitArray(3),
                            make_qarray(QubitArray(2), 2),
                            Qubit ),
                          'mytuple')
    builder.declare_qvars(mytuple)
    mytuple[0].create_state_by_01pm_str('+1-')
    mytuple[1][0].create_complementary_superposition('00')
    gate('SWAP', [mytuple[1][1][0], mytuple[1][1][1]])
    gate('T', [mytuple[2]])
    builder.measure_all()

# Test compile QUnion
def cir_TestQUnion(*args) -> CircuitIO:
    qc = CircuitIO(4, 4)
    qc.apply_gate('H', [0])
    qc.apply_gate('X', [1])
    qc.apply_gate('X', [2])
    qc.apply_gate('H', [2])
    qc.apply_gate('H', [0])
    qc.apply_gate('CNOT', [0, 1])
    qc.apply_gate('SWAP', [2, 3])
    qc.apply_gate('T', [0])
    return qc

def prog_TestQUnion(builder : QProgramBuilder):
    myunion = MyUnion('myunion')
    builder.declare_qvars(myunion)
    apply_on_mydata(myunion)

# Test compile QArray
def cir_TestQArray(*args) -> CircuitIO:
    qc = CircuitIO(8, 8)
    qc << parallel_circuits(cir_TestQUnion(), cir_TestQUnion())
    return qc

def prog_TestQArray(builder : QProgramBuilder):
    myarray = make_qarray(MyUnion, 2, 'myarray')
    builder.declare_qvars(myarray)
    apply_on_mydata(myarray[0])
    apply_on_mydata(myarray[1])
    myarray[0].set_activity_item(myarray[0].y)
    myarray[1].set_activity_item(myarray[1].x)
    builder.measure_all()

# Empty data structure
class EmptyQStruct(QStruct):
    def __init__(self, varname=None):
        super().__init__(varname)
        self.init_qstruct()
class EmptyQUnion(QUnion):
    def __init__(self, varname=None):
        super().__init__(varname)
        self.init_qunion()

def prog_EmptyType(builder : QProgramBuilder):
    eqs = EmptyQStruct('eqs')
    equ = EmptyQUnion('equ')
    eqa1 = make_qarray(EmptyQStruct, 5, 'eqa1')
    eqa2 = make_qarray(Qubit, 0, 'eqa2')
    eqa3 = QubitArray(0, 'eqa3')
    builder.declare_qvars(eqs, equ, eqa1, eqa2, eqa3)
    builder.measure_all()

# ---------- test cases for interpreting results ----------
def prog_TestQUnion_Mx(builder : QProgramBuilder):
    myunion = MyUnion('myunion')
    builder.declare_qvars(myunion)
    apply_on_mydata(myunion)
    myunion.set_activity_item(myunion.x)
    builder.measure_all()

def prog_TestQUnion_My(builder : QProgramBuilder):
    myunion = MyUnion('myunion')
    builder.declare_qvars(myunion)
    apply_on_mydata(myunion)
    myunion.set_activity_item(myunion.y)
    builder.measure_all()

def prog_TestQUnion_Mz(builder : QProgramBuilder):
    myunion = MyUnion('myunion')
    builder.declare_qvars(myunion)
    apply_on_mydata(myunion)
    myunion.set_activity_item(myunion.z)
    builder.measure_all()

def prog_PartialMeasure(builder : QProgramBuilder):
    q1 = QubitArray(3, 'q1')
    q2 = QubitArray(2, 'q2')
    q3 = QubitArray(4, 'q3')
    builder.declare_qvars(q3, q2, q1)
    builder.measure(q1, q3)
def prog_PartialMeasure2(builder : QProgramBuilder):
    q1 = QubitArray(3, 'q1')
    q2 = QubitArray(2, 'q2')
    q3 = QubitArray(4, 'q3')
    builder.declare_qvars(q3, q2, q1)
    builder.measure(q3, q2)

def prog_TwoQuInt(builder : QProgramBuilder):
    qnum1 = QuInt(6, 'qnum1')
    qnum2 = QuInt(6, 'qnum2')
    builder.declare_qvars(qnum1, qnum2)

    qnum1.create_two_value_superposition(43, 57)
    qnum2.create_two_value_superposition(7, 12)

    builder.measure_all()

# ---------- test cases for special methods ----------
class SpecialQStruct(QStruct):
    def __init__(self, varname=None):
        super().__init__(varname)
        self.__q = Qubit('q')
        self.init_qstruct(self.__q)
    def _initialize_(self):
        super()._initialize_()
        print("<SpecialQStruct._initialize_> is called")
    def _premeasure_(self):
        super()._premeasure_()
        print("<SpecialQStruct._premeasure_> is called")
    def _gate_(self, *args):
        print("<SpecialQStruct._gate_> is called")
        return self.__q
    def _interpret_(self, output):
        if self.__q._interpret_(output) == '1':
            return 'ONE'
        else:
            return 'ZERO'

def prog_TestSpecialMethods(builder : QProgramBuilder):
    sqs = SpecialQStruct('sqs')
    builder.declare_qvars(sqs)
    gate('H', [sqs])
    builder.measure_all()
