#!/usr/bin/env python
# -*- coding:UTF-8
__author__ = 'shenshijun'
"""
使用自下而上的方法实现的最长回文序列
"""


def lps(seq):
    value_dict = {}
    seq_len = len(seq)
    seq_dict = {}
    for i in xrange(seq_len):
        value_dict[(i, i)] = 1
        seq_dict[(i, i)] = "/"

    for j in xrange(seq_len):
        for i in reversed(xrange(j)):
            if seq[i] == seq[j]:
                # 注意：在对角线上的对称点必须按照0算，不能按照一算
                value_dict[(i, j)] = value_dict.get((i + 1, j - 1), 0) + 2
                seq_dict[(i, j)] = "/"
            else:
                value_dict[(i, j)] = max(value_dict[(i + 1, j)], value_dict[(i, j - 1)])
                seq_dict[(i, j)] = '|' if value_dict[(i + 1, j)] > value_dict[(i, j - 1)] else '-'
    return {
        "len": value_dict[(0, seq_len - 1)],
        "char": "".join(extra_lps(seq_dict, 0, seq_len - 1, seq).values())}


def extra_lps(seq, start, end, origin_list):
    cur_x = start
    cur_y = end
    result = {}
    while (cur_x, cur_y) in seq:
        if seq[(cur_x, cur_y)] == '/':
            result[cur_x] = origin_list[cur_x]
            result[cur_y] = origin_list[cur_y]
            cur_x += 1
            cur_y -= 1
        elif seq[cur_x, cur_y] == '-':
            cur_y -= 1
        else:
            cur_x += 1
    return result


def main():
    print lps('character')


if __name__ == "__main__":
    main()
