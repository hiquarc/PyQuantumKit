# Classical/RunResult.py
#    2025/6/14
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

def get_substr_by_indexlist(string : str, index_list : list[int], reverse : bool = False) -> str:
    """
    Get the substring according to an index list
    """
    ret = ''
    s = string[::-1] if reverse else string
    for index in index_list:
        ret += s[index]
    return ret


def count_subset_of_result_dict(counts_dict : dict, bit_index_list : list[int], reverse : bool) -> dict:
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
    ret = {}
    for k in counts_dict:
        subk = get_substr_by_indexlist(k, bit_index_list, reverse)
        if subk in ret:
            ret[subk] += counts_dict[k]
        else:
            ret[subk] = counts_dict[k]
    return ret


def count_first_bits_of_result_dict(counts_dict : dict, length : int, reverse : bool) -> dict:
    """
    Count the number from the first several bits of result dict

        e.g. counts_dict = {'000' : 5, '010' : 6, '100' : 7, '110' : 8}
             bit_index_list = 2
             reverse = False
          -> {'00' : 5, '01' : 6, '10' : 7, '11' : 8}
    """
    return count_subset_of_result_dict(counts_dict, range(length), reverse)

def count_last_bits_of_result_dict(counts_dict : dict, length : int, reverse : bool) -> dict:
    """
    Count the number from the last several bits of result dict

        e.g. counts_dict = {'000' : 5, '010' : 6, '100' : 7, '110' : 8}
             bit_index_list = 2
             reverse = False
          -> {'00' : 12, '10' : 14}
    """
    return count_subset_of_result_dict(counts_dict, range(length), not reverse)


def get_first_result_str(counts_dict : str, bit_index_list : list[int] = None, reverse : bool = False) -> str:
    """
    Count the number from the last several bits of result dict
    """
    if bit_index_list is None:
        return next(iter(counts_dict))
    temp = count_subset_of_result_dict(counts_dict, bit_index_list, reverse)
    return next(iter(temp))
