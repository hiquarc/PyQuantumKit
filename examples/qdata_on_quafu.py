import quafu
from pyquantumkit import QProgramBuilder, update_language_translation
from pyquantumkit.program.std import *
from pyquantumkit.program.quint import *

# 输入的整数和长度
N = 6       # 每个整数占6位
a = 44
b = 58
c = 5
d = 12

# ---------- 主函数 ----------
def qmain(builder : QProgramBuilder):
    # 声明两个量子整型变量
    qnum1 = QuInt(N, 'qnum1')
    qnum2 = QuInt(N, 'qnum2')
    builder.declare_qvars(qnum1, qnum2)

    # 分别为两个量子整型变量制备二值叠加态
    qnum1.create_two_value_superposition(a, b)
    qnum2.create_two_value_superposition(c, d)

    # 测量
    builder.measure_all()

builder = QProgramBuilder()
builder.build(qmain)

code = builder.get_built_circuit().export_standalone_code('OpenQASM2.0', 'qs')
print(code)

# for d in quafu.devices():
#     print(d["name"], d["kind"], d["status"], d["n_qubits"], d["queue"])

job = quafu.submit(code, target="sim", shots=1024)
print("任务组号：", job.id)

raw_counts = job.result().counts
print("原始结果：", raw_counts)

interpret_counts = builder.interpret_result_dict(raw_counts, 'r')
print("解读结果：", interpret_counts)
