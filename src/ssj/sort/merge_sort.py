#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
归并排序可以把sort和merge分离出来
"""


def main():
    l = [2, 3, 4, 1, 7, 3, 8, 1100, 282828, 1, 20, 0]
    len_l = len(l)
    print merge_sort(l[0:len_l / 2], l[len_l / 2:len_l])


def merge_sort(llist, rlist):
    llen = len(llist)
    rlen = len(rlist)
    # 递归结束时间：[]和[ele]
    if llen + rlen < 2:
        return llist + rlist
    lrst = merge_sort(llist[:llen / 2], llist[llen / 2:])
    rrst = merge_sort(rlist[:rlen / 2], rlist[rlen / 2:])
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


if __name__ == '__main__':
    main()
