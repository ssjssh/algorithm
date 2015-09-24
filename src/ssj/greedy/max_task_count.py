#!/usr/bin/env python
# -*- coding:UTF-8
__author__ = 'shenshijun'
"""
贪心选择实现的最大活动个数算法
"""


def max_task_count(start_list, end_list):
    if len(start_list) != len(end_list):
        raise IndexError()
    # 因为Action是按照结束时间来排序的，所以第一个肯定是符合条件的
    task_set = [(start_list[0], end_list[0])]
    # 表示下一个要比较的位置
    for x in xrange(1, len(start_list)):
        if start_list[x] >= task_set[-1][1]:
            task_set.append((start_list[x], end_list[x]))
    return task_set


def main():
    task_start_list = [1, 3, 0, 5, 3, 5, 6, 8, 8, 2, 12]
    task_end_list = [4, 5, 6, 7, 9, 9, 10, 11, 12, 14, 16]
    print max_task_count(task_start_list, task_end_list)


if __name__ == "__main__":
    main()
