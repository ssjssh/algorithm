#!/usr/bin/env python
# -*- coding:UTF-8
__author__ = 'shenshijun'
"""
There are two sorted arrays nums1 and nums2 of size m and n respectively. Find the median of the two sorted arrays. The overall run time complexity should be O(log (m+n)).
"""
"""
思路一:遍历一遍就可以把两个数组排序,然后取中点的值就可以了,这样的复杂度是O(m+n)
思路二:排序显然做了许多无用功,因为只需要一个中间数就可以了
参考:http://www.cnblogs.com/lichen782/p/leetcode_Median_of_Two_Sorted_Arrays.html
可以分成四种情况考虑
1,两个列表都没有数据,那么返回0
2,两个列表中只有一个列表有数据,那么返回其中一个列表的中间点
3,两个列表中的一个列表整体大于另一个列表,那么可以在逻辑上把这两个列表合并起来求出合并后的中点
4,问题可以简化成从两个排序列表中求出第k个数,也就是从两个数组的开头取出k个数字,这k个数字比留在数组中的数字要小
那么可以开始从两个数组中取出k/2的数字(这样做每次可以把问题的规模减小一半,整体的复杂度也就是指数级的),
比较k/2位置处数字的大小,小的那一部分一定是在k小的数字之内(可以假设法证明),这样剩下的问题就是从剩下的列表中找
第k/2位数了.等到这个数为1,那么就好计算了.

"""


class Solution(object):
    def findMedianSortedArrays(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: float
        """
        if not nums1:
            return self.__findMedian(nums2)
        elif not nums2:
            return self.__findMedian(nums1)
        elif not nums1 and not nums2:
            return 0

        len1 = len(nums1)
        len2 = len(nums2)

        if (len1 + len2) % 2 is 0:
            return (self.__findKth((len1 + len2) / 2 + 1, nums1, nums2) + self.__findKth((len1 + len2) / 2, nums1,
                                                                                         nums2)) / 2.0
        else:
            return self.__findKth((len1 + len2) / 2 + 1, nums1, nums2)

    @staticmethod
    def __findMedian(li):
        median = len(li) / 2
        if len(li) % 2 is 0:
            return (li[median] + li[median - 1]) / 2.0
        else:
            return li[median]

    @staticmethod
    def __findKth(k, l1, l2):
        l1_start = 0
        l2_start = 0
        k -= 1
        while (len(l1) + len(l2) - l1_start - l2_start - 1) >= k:
            if k is 0:
                return min(l1[l1_start], l2[l2_start])
            if len(l1) - l1_start < len(l2) - l2_start:
                l1_comp_start = l1_start + min(len(l1), k / 2)
                l2_comp_start = k - min(len(l1), k / 2) + l2_start
            else:
                l2_comp_start = min(len(l2), k / 2) + l2_start
                l1_comp_start = k - min(len(l2), k / 2) + l1_start

            if l1[l1_comp_start] > l2[l2_comp_start]:
                k -= (l2_comp_start - l2_start)
                l2_start = l2_comp_start + 1
            elif l1[l1_comp_start] < l2[l2_comp_start]:
                k -= (l1_comp_start - l1_start)
                l1_start = l1_comp_start + 1
            else:
                return l1[l1_comp_start]
        return 0


def main():
    print(Solution().findMedianSortedArrays([0, 1, 2, 3, 4], [0, 1, 2]))  # 1
    print(Solution().findMedianSortedArrays([], [1]))  #


if __name__ == "__main__":
    main()
