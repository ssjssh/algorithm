#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from random import randint


def partition(li, start, end):
    li_len = end - start + 1
    if li_len < 2:
        raise ValueError("list which lenght is less then 2 do not need to partition")
    # 使用随机元素元素作为分割点并且把随机元素放在列表最后
    # 这样就可以不变动原来的逻辑了
    key_index = randint(start, end)
    key = li[key_index]
    li[key_index], li[end] = li[end], li[key_index]
    middle_index = start
    for x in xrange(start, end + 1):
        if li[x] < key:
            li[middle_index], li[x] = li[x], li[middle_index]
            middle_index += 1
    li[end], li[middle_index] = li[middle_index], li[end]
    return middle_index


"""
 可以预先对k做一些检查，但是这儿就不检查了
"""


def selection(li, start, end, kth):
    # 一定会找到一个元素，因此这儿直接返回是对的。
    if start == end:
        return start
    mid_index = partition(li, start, end)
    midth = mid_index - start
    if midth == kth:
        return mid_index
    elif midth > kth:
        return selection(li, start, mid_index - 1, kth)
    elif midth < kth:
        """
        这儿后面必须减去1，这是因为mth和kth都是从0开始计算的
        """
        return selection(li, mid_index + 1, end, kth - midth - 1)


"""
算法比较简单，假设n/k是一个整数。实际上亦可以考虑在不够的时候添加一些元素保证整除。
在k是偶数的时候比较好处理，因为只要从中间分开就可以了。
在k是奇数的时候需要从中间向左向右取出两个点，因为只要从中间分开就可以了。
"""


def split_even_nth(li, start, end, k, kth_list):
    if k is 1:
        return kth_list
    if k % 2 is 1:
        return split_odd_nth(li, start, end, k, kth_list)
    middle_index = selection(li, start, end, (end - start - 1) / 2)  # 必须要减一，分割的点是中间元素的前一个
    print "start:%s,end:%s,mid_index:%s" % (start, end, middle_index)
    kth_list.append(li[middle_index])
    split_even_nth(li, start, middle_index, k / 2, kth_list)
    split_even_nth(li, middle_index + 1, end, k / 2, kth_list)
    return kth_list


def split_odd_nth(li, start, end, k, kth_list):
    if k is 1:
        return kth_list
    if k % 2 is 0:
        return split_even_nth(li, start, end, k, kth_list)
    n = end - start + 1
    min_ele_count = n / k
    middle_pos = (start + end) / 2
    if min_ele_count % 2 is 0:
        left_pos = middle_pos - min_ele_count / 2 + 1
    else:
        left_pos = middle_post - min_ele_count / 2
    left_middle_index = selection(li, start, end, left_pos)
    right_middle_index = selection(li, left_middle_index, end, min_ele_count)
    kth_list.append(li[left_middle_index], li[right_middle_index])
    split_odd_nth(li, start, left_middle_index, k / 2, kth_list)
    split_odd_nth(li, right_middle_index, end, k / 2, kth_list)
    return kth_list


def main():
    l = [2, 3, 4, 1, 7, 3, 8, 1100, 282828, 1, 20, 0, 2, 2, 3, 4]
    print split_even_nth(l, 0, len(l) - 1, 4, [])
    print l


if __name__ == '__main__':
    main()
