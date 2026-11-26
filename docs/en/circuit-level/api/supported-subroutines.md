# Quantum Subroutines Supported by PyQuantumKit

This page gives the quantum subroutines supported by PyQuantumKit and the corresponding call strings of the `apply_subroutine` function, for users to consult. **Please note that when a quantum circuit containing quantum subroutines needs to be applied to a specific quantum development framework, it is necessary to pay attention to whether the target quantum development framework supports the subroutine.** Unlike quantum gates, if the target platform does not support a certain subroutine, PyQuantumKit directly reports an "unsupported" error, and does not perform equivalence transformations for compatibility.

## Quantum Fourier transform series subroutines

### Standard quantum Fourier transform
- Call string of the apply_subroutine function (case-insensitive, same below): `'QFT'`

### Quantum Fourier transform without the SWAP gates at the end
- Call string of the apply_subroutine function: `'QFT_NS'`

### Standard inverse quantum Fourier transform
- Call string of the apply_subroutine function: `'IQFT'`

### Inverse quantum Fourier transform without the SWAP gates at the beginning
- Call string of the apply_subroutine function: `'IQFT_NS'`