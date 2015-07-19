#!/usr/bin/env python
# -*- coding:UTF-8
__author__ = 'shenshijun'
"""
自上而下实现最长回文子序列问题，即从一个字符串中求出一个子序列，其内容是回文，而且保证长度是最长的。
注意：并不要求子序列是连续的。
"""
__value_dict = {}
__seq_dict = {}


def lps(seq, start, end):
    global __value_dict
    global __seq_dict
    if (start, end) in __value_dict:
        return __value_dict[(start, end)]
    if start == end:
        result = 1
        __seq_dict[(start, end)] = "/"
    elif start > end:
        return 0
    elif seq[start] == seq[end]:
        result = lps(seq, start + 1, end - 1) + 2
        __seq_dict[(start, end)] = "/"
    else:
        left = lps(seq, start + 1, end)
        right = lps(seq, start, end - 1)
        result = max(left, right)
        __seq_dict[(start, end)] = "-" if right >= left else "|"
    __value_dict[(start, end)] = result
    return result


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
    char_list = "character"
    print lps(char_list, 0, len(char_list) - 1)
    print extra_lps(__seq_dict, 0, len(char_list) - 1, char_list)


if __name__ == "__main__":
    main()
