#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
实现一个带哨兵的双向循环链表。一个哨兵是一个空对象，在双向链表实现中简化了改变链接的时候需要判断None的情况。
实现这个链表的过程时刻记得更新插入和删除节点的前后节点的指针
"""
from __builtin__ import object


class LinkedList(object):
    class Node(object):
        """docstring for LinkedList.Node"""

        def __init__(self, key, prev, next):
            super(LinkedList.Node, self).__init__()
            self.key = key
            self.prev = prev
            self.next = next

        def __str__(self):
            return "".join([str(self.key), "-->"])

    def __init__(self, *arg):
        super(LinkedList, self).__init__()
        self.__nil = LinkedList.Node(None, None, None)
        self.__nil.prev = self.__nil
        self.__nil.next = self.__nil
        self.__length = 0
        for key in arg:
            self.append(key)

    def insert(self, index, value):
        if index > self.__length:
            raise IndexError("can not insert beyond the list")
        cur_pos = 0
        cur_node = self.__nil
        while cur_pos < index:
            cur_node = cur_node.next
            cur_pos += 1
        prev_node = cur_node.prev
        node = LinkedList.Node(value, prev_node, cur_node)
        cur_node.prev = node
        prev_node.next = node
        self.__length += 1
        return node

    def append(self, value):
        last_node = self.__nil.prev
        node = LinkedList.Node(value, last_node, self.__nil)
        # 现在结尾的节点指向新加的结尾点
        last_node.next = node
        self.__nil.prev = node
        self.__length += 1
        # 处理空链表的情况
        if self.__nil.next is self.__nil:
            self.__nil.next = node
        return node

    def prepend(self, value):
        node = LinkedList.Node(value, self.__nil, self.__nil.next)
        self.__nil.next = node
        self.__nil.next.prev = node
        # 处理空链表的情况
        if self.__nil.prev is self.__nil:
            self.__nil.prev = node
        self.__length += 1
        return node

    def search(self, value):
        cur_node = self.__nil.next
        while cur_node is not self.__nil and cur_node.key != value:
            cur_node = cur_node.next
        return cur_node.key

    def delete(self, value):
        cur_node = self.__nil.next
        while cur_node is not self.__nil and cur_node.key != value:
            cur_node = cur_node.next
        # 如果不是空链表，那么就是查找到了相应的元素
        if cur_node is not self.__nil:
            cur_node.prev.next = cur_node.next
            cur_node.next.prev = cur_node.prev

        return cur_node.key

    def __len__(self):
        return self.__length

    def __str__(self):
        cur_node = self.__nil.next
        li = []
        while cur_node is not self.__nil:
            li.append(str(cur_node))
            cur_node = cur_node.next
        return "".join(li)


def main():
    li = LinkedList(20, 40, 5050, 495, 39948)
    print "li: ", li
    print li.search(5050)
    li.delete(5050)
    print li
    li = LinkedList()
    for x in xrange(1, 10):
        li.insert(0, x)
    print li


if __name__ == '__main__':
    main()
