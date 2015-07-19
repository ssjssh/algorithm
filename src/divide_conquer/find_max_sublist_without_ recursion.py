#!/usr/bin/env python 
# -*-coding:utf-8 -*-
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
