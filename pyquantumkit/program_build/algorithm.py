# program_build/algorithm.py
#    2026/10/10
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

import abc
import functools
from pyquantumkit.program_build.qtype import QuantumProgramBuildError

class AutoParas:
    pass

SUBROUTINE_OPTION_STR = {
    "auto",
    "native-prior",
    "native",
    "pyquantumkit",
}

class QAlg(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def _general_impl_(cls, *args, **kwargs):
        pass

    @classmethod
    def _meta_info_(cls, *args, **kwargs):
        pass

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    def apply():
        pass

    # SUBROUTINE_NAME = None
    # DEFAULT_CONSTRUCT_PARAS = []

    # @classmethod
    # def apply_specific(cls, inherent_paras, construct_paras):
    #     return cls._general_impl_(inherent_paras, construct_paras)

    # @classmethod
    # def apply_default(cls, *args):
    #     return cls._general_impl_(args, cls.DEFAULT_CONSTRUCT_PARAS)

    # @classmethod
    # def apply_native(cls, *args):
    #     if cls.SUBROUTINE_NAME is None:
    #         raise QuantumProgramBuildError(f"QAlg <{cls}> does not correspond to any native quantum subroutine.")
    #     # TODO: finish the translation to Subroutine

    # @classmethod
    # def apply(cls, *args):
    #     # TODO: the selection strategies for construct_paras
    #     if cls.SUBROUTINE_NAME is not None:
    #         return cls.apply_native(*args)
    #     return cls.apply_default(*args)

    # def __init__(self):
    #     self.subroutine_option = "auto"
