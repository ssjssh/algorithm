#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
实现一个带哨兵的双向循环链表。一个哨兵是一个空对象
在双向链表实现中简化了改变链接的时候需要判断None的情况。
实现这个链表的过程时刻记得更新插入和删除节点的前后节点的指针
"""
from __builtin__ import object


class LinkedList(object):
    class Node(object):
        """docstring for LinkedList.Node"""

        def __init__(self, value, prev, next_node):
            super(LinkedList.Node, self).__init__()
            self.value = value
            self.prev = prev
            self.next_node = next_node

        def __str__(self):
            return str(self.value)

    def __init__(self, *arg):
        """
        创建一个链表
        :param arg: 可变参数,是列表的初始元素
        :return:
        """
        super(LinkedList, self).__init__()
        # dump对象的prev指针始终指向列表的尾巴
        # 而列表的最后一个元素的next指针则始终指向列表开头,整个列表就是一个环
        self.__dump = LinkedList.Node(None, None, None)
        self.__dump.prev = self.__dump
        self.__dump.next_node = self.__dump
        self.__length = 0
        for value in arg:
            self.append(value)

    def insert(self, index, value):
        """
        在列表的中间插入一个元素
        :param index: 要插入的位置
        :param value: 要插入的值
        :return: 插入值之后列表的大小
        """
        if index > self.__length:
            raise IndexError("can not insert beyond the list")

        cur_pos = 0
        cur_node = self.__dump
        while cur_pos < index:
            cur_node = cur_node.next_node
            cur_pos += 1

        prev_node = cur_node.prev
        node = LinkedList.Node(value, prev_node, cur_node)
        cur_node.prev = node
        prev_node.next_node = node
        self.__length += 1
        return self.__length

    def append(self, value):
        """
        在列表的结尾插入一个元素
        :param value:要插入的元素
        :return: 插入之后列表的大小
        """
        last_node = self.__dump.prev
        node = LinkedList.Node(value, last_node, self.__dump)
        # 现在结尾的节点指向新加的结尾点
        last_node.next_node = node
        self.__dump.prev = node
        self.__length += 1
        return self.__length

    def prepend(self, value):
        """
        在列表的最前面插入一个值
        :param value: 要插入的元素
        :return: 插入之后列表的大小
        """
        node = LinkedList.Node(value, self.__dump, self.__dump.next_node)
        self.__dump.next_node.prev = node
        self.__dump.next_node = node
        self.__length += 1
        return self.__length

    def search(self, value):
        """
        寻找一个元素是否存在于列表中
        :param value: 要寻找的元素
        :return: 如果没有,返回None;如果有,则返回找到的值
        """
        cur_node = self.__dump.next_node
        while cur_node is not self.__dump and cur_node.value != value:
            cur_node = cur_node.next_node
        return cur_node.value

    def delete(self, value):
        """
        删除一个值
        :param value: 要删除的元素
        :return: 被删除的值
        """
        cur_node = self.__dump.next_node
        while cur_node is not self.__dump and cur_node.value != value:
            cur_node = cur_node.next_node

        # 如果不是空链表，那么就是查找到了相应的元素
        if cur_node is not self.__dump:
            cur_node.prev.next_node = cur_node.next_node
            cur_node.next_node.prev = cur_node.prev
            self.__length -= 1

        return cur_node.value

    def __len__(self):
        return self.__length

    def __str__(self):
        cur_node = self.__dump.next_node
        li = []
        while cur_node is not self.__dump:
            li.append(str(cur_node))
            cur_node = cur_node.next_node
        return '[' + ", ".join(li) + ']'


def main():
    li = LinkedList(20, 40, 5050, 495, 39948)
    print "li: ", li
    print li.search(5050)
    li.delete(5050)
    print li
    li = LinkedList()
    for x in range(1, 10):
        li.insert(0, x)
    print li

    li = LinkedList()
    for x in range(1, 10):
        li.append(x)
    print li

    li = LinkedList()
    for x in range(1, 10):
        li.prepend(x)
    print li


if __name__ == '__main__':
    main()
