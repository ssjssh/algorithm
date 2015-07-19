#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
假设列表是按照从小到大排序的，在函数中就不需要再去判断列表的排序情况了。
算法的最好条件是要查询的数据在列表中间:O(1)
最坏条件是在左右两边，但是由于while在这个时候执行了lgn次，因此最坏的算法
复杂度是O(lgn)
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
            index += (list_len - index) / 2
        if temp == index:
            break
    if value != sorted_list[index]:
        return None
    else:
        return index


def main():
    print binary_search([1, 2, 3, 5, 6, 7, 101010, 1928394, 10299283, 28282829338474], 1928394)


if __name__ == '__main__':
    main()
