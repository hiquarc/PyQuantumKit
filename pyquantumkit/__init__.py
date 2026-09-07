# __init__.py
#    2025/6/10
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

__version__ = '0.2.0b'

import sys
import os
import importlib, importlib.metadata

# Dict to record supported quantum frameworks
Supported_Frameworks = {}
# Dict to record namespace of each quantum frameworks
Framework_Namespace = {}
# Dict to record the version of each quantum frameworks
Framework_Version = {}

def get_framework_from_type(t : type) -> str:
    modstr = t.__module__
    if modstr.find('pyquantumkit') != -1:
        return 'pyquantumkit'
    for lib_name in Supported_Frameworks:
        for module_name in Supported_Frameworks[lib_name]:
            if modstr.find(module_name) != -1:
                return lib_name
        if modstr.find(lib_name) != -1:
            return lib_name
    return ''

def get_framework_from_object(obj) -> str:
    return get_framework_from_type(type(obj))

def framework_modules(fm_name : str, index : int = 0):
    return Framework_Namespace[fm_name][index]
def framework_version(fm_name : str):
    return Framework_Version[fm_name]

# the error type in PyQuantumKit
class PyQuantumKitError(Exception):
    pass

def pyquantumkit_init():
    # Load and initialize supported quantum frameworks
    current_dir = os.path.dirname(os.path.abspath(__file__))
    fname = os.path.join(current_dir, 'init_frame.txt')
    with open(fname, 'r') as f:
        for line in f:
            sharpindex = line.find('#')
            s = line if sharpindex == -1 else line[:sharpindex]
            if s.strip():
                rawlist = s.split()
                Supported_Frameworks[rawlist[0]] = rawlist[1:] if len(rawlist) > 1 else []

    # Initialize the namespace and version of imported frameworks
    for lib_name in Supported_Frameworks:
        namespace_items = []
        for fn_item in Supported_Frameworks[lib_name]:
            if fn_item in sys.modules:
                namespace_items.append(importlib.import_module(fn_item))
        Framework_Namespace[lib_name] = namespace_items
        if namespace_items:
            Framework_Version[lib_name] = importlib.metadata.version(lib_name)

pyquantumkit_init()

# default imported modules
from .procedure.generic import *
from .procedure.circuit_io import CircuitIO
from .program_build.builder import QProgramBuilder
from ._qframes.user_define import add_extra_framework
from ._qframes.code_translate import get_standard_gatename
