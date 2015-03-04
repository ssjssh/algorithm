#!/usr/bin/env python
# -*- coding:utf-8 -*-
from lib.queue import Queue
from lib.stack import Stack


class BSTree(object):
    """
    实现二叉搜索树,并没有任何平衡树的逻辑
    """

    class Node(object):
        """
        表示树中的节点
        """

        def __init__(self, value, left, right, parent):
            self.value = value
            self.left = left
            self.right = right
            self.parent = parent

        def __cmp__(self, other):
            return cmp(self.value, other.value)

        def __str__(self):
            return "".join(["Node(value=", str(self.value), ")"])

    def __init__(self, *arg):
        super(BSTree, self).__init__()
        self.__root = None
        self.__size = 0
        map(self.insert, arg)

    def __find(self, value):
        if value is None:
            raise ValueError("None value not allowed in BSTree")
        cur_node = self.__root
        while cur_node is not None and cur_node.value != value:
            if cur_node.value < value:
                cur_node = cur_node.right
            else:
                cur_node = cur_node.left
        return cur_node

    def find(self, value):
        return True if self.__find(value) is not None else False

    def insert(self, value):
        if value is None:
            raise ValueError("BSTree don't allow None")
        self.__size += 1

        node = self.Node(value, None, None, None)
        if self.__root is None:
            self.__root = node
        else:
            cur_node = self.__root
            while True:
                cur_child_node = cur_node.left if node <= cur_node else cur_node.right
                if cur_child_node is not None:
                    cur_node = cur_child_node
                else:
                    node.parent = cur_node
                    if cur_node <= node:
                        cur_node.right = node
                    else:
                        cur_node.left = node
                    break

    def preorder(self, f):
        result = []
        stack = Stack(self.__root)
        while True:
            cur_node = stack.pop()
            # 栈中没有元素的时候就表示所有的元素都已经遍历完了
            if cur_node is None:
                break
            result.append(f(cur_node.value))
            if cur_node.left is not None:
                stack.push(cur_node.left)
            if cur_node.right is not None:
                stack.push(cur_node.right)
        return result

    def midorder(self, f):
        result = []
        stack = Stack(self.__root)
        cur_node = self.__root.left
        # 第一个阶段首先把所有树左边的节点放进栈里,这个时候并不遍历
        # 第二个阶段的时候由于左节点遍历了之后,再遍历右节点
        while not stack.empty() or cur_node is not None:
            # 第二个判断条件比较重要,因为如果根节点没有左子树,这个时候栈就是空的,会直接退出循环
            if cur_node is not None:
                stack.push(cur_node)
                cur_node = cur_node.left
            else:
                cur_node = stack.pop()
                result.append(f(cur_node.value))
                cur_node = cur_node.right
        return result

    def postorder(self, f):
        """
        后序遍历最好实现了,把前序遍历调转下就是后序遍历
        """
        return reversed(self.preorder(f))

    def flatorder(self, f):
        result = []
        queue = Queue(self.__root)
        while not queue.empty():
            cur_node = queue.exit()
            result.append(f(cur_node.value))
            if cur_node.left is not None:
                queue.enter(cur_node.left)

            if cur_node.right is not None:
                queue.enter(cur_node.right)
        return result

    def max(self):
        max_node = BSTree.__max(self.__root)
        return max_node.value if max_node is not None else None

    @classmethod
    def __max(cls, root):
        cur_node = root
        while cur_node.right is not None:
            cur_node = cur_node.right
        return cur_node

    @classmethod
    def __min(cls, root):
        cur_node = root
        while cur_node.left is not None:
            cur_node = cur_node.left
        return cur_node

    def min(self):
        min_node = BSTree.__min(self.__root)
        return min_node.value if min_node is not None else None

    def __str__(self):
        return "\t".join(self.midorder(lambda s: str(s)))

    def successor(self, value):
        find_node = self.__find(value)
        if find_node is None:
            # 处理节点不存在的情况
            return None
        if find_node.right is not None:
            min_node = BSTree.__min(find_node.right)
            return min_node.value if min_node is not None else None
        else:
            cur_parent = find_node.parent
            cur_sub = find_node
            while cur_parent is not None and cur_parent.right is cur_sub:
                # 第一个条件是为了处理没有找到符合条件的父节点的情况,这个时候搜索失败
                cur_parent, cur_sub = cur_parent.parent, cur_parent
            return cur_parent.value if cur_parent is not None else None

    def predecessor(self, value):
        find_node = self.__find(value)
        if find_node is None:
            # 处理节点不存在的情况
            return None
        if find_node.left is not None:
            max_node = BSTree.__max(find_node.left)
            return max_node.value if max_node is not None else None
        else:
            cur_parent = find_node.parent
            cur_sub = find_node
            while cur_parent is not None and cur_parent.left is cur_sub:
                cur_parent, cur_sub = cur_parent.parent, cur_parent
            return cur_parent.value if cur_parent is not None else None

    def __delete__(self, instance):
        """
        删除节点
        :param instance:
        :return:
        """
        node = self.__find(instance)
        if node is None:
            # 没有找到相应的节点直接退出
            return None
        if node.left is None:  # 第一二种情况
            self.__transplant(node, node.right)
        elif node.right is None:
            self.__transplant(node, node.left)
        else:  # 第三种情况,有两个子节点
            successor = self.__find(self.successor(instance))  # 不考虑节点重复的问题,因此find方法可以正确找到对应的节点
            if node.right is not successor:
                self.__transplant(successor, successor.right)
                # 后面的是设置移动之后新位置的节点,后继节点净身出户
                successor.right = node.right
                successor.right.parent = successor
            self.__transplant(node, successor)
            successor.left = node.left
            successor.left.parent = successor

    def __transplant(self, old, new):
        """
        移植操作,用new子树替换new子树
        :param old:要被替换的子树
        :param new:替换的子树
        :return:
        """
        if self.__root is old:
            self.__root = new
        parent = old.parent
        if parent.left is old:
            parent.left = new
        else:
            parent.right = new
        if new is not None:
            new.parent = parent


def main():
    print "\ncheck stack"
    stack = Stack(1, 2, 34, 5)
    for x in range(0, 5):
        stack.push(x)
    print stack
    for x in range(0, 15):
        print "".join(["size=", str(len(stack)), " cur_node=", str(stack.pop())])

    print "\ncheck queue"
    queue = Queue(1, 2, 34, 5)
    for x in range(0, 5):
        queue.enter(x)
    print stack
    for x in range(0, 15):
        print "".join(["size=", str(len(queue)), " cur_node=", str(queue.exit())])

    print "\ncheck BSTree"
    tree = BSTree(1, 2, 34, 5)
    print tree
    print tree.find(10)
    print tree.find(5)
    print tree.max()
    print tree.min()
    print tree.successor(34)
    print tree.successor(5)
    print tree.predecessor(1)
    print tree.predecessor(2)


if __name__ == '__main__':
    main()
