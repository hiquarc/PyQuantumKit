# __init__.py
#    2025/6/10
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

__version__ = '0.1.0'

import sys
import importlib as IL

# Add names of supported framework here
#   key   = name of framework
#   value = import string of framework
Supported_Frameworks = {
    'pyqpanda3' : 'pyqpanda3.core',
    'qiskit'    : 'qiskit',
}
Framework_Namespace = {}

def get_framework_from_type(t : type) -> str:
    modstr = t.__module__
    for fname in Supported_Frameworks:
        if fname in modstr:
            return fname
    return ''

def get_framework_from_object(obj) -> str:
    return get_framework_from_type(type(obj))

# the error type for unsupported error
class PyQuantumKitError(Exception):
    pass

def pyquantumkit_init():
    for fname in Supported_Frameworks:
        if fname in sys.modules:
            # Initialize the namespace of imported frameworks
            Framework_Namespace[fname] = IL.import_module(Supported_Frameworks[fname])


pyquantumkit_init()
