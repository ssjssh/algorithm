#!/usr/bin/env python
# -*- coding:UTF-8
__author__ = 'shenshijun'

"""
自底向上实现LCS
"""


# 使用字典保存子问题的结果
def lcs(list_x, list_y):
    __len_dict = {}
    __ele_dict = {}
    end_x = len(list_x) - 1
    end_y = len(list_y) - 1
    result = __lcs(list_x, list_y, end_x, end_y, __len_dict, __ele_dict)
    return {
        'length': result,
        'lcs': extra_lcs(__ele_dict, list_x, end_x, end_y)
    }


def extra_lcs(ele_dict, list_x, end_x, end_y):
    lcs_list = []
    index_x = end_x
    index_y = end_y
    while True:
        cur_direct = ele_dict[(index_x, index_y)]
        if cur_direct == '\\':
            lcs_list.append(list_x[index_x])
            index_x -= 1
            index_y -= 1
        elif cur_direct == '|':
            index_x -= 1
        else:
            index_y -= 1
        if index_x < 0 or index_y < 0:
            break
    return reversed(lcs_list)


def __lcs(list_x, list_y, end_x, end_y, __len_dict, __ele_dict):
    # 插入-1是为了在后面计算的时候可以不用判断边界情况
    for y in xrange(-1, end_y + 1):
        __len_dict[(-1, y)] = 0

    for x in xrange(-1, end_x + 1):
        __len_dict[(x, -1)] = 0
    for x in xrange(0, end_x + 1):
        for y in xrange(0, end_y + 1):
            if list_x[x] == list_y[y]:
                __len_dict[(x, y)] = 1 + __len_dict[(x - 1, y - 1)]
                __ele_dict[(x, y)] = "\\"
            elif __len_dict[(x - 1, y)] >= __len_dict[(x, y - 1)]:
                __len_dict[(x, y)] = __len_dict[(x - 1, y)]
                __ele_dict[(x, y)] = '|'
            else:
                __len_dict[(x, y)] = __len_dict[(x, y - 1)]
                __ele_dict[(x, y)] = '-'
    return __len_dict[(end_x, end_y)]


def main():
    list_x = ['A', 'B', 'C', 'B', 'D', 'A', 'B']
    list_y = ['B', 'D', 'C', 'A', 'B', 'A']
    result_dict = lcs(list_x, list_y)
    print result_dict['length']
    for char in result_dict['lcs']:
        print char


if __name__ == "__main__":
    main()
