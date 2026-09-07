# _qframes/user_define.py
#    2026/8/11
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

import sys
import importlib, importlib.metadata
from pyquantumkit import Supported_Frameworks, Framework_Namespace, Framework_Version
from .framework_map import Translate_Namespace

def add_extra_framework(framework_name : str, import_packages : list[str],
                        translate_rule_file : str):
    """
    Add an extra framework and corresponding translate rules

        framework_name  : (str) the name of framework.
                         if name is native supported or has been added, nothing will happen.
        import_packages : (list[str]) the packages need to be imported.
        translate_rule_file : (str) a .py file to specify the translation rule.
    """
    if framework_name in Supported_Frameworks:
        return
    
    namespace_items = []
    for fn_item in import_packages:
        if fn_item in sys.modules:
            namespace_items.append(importlib.import_module(fn_item))
    Framework_Namespace[framework_name] = namespace_items
    Framework_Version[framework_name] = importlib.metadata.version(framework_name)

    Translate_Namespace[framework_name] = importlib.import_module(translate_rule_file)
