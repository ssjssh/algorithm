#!/usr/bin/env python 
# -*-  coding:utf-8 -*-

"""
最大子数组只有可能有三个地方出现：
1，左半部分内。
2，右半部分内。
3，跨越了左右半部分。这个时候只要从中点开始分别在左右找最大子数组就可以了。
边界条件是：列表中的元素只有一个的时候
"""


def find_max_sublist(li):
    li_len = len(li)
    if li_len < 2:
        return (0, 0, sum(li))
    middle = li_len / 2
    m_x, m_y, m_sum = find_max_in_middle(li, middle)
    l_x, l_y, l_sum = find_max_sublist(li[:middle])
    r_x, r_y, r_sum = find_max_sublist(li[middle + 1:])
    if m_sum >= l_sum and m_sum >= r_sum:
        return (m_x, m_y, m_sum)
    elif l_sum >= m_sum and l_sum >= r_sum:
        return (l_x, l_y, l_sum)
    else:
        return (r_x, r_y, r_sum)


"""
思想：如果以中点开始，分别计算左右两边的最大子数列，那么他们的合并
也是最大的（除去某些边结果为负数的情况）
优化：
和插入排序类似的思想就是从从中点开始分别向左向右累计求和
这样的好处是：在累计求和的过程中就可以寻找最大值。
而不是先累计求和再求最大值，这样需要额外的循环
"""


def find_max_in_middle(li, middle):
    li_len = len(li)
    left_max_index, right_max_index = 0, middle
    # 这里有一个bug，如果列表里面所有的数据都是负的，那么就找不到最小值了
    left_max_sum, cur_sum, right_max_sum = li[middle - 1], 0, li[middle]
    for x in reversed(xrange(0, middle)):
        cur_sum += li[x]
        if cur_sum > left_max_sum:
            left_max_sum = cur_sum
            left_max_index = x
    cur_sum = 0
    for x in xrange(middle, li_len):
        cur_sum += li[x]
        if cur_sum > right_max_sum:
            right_max_sum = cur_sum
            right_max_index = x
    # 这里并没有判断一端结果为负的情况，因为这个时候可以在其中一端的列表中得到最大子数列
    return (left_max_index, right_max_index, right_max_sum + left_max_sum)


def main():
    print find_max_sublist([0])


if __name__ == '__main__':
    main()
