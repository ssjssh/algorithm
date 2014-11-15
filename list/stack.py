#!/usr/bin/env python
# -*- coding:utf-8 -*-

class Stack(object):
    """docstring for Stack"""

    def __init__(self, cap):
        super(Stack, self).__init__()
        self.__cap = cap  # 栈大小
        self.__length = 0  # 栈长度
        if self.__cap < 0:
            raise ValueError("length of Stack can not be negtive")
        self.__values = [0 for x in xrange(0, self.__cap)]

    def empty(self):
        return self.__length is 0

    def push(self, x):
        if self.__length >= self.__cap:
            raise IndexError("stack is full, can not push any object")
        self.__values[self.__length] = x
        self.__length += 1

    def pop(self):
        if self.__length <= 0:
            return None
        self.__length -= 1
        return self.__values[self.__length]

    def __str__(self):
        return "".join(["Stack, Value: ", str(self.__values), " cap: ", str(self.__cap),
                        " length:", str(self.__length)])


def main():
    stack = Stack(5)
    for x in xrange(0, 5):
        stack.push(x)
    print "full stack"
    print stack
    print "pop everything"
    for x in xrange(0, 7):
        print stack.pop()

    print "index of bound error"
    for x in xrange(0, 7):
        stack.push(x)


if __name__ == '__main__':
    main()
