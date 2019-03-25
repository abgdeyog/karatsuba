import math
import time
import random
import numpy as np


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


def convolution(g, f, base):
    len_g = len(g)
    len_f = len(f)
    min_len = min(len_g, len_f)
    res = [[0] for i in range(len_g + len_f)]
    for t in range(len_g + len_f):
        for j in range(min_len):
            if j < len_g and 0 <= t - j < len_f:
                res[t] = add(res[t], multiply(g[j], f[t - j], base), base)
    count = 0
    for i in range(len(res) - 1, -1, -1):
        if res[i] != [0]:
            count = i
            break
    return res[:count + 1]


def convolution_karatsuba(g, f, base):
    len_g = len(g)
    len_f = len(f)
    min_len = min(len_g, len_f)
    res = [[0] for i in range(len_g + len_f)]
    for t in range(len_g + len_f):
        for j in range(min_len):
            if j < len_g and 0 <= t - j < len_f:
                res[t] = add(res[t], multiply(g[j], f[t - j], base), base)
    count = 0
    for i in range(len(res) - 1, -1, -1):
        if res[i] != [0]:
            count = i
            break
    return res[:count + 1]


def generate_number(n_digits, base):
    test_number = [0] * n_digits
    for i in range(n_digits):
        test_number[i] = int(base * random.random())
        if test_number[i] == base:
            test_number[i] = base - 1
    return test_number


def arrint_to_int(arrint, base):
    res = 0
    for i in range(len(arrint)):
        res += arrint[i] * pow(base, i)
    return res


def arrsignal_to_intsignal(signal, base):
    res = [0] * len(signal)
    for i in range(len(signal)):
        res[i] = arrint_to_int(signal[i], base)
    return res


#
# signal_a = [19, 20, 21, 34, 65, 78]
# signal_a_arr = [[9, 1], [0, 2], [1, 2], [4, 3], [5, 6], [8, 7]]
# signal_b = [21, 456, 23, 94, 34, 3456]
# signal_b_arr = [[1, 2], [6, 5, 4], [3, 2], [4, 9], [4, 3], [6, 5, 4, 3]]
# conv_np = np.convolve(signal_a, signal_b)


def generate_signal(n_length, max_digits, base):
    signal = [[] for i in range(n_length)]
    for i in range(n_length):
        #length = int(max_digits/2 + random.random() * (max_digits/2))
        length = max_digits
        signal[i] = generate_number(length, base)
    return signal


params_ = [{"base": 2, "signal_length": 10, "maximum_number_length": 400} for i in range(100)]
time_results = []
for params in params_:
    base = params["base"]
    signal_a = generate_signal(params["signal_length"], params["maximum_number_length"], base)
    signal_b = generate_signal(params["signal_length"], params["maximum_number_length"], base)
    signal_a_ = arrsignal_to_intsignal(signal_a, base)

    common_multiplication_time_start = time.time()
    conv_my = convolution(signal_a, signal_b, base)
    common_multiplication_time_end = time.time()
    karatsuba_time_start = time.time()
    conv_karatsuba = convolution_karatsuba(signal_a, signal_b, base)
    karatsuba_time_end = time.time()

    conv_np = np.convolve(arrsignal_to_intsignal(signal_a, base), arrsignal_to_intsignal(signal_b, base))
    # print(conv_np)
    print(conv_my)
    print("multiplication_time = " + str(common_multiplication_time_end - common_multiplication_time_start))
    print(conv_karatsuba)
    print("karatsuba_time = " + str(karatsuba_time_end - karatsuba_time_start))
    time_results.append([karatsuba_time_end - karatsuba_time_start, common_multiplication_time_end - common_multiplication_time_start])
    # if not (len(conv_np) == len(conv_karatsuba) == len(conv_my)):
    #     print("convolution errors, wrong length")
    #     print("np conv = " + str(len(conv_np)))
    #     print("karatsuba conv = " + str(len(conv_karatsuba)))
    #     print("my conv = " + str(len(conv_my)))
    #     exit()
    for i in range(len(conv_my)):
        if not (arrint_to_int(conv_my[i], base) == arrint_to_int(conv_karatsuba[i], base) == conv_np[i]):
            print("convolution errors, different elements")
            exit()
    print("signals are the same")
avg_difference = 0
avg_karatsuba_time = 0
avg_ratio = 0
avg_multiplication_time = 0
for time in time_results:
    avg_difference += time[0] - time[1]
    avg_karatsuba_time += time[1]
    avg_multiplication_time += time[0]
    avg_ratio += time[0]/time[1]
avg_difference /= len(time_results)
avg_ratio /= len(time_results)
avg_karatsuba_time /= len(time_results)
avg_multiplication_time /= len(time_results)
print("avg karatsuba time = " + str(avg_karatsuba_time))
print("avg multiplication time = " + str(avg_multiplication_time))
print("avg ratio = " + str(avg_ratio))
print("avg difference = " + str(avg_difference))
exit()


n_length = 100000
base = 10
test_number_a = [0] * n_length
for i in range(n_length):
    test_number_a[i] = base * random.random()
    if (test_number_a[i] == base):
        test_number_a[i] = base - 1

test_number_b = [0] * n_length
for i in range(n_length):
    test_number_b[i] = base * random.random()
    if (test_number_b[i] == base):
        test_number_b[i] = base - 1

karatsuba_time_start = time.time()

karatsuba(test_number_a, test_number_b, base)

karatsuba_time_end = time.time()

print("karatsuba_time = " + str(karatsuba_time_end - karatsuba_time_start))

common_multiplication_time_start = time.time()

multiply(test_number_a, test_number_b, base)

common_multiplication_time_end = time.time()

print("multiplication_time = " + str(common_multiplication_time_end - common_multiplication_time_start))
