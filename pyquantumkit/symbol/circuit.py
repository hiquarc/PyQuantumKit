# symbol/circuit.py
#    2025/12/15
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

import sympy
from pyquantumkit.classical.common import dim2nbits, contain_duplicates, remap_bits

def symbol_apply_gate(gate : sympy.MatrixBase, nqbits : int, indexlist : list[int]) -> sympy.Matrix:
    """
    Apply a target gate on several qubits of the circuit, returning the total matrix

        gate      : matrix applied gate (must be 2^k x 2^k)
        nqbits    : (int) the total number of qubits n of the circuit
                    NOTE: n >= k
        indexlist : (list[int]) the index list to identify the target qubits to be applied 
                    NOTE: the length of <indexlist> must equal k

    -> Return : the total matrix
    """
    if gate.rows != gate.cols:
        raise ValueError("Unequal number of rows and columns of <gate>!")
    gdim = gate.rows
    (ngatebits, flag) = dim2nbits(gdim)
    if not flag:
        raise ValueError("The matrix dimension of <gate> is not the power of 2!")
    if len(indexlist) > nqbits:
        raise ValueError("The number of gate qubits is larger than length of <indexlist>")
    if len(indexlist) != ngatebits:
        raise ValueError("The length of <indexlist> does not match the dimension of <gate>")
    if contain_duplicates(indexlist):
        raise ValueError("<indexlist> contains duplicated elements!")
    
    revindexlist = [nqbits - item - 1 for item in indexlist][::-1]
    compindexlist = [item for item in range(0, nqbits) if item not in revindexlist]
    ret = sympy.zeros(2 ** nqbits)
    for i in range(0, gdim):
        remap_i = remap_bits(i, revindexlist)
        for j in range(0, gdim):
            remap_j = remap_bits(j, revindexlist)
            for k in range(0, 2 ** len(compindexlist)):
                remap_k = remap_bits(k, compindexlist)
                applied_i = remap_k | remap_i
                applied_j = remap_k | remap_j
                ret[applied_i, applied_j] = gate[i, j]
    return ret
    

def symbol_controlled_gate(gate : sympy.MatrixBase, nctrlbits : int) -> sympy.BlockDiagMatrix:
    """
    Given the matrix of a gate and the number of controlling qubits, return its controlled version matrix

        gate      : matrix applied gate (dimension 2^k x 2^k)
        nctrlbits : (int) the number of controlling qubits n

    Return : the BlockDiagMatrix object with dimension 2^(n+k) x 2^(n+k)
             the first n qubits are controlling qubits, the rest k qubits are target qubits
    """
    if gate.rows != gate.cols:
        raise ValueError("Unequal number of rows and columns of <gate>!")
    ids = sympy.Identity(gate.rows * (2 ** nctrlbits - 1))
    return sympy.BlockDiagMatrix(ids, gate)


def symbol_multi_apply_sqgate(sqgate : sympy.MatrixBase, nqbits : int) -> sympy.Matrix:
    """
    Apply a series of single-qubit gates on every qubit, returning the total matrix

        sqgate  : 2x2 matrix to represent the single-qubit gate
        nqubits : (int) the total number of qubits
    """
    ret = sympy.Matrix([[1]])
    for i in range(nqbits):
        ret = sympy.kronecker_product(ret, sqgate)
    return ret


# def symbol_check_circuit_equivalence(cirmat1 : sympy.Matrix, cirmat2 : sympy.Matrix) -> sympy.Matrix:
#     """
#     """
#     pass
