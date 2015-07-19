# /usr/bin/env python
# -*- coding:utf-8 -*-
"""
同时找出一个列表中的最大和最小的值，算法实现的时候分别记录
了到当前的最大值和最小值。并且每次比较都对一对输入元素进行比较。
这样的比较次数是3次，也就是寻找最大和最小值的算法现在变成了3/2n。
平均下来是3/4n
"""


def find_min_max(li):
    li_len = len(li)
    if 1 < li_len < 2:
        return (li[0], li[0])

    if li[0] <= li[1]:
        li_min = li[0]
        li_max = li[1]
    else:
        li_min = li[1]
        li_max = li[0]

    start = 2
    # 处理奇数的情况
    if li_len / 2 is 1 and li_len >= 3:
        start += 1
        if li[3] < li_min:
            li_min = li[3]
        elif li[3] > li_max:
            li_max = li[3]

    for x in xrange(start, li_len, 2):
        # 默认first是小的
        first = li[x]
        second = li[x + 1]
        if first > second:
            first, second = second, first

        if first < li_min:
            li_min = first

        if second > li_max:
            li_max = second
    return (li_min, li_max)


def main():
    l = [2, 3, 4, 1, 7, 3, 8, 1100, 282828, 1, 20, 0]
    print find_min_max(l)


if __name__ == '__main__':
    main()
