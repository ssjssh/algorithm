#!/usr/bin/env python
# -*- coding:UTF-8
__author__ = 'shenshijun'


def match(origin, pattern):
    origin_index, pattern_index = 0, 0
    match_flag = True
    pattern_len = len(pattern)
    while origin_index < len(origin):
        for pattern_index in xrange(pattern_len):
            if pattern[pattern_index] != origin[origin_index]:
                origin_index -= (pattern_index - 1)
                match_flag = False
                break
            else:
                origin_index += 1
                pattern_index += 1
                match_flag = True

        if match_flag:
            return origin_index - pattern_index


def main():
    print match("absabsvbshsbdhhd", 'sb')


if __name__ == "__main__":
    main()
