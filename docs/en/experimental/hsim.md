# Quantum Hamiltonian Simulation
**Note: This feature is experimental, has not undergone systematic testing, and the interface may change in the future. Please use it with caution.**

PyquantumKit provides a library of quantum Hamiltonian simulation algorithms that can be used to build quantum Hamiltonian simulation programs. The quantum Hamiltonian simulation algorithm implements the transformation: $U=e^{-iHt}$, where $H$ is a Hermitian matrix representing the Hamiltonian of the quantum system, and $t$ is the set evolution time.

PyQuantumKit currently supports representing Hamiltonians as linear combinations of Pauli operators:

$$H=\sum_{i_1,i_2,\dots,i_n\in\{0,1,2,3\}} k_{i_1,i_2,\dots i_n} \sigma_{i_1}\otimes\sigma_{i_2}\otimes \dots \otimes\sigma_{i_n}$$

Each term corresponds to an $n$-qubit Pauli operator, which is the tensor product of single-qubit Pauli operators. $k_{i_1,i_2,\dots i_n} \in \mathbb{R}$ is the linear combination coefficient corresponding to the Pauli operator, and the sum has at most $4^n$ terms. There are 4 single-qubit Pauli operators:

$$\sigma_0 = \left[\begin{array}{cc}1&0\\0&1\end{array}\right], \sigma_1 = \left[\begin{array}{cc}0&1\\1&0\end{array}\right], \sigma_2 = \left[\begin{array}{cc}0&-i\\i&0\end{array}\right], \sigma_3 = \left[\begin{array}{cc}1&0\\0&-1\end{array}\right]$$

Practical Hamiltonians are often sparse, meaning only $O(n)$ of the $4^n$ combination coefficients are non-zero. Therefore, the simulation of the Hamiltonian can be decomposed into a combination of simulations of each Pauli matrix form.

Let the total Hamiltonian be written as the sum of $m$ local Hamiltonians $H=H_1+H_2+\dots+H_m$. If these $m$ local Hamiltonians commute pairwise (i.e., multiplication is commutative: $\forall i\neq j, H_iH_j=H_jH_i$), then the simulation of the total Hamiltonian can be strictly decomposed into sequential simulations of each local Hamiltonian:

$$ e^{-i(H_1+H_2+\dots+H_m)t} = e^{-iH_1t}e^{-iH_2t} \dots e^{-iH_mt} $$

However, in practice, local Hamiltonians often do not have commutative properties, so certain approximation formulas need to be used for simulation. Two commonly used approximation methods are Lie-Trotter and 2nd-order Suzuki, which can approximate to the square and cube of the time step $\Delta t$, respectively.
Lie-Trotter formula:

$$e^{-i(H_1+H_2+\dots+H_m)\Delta t} = e^{-iH_1 \Delta t}e^{-iH_2 \Delta t} \dots e^{-iH_m \Delta t} + O(\Delta t^2)$$

2nd-order Suzuki formula:

$$e^{-i(H_1+H_2+\dots+H_m)\Delta t} = e^{-iH_1 \Delta t/2}e^{-iH_2 \Delta t/2} \dots e^{-iH_m \Delta t/2}e^{-iH_m \Delta t/2}e^{-iH_{m-1} \Delta t/2} \dots e^{-iH_1 \Delta t/2} + O(\Delta t^3)$$

Therefore, in practice, we can select a repetition number $n$ and take the time step $\Delta t=t/n$. Then the total Hamiltonian simulation can be decomposed into $n$ repetitions:

$$e^{-i(H_1+H_2+\dots+H_m)t} \sim \left( e^{-iH_1 t/n}e^{-iH_2 t/n} \dots e^{-iH_m t/n} \right)^n$$

$$e^{-i(H_1+H_2+\dots+H_m)t} \sim \left( e^{-iH_1 t/2n}e^{-iH_2 t/2n} \dots e^{-iH_m t/2n}e^{-iH_m t/2n}e^{-iH_{m-1} t/2n} \dots e^{-iH_1 t/2n} \right)^n$$

PyQuantumKit provides quantum Hamiltonian simulation algorithms based on the above two decomposition methods, with the function prototypes:

