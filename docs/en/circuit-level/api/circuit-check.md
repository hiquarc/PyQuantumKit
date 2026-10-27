# pyquantumkit.circuit_check module
The circuit_check module provides functions for checking quantum circuits and quantum programs.

## pyquantumkit.circuit_check.matrix_based module
`pyquantumkit.circuit_check.matrix_based` provides methods for checking quantum circuits based on matrix representation.

### numeric_equivalence_check function
The `numeric_equivalence_check` function takes the NumPy matrices representing two quantum circuits and uses the matrix norm to check whether they are equivalent. The function prototype is:

```python
def numeric_equivalence_check(cirmat1 : numpy.array, cirmat2 : numpy.array,
                              ignore_global_phase : bool = True,
                              tolerance : float = DEFAULT_TOLERANCE,
                              norm = numpy_2_norm) -> bool:
```

- The parameter `cirmat1` is the NumPy matrix representing the first quantum circuit (it can be obtained using the `get_numpy_matrix` function of the CircuitIO class, [click here](./circuitio.md#get_numpy_matrix)).
- The parameter `cirmat2` is the NumPy matrix representing the second quantum circuit.
- The parameter `ignore_global_phase` specifies whether to ignore the global phase when checking equivalence. If set to `False`, the two quantum circuits are considered equivalent only when their corresponding matrices are equal within the tolerance; if set to `True`, the two quantum circuits are considered equivalent as long as their corresponding matrices differ only by a global phase. The default is `True`.
- The parameter `tolerance` specifies the error tolerance when determining equality; the default is `DEFAULT_TOLERANCE = 0.001`.
- The parameter `norm` specifies the matrix norm function used in the computation. The norm function should take a `numpy.array` type as its only parameter and return a `float` type. You can use a custom norm function, or use the following predefined norm functions (the default is `numpy_2_norm`):

    - `numpy_1_norm`: 1-norm $\|A\|_1 = \max_{1\leq j \leq n}\sum_{i=1}^n a_{ij}$
    - `numpy_2_norm`: 2-norm (spectral norm), the square root of the largest eigenvalue of $A^T A$.
    - `numpy_inf_norm`: $\infty$-norm $\|A\|_{\infty} = \max_{1\leq i \leq n}\sum_{j=1}^n a_{ij}$
    - `numpy_frobenius_norm`: Frobenius norm $\|A\|_F = \sqrt{\sum_{i=1}^n \sum_{j=1}^n |a_{ij}|^2}$

If the two quantum circuits are determined to be equal, `True` is returned; otherwise `False` is returned.

The specific execution flow of this function is as follows: let the matrices corresponding to the two quantum circuits be $A$, $B$, and let the passed-in `tolerance` parameter be $\epsilon$

- If `ignore_global_phase` is set to `False`, the function computes the norm of the difference of the two matrices $\|A-B\|$ using the given norm function `norm` and compares it with $\epsilon$; the function returns `True` if and only if $\|A-B\| \leq \epsilon$.
- If `ignore_global_phase` is set to `True`, the function first finds the element of largest magnitude in $B$, assuming its indices are $i',j'$; then the function computes the possible phase difference between $A$ and $B$ from the element's indices: $\kappa=a_{i'j'}/b_{i'j'}$; finally the function computes the norm $\|A-\kappa B\|$ using the given norm function `norm` and compares it with $\epsilon$; the function returns `True` if and only if $\|A-\kappa B\| \leq \epsilon$.

### numeric_identity_check function
The `numeric_identity_check` function takes a NumPy matrix representing a quantum circuit and uses the matrix norm to check whether it is the identity transformation (Identity). The function prototype is:

```python
def numeric_identity_check(cirmat : numpy.array,
                           ignore_global_phase : bool = True,
                           tolerance : float = DEFAULT_TOLERANCE,
                           norm = numpy_2_norm) -> bool:
```

- The parameter `cirmat` is the NumPy matrix representing the quantum circuit to be checked.
- The parameter `ignore_global_phase` specifies whether to ignore the global phase when checking equivalence. If set to `False`, the two quantum circuits are considered equivalent only when their corresponding matrices are equal within the tolerance; if set to `True`, the two quantum circuits are considered equivalent as long as their corresponding matrices differ only by a global phase. The default is `True`.
- The parameter `tolerance` specifies the error tolerance when determining equality; the default is `DEFAULT_TOLERANCE = 0.001`.
- The parameter `norm` specifies the matrix norm function used in the computation (the same as the parameter of the same name in the `numeric_equivalence_check` function); the default is `numpy_2_norm`.

If the quantum circuit is determined to be the identity transformation, `True` is returned; otherwise `False` is returned.

This function is equivalent to calling the `numeric_equivalence_check` function on `cirmat` and the identity matrix of the same order.
