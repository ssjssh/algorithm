#!/usr/bin/env python 
# -*-coding:utf-8 -*-
def main():
    print reverse_insert_sort([2, 13, 4, 1919, 1, 1100, 1, 2, 3, 373737, 0])


# 从小到大排序
def insert_sort(li):
    list_len = len(li)
    if list_len < 2:
        return li
    for x in xrange(1, list_len):
        cursor = li[x]
        # 算法不是从头开始比较的，而是从Cursor的上一个元素比较的，否则必须使用多个循环。
        for y in reversed(xrange(0, x)):
            if cursor < li[y]:  # 一个重要的细节：如果两个元素相等，那么它们的顺序不会变
                # 忽略了一个边界条件cursor=1,而li[0]=2的时候，需要li[0]=cursor
                li[y + 1], li[y] = li[y], cursor
            else:
                li[y + 1] = cursor
                break
    return li


def reverse_insert_sort(li):
    list_len = len(li)
    if list_len < 2:
        return li
    for x in xrange(1, list_len):
        cursor = li[x]
        # 算法不是从头开始比较的，而是从Cursor的上一个元素比较的，负责必须使用多个循环。
        for y in reversed(xrange(0, x)):
            if cursor > li[y]:  # 一个重要的细节：如果两个元素相等，那么它们的顺序不会变
                # 忽略了一个边界条件cursor=1,而li[0]=2的时候，需要li[0]=cursor
                li[y + 1], li[y] = li[y], cursor
            else:
                li[y + 1] = cursor
                break
    return li


if __name__ == '__main__':
    main()
