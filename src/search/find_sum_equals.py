#!/usr/bin/env python 
# -*- coding:utf-8 -*-
"""
从列表中查询出两个元素的和，他们的和正好等于要查询的一个值。
算法的思路是：1，使用一个O(nlgn)的算法首先对数据排序。2，对于列表中的每一个数据求出和要查询的数据的差值并在列表中查(可以使用二分查询)。这样总体的复杂度就是O(nlgn)
"""


def binary_search(sorted_list, value):
    list_len = len(sorted_list)
    index = list_len / 2
    """
    temp是这个循环的退出条件，非常重要。while里面的条件会在找到数据的时候退出。
    而temp的条件则是在查找不到数据的时候退出，推出的条件其实就是头尾。
    还有要注意的是其实二分分割的具体位置不重要，因为分割的位置其实是一个趋近的过程。
    """
    while value != sorted_list[index]:
        temp = index
        if value < sorted_list[index]:
            index /= 2
        else:
            index = index + (list_len - index) / 2
        if temp == index:
            break
    if value != sorted_list[index]:
        return None
    else:
        return index


def __merge_sort__(llist, rlist):
    llen = len(llist)
    rlen = len(rlist)
    # 递归结束时间：[]和[ele]
    if llen + rlen < 2:
        return llist + rlist
    lrst = __merge_sort__(llist[:llen / 2], llist[llen / 2:])
    rrst = __merge_sort__(rlist[:rlen / 2], rlist[rlen / 2:])
    lcursor, rcursor = 0, 0
    result = []
    min_len = min(llen, rlen)
    # 从小到大排序
    while lcursor < llen and rcursor < rlen:
        if lrst[lcursor] < rrst[rcursor]:
            result.append(lrst[lcursor])
            lcursor += 1
        else:
            result.append(rrst[rcursor])
            rcursor += 1
    # 把没有合并的数据合并起来。
    result.extend(lrst[lcursor:])
    result.extend(rrst[rcursor:])
    return result


def merge_sort(l):
    len_l = len(l)
    return __merge_sort__(l[0:len_l / 2], l[len_l / 2:len_l])


def find_equal_sum(li, value):
    li_len = len(li)
    sorted_list = merge_sort(li)
    half_list = sorted_list[li_len / 2:]
    for x in half_list:
        other_part = value - x
        result = binary_search(sorted_list, other_part)
        if result is not None:
            yield (x, other_part)


def main():
    for x, y in find_equal_sum([1, 2, 10, 9], 11):
        print "find a pair:(%s,%s)" % (x, y)


if __name__ == '__main__':
    main()
