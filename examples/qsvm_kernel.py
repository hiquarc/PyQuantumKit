# example/qsvm_kernel.py
#    2026/2/4
#    PyQuantumKit实现计算QVSM核函数的演示程序
#    原作者：伍思扬
#    移植：龙沛洵

import numpy as np
import pandas as pd
import pyqpanda3.core as qpanda
import qiskit, qiskit_aer
import pyquantumkit as pqk


def feature_map(x, circuit):
    n_qubits = len(x)

    for i in range(0, n_qubits):
        pqk.apply_gate(circuit, 'H', [i])
        angle = float(2 * x[i])
        pqk.apply_gate(circuit, 'U1', [i], [angle])

    for i in range(0, n_qubits - 1):
        pqk.apply_gate(circuit, 'CNOT', [i, i + 1])
        angle = float(2 * (np.pi - x[i]) * (np.pi - x[i + 1]))
        pqk.apply_gate(circuit, 'U1', [i + 1], [angle])
        pqk.apply_gate(circuit, 'CNOT', [i, i + 1])


def K_Q_circuit(x, y, prog):
    n_feature = len(x)
    cio = pqk.CircuitIO(n_feature)
    cio_y = pqk.CircuitIO(n_feature)
    
    feature_map(x, cio)         # 插入 feature_map(x) 门
    feature_map(y, cio_y)
    cio_y.inverse()
    cio << cio_y                # 插入 feature_map(y) 门的逆
    cio.apply_measure(range(0, n_feature), range(0, n_feature))
    cio >> prog


# Run K_Q_circuit on <qvm> with shots=<measure_time>
def K_Q(qvm, x, y, measure_time : int):
    if (len(x) != len(y)):
        raise ValueError("Invalid Feature! ")
    n_feature = len(x)

    # 由传入的qvm获取所使用的框架名称
    qframe = pqk.get_framework_from_object(qvm)
    # 新建相应框架的量子线路对象
    prog = pqk.new_program(qframe, n_feature, n_feature)
    # 在其上构造所需量子线路：K_Q_circuit
    K_Q_circuit(x, y, prog)
    # 调用run_and_get_counts执行并取得测量结果（实验性功能）
    result = pqk.run_and_get_counts(qvm, prog, measure_time)
    # NOTE: PyQuantumKit已经可以实现统一方式构造量子线路，但统一方式执行还需要做一些工作。
    #   目前有的run_and_get_counts函数只是实验性功能，我在写这个程序的时候注意到了上述工作流程的局限性。
    #   因此，后面我们需要根据在真机上的实现方式来考虑如何改进。

    target = '0' * n_feature
    if target in result:
        return result[target] / float(measure_time)
    else:
        return 0.0


def quantum_kernel(qvm, X, Y, measure_time : int = 1000000):
    X = np.array(X)
    Y = np.array(Y)
    n_events_X, n_features_X = np.shape(X)
    n_events_Y, n_features_Y = np.shape(Y)

    K = np.ones([n_events_X, n_events_Y])
    for i in range(0, n_events_X):
        for j in range(0, n_events_Y):
            K[i][j] = K_Q(qvm, X[i], Y[j], measure_time)

    return K


data1 = pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]], columns = ["x", "y", "z"])
data2 = pd.DataFrame([[4, 5, 6], [3, 2, 1]], columns = ["x", "y", "z"])

# Run on QPanda3
qvm_qpanda = qpanda.CPUQVM()
kernel_qpanda = quantum_kernel(qvm_qpanda, data1, data2)
print(f"kernel_qpanda = \n{kernel_qpanda}")

# Run on Qiskit
qvm_qiskit = qiskit_aer.Aer.get_backend('aer_simulator')
kernel_qiskit = quantum_kernel(qvm_qiskit, data1, data2)
print(f"kernel_qiskit = \n{kernel_qiskit}")
