# classical/common.py
#    2025/6/10
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

def rand_diff_int_pair(a : int, b : int) -> tuple[int, int]:
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


def dim2nbits(dimension : int) -> tuple[int, bool]:
    """
    Given the dimension d, calculate the corresponding number of bits
    -> Return : (k, True), if d == 2 ^ k
                (ceil(log_2(d)), False), otherwise

        e.g. 2 -> (1, True)
             8 -> (3, True)
             64 -> (6, True)
             62 -> (6, False)
    """
    if dimension < 1:
        return (0, False)
    k = 0
    while 2 ** k <= dimension:
        if 2 ** k == dimension:
            return (k, True)
        k += 1
    return (k, False)
        
def contain_duplicates(tarlist : list) -> bool:
    """
    Return whether there are duplicated elements in a list

        e.g. [1, 2, 3, 4] -> False
             [1, 2, 2, 3] -> True
             ['a', 7, '1', 1] -> False
             ['a', 7, '1', '1'] -> True
    """
    return len(tarlist) != len(set(tarlist))

def remap_bits(num : int, remaplist : list[int]) -> int:
    """
    Given a positive integer, remap its bits according to <remaplist>

        num       : (int) the integer number
        remaplist : (list[int]) the list to identify the remap
                NOTE: the lowest bit is indexed as 0

        e.g. 78 = 1001110b
        remap_bits(78, [6, 5, 4, 3, 2, 1, 0]) = 0111001b = 57
        remap_bits(78, [0, 1, 2, 4, 5, 6, 7]) = 10010110b = 150
        remap_bits(78, [0, 2, 4, 6, 8, 10, 12]) = 1000001010100b = 4180
    """
    ret = 0
    j = 0
    for i in remaplist:
        curbit = 0 if (num & (1 << j)) == 0 else 1
        ret |= (curbit << i)
        j += 1
    return ret

def sub_bits(num : int, subindex : list[int]) -> int:
    """
    Return the integer about the subindexes of a given integer

        num      : (int) the integer number
        subindex : (list[int]) the list to indentify the subindexes
                NOTE: the lowest bit is indexed as 0

        e.g. 78 = 1001110b
        sub_bits(78, [0, 1, 3]) = 110b = 6
        sub_bits(78, [2, 4, 5]) = 001b = 1
        sub_bits(78, [0, 2, 4, 6, 8]) = 01010b = 10
    """
    ret = 0
    j = 0
    for i in subindex:
        curbit = 0 if (num & (1 << i)) == 0 else 1
        ret |= (curbit << j)
        j += 1
    return ret

def reverse_endianness(num : int, nbits : int) -> int:
    """
    Reverse the endianness of the binary bits

        num   : (int) the target integer to be reversed
        nbits : (int) the total number of bits

    -> Return : the reversed integer

        e.g. 78 = 01001110b
        reverse_endianness(78, 7) = 0111001b = 57
        reverse_endianness(78, 8) = 01110010b = 114
    """    
    return remap_bits(num, list(range(nbits - 1, -1, -1)))

