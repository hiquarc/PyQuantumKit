# Quantum Hamiltonian Simulation Algorithms
**Note: This feature is experimental, has not been systematically tested, and its interface may change in the future. Please use it with caution.**

PyQuantumKit provides an algorithm library for quantum Hamiltonian simulation, which can be used to construct quantum Hamiltonian simulation programs. The quantum Hamiltonian simulation algorithm implements the transformation: $U=e^{-iHt}$, where $H$ is the Hermitian matrix representing the Hamiltonian of the quantum system and $t$ is the set evolution time.

PyQuantumKit currently supports representing the Hamiltonian as a linear combination of Pauli operators:

$$H=\sum_{i_1,i_2,\dots,i_n\in\{0,1,2,3\}} k_{i_1,i_2,\dots i_n} \sigma_{i_1}\otimes\sigma_{i_2}\otimes \dots \otimes\sigma_{i_n}$$

Each term corresponds to an $n$-qubit Pauli operator, which is the tensor product of single-qubit Pauli operators, and $k_{i_1,i_2,\dots i_n} \in \mathbb{R}$ is the linear combination coefficient corresponding to that Pauli operator, with the sum over at most $4^n$ terms. There are 4 single-qubit Pauli operators:

$$\sigma_0 = \left[\begin{array}{cc}1&0\\0&1\end{array}\right], \sigma_1 = \left[\begin{array}{cc}0&1\\1&0\end{array}\right], \sigma_2 = \left[\begin{array}{cc}0&-i\\i&0\end{array}\right], \sigma_3 = \left[\begin{array}{cc}1&0\\0&-1\end{array}\right]$$

An actual Hamiltonian is often sparse, that is, among the $4^n$ combination coefficients only $O(n)$ are nonzero, so the simulation of the Hamiltonian can be decomposed into a combination of simulations of each Pauli matrix form.

Suppose the total Hamiltonian can be written as the sum of $m$ local Hamiltonians $H=H_1+H_2+\dots+H_m$. If these $m$ local Hamiltonians commute pairwise (that is, multiplication is commutative: $\forall i\neq j, H_iH_j=H_jH_i$), then the simulation of the total Hamiltonian can be strictly decomposed into the sequential simulation of each local Hamiltonian:

$$ e^{-i(H_1+H_2+\dots+H_m)t} = e^{-iH_1t}e^{-iH_2t} \dots e^{-iH_mt} $$

However, in practice, the local Hamiltonians often do not have the commuting property, so certain approximation formulas need to be used for simulation. There are two commonly used approximation methods: Lie-Trotter and 2nd-order Suzuki, which can approximate to the square and the cube of the time step $\Delta t$, respectively.
Lie-Trotter formula:

$$e^{-i(H_1+H_2+\dots+H_m)\Delta t} = e^{-iH_1 \Delta t}e^{-iH_2 \Delta t} \dots e^{-iH_m \Delta t} + O(\Delta t^2)$$

2nd-order Suzuki formula:

$$e^{-i(H_1+H_2+\dots+H_m)\Delta t} = e^{-iH_1 \Delta t/2}e^{-iH_2 \Delta t/2} \dots e^{-iH_m \Delta t/2}e^{-iH_m \Delta t/2}e^{-iH_{m-1} \Delta t/2} \dots e^{-iH_1 \Delta t/2} + O(\Delta t^3)$$

Therefore, in practice, one can choose a repetition number $n$ and take the time step $\Delta t=t/n$, so that the total Hamiltonian simulation can be decomposed into $n$ repetitions:

$$e^{-i(H_1+H_2+\dots+H_m)t} \sim \left( e^{-iH_1 t/n}e^{-iH_2 t/n} \dots e^{-iH_m t/n} \right)^n$$

$$e^{-i(H_1+H_2+\dots+H_m)t} \sim \left( e^{-iH_1 t/2n}e^{-iH_2 t/2n} \dots e^{-iH_m t/2n}e^{-iH_m t/2n}e^{-iH_{m-1} t/2n} \dots e^{-iH_1 t/2n} \right)^n$$

PyQuantumKit provides quantum Hamiltonian simulation algorithms based on the above two decomposition methods. The function prototypes are:

```python
def pqk_hsim_paulis_trotter(q_circuit, hamiltonian : PauliHamiltonian, t : float, n : int, qindex : list[int]):
def pqk_hsim_paulis_suzuki2(q_circuit, hamiltonian : PauliHamiltonian, t : float, n : int, qindex : list[int]):
```

- The parameter `q_circuit` specifies the target quantum circuit.
- The parameter `hamiltonian` is a `PauliHamiltonian` class, used to specify the target Hamiltonian $H$;
- The parameter `t` specifies the evolution time;
- The parameter `n` specifies the repetition number of the decomposition;
- The parameter `qindex` is a list of integers, specifying the indices of the qubits on which the Hamiltonian simulation is to be applied.

The functions use the `PauliHamiltonian` class to represent the Hamiltonian. The member function `append_pauli` is used to add a Pauli term of the Hamiltonian to the `PauliHamiltonian` class. The prototype is:

```python
class PauliHamiltonian:
    def append_pauli(self, paulistr : str, factor : float, focus : int = 0) -> None:
```

- The parameter `paulistr` is a string composed of `'I'`, `'X'`, `'Y'`, `'Z'`, used to specify the corresponding Pauli operator; the length of the string should match the number of qubits specified when the `PauliHamiltonian` object is constructed.
- The parameter `factor` is a float specifying the coefficient of this term;
- The parameter `focus` is an optional parameter used to control the way the quantum circuit is generated; the default is 0.

The following example shows how to use PyQuantumKit to construct a quantum Hamiltonian simulation circuit. Consider the transverse-field Ising model, where each particle is represented by one qubit, with the Hamiltonian:

$$H=-J\sum_{\langle i,j \rangle}\sigma_3^{(i)}\sigma_3^{(j)} - B\sum_{i}\sigma_1^{(i)} $$

where $\sigma_3^{(i)}\sigma_3^{(j)}$ means that the Pauli operator on the $i,j$-th qubits is $\sigma_3$ and on the remaining qubits is $\sigma_0$; $\sigma_1^{(i)}$ means that the Pauli operator on the $i$-th qubit is $\sigma_1$ and on the remaining qubits is $\sigma_0$. The summation subscript $\langle i,j \rangle$ indicates summation over neighboring particles.

Here we consider a specific case. There are $N=5$ particles in total, arranged in a ring, with interactions between adjacent particles on the ring. The interaction strength is set to $J=1.0$, the strength of the external magnetic field to $B=1.0$, and the evolution time to $t=1.0$. Using the Lie-Trotter decomposition scheme, the repetition number is set to $n=20$. The code for constructing the quantum circuit on QPanda3 and Qiskit using PyQuantumKit is as follows:

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
