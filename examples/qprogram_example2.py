import pyqpanda3.core as qpanda
import qiskit
import qiskit_aer

# import QProgramBuilder and pyquantumkit.program.* modules
from pyquantumkit import QProgramBuilder
from pyquantumkit.program.std import *
from pyquantumkit.program.quint import *


# 从命令行中读入整数，并进行校验
def input_numbers():
    # 从命令行读取输入（默认以空格分隔）
    raw_input = input("请输入4个整数（以空格分隔）: ").split()
    
    # 校验输入数量
    if len(raw_input) != 4:
        print("错误：请输入恰好4个整数。")
        return None
    try:
        # 转换为整数列表（若包含非数字字符会触发 ValueError）
        nums = [int(x) for x in raw_input]
        # 逐一检查范围是否在 [0, 63]
        for i, val in enumerate(nums, start=1):
            if not (0 <= val <= 63):
                print(f"错误：第{i}个整数 {val} 不在 0 ~ 63 范围内。")
                return None
        # 全部满足约束，返回列表
        return nums    
    except ValueError:
        print("错误：输入包含非整数字符，请输入有效的整数。")
        return None


# ---------- The main function of quantum program ----------
#            The 1st parameter must be a QProgramBuilder object
def qmain(builder : QProgramBuilder, a : int, b : int, c : int, d : int):
    qnum1 = QuInt(6, 'qnum1')
    qnum2 = QuInt(6, 'qnum2')
    builder.declare_qvars(qnum1, qnum2)
    qnum1.create_two_value_superposition(a, b)
    qnum2.create_two_value_superposition(c, d)
    builder.measure_all()


numbers = input_numbers()
while numbers is None:
    numbers = input_numbers()

a, b, c, d = numbers
qpbuilder = QProgramBuilder()
qpbuilder.build(qmain, a, b, c, d)

# ---------- Run on qiskit ----------
print("---------- Run on qiskit ----------")
qiskit_cir = qiskit.QuantumCircuit(12, 12)

# Call qpbuilder.get_built_circuit() to get the built circuit (as a CircuitIO object).
#    Then use the >> operation of CircuitIO to append it into the Qiskit circuit.
qpbuilder.get_built_circuit() >> qiskit_cir
print(qiskit_cir)

# Run on Qiskit's simulator and get the result dict
qiskit_sim = qiskit_aer.AerSimulator()
result = qiskit_sim.run(qiskit_cir, shots = 1000).result().get_counts()
print(result)

# Call interpret_result_dict() of the QProgramBuilder object to interpret the result dict
rec_result = qpbuilder.interpret_result_dict(result, 'qiskit')
print(rec_result)


# ---------- Run on pyqpanda3 ----------
print("---------- Run on pyqpanda3 ----------")
qpanda_cir = qpanda.QProg()

# Call qpbuilder.get_built_circuit() to get the built circuit (as a CircuitIO object).
#    Then use the >> operation of CircuitIO to append it into the QPanda3 circuit.
qpbuilder.get_built_circuit() >> qpanda_cir
print(qpanda_cir)

# Run on QPanda3's simulator and get the result dict
qpanda_qvm = qpanda.CPUQVM()
qpanda_qvm.run(qpanda_cir, 1000)
qpanda_result = qpanda_qvm.result().get_counts()
print(qpanda_result)

# Call interpret_result_dict() of the QProgramBuilder object to interpret the result dict
rec_result = qpbuilder.interpret_result_dict(qpanda_result, 'pyqpanda3')
print(rec_result)
