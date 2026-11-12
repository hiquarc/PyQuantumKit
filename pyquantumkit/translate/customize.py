# translate/customize.py
#    2026/8/11
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

import sys
import importlib, importlib.metadata
from pyquantumkit import Supported_Frameworks, Framework_Namespace, Framework_Version
from .framework_map import Translate_Namespace
from .extra_languages import Support_Languages, ELEMENTS

def update_framework_translation(framework_name : str, translate_rule_file : str, import_packages : list[str]) -> None:
    """
    Add an extra Python's framework and corresponding translate rules

        framework_name  : the name of framework.
                          If name is native supported or has been added, the translation rule will be replaced.
        import_packages : (list[str]) the packages need to be imported.
        translate_rule_file : the Python file (.py) to describe the translation rule
    """
    namespace_items = {}
    for fn_item in import_packages:
        if fn_item in sys.modules:
            namespace_items[fn_item] = importlib.import_module(fn_item)
    Framework_Namespace[framework_name] = namespace_items
    Framework_Version[framework_name] = importlib.metadata.version(framework_name)
    Translate_Namespace[framework_name] = importlib.import_module(translate_rule_file)
    


def update_language_translation(language_name : str, translate_rule_file : str) -> None:
    """
    Add or update a translation rule for an extra quantum language

        language_name       : the name of language.
                              If name is native supported or has been added, the translation rule will be replaced.
        translate_rule_file : the Python file (.py) to describe the translation rule
    """
    imp = {
        language_name : [getattr(importlib.import_module(translate_rule_file), var, None) for var in ELEMENTS]
    }
    Support_Languages.update(imp)
