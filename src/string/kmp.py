#!/usr/bin/env python
# -*- coding:UTF-8
__author__ = 'shenshijun'


def match(origin, pattern):
    origin_len = len(origin)
    pattern_len = len(pattern)

    def build_next():
        _next_list = [0 for x in xrange(pattern_len)]
        last_match = 0
        for cur_index in xrange(1, pattern_len):
            while last_match > 0 and pattern[last_match] != pattern[cur_index]:
                last_match = _next_list[last_match]
            if pattern[last_match] == pattern[cur_index]:
                last_match += 1
            _next_list[cur_index] = last_match
        return _next_list

    origin_index, pattern_index = 0, 0
    next_list = build_next()
    while origin_index < origin_len:
        # while需要放在前面，如果放在后面的话且有匹配的情况下pattern[pattern_index]就会越界
        while pattern_index > 0 and origin[origin_index] != pattern[pattern_index]:
            pattern_index = next_list[pattern_index]
        if pattern[pattern_index] == origin[origin_index]:
            pattern_index += 1
        origin_index += 1

        if pattern_index == pattern_len:
            return origin_index - pattern_len


def main():
    print match("assssbsss", 'sb')


if __name__ == "__main__":
    main()
