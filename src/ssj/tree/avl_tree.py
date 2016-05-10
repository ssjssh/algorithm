#!/usr/bin/env python
# -*- coding:UTF-8
__author__ = 'shenshijun'

"""
定义:
AVL树是高度平衡的二叉搜索树,平衡的方式是每一个节点左右子树高度差顶多为1.
每一个节点中会存储这个节点的高度。节点高度是指从这个节点到叶节点的最大距离。

高度:
AVL树的高度大约是1.44log(N)。
高度为n的AVL树的最小节点数：s(h)=s(h-1)+s(h-2)+1
"""


class Node(object):
    """"""

    def __init__(self, value, parent, left, right, height=0):
        """Constructor for Node"""
        self.value = value
        self.height = height
        self.parent = parent
        self.left = left
        self.right = right


class AVLTree(object):
    """"""

    def __init__(self):
        """Constructor for """
        self.__root = None
        self.__size = 0

    def insert(self, value):
        pass
