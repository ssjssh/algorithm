#!/usr/bin/env python
# -*- coding:UTF-8
__author__ = 'shenshijun'

"""
Given a string, find the length of the longest substring without repeating characters. For example, the longest substring without repeating letters for "abcabcbb" is "abc", which the length is 3. For "bbbbb" the longest substring is "b", with the length of 1.
"""

"""
思路:使用两个指针来遍历字符串,他们之间的字符是不重复的字符.前面的指针每次前进一步都会判断新扫描的字符是不是和两个指针的间的字符重复
s a f b r g r e g
  ^       ^
  |       |index
start_index
为了这个目的,使用了哈希表.
如果重复,那么就找到一个连续的非重复字符串,这里就是afbrg(index现在在r的位置),判断这个字符串长度和已有的最大长度的大小,
并且记录下最大值.发生重复之后的处理非常重要,是把前面重复的部分丢弃掉,这样后面的字符串还是一个非重复的字符串(start_index在g的位置)
这样的目的是尽量构建一个长的非重复字符串

如果没有重复,那么就把字符和对应的索引放入哈希表,以备后面使用

如果限定了字符集,那么可以使用数组来模拟哈希表,这样的效率更高.
"""


class Solution(object):
    def lengthOfLongestSubstring(self, s):
        """
        :type s: str
        :rtype: int
        """
        if not s:
            return 0
        tmp_dict = {}
        # 字符串不为空,因此最小值是1
        max_length = 1
        start_index = 0
        for index, ch in enumerate(s):
            if ch in tmp_dict:
                if max_length < index - start_index:
                    max_length = index - start_index
                dup_index = tmp_dict[ch]
                for i in range(start_index, dup_index + 1):
                    del tmp_dict[s[i]]
                start_index = dup_index + 1
            tmp_dict[ch] = index
        # 注意结束的时候如果没有重复,那么会安静退出循环而不发生任何比较,所以在退出循环的时候要比较
        return len(tmp_dict) if len(tmp_dict) > max_length else max_length


def main():
    print(Solution().lengthOfLongestSubstring("bbbbbb"))  # 1
    print(Solution().lengthOfLongestSubstring("abcabcbb"))  # 3
    print(Solution().lengthOfLongestSubstring("dvdfefqwfqwef"))  # 3


if __name__ == "__main__":
    main()
