import math
import time
import random


def multiply(a, b, base):
    len_a = len(a)
    len_b = len(b)
    res = [0] * (len_a + len_b)
    for b_i in range(0, len_b):
        carry = 0
        for a_i in range(0, len_a):
            res[b_i + a_i] += carry + a[a_i] * b[b_i]
            carry = int(res[a_i + b_i] / base)
            res[a_i + b_i] = res[a_i + b_i] % base
        res[b_i + len_a] += carry
    offset = 0
    for i in range(len_b + len_a - 1, -1, -1):
        if res[i] != 0:
            offset = i
            break
    return res[0:offset + 1]


def karatsuba(a, b, base):
    len_a = len(a)
    len_b = len(b)

    if (len_a <= 1) or (len_b <= 1):
        return multiply(a, b, base)

    m = min(len_a, len_b)
    m2 = math.floor(m / 2)
    low1 = a[0:m2]
    high1 = a[m2:]
    low2 = b[0:m2]
    high2 = b[m2:]
    bd = karatsuba(low1, low2, base)
    abcd = karatsuba(add(low1, high1, base), add(low2, high2, base), base)
    ac = karatsuba(high1, high2, base)
    sub = subtract(subtract(abcd, bd, base), ac, base)
    res = add(add([0] * (m2 * 2) + ac, bd, base), [0] * m2 + sub, base)
    count = 0
    for i in range(len(res) - 1, -1, -1):
        if res[i] != 0:
            count = i
            break
    return res[0:count + 1]


def add(a, b, base):
    len_a = len(a)
    len_b = len(b)
    max_len = max(len_a, len_b)
    carry = 0
    res = []
    for i in range(max_len + 1):
        if (i < len_b) and (i < len_a):
            sum = a[i] + b[i] + carry
            res.append(sum % base)
            carry = int(sum / base)
        elif i < len_b:
            sum = b[i] + carry
            res.append(sum % base)
            carry = int(sum / base)
        elif i < len_a:
            sum = a[i] + carry
            res.append(sum % base)
            carry = int(sum / base)
        elif carry != 0:
            sum = carry
            res.append(sum % base)
            carry = int(sum / base)
    count = 0
    for i in range(len(res) - 1, -1, -1):
        if res[i] != 0:
            count = i
            break
    return res[0:count + 1]


def subtract(a, b, base):
    len_a = len(a)
    len_b = len(b)
    max_len = max(len_a, len_b)
    carry = 0
    res = []
    for i in range(max_len + 1):
        if (i < len_b) and (i < len_a):
            sum = a[i] - b[i] + carry
            res.append(sum % base)
            carry = int((sum - base + 1) / base)
        elif i < len_b:
            sum = -b[i] + carry
            res.append(sum % base)
            carry = int((sum - base + 1) / base)
        elif i < len_a:
            sum = a[i] + carry
            res.append(sum % base)
            carry = int((sum - base + 1) / base)
        elif carry != 0:
            sum = carry
            res.append(sum % base)
            carry = int((sum - base + 1) / base)
    count = 0
    for i in range(len(res) - 1, -1, -1):
        if res[i] != 0:
            count = i
            break
    return res[0:count + 1]


def compare(a, b):
    len_a = len(a)
    len_b = len(b)
    if (len_a > len_b):
        return 1
    elif len_b > len_a:
        return -1
    for i in range(len_a - 1, -1, -1):
        if a[i] > b[i]:
            return 1
        elif a[i] < b[i]:
            return -1
    return 0


#
# print(multiply([6, 7, 8], [6, 9], 10))
# print(subtract([0, 0, 0, 1], [9], 10))
# print(multiply([6, 7, 8], [6, 9], 10))
# print(karatsuba([6, 7, 8], [6, 9], 10))
# print(add([2, 4], [3, 9, 8], 10))
# print(subtract([3, 9, 8], [2, 4], 10))
# print(compare([2, 6], [2, 6]))
n_length = 100000
base = 10
test_number_a = [0]*n_length
for i in range(n_length):
    test_number_a[i] = base * random.random()
    if(test_number_a[i] == base):
        test_number_a[i] = base - 1


test_number_b = [0]*n_length
for i in range(n_length):
    test_number_b[i] = base * random.random()
    if(test_number_b[i] == base):
        test_number_b[i] = base - 1

karatsuba_time_start = time.time()

karatsuba(test_number_a, test_number_b, base)

karatsuba_time_end = time.time()

print("karatsuba_time = " + str(karatsuba_time_end - karatsuba_time_start))

common_multiplication_time_start = time.time()

multiply(test_number_a, test_number_b, base)

common_multiplication_time_end = time.time()

print("multiplication_time = " + str(common_multiplication_time_end - common_multiplication_time_start))
