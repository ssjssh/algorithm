#!/usr/bin/env python
# -*- coding:UTF-8
__author__ = 'shenshijun'
import copy


class Queue(object):
    """
    使用Python的list快速实现一个队列
    """

    def __init__(self, *arg):
        super(Queue, self).__init__()
        self.__queue = list(copy.copy(arg))
        self.__size = len(self.__queue)

    def enter(self, value):
        self.__size += 1
        self.__queue.append(value)

    def exit(self):
        if self.__size <= 0:
            return None
        else:
            value = self.__queue[0]
            self.__size -= 1
            del self.__queue[0]
            return value

    def __len__(self):
        return self.__size

    def empty(self):
        return self.__size <= 0

    def __str__(self):
        return "".join(["Queue(list=", str(self.__queue), ",size=", str(self.__size)])
