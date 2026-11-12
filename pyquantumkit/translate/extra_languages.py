# translate/extra_languages.py
#    2025/7/25
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

import importlib
from .common import FrameworkMapError

EXTRA_STR = "pyquantumkit.translate.extra."
LANGUAGES = [("OpenQASM2.0", "openqasm2"),
             ("Q#", "qsharp"),
             ("isQ", "isq"),
             ]
ELEMENTS = ["EXPORT_CONSTANTS",
            "IMPORT",
            "DECLARE",
            "APPLY",
            "SUPPORT_SUBROUTINES",
            ]

def collect_builtin_languages(module_names : list[str], elements : list[str]):
    return {
        name[0] : [getattr(importlib.import_module(EXTRA_STR + name[1]), var, None) for var in elements]
                for name in module_names
    }

Support_Languages = collect_builtin_languages(
    LANGUAGES,
    ELEMENTS
)

def load_language_element(language : str, element_index : int):
    try:
        return Support_Languages[language][element_index]
    except KeyError:
        raise FrameworkMapError(f"Unsupported language: {language}")
    
def extra_language_CONSTANTS(language : str) -> dict[str]:
    return load_language_element(language, 0)

def extra_language_IMPORT(language : str) -> callable:
    return load_language_element(language, 1)

def extra_language_DECLARE(language : str) -> callable:
    return load_language_element(language, 2)

def extra_language_APPLY(language : str) -> callable:
    return load_language_element(language, 3)

def extra_languate_SUBROUTINES(language : str) -> dict[str]:
    return load_language_element(language, 4)
