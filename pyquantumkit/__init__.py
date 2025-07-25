# __init__.py
#    2025/6/10
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

__version__ = '0.1.2'

import sys
import os
import importlib as IL

# Dict to record supported quantum frameworks
Supported_Frameworks = {}
# Dict to record namespace of each quantum frameworks
Framework_Namespace = {}

def get_framework_from_type(t : type) -> str:
    modstr = t.__module__
    if modstr.find('pyquantumkit') != -1:
        return 'pyquantumkit'
    for fname in Supported_Frameworks:
        if modstr.find(fname) != -1:
            return fname
    return ''

def get_framework_from_object(obj) -> str:
    return get_framework_from_type(type(obj))

def FN(fm_name : str, index : int = 0):
    return Framework_Namespace[fm_name][index]

# the error type for unsupported error
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

    # Initialize the namespace of imported frameworks
    for fname in Supported_Frameworks:
        if fname in sys.modules:
            namespace_items = []
            for fn_item in Supported_Frameworks[fname]:
                if fn_item in sys.modules:
                    namespace_items.append(IL.import_module(fn_item))
            Framework_Namespace[fname] = namespace_items

pyquantumkit_init()

# default imported modules
from .procedure.generic import *
from .procedure.circuit_io import CircuitIO
