#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
用list实现队列
"""


class Queue(object):
    """docstring for Queue"""

    class EmptyNode(object):
        """
        用EmptyNode来实现特殊的空节点表示
        """
        pass

    def __init__(self, cap):
        super(Queue, self).__init__()
        self.__empty = self.EmptyNode()
        self.__cap = cap
        if cap < 0:
            raise ValueError("cap of  queue can not be negative")
        self.__value = [self.__empty for x in xrange(0, cap)]
        # head指向下一个要出队列的元素，tail指向下一个要插入元素的位置。规定数据结构中的指针是简化逻辑的方法
        self.__head = 0
        self.__tail = 0

    def enter(self, x):
        if self.__tail == self.__head and self.__value[self.__head] is not self.__empty:
            raise IndexError("queue is full")
        self.__value[self.__tail] = x
        self.__tail += 1
        if self.__tail >= self.__cap:
            self.__tail = 0

    def exit(self):
        if self.__tail == self.__head and self.__value[self.__head] is self.__empty:
            raise IndexError("queue is empty")
        v = self.__value[self.__head]
        self.__head += 1
        if self.__head >= self.__cap:
            self.__head = 0
        return v

    def __len__(self):
        if self.__tail > self.__head:
            return self.__tail - self.__head
        elif self.__head > self.__tail:
            return self.__cap - (self.__head - self.__tail)
        else:
            if self.__value[self.__head] is self.__empty:
                return 0
            else:
                return self.__cap