```python
def pqk_hsim_paulis_trotter(q_circuit, hamiltonian : PauliHamiltonian, t : float, n : int, qindex : list[int]):
def pqk_hsim_paulis_suzuki2(q_circuit, hamiltonian : PauliHamiltonian, t : float, n : int, qindex : list[int]):
```

- The parameter `q_circuit` specifies the target quantum circuit.
- The parameter `hamiltonian` is a `PauliHamiltonian` class used to specify the target Hamiltonian $H$;
- The parameter `t` specifies the evolution time;
- The parameter `n` specifies the number of decomposition repetitions;
- The parameter `qindex` is a list of integers specifying the subscripts of the qubits to which the Hamiltonian simulation is applied.

The `PauliHamiltonian` class is used in the functions to represent the Hamiltonian. Its member function `append_pauli` is used to add a Pauli factor of the Hamiltonian to the `PauliHamiltonian` class, with the prototype:

```python
class PauliHamiltonian:
    def append_pauli(self, paulistr : str, factor : float, focus : int = 0) -> None:
```

- The parameter `paulistr` is a string composed of `'I'`, `'X'`, `'Y'`, `'Z'` used to specify the corresponding Pauli operator. The length of the string should match the number of qubits specified when constructing the `PauliHamiltonian` object.
- The parameter `factor` is a floating-point number specifying the coefficient of this factor;
- The parameter `focus` is an optional parameter used to control the way the quantum circuit is generated, with a default value of 0.

The following example shows how to use PyQuantumKit to construct a quantum Hamiltonian simulation circuit. Consider the transverse-field Ising model, where each particle is represented by a qubit, and the Hamiltonian is:

$$H=-J\sum_{\langle i,j \rangle}\sigma_3^{(i)}\sigma_3^{(j)} - B\sum_{i}\sigma_1^{(i)} $$

where $\sigma_3^{(i)}\sigma_3^{(j)}$ means the Pauli operator on the $i$-th and $j$-th qubits is $\sigma_3$, and $\sigma_0$ on the remaining qubits; $\sigma_1^{(i)}$ means the Pauli operator on the $i$-th qubit is $\sigma_1$, and $\sigma_0$ on the remaining qubits. The summation subscript $\langle i,j \rangle$ denotes summation over neighboring particles.

Here we consider a specific case. There are a total of $N=5$ particles arranged in a ring, with interactions between adjacent particles on the ring. Set the interaction strength $J=1.0$, the external magnetic field strength $B=1.0$, and the evolution time $t=1.0$. The Lie-Trotter decomposition scheme is adopted, with the number of repetitions set to $n=20$. The code for constructing quantum circuits on QPanda3 and Qiskit using PyQuantumKit is as follows:

```python
import pyqpanda3.core as qpanda
import qiskit, qiskit_aer
import pyquantumkit as PQK
import pyquantumkit.library.hamiltonian as PQKHami

N = 5           # number of particles
J = 1.0         # interaction
B = 1.0         # magnatic field
t = 1.0         # evolution time
n = 20          # rounds of decomposition

# ----- Build the Hamiltonian -----
# construct a PauliHamiltonian object, the parameter is the number of qubits
TFIsing = PQKHami.PauliHamiltonian(N)
# interaction terms
TFIsing.append_pauli('ZZIII', -J)
TFIsing.append_pauli('IZZII', -J)
TFIsing.append_pauli('IIZZI', -J)
TFIsing.append_pauli('IIIZZ', -J)
TFIsing.append_pauli('ZIIIZ', -J)
# magnatic field terms
TFIsing.append_pauli('XIIII', -B)
TFIsing.append_pauli('IXIII', -B)
TFIsing.append_pauli('IIXII', -B)
TFIsing.append_pauli('IIIXI', -B)
TFIsing.append_pauli('IIIIX', -B)

# construct circuit on qpanda
qpanda_circuit = qpanda.QCircuit(N)
PQKHami.pqk_hsim_paulis_trotter(qpanda_circuit, TFIsing, t, n, range(N))
print(qpanda_circuit)

# construct circuit on qiskit
qiskit_circuit = qiskit.QuantumCircuit(N)
PQKHami.pqk_hsim_paulis_trotter(qiskit_circuit, TFIsing, t, n, range(N))
print(qiskit_circuit)
```