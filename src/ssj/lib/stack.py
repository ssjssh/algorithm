#!/usr/bin/env python
# -*- coding:UTF-8
import copy

__author__ = 'shenshijun'


class Stack(object):
    """
    使用Python快速实现一个栈
    """

    def __init__(self, *arg):
        super(Stack, self).__init__()
        self.__stack = list(copy.copy(arg))
        self.__size = len(self.__stack)

    def push(self, value):
        self.__stack.append(value)
        self.__size += 1

    def pop(self):
        if self.__size <= 0:
            return None
        else:
            value = self.__stack[-1]
            self.__size -= 1
            del self.__stack[-1]
            return value

    def __len__(self):
        return self.__size

    def empty(self):
        return self.__size <= 0

    def __str__(self):
        return "".join(["Stack(list=", str(map(lambda s: str(s), self.__stack)), ",size=", str(self.__size), ')'])
