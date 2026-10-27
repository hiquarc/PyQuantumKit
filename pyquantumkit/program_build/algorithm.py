# program_build/algorithm.py
#    2026/10/10
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

import abc

class AutoParas:
    pass

COMPILE_OPTION_STR = {
    "auto",
    "native-prior",
    "native",
    "pyquantumkit",
}

class QAlg(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def impl(cls, *args, **kwargs) -> callable:
        pass

    @classmethod
    @abc.abstractmethod
    def impl_auto(cls, *args, **kwargs) -> callable:
        pass
