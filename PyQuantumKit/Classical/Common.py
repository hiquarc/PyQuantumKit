# Classical/Common.py
#    2025/6/10
#    Author: Peixun Long
#    Computing Center, Institute of High Energy Physics, CAS

# Generate two different random int in range [a, b]
def randdiffintpair(a : int, b : int) -> tuple[int, int]:
    from random import randint
    num1 = randint(a, b)
    num2 = randint(a, b)
    while num1 == num2:
        num2 = randint(a, b)
    return (num1, num2)

# '0'/'1' string to int (little-endian mode)
def Binstr2intLE(binstr : str) -> int:
    return int(binstr[::-1], 2)

# '0'/'1' string to int (big-endian mode)
def Binstr2intBE(binstr : str) -> int:
    return int(binstr, 2)


# Given an index list, return the corresponding length of the index
def LengthOfIndexList(indexlist : list) -> int:
    if indexlist == None or len(indexlist) <= 0:
        return 0
    return max(indexlist) + 1


def ShiftIntbits(num : int, shiftindex : list[int]) -> int:
    ret = 0
    j = 0
    for i in shiftindex:
        curbit = 0 if (num & (1 << j)) == 0 else 1
        ret |= (curbit << i)
        j += 1
    return ret

def SubIntbits(num : int, subindex : list[int]) -> int:
    ret = 0
    j = 0
    for i in subindex:
        curbit = 0 if (num & (1 << i)) == 0 else 1
        ret |= (curbit << j)
        j += 1
    return ret

def FuseIntbits(a : int, b : int, a_index : list[int], b_index : list[int]) -> int:
    return ShiftIntbits(a, a_index) | ShiftIntbits(b, b_index)
