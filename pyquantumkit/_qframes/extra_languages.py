# _qframes/extra_languages.py
#    2025/7/25
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from .extra.qsharp import CODE as QSharp_CODE
from .extra.isq import CODE as isQ_CODE

Extra_Languages_CODE = {
    'QSharp' : QSharp_CODE, 'Q#' : QSharp_CODE,
    'isQ' : isQ_CODE,
}
