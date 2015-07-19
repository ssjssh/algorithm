#!/usr/bin/env python
# -*- coding:utf-8 -*-
class MultiArrayLinkedList(object):
    """
    用三个数组实现LinkedList，并且使用一个free指针指向空的位置
    """

    class EmptyNode(object):
        """
        最好使用自定义的对象作为空元素，用None作为空元素会导致列表中无法存储None
        """

        def __str__(self):
            return "<empty node>"

    def __init__(self, length):
        super(MultiArrayLinkedList, self).__init__()
        self.__empty = self.EmptyNode()
        self.__cap = length
        self.__lenght = 0
        self.__key = [self.__empty for x in xrange(0, length + 1)]
        self.__prev = [-1 for x in xrange(0, length + 1)]
        self.__next = [x + 1 for x in xrange(0, length + 1)]  # next数组在节点为空的时候存储的是下一个空节点的位置
        self.__free = 1  # 第一个空元素位置
        # 设置哨兵元素
        self.__key[0] = self.__empty
        self.__prev[0] = 0
        self.__next[0] = 0
        self.__full = 0  # 第一个元素位置

    def prepend(self, value):
        first_node = self.__next[0]
        self.__key[self.__free] = value
        next_free = self.__next[self.__free]
        self.__next[self.__free] = first_node
        self.__prev[self.__free] = 0
        self.__prev[first_node] = self.__free
        self.__next[0] = self.__free
        self.__full = self.__free
        self.__free = next_free

    def append(self, value):
        last_node = self.__prev[0]
        # 创建新节点
        self.__key[self.__free] = value
        self.__prev[self.__free] = last_node
        next_free = self.__next[self.__free]
        self.__next[self.__free] = 0
        # 设置上一个节点
        self.__next[last_node] = self.__free
        # 设置起始节点
        self.__prev[0] = self.__free
        # 设置空链表
        self.__free = next_free
        self.__full = self.__next[0]

    """
    TODO：偷个懒，insert就不实现了
    """

    def insert(self, index, value):
        pass

    def search(self, value):
        self.__key[0] = value
        cur_pos = self.__full
        while self.__key[cur_pos] != value:
            cur_pos = self.__next[cur_pos]
        self.__key[0] = self.__empty
        if cur_pos is 0:
            return None
        else:
            return cur_pos

    def delete(self, value):
        ele_pos = self.search(value)
        if ele_pos is not None:
            prev_node = self.__prev[ele_pos]
            next_node = self.__next[ele_pos]
            self.__key[ele_pos] = self.__empty
            self.__prev[ele_pos] = -1
            self.__next[ele_pos], self.__free = self.__free, ele_pos
            self.__next[prev_node] = next_node
            self.__prev[next_node] = prev_node
            if self.__full == ele_pos:
                self.__full = next_node
            return True
        else:
            return False

    """
    整理链表的方法：如果事先知道有n个元素，那么就可以把full链表中超过n的元素移动到n以内，
    也就是两个循环一个循环查找n内的空位置，另一个循环查找超过n的元素，然后就把他们交换就可以了。
    这样复杂度是O(n)
    """

    def compactify(self):
        pass

    def __str__(self):
        li = []
        cur_pos = self.__full
        while self.__key[cur_pos] is not self.__empty:
            li.append("prev: " + str(self.__prev[cur_pos]) + " key: " + str(self.__key[cur_pos]) + " next: " + str(
                self.__next[cur_pos]))
            cur_pos = self.__next[cur_pos]
        li.append("free: " + str(self.__free))
        li.append("full: " + str(self.__full))
        return "\n".join(li)


def main():
    li = MultiArrayLinkedList(10)
    for x in xrange(1, 10):
        li.prepend(x)
    print li
    li = MultiArrayLinkedList(10)
    for x in xrange(1, 10):
        li.append(x)
    print li
    print li.search(8)
    print li.delete(8)
    print li


if __name__ == '__main__':
    main()
