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
        return start
    mid_index = partition(li, start, end)
    midth = mid_index - start
    if midth == kth:
        return mid_index
    elif midth > kth:
        return selection(li, start, mid_index - 1, kth)
    elif midth < kth:
        """
        这儿后面必须减去1，这是因为mth和kth都是从0开始计算的
        """
        return selection(li, mid_index + 1, end, kth - midth - 1)


class Node(object):
    """docstring for Node"""

    def __init__(self, _value, _weight):
        super(Node, self).__init__()
        self.value = _value
        self.weight = _weight

    def __cmp__(self, other):
        return cmp(self.value, other.value)

    def __str__(self):
        return "".join(["Node : value", str(self.value), ", weight:", str(self.weight)])


def find_weighted(li, start, end, left_weight, right_weight):
    if start == end:
        return li[start]
    middle_index = selection(li, start, end, (end - start) / 2)
    right_weight_sum = 0
    for x in xrange(middle_index + 1, end + 1):
        right_weight_sum += li[x].weight

    left_weight_sum = 0
    for x in xrange(start, middle_index):
        left_weight_sum += li[x].weight

    if right_weight_sum <= right_weight and left_weight_sum < left_weight:
        return li[middle_index]
    elif right_weight_sum > right_weight:
        return find_weighted(li, middle_index + 1, end,
                             left_weight - left_weight_sum - li[middle_index].weight, right_weight)
    elif left_weight_sum > left_weight:
        return find_weighted(li, start, middle_index - 1, left_weight,
                             right_weight - right_weight_sum - li[middle_index].weight)


def main():
    li = [Node(0.35, 0.35), Node(0.1, 0.1), Node(0.05, 0.05), Node(0.1, 0.1), Node(0.15, 0.15), Node(0.05, 0.05),
          Node(0.2, 0.2)]
    print find_weighted(li, 0, len(li) - 1, 0.5, 0.5)


if __name__ == '__main__':
    main()
