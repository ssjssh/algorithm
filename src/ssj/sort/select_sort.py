#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
如果按照算法描述，这里容易犯一个错误，认为可以使用查询到的最小值替换列表中的元素。
其实不是替换，而是把列表要替换的元素和找到的最小值交换。否则会出项系统中的一些值
被最小值覆盖掉的问题
"""


def select_sort(li):
    li_len = len(li)
    for x in xrange(0, li_len - 1):
        index = x
        temp = li[index]
        for y in xrange(x + 1, li_len):
            if temp > li[y]:
                temp = li[y]
                index = y
        li[x], li[index] = li[index], li[x]
    return li


def main():
    print select_sort([2, 1, 3, 4, 5, 6, 19, 0])


if __name__ == '__main__':
    main()
