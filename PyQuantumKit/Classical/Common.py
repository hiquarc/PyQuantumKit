# classical/common.py
#    2025/6/10
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

def randdiffintpair(a : int, b : int) -> tuple[int, int]:
    """
    Generate two different random int in range [a, b]
    """
    from random import randint
    num1 = randint(a, b)
    num2 = randint(a, b)
    while num1 == num2:
        num2 = randint(a, b)
    return (num1, num2)


def get_int_from_binstr_le(binstr : str) -> int:
    """
    '0'/'1' string to int (little-endian mode)

        e.g. '10110' -> 13 (01101b)
    """
    return int(binstr[::-1], 2)

def get_int_from_binstr_be(binstr : str) -> int:
    """
    '0'/'1' string to int (big-endian mode)

        e.g. '10110' -> 22 (10110b)
    """
    return int(binstr, 2)


def indexlist_length(indexlist : list) -> int:
    """
    Given an index list, return the corresponding length of the index

        e.g. None -> 0
             [] -> 0
             [0, 1, 2, 3] -> 4
             [0, 2, 4, 7] -> 8 (the max index is 7, so the length is 8)
    """
    if indexlist is None or len(indexlist) <= 0:
        return 0
    return max(indexlist) + 1


def shift_int_bits(num : int, shiftindex : list[int]) -> int:
    ret = 0
    j = 0
    for i in shiftindex:
        curbit = 0 if (num & (1 << j)) == 0 else 1
        ret |= (curbit << i)
        j += 1
    return ret

def sub_int_bits(num : int, subindex : list[int]) -> int:
    ret = 0
    j = 0
    for i in subindex:
        curbit = 0 if (num & (1 << i)) == 0 else 1
        ret |= (curbit << j)
        j += 1
    return ret

def fuse_int_bits(a : int, b : int, a_index : list[int], b_index : list[int]) -> int:
    return shift_int_bits(a, a_index) | shift_int_bits(b, b_index)
