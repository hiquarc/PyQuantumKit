import pyqpanda3.core as qpanda
import qiskit
import qiskit_aer
from math import pi

# import QProgramBuilder and pyquantumkit.program.* modules
from pyquantumkit import QProgramBuilder
from pyquantumkit.program.std import *
from pyquantumkit.program.quint import *

# ---------- The main function of quantum program ----------
#            The 1st parameter must be a QProgramBuilder object
def qmain(builder : QProgramBuilder):
    # Declare quantum variables
    qnum = QuInt(6, 'qnum')         
    builder.declare_qvars(qnum)     # this line is required

    # Main body of function
    qnum.create_two_value_superposition(44, 58, pi / 3)

    # Measurement
    builder.measure(qnum)

# Declare a QProgramBuilder object
qpbuilder = QProgramBuilder()
# Build the qmain program into quantum circuit, saving it in the QProgramBuilder object
qpbuilder.build(qmain)

# You can use qpbuilder.get_built_circuit() to get the built circuit


# ---------- Run on qiskit ----------
qiskit_cir = qiskit.QuantumCircuit(6, 6)

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
