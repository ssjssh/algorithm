#!/usr/bin/env python 
# -*- coding:utf-8 -*-

def power(x, n):
    if n is 1:
        return x
    elif n is 0:
        return 1
    if n % 2 is 0:
        return power(x ** x, n / 2)
    else:
        return power(x ** x, (n - 1) / 2) * x


def main():
    print power(1000, 1)


if __name__ == '__main__':
    main()
