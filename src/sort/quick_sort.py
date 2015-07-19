#!/usr/bin/env python 
# -*- coding:utf-8 -*-

def partition(li, start, end):
    li_len = end - start + 1
    if li_len < 2:
        raise ValueError("list which lenght is less then 2 do not need to partition")
    # 使用最后一个元素作为分割点
    key = li[end]
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


def main():
    l = [2, 3, 4, 1, 7, 3, 8, 1100, 282828, 1, 20, 0]
    li = sort(l, 0, len(l) - 1)
    print li


if __name__ == '__main__':
    main()
