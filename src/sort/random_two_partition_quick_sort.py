#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
把列表分成三个部分，中间的部分是相等的部分。
"""


def partition(li, start, end):
    key = li[start]
    m_start, m_end, i = start, start, start
    for j in xrange(start, end + 1):
        cur_ele = li[j]
        if cur_ele == key:
            li[j], li[m_end] = li[m_end], li[j]
            m_end += 1
        elif cur_ele < key:
            li[m_end], li[j] = li[j], li[m_end]
            li[m_end], li[m_start] = li[m_start], li[m_end]
            m_start += 1
            m_end += 1
    return m_start, m_end


def sort(li, start, end):
    if end - start < 2:
        return li
    m_start, m_end = partition(li, start, end)
    sort(li, start, m_start - 1)
    sort(li, m_end, end)
    return li


def main():
    li = [7, 4, 8, 7, 4, 5, 7, 7, 8, 9, 11, 12, 7, 19, 21]
    print sort(li, 0, 14)


if __name__ == '__main__':
    main()
