#!/usr/bin/env python
# -*- coding:UTF-8
__author__ = 'shenshijun'


class FibonacciHeap(object):
    """实现斐波那契堆,斐波那契堆在一些操作执行的时候负责度比较低，而其他操作的复杂度和普通的堆是一样的"""

    class Node(object):
        """节点实现"""

        def __init__(self, key, parent=None, child=None, left=None, right=None):
            """Constructor for """
            self.key = key
            self.degree = 0
            self.mark = False
            self.parent = parent
            self.child = child
            self.left = left or self
            self.right = right or self

        def __str__(self):
            return str(self.key) + " : " + str(self.degree)

    def __init__(self, *argv):
        """Constructor for """
        self.__root = None
        self.__size = 0
        map(self.insert, argv)

    def insert(self, key):
        self.__size += 1
        if self.__root is None:
            self.__root = self.Node(key)
        else:
            new_node = self.Node(key, left=self.__root.left, right=self.__root)
            self.__root.left.right = new_node
            self.__root.left = new_node
            if new_node.key < self.__root.key:
                self.__root = new_node

    def extract_min(self):
        if self.__root is None:
            return None

        result = self.__root
        self.__size -= 1

        # 首先把根节点的子节点全部移到根链表上
        child = self.__root.child
        for i in xrange(0, self.__root.degree):
            next_node = child.right
            self.__root.left.right = child
            child.left = self.__root.left
            self.__root.left = child
            child.right = self.__root
            child.parent = None
            child = next_node

        # 移除根节点
        self.__root.left.right = self.__root.right
        self.__root.right.left = self.__root.left
        if self.__root.right is self.__root:
            self.__root = None
        else:
            self.__root = self.__root.right
            self.__extract_consolidating()

        return result.key

    def __extract_consolidating(self):
        # 合并根链表
        node_degrees = {}
        pass_root = False
        cur_node = self.__root
        after_merge = False
        next_node = None
        while cur_node is not self.__root or not pass_root or after_merge:
            if cur_node == self.__root:
                pass_root = True

            if not after_merge:
                next_node = cur_node.right

            d = cur_node.degree
            if d in node_degrees:
                other_node = node_degrees[d]
                sm_node = cur_node if cur_node.key <= other_node.key else other_node
                bg_node = cur_node if cur_node.key > other_node.key else other_node
                # 把大的节点连接到小的节点上面,然后继续在sm_node上面循环，因为sm_node的度数发生了变化
                self.__link_to(bg_node, sm_node)
                del node_degrees[d]
                after_merge = True
                cur_node = sm_node
            else:
                after_merge = False
                node_degrees[d] = cur_node
                cur_node = next_node

        self.__root = None

        for d, node in node_degrees.iteritems():
            node.parent = None
            if self.__root is None:
                self.__root = node
                self.__root.left = node
                self.__root.right = node
            else:
                node.left = self.__root.left
                node.right = self.__root
                self.__root.left.right = node
                self.__root.left = node

            if self.__root.key > node.key:
                self.__root = node

    @staticmethod
    def __link_to(src, dest):
        """
         bugfix: 不能把src从根链表移除,这样的话会破坏根链表，导致在__extract_consolidating中的while找不到退出条件
         我是为了避免重新创建根链表而把src从根链表中移除，这段注释只是为了提醒
        :param src:
        :param dest:
        :return:
        """
        src.mark = False

        dest_child = dest.child
        src.parent = dest
        if dest_child is None:
            dest.child = src
            src.left = src
            src.right = src
        else:
            src.left = dest_child.left
            dest_child.left.right = src
            dest_child.left = src
            src.right = dest_child
        dest.degree += 1

    def union(self, other):
        pass

    def min(self):
        return None if self.__root is None else self.__root.key

    def change_key(self, node, new_key):
        pass

    def __len__(self):
        return self.__size

    def delete(self, node):
        self.change_key(node, float('-Inf'))
        self.extract_min()


def main():
    test = ['O', 'J', 'S', 'Y', 'C', 'M', 'B', 'R', 'N', 'F', 'L', 'Z', 'U', 'Q', 'A', 'G', 'V', 'E', 'D', 'W', 'I',
            'H', 'T', 'K', 'X', 'P']

    heap = FibonacciHeap(*test)
    for i in xrange(0, len(heap)):
        print(heap.extract_min())


if __name__ == "__main__":
    main()
