#!/usr/bin/env python
# -*- coding:UTF-8
"""
Given an array of integers, find two numbers such that they add up to a specific target number.
The function twoSum should return indices of the two numbers such that they add up to the target,
where index1 must be less than index2.Please note that your returned answers (both index1 and index2) are not zero-based.

You may assume that each input would have exactly one solution.

Input: numbers={2, 7, 11, 15}, target=9
Output: index1=1, index2=2
"""

__author__ = 'shenshijun'

"""
本题有两个思路:
一:  利用排序和二分查找
先排序得到一个排序的数列,复杂度是O(nlgn),然后遍历数列,每遍历到一个元素的时候使用二分查询查找另外一个数字是否存在,复杂度仍然是O(nlgn)

二: 使用hash表
思路一为了快速查找而把数据都排了序,为了查找,显然可以使用hash表.而hash表是更高效的实现.一遍完成,因此复杂度是O(n)
"""


class Solution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        d = {}
        for ind, num in enumerate(nums):
            # 为了防止列表中出现重复的数,并且保证列表前面的index比后面的index小
            if num in d:
                if type(d[num]) is list:
                    d[num].append(ind)
                else:
                    d[num] = [d[num], ind]
            else:
                d[num] = ind

        for num, ind in d.iteritems():
            # 注意:要同时考虑ind和d[other_part]都为list的情况
            # 还要考虑,找到的index不能是同一个,并且不能重复
            this_indexs = ind if type(ind) == list else [ind]
            other_part = target - num
            for this_index in this_indexs:
                if other_part in d:
                    if type(d[other_part]) == list:
                        for other_index in d[other_part]:
                            if other_index != this_index:
                                return [min(other_index, this_index) + 1, max(other_index, this_index) + 1]
                    elif d[other_part] != this_index:
                        return [min(d[other_part], this_index) + 1, max(d[other_part], this_index) + 1]

        return [-1, -1]


def main():
    print(Solution().twoSum([0, 4, 3, 0], 0))
    print(Solution().twoSum([2, 7, 11, 15], 9))
    print(Solution().twoSum([-3, 4, 3, 90], 0))


if __name__ == "__main__":
    main()
