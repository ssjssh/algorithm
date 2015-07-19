#!/usr/bin/env python 
# -*- coding:utf-8 -*-
"""
从小到大的排序
"""


def bubble_sort(li):
    li_len = len(li)
    for x in xrange(0, li_len - 1):
        big_value = li[x]
        index = x
        for y in xrange(x + 1, li_len):
            if big_value >= li[y]:
                big_value = li[y]
                index = y
        li[x], li[index] = li[index], li[x]
    return li


def main():
    print bubble_sort([2, 1, 3, 0, 3837, 1, 33, 464])


if __name__ == '__main__':
    main()
