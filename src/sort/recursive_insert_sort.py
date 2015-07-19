#!/usr/bin/env python 
# -coding:utf-8 -*-
"""
这里面虽然使用了两个变量来存储列表，但是其他他们引用的都是同一个列表对象。
这样的程序在每一个递归函数中重新声明一个列表存储数据的时候逻辑也是正确的。
只是由于递归每次都需要声明一个列表，这样需要更多的内存。
具体是1+2+3...+n=n*(n+1)/2
"""


def recursive_insert_sort(li):
    li_len = len(li)
    if li_len < 2:
        return li
    first = li[0]  # 取出第一个元素
    sorted_li = recursive_insert_sort(li[1:])  # 默认从小到大
    for x in xrange(0, li_len - 1):
        if first > sorted_li[x]:
            li[x] = sorted_li[x]
        else:
            # 由于Python列表切片的规则，这个地方不用判断列表的索引是不是
            # 超过了列表的大小，因为如果在切片中超出列表大小，返回的是一个
            # 空列表
            li[x] = first
            li[x + 1:] = sorted_li[x:]
            break
    """
    有两个退出方式，如果是break，那么根据执行的语句可知一定有li[x]<=li[x+1]，因此可以根据这个条件来判断
    是不是因为for循环执行完了。
    """
    if li[x] >= li[x + 1]:
        li[x + 1] = first
        li[x + 2:] = sorted_li[x + 1:]
    return li


def main():
    print recursive_insert_sort([3, 1, 2, 4, 5, 0, 1, 2])


if __name__ == '__main__':
    main()
