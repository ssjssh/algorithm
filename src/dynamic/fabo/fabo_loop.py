#!/usr/bin/env python 
# -*- coding:utf-8 -*-
"""
使用循环实现的斐波那契数列其实就是自底向上方式实现的动态规划
"""


def loop_fibonacci(n):
    this = 0
    next = 1
    result = this + next
    if n is 1:
        return this
    elif n is 2:
        return next
    elif n is 3:
        return result
    else:
        for x in xrange(1, n - 2):
            result, next, this = next + result, result, next
        return result


def main():
    print loop_fibonacci(8)


if __name__ == '__main__':
    main()
