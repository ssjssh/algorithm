#!/usr/bin/env python
# -*- coding:UTF-8
__author__ = 'shenshijun'
"""
Given a string S, find the longest palindromic substring in S. You may assume that the maximum length of S is 1000, and there exists one unique longest palindromic substring.

我的解法就是这个解法：http://taop.marchtea.com/01.05.html
感谢
"""


class Solution(object):
    def longestPalindrome(self, original):
        """
        :type s: str
        :rtype: str
        """
        if not original:
            return 0
        s = self.__preProcess(original)
        longest_right_bound = 0
        longest_median = 0
        pali_list = [1 for i in range(len(s))]
        # 注意迭代位置，为了不出现越界，最前和最后的字符串是不会被遍历的
        for i in range(1, len(s) - 1):
            # 这边使用的是对称的原理，使得可以快速个p[i]一个基础的值
            if longest_right_bound > i:
                if longest_right_bound - i <= pali_list[2 * longest_median - i]:
                    pali_list[i] = longest_right_bound - i
                else:
                    pali_list[i] = pali_list[2 * longest_median - i]
            # 在字符串的最前面和最后面都必须加上一个特殊字符，用于防止越界
            # 另一个方法是在每次循环的时候都判断边界，但是效率比直接加特殊字符低
            while s[i + pali_list[i]] == s[i - pali_list[i]]:
                pali_list[i] += 1
            if pali_list[i] >= longest_right_bound - longest_median:
                longest_right_bound = pali_list[i] + i
                longest_median = i
        return self.__clearString(s[2 * longest_median - longest_right_bound + 1:longest_right_bound])

    def __clearString(self, sub_str):
        return "".join([ch for ch in sub_str if ch != '#'])

    def __preProcess(self, s):
        str_list = ['#{}'.format(ele) for ele in s]
        str_list.append("#$")
        str_list.insert(0, '^')
        return "".join(str_list)


def main():
    print(Solution().longestPalindrome("bbbbbb"))  # 6
    print(Solution().longestPalindrome("fqwefqwefqwadccdaafwfawef"))  # 6
    print(Solution().longestPalindrome("qwefqwefqsjsjsssgsssjsjsg3q4gekwSKDFKALJKFIUWIUEFWEG"))  # 15
    print(Solution().longestPalindrome("ababababa"))  # 10


if __name__ == "__main__":
    main()
