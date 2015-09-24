#!/usr/bin/env python
# -*- coding:UTF-8
__author__ = 'shenshijun'

"""
带备忘的自顶向下动态规划实现的斐波那契数列，算法的性能是O(n)
"""

__dict = {1: 1, 2: 1}


def fabo(n):
    global __dict
    if n in __dict:
        return __dict[n]
    else:
        result = fabo(n - 1) + fabo(n - 2)
        __dict[n] = result
        return result


def main():
    print fabo(8)


if __name__ == "__main__":
    main()
