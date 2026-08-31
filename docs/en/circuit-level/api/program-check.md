# pyquantumkit.program_check Module
The program_check module provides functions for verifying quantum circuits and quantum programs.

## pyquantumkit.program_check.matrix_based Module
`pyquantumkit.program_check.matrix_based` provides matrix representation-based verification methods for quantum circuits.

### numeric_equivalence_check Function
The `numeric_equivalence_check` function takes NumPy matrices representing two quantum circuits and checks their equivalence using matrix norms. The function prototype is:

```python
def numeric_equivalence_check(cirmat1 : numpy.array, cirmat2 : numpy.array,
                              ignore_global_phase : bool = True,
                              tolerance : float = DEFAULT_TOLERANCE,
                              norm = numpy_2_norm) -> bool:
```
- Parameter `cirmat1` is the NumPy matrix representing the first quantum circuit (which can be obtained using the `get_numpy_matrix` function of the CircuitIO class, [see here](./circuitio.md#get_numpy_matrix)).
- Parameter `cirmat2` is the NumPy matrix representing the second quantum circuit.
- Parameter `ignore_global_phase` specifies whether to ignore the global phase when checking equivalence. If set to `False`, the two quantum circuits are judged to be equivalent only if their corresponding matrices are equal within the error tolerance; if set to `True`, the two quantum circuits are judged to be equivalent as long as their corresponding matrices differ only by a global phase. The default value is `True`.
- Parameter `tolerance` specifies the error tolerance for judging equality, with a default value of `DEFAULT_TOLERANCE = 0.001`.
- Parameter `norm` specifies the matrix norm function used for calculation. The norm function should take a `numpy.array` type as the only parameter and return a `float` type. Users can use custom norm functions or the following preset norm functions (the default is `numpy_2_norm`):
    - `numpy_1_norm`: 1-norm $\|A\|_1 = \max_{1\leq j \leq n}\sum_{i=1}^n a_{ij}$
    - `numpy_2_norm`: 2-norm (spectral norm), the square root of the largest eigenvalue of $A^T A$.
    - `numpy_inf_norm`: $\infty$-norm $\|A\|_{\infty} = \max_{1\leq i \leq n}\sum_{j=1}^n a_{ij}$
    - `numpy_frobenius_norm`: Frobenius norm $\|A\|_F = \sqrt{\sum_{i=1}^n \sum_{j=1}^n |a_{ij}|^2}$

Returns `True` if the two quantum circuits are judged to be equivalent; otherwise returns `False`.

The specific execution process of the function is as follows: let the matrices corresponding to the two quantum circuits be $A$ and $B$ respectively, and the input `tolerance` parameter be denoted as $\epsilon$.
- If `ignore_global_phase` is set to `False`, the function calculates the norm of the difference between the two matrices $\|A-B\|$ according to the given norm function `norm` and compares it with $\epsilon$. The function returns `True` if and only if $\|A-B\| \leq \epsilon$.
- If `ignore_global_phase` is set to `True`, the function first finds the element with the largest modulus in $B$, assuming its subscript is $i',j'$; then the function calculates the possible phase difference between $A$ and $B$ through this element subscript: $\kappa=a_{i'j'}/b_{i'j'}$; finally the function calculates the norm $\|A-\kappa B\|$ according to the given norm function `norm` and compares it with $\epsilon$. The function returns `True` if and only if $\|A-\kappa B\| \leq \epsilon$.

### numeric_identity_check Function
The `numeric_identity_check` function takes a NumPy matrix representing a quantum circuit and checks whether it is an identity transformation using matrix norms. The function prototype is:

```python
def numeric_identity_check(cirmat : numpy.array,
                           ignore_global_phase : bool = True,
                           tolerance : float = DEFAULT_TOLERANCE,
                           norm = numpy_2_norm) -> bool:
```
- Parameter `cirmat` is the NumPy matrix representing the quantum circuit to be verified.
- Parameter `ignore_global_phase` specifies whether to ignore the global phase when checking equivalence. If set to `False`, the two quantum circuits are judged to be equivalent only if their corresponding matrices are equal within the error tolerance; if set to `True`, the two quantum circuits are judged to be equivalent as long as their corresponding matrices differ only by a global phase. The default value is `True`.
- Parameter `tolerance` specifies the error tolerance for judging equality, with a default value of `DEFAULT_TOLERANCE = 0.001`.
- Parameter `norm` specifies the matrix norm function used for calculation (the same as the homonymous parameter of the `numeric_equivalence_check` function), with a default value of `numpy_2_norm`.

Returns `True` if the quantum circuit is judged to be an identity transformation; otherwise returns `False`.

This function is equivalent to calling the `numeric_equivalence_check` function with `cirmat` and an identity matrix of the same order as it.
