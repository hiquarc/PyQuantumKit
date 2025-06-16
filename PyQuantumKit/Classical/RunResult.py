# Classical/RunResult.py
#    2025/6/14
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

from .Common import *

def GetSubStringByIndexList(string : str, index_list : list[int], reverse : bool = False) -> str:
    ret = ''
    s = string[::-1] if reverse else string
    for index in index_list:
        ret += s[index]
    return ret


def CountSubsetOfResultDict(counts_dict : dict, bit_index_list : list[int], reverse : bool) -> dict:
    ret = {}
    for k in counts_dict:
        subk = GetSubStringByIndexList(k, bit_index_list, reverse)
        if subk in ret:
            ret[subk] += counts_dict[k]
        else:
            ret[subk] = counts_dict[k]
    return ret


def CountFirstBitsOfResultDict(counts_dict : dict, length : int, reverse : bool) -> dict:
    return CountSubsetOfResultDict(counts_dict, range(length), reverse)

def CountLastBitsOfResultDict(counts_dict : dict, length : int, reverse : bool) -> dict:
    return CountSubsetOfResultDict(counts_dict, range(length), not reverse)


def FirstResultStr(counts_dict : str, bit_index_list : list[int] = None, reverse : bool = False) -> str:
    if bit_index_list == None:
        return next(iter(counts_dict))
    temp = CountSubsetOfResultDict(counts_dict, bit_index_list, reverse)
    return next(iter(temp))
