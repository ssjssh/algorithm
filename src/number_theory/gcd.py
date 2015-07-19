#!/usr/bin/env python
# -*- coding:UTF-8
__author__ = 'shenshijun'


def gcd(a, b):
    divisor = a
    dividend = b
    while dividend is not 0:
        divisor, dividend = dividend, divisor % dividend
    return divisor


def main():
    print(gcd(12, 18))


if __name__ == "__main__":
    main()
