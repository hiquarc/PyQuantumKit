#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

import unittest as UT
from .common import *
from pyquantumkit import *
from pyquantumkit.classical.run_result import *
from pyquantumkit.classical.common import *
from pyquantumkit.procedure.generic import *
from pyquantumkit.procedure.qft import *


class Test_procedure_qft(UT.TestCase):
    """
    Test cases for subpackage "procedure/qft"
    """
    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
        self._fm = ''
        self._qvm = None
    def setUp(self):
        self.skipTest('Do not test base class')
