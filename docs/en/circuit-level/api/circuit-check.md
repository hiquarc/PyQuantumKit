# The pyquantumkit.circuit_check module
The circuit_check module provides functions for checking quantum circuits and quantum programs.

## The pyquantumkit.circuit_check.matrix_based module
`pyquantumkit.circuit_check.matrix_based` provides quantum circuit checking methods based on matrix representation.

### The numeric_equivalence_check function
The `numeric_equivalence_check` function takes NumPy matrices representing two quantum circuits as input and checks whether they are equivalent using the matrix norm. Its prototype is:

```python
def numeric_equivalence_check(cirmat1 : numpy.array, cirmat2 : numpy.array,
                              ignore_global_phase : bool = True,
                              tolerance : float = DEFAULT_TOLERANCE,
                              norm = numpy_2_norm) -> bool:
```

- The parameter `cirmat1` is the NumPy matrix representing the first quantum circuit (which can be obtained using the `get_numpy_matrix` function of the CircuitIO class, [click here](./circuitio.md#get_numpy_matrix)).
- The parameter `cirmat2` is the NumPy matrix representing the second quantum circuit.
- The parameter `ignore_global_phase` specifies whether to ignore the global phase when checking equivalence. If set to `False`, the two quantum circuits are judged equivalent only when their corresponding matrices are equal within the error range; if set to `True`, the two quantum circuits are judged equivalent as long as their corresponding matrices differ only by a global phase. It defaults to `True`.
- The parameter `tolerance` specifies the error tolerance when judging equality, and defaults to `DEFAULT_TOLERANCE = 0.001`.
- The parameter `norm` specifies the matrix norm function used in the computation; the norm function should take a `numpy.array` type as its only parameter and return a `float` type. Users can define a custom norm function, or use the following predefined norm functions (the default is `numpy_2_norm`):

    - `numpy_1_norm`: the 1-norm $\|A\|_1 = \max_{1\leq j \leq n}\sum_{i=1}^n a_{ij}$
    - `numpy_2_norm`: the 2-norm (spectral norm), the square root of the largest eigenvalue of $A^T A$.
    - `numpy_inf_norm`: the $\infty$-norm $\|A\|_{\infty} = \max_{1\leq i \leq n}\sum_{j=1}^n a_{ij}$
    - `numpy_frobenius_norm`: the Frobenius norm $\|A\|_F = \sqrt{\sum_{i=1}^n \sum_{j=1}^n |a_{ij}|^2}$

If the two quantum circuits are judged to be equal, it returns `True`; otherwise it returns `False`.

The specific execution process of this function is: let the matrices corresponding to the two quantum circuits be $A$ and $B$ respectively, and let the passed `tolerance` parameter be denoted $\epsilon$.

- If `ignore_global_phase` is set to `False`, the function computes the norm $\|A-B\|$ of the difference of the two matrices according to the given norm function `norm` and compares it with $\epsilon$; the function returns `True` if and only if $\|A-B\| \leq \epsilon$.
- If `ignore_global_phase` is set to `True`, the function first finds the element with the largest modulus in $B$, assuming its index is $i',j'$; then the function computes the possible phase difference between $A$ and $B$ through this element index: $\kappa=a_{i'j'}/b_{i'j'}$; finally the function computes the norm $\|A-\kappa B\|$ according to the given norm function `norm` and compares it with $\epsilon$; the function returns `True` if and only if $\|A-\kappa B\| \leq \epsilon$.

### The numeric_identity_check function
The `numeric_identity_check` function takes a NumPy matrix representing a quantum circuit as input and checks whether it is the identity transformation using the matrix norm. Its prototype is:

```python
def numeric_identity_check(cirmat : numpy.array,
                           ignore_global_phase : bool = True,
                           tolerance : float = DEFAULT_TOLERANCE,
                           norm = numpy_2_norm) -> bool:
```

- The parameter `cirmat` is the NumPy matrix representing the quantum circuit to be checked.
- The parameter `ignore_global_phase` specifies whether to ignore the global phase when checking equivalence. If set to `False`, the two quantum circuits are judged equivalent only when their corresponding matrices are equal within the error range; if set to `True`, the two quantum circuits are judged equivalent as long as their corresponding matrices differ only by a global phase. It defaults to `True`.
- The parameter `tolerance` specifies the error tolerance when judging equality, and defaults to `DEFAULT_TOLERANCE = 0.001`.
- The parameter `norm` specifies the matrix norm function used in the computation (the same as the parameter of the same name in the `numeric_equivalence_check` function), and defaults to `numpy_2_norm`.

If the quantum circuit is judged to be the identity transformation, it returns `True`; otherwise it returns `False`.

This function is equivalent to calling the `numeric_equivalence_check` function on `cirmat` and the identity matrix of the same order.