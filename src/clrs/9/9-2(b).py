#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from random import randint

"""
算法的思想是首先排序，然后从一端开始累加，在遇到使得结果值大于等于0.5的值的权的时候就把这个元素返回。
由于带权中位数偏向于大端，所以从大端开始累加。
证明算法的正确性：首先在返回结果的时候肯定在小的一端满足结果。这个时候可以证明在上一次的时候必定有累加
值小于0.5，否则就返回了。
"""


def partition(li, start, end):
    li_len = end - start + 1
    if li_len < 2:
        raise ValueError("list which lenght is less then 2 do not need to partition")
    # 使用随机元素元素作为分割点并且把随机元素放在列表最后
    # 这样就可以不变动原来的逻辑了
    key_index = randint(start, end)
    key = li[key_index]
    li[key_index], li[end] = li[end], li[key_index]
    middle_index = start
    for x in xrange(start, end):
        if li[x] < key:
            li[middle_index], li[x] = li[x], li[middle_index]
            middle_index += 1
    li[end], li[middle_index] = li[middle_index], li[end]
    return middle_index


def sort(li, start, end):
    li_len = end - start + 1
    if li_len < 2:
        return li
    middle_index = partition(li, start, end)
    sort(li, start, middle_index - 1)
    sort(li, middle_index + 1, end)
    return li


def find_weight_middle(li):
    li_len = len(li)
    sorted_list = sort(li, 0, li_len - 1)
    weight_sum = 0
    for x in reversed(xrange(0, li_len)):
        weight_sum += li[x]
        if weight_sum > 0.5:
            return li[x]
        elif weight_sum == 0.5:
            return li[x - 1]


def main():
    l = [0.1, 0.35, 0.05, 0.1, 0.15, 0.05, 0.2]
    print find_weight_middle(l)
    print sort(l, 0, len(l) - 1)


if __name__ == '__main__':
    main()
