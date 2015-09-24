#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from random import randint


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
    for x in xrange(start, end + 1):
        if li[x] < key:
            li[middle_index], li[x] = li[x], li[middle_index]
            middle_index += 1
    li[end], li[middle_index] = li[middle_index], li[end]
    return middle_index


"""
 可以预先对k做一些检查，但是这儿就不检查了
"""


def selection(li, start, end, kth):
    # 一定会找到一个元素，因此这儿直接返回是对的。
    if start == end:
        return li[start]
    mid_index = partition(li, start, end)
    midth = mid_index - start
    if midth == kth:
        return li[mid_index]
    elif midth > kth:
        return selection(li, start, mid_index - 1, kth)
    elif midth < kth:
        """
        这儿后面必须减去1，这是因为mth和kth都是从0开始计算的
        """
        return selection(li, mid_index + 1, end, kth - midth - 1)


def main():
    l = [2, 3, 4, 1, 7, 3, 8, 1100, 282828, 1, 20, 0]
    print selection(l, 0, len(l) - 1, 10)


if __name__ == '__main__':
    main()
