#!/usr/bin/env python
# -*- coding:UTF-8
__author__ = 'shenshijun'


class Node(object):
    """
    带权图的中存储元素的节点
    """

    def __init__(self, key, weight):
        """Constructor for """
        self.key = key
        self.weight = weight

    def __cmp__(self, other):
        return cmp(self.key, other.key)

    def __hash__(self):
        return hash(self.key)

    def __str__(self):
        return "".join(['Node(key=', str(self.key), ',weight=', str(self.weight), ")"])


__dict = {}
a1 = Node('A', 1)
a2 = Node('A', 2)
__dict[a1] = a1
print(a1 == a2)
print(a2 in __dict)
print(__dict.get(a2))
import sys

print(sys.version)


