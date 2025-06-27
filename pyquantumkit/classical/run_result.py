# Classical/RunResult.py
#    2025/6/14
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

def get_substr_by_indexlist(string : str, index_list : list[int], reverse : bool = False) -> str:
    """
    Get the substring according to an index list

        e.g. string = 'abcdef'
             index_list = [0,2,3]
             reverse = False
          -> 'acd'

        e.g. string = 'abcdef'
             index_list = [0,2,3]
             reverse = True
          -> 'fdc'
    """
    ret = ''
    s = string[::-1] if reverse else string
    for index in index_list:
        ret += s[index]
    return ret


def count_subset_of_result_dict(counts_dict : dict, bit_index_list : list[int], reverse : bool = False) -> dict:
    """
    Count the number from a subset of result dict

        e.g. counts_dict = {'00' : 5, '01' : 6, '10' : 7, '11' : 8}
             bit_index_list = [0]
             reverse = False
          -> {'0' : 11, '1' : 15}

        e.g. counts_dict = {'00' : 5, '01' : 6, '10' : 7, '11' : 8}
             bit_index_list = [1]
             reverse = False
          -> {'0' : 12, '1' : 14}
    """
    if not bit_index_list:
        return {}
    ret = {}
    for k in counts_dict:
        subk = get_substr_by_indexlist(k, bit_index_list, reverse)
        if subk in ret:
            ret[subk] += counts_dict[k]
        else:
            ret[subk] = counts_dict[k]
    return ret


def count_first_bits_of_result_dict(counts_dict : dict, index_length : int, reverse : bool = False) -> dict:
    """
    Count the number from the first several bits of result dict

        e.g. counts_dict = {'000' : 5, '010' : 6, '100' : 7, '110' : 8}
             index_length = 2
             reverse = False
          -> {'00' : 5, '01' : 6, '10' : 7, '11' : 8}
    """
    return count_subset_of_result_dict(counts_dict, range(index_length), reverse)

def count_last_bits_of_result_dict(counts_dict : dict, index_length : int, reverse : bool = False) -> dict:
    """
    Count the number from the last several bits of result dict

        e.g. counts_dict = {'000' : 5, '010' : 6, '100' : 7, '110' : 8}
             index_length = 2
             reverse = False
          -> {'00' : 12, '10' : 14}
    """
    return count_subset_of_result_dict(counts_dict, range(index_length)[::-1], not reverse)


def get_result_str_set(counts_dict : dict, reverse : bool = False) -> set:
    """
    Get the keys list of counts dict (i.e., existing results)

        e.g. counts_dict = {'000' : 5, '010' : 6, '100' : 7, '110' : 8}
            reverse = False
        -> {'000', '010', '100', '110'}

        {} -> {}
        None -> {}
    """
    if not counts_dict:
        return {}
    ret = set(counts_dict.keys())
    if reverse:
        ret = {s[::-1] for s in ret}
    return ret


# def get_first_result_str(counts_dict : dict, bit_index_list : list[int] = None, reverse : bool = False) -> str:
#     """
#     Count the number from the last several bits of result dict
#     """
#     if bit_index_list is None:
#         return next(iter(counts_dict))
#     temp = count_subset_of_result_dict(counts_dict, bit_index_list, reverse)
#     return next(iter(temp))
