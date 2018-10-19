# -*- coding: utf-8 -*-

import random
import time

def insertionsort(data):
    # 插入排序
    for i in range(0, len(data)):
        data_i = data[i]
        j = i - 1
        while j >= 0 and data_i < data[j]:
            data[j + 1] = data[j]
            data[j] = data_i
            j -= 1
    return

def quicksort(data, low, high):
    # 快速排序
    if high - low < 2:
        return
    p = partition(data, low, high)
    quicksort(data, low, p)
    quicksort(data, p + 1, high)
    return

def partition(data, low, high):
    # 快速排序划分
    i = random.randint(low, high - 1)
    temp = data[i]
    data[i] = data[high - 1]
    data[high - 1] = temp
    i = low - 1
    x = data[high - 1]
    for j in range(low, high - 1):
        if data[j] <= x:
            i += 1
            temp = data[i]
            data[i] = data[j]
            data[j] = temp
    temp = data[i + 1]
    data[i + 1] = data[high - 1]
    data[high - 1] = temp
    return i + 1

def radixsort(data, digit):
    # 基数排序，digit为数字位数，进行d轮排序
    for k in range(digit):
        s = [[] for i in range(10)]  # 因为每一位数字都是0~9，故建立10个桶

        for i in data:
            t = round(i // (10 ** k) % 10)
            s[t].append(i)
        data = [j for i in s for j in i]
    return data

def shellsort(data):
    # 希尔排序,gap取较优的Hibbard增量
    gap = 1
    while gap < len(data) / 3:
        gap = gap * 3 + 1

    while gap > 0:
        for i in range(gap, len(data)):
            data_i = data[i]
            j = i - gap
            while j >= 0 and data_i < data[j]:
                data[j + gap] = data[j]
                data[j] = data_i
                j -= gap
        gap = int(round(gap / 3))
    return data

def mergesort(data, left, right):
    # 归并排序
    mid = int(round((left + right) / 2))
    if right - left > 1:
        mergesort(data, left, mid)
        mergesort(data, mid, right)
    else:
        return
    mergelist(data, left, right)
    return data

def mergelist(data, left, right):
    # 归并排序合并
    mid = int(round((left + right) / 2))
    temp = []
    i = left
    j = mid
    while (i < mid and j < right):
        if data[i] <= data[j]:
            temp.append(data[i])
            i = i + 1
        else:
            temp.append(data[j])
            j = j + 1
    if i < mid:
        for cur in range(i, mid):
            temp.append(data[cur])
    if j < right:
        for cur in range(j, right):
            temp.append(data[cur])
    for k in range(left, right):
        data[k] = temp[k - left]
    return

if __name__ == '__main__':
    for iter in range(1, 9):
        if iter == 9:
            length = 2 * 10 ** (iter-1)
        else:
            length = 10 ** iter
        print('*******************************')
        print('num of data:{}'.format(length))

        MAX = 2 ** 32 - 1

        test_data = []
        for i in range(length):
            test_data.append(random.randint(0, MAX))
        start = time.clock()
        quicksort(test_data, 0, len(test_data))
        end = time.clock()
        print('quicksort: {}'.format(end - start))

        test_data = []
        for i in range(length):
            test_data.append(random.randint(0, MAX))
        start = time.clock()
        shellsort(test_data)
        end = time.clock()
        print('shellsort: {}'.format(end - start))

        test_data = []
        for i in range(length):
            test_data.append(random.randint(0, MAX))
        start = time.clock()
        mergesort(test_data, 0, len(test_data))
        end = time.clock()
        print('mergesort: {}'.format(end - start))

        test_data = []
        for i in range(length):
            test_data.append(random.randint(0, MAX))
        start = time.clock()
        radixsort(test_data,iter)
        end = time.clock()
        print('radixsort: {}'.format(end - start))

        if iter <= 5:
            test_data = []
            for i in range(length):
                test_data.append(random.randint(0, MAX))
            start = time.clock()
            insertionsort(test_data)
            end = time.clock()
            print('insertionsort: {}'.format(end - start))
