#!/usr/bin/env python 
# -*-coding:utf-8 -*-

"""
复杂度是O(N),因为只需要遍历一遍数组就可以了
"""

"""
思想：采取打擂台的方法，也就是把最大值时刻放在擂台上和别的和比较。
同样的方法我用来解决leecode的问题中的https://leetcode.com/problems/longest-palindromic-substring/
采用打擂台的方法解决的问题有同样的特点就是：他们都要求连续，只要要求连续才能保证算法的正确性。

对于本题的算法正确性，可以使用递归法来证明：
基本情况：不用证明。
"""


def find_max_sublist(li):
    b, max_sum, left, right = 0, 0, 0, 0
    li_len = len(li)
    for x in xrange(0, li_len):
        if b < 0:
            b = li[x]
            left = x
        else:
            b += li[x]
        if max_sum < b:
            right = x
            max_sum = b

    return left, right, max_sum


def main():
    print find_max_sublist([1, -2, 3, 10, -4, 7, 2, -5])


if __name__ == '__main__':
    main()
