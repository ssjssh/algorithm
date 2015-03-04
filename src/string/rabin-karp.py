#!/usr/bin/env python
# -*- coding:UTF-8
__author__ = 'shenshijun'
"""
首先计算pattern字符串的hash值，然后在从目标字符串的开头，计算相同长度字符串的hash值。若hash值相同，则表示匹配，若不同，则向右移动一位，计算新的hash值。整个过程，与暴力的字符串匹配算法很相似，
但由于计算hash值时，可以利用上一次的hash值，从而使新的hash值只需要加上新字母的计算，并减去上一次的第一个字母的计算，即可。
Rabin-Karp算法的预处理时间为O(m)，最坏情况下该算法的匹配时间为O((n-m+1)m)，期望复杂度O(m+n)
"""


def match(origin, pattern):
    pattern_len = len(pattern)

    def _hash(string, start=0):
        hash_code = 0
        for x in xrange(pattern_len):
            hash_code += ord(string[start + x]) * 2 ** (pattern_len - x - 1)
        return hash_code

    def _refresh(old_hash, old_char, new_char):
        return (old_hash - ord(old_char) * 2 ** (pattern_len - 1)) * 2 + ord(new_char)

    def test_equal(start_index):
        for x in xrange(pattern_len):
            if origin[x + start_index] != pattern[x]:
                return False
        return True

    origin_index = 0
    pattern_hash = _hash(pattern)
    origin_hash = _hash(origin)
    while origin_index < len(origin) - pattern_len - 1:
        if pattern_hash == origin_hash and test_equal(origin_index):
            return origin_index
        else:
            print "origin hash:%s,pattern hash:%s" % (origin_hash, pattern_hash)
            origin_hash = _refresh(origin_hash, origin[origin_index], origin[origin_index + pattern_len])
            origin_index += 1


def main():
    print match("sbsfsdgdgfgasbssssfsfdfeferf", 'sb')


if __name__ == "__main__":
    main()
