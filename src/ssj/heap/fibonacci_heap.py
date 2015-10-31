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
        return self.__insert_root(self.Node(key))

    def __insert_root(self, node, change_root=True):
        node.parent = None
        if not self.__root:
            self.__root = node
            self.__root.left = node
            self.__root.right = node
        else:
            node.left = self.__root.left
            node.right = self.__root
            self.__root.left.right = node
            self.__root.left = node

            if self.__root.key > node.key and change_root:
                self.__root = node
        return node

    def extract_min(self):
        if not self.__root:
            return None

        result = self.__root
        self.__size -= 1

        # 首先把根节点的子节点全部移到根链表上
        child = self.__root.child
        for i in xrange(0, self.__root.degree):
            next_node = child.right
            self.__remove_self(child)
            self.__insert_root(child)
            child = next_node

        # 移除根节点
        self.__remove_self(self.__root)
        if self.__root.right is self.__root:
            self.__root = None
        else:
            self.__root = self.__root.right
            self.__extract_consolidating()

        result.left = result
        result.right = result
        result.parent = None
        return result.key

    @classmethod
    def __remove_self(cls, node):
        node.left.right = node.right
        node.right.left = node.left

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
            self.__insert_root(node)

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
        if not dest_child:
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
        if not self.__root:
            self.__root = other.__root
        else:
            self_left = self.__root.left
            other_right = other.__root.right
            self.__root.left = other.__root
            other.__root.right = self.__root
            self_left.right = other_right
            other_right.left = self_left
            self.__root = self.__root if self.__root.key < other.__root.key else other.__root
            self.__size += other.__size

        return self

    def min(self):
        return None if self.__root else self.__root.key

    def change_key(self, node, new_key):
        """
        给node设置一个比其key小的值
        :param node:
        :param new_key:
        :return:
        """
        if node.key < new_key:
            return
        node.key = new_key
        parent = node.parent
        if parent and parent.key > node.key:
            self.__cut(node)
            self.__cascade_cut(parent)
        if self.__root.key > node.key:
            self.__root = node

    def __len__(self):
        return self.__size

    def delete(self, node):
        self.change_key(node, float('-Inf'))
        self.extract_min()

    def __cut(self, node):
        parent = node.parent
        if not parent:
            return node

        # 处理parent的child指针
        if node.right is node:
            parent.child = None
        else:
            parent.child = node.right
        self.__remove_self(node)
        parent.degree -= 1
        self.__insert_root(node)
        node.mark = False
        return node

    def __cascade_cut(self, node):
        parent = node.parent
        # 如果parent为None，说明这个节点在根链表上，因此不需要继续处理
        if parent:
            if not node.mark:
                node.mark = True
            else:
                # 如果已经丢失了两个节点，那么要把本节点移到根链表上
                self.__cut(node)
                self.__cascade_cut(parent)


def main():
    import random
    test = ['O', 'J', 'S', 'Y', 'C', 'M', 'B', 'R', 'N', 'F', 'L', 'Z', 'U', 'Q', 'A', 'G', 'V', 'E', 'D', 'W', 'I',
            'H', 'T', 'K', 'X', 'P']
    random.shuffle(test)
    rele = 'Z'
    test.remove(rele)
    heap = FibonacciHeap(*test)
    rnode = heap.insert(rele)

    for i in xrange(0, random.randint(1, len(heap))):
        print(heap.extract_min())

    print("change a node key")
    heap.change_key(rnode, 0)

    for i in xrange(0, len(heap)):
        print(heap.extract_min())

    print("test union")
    one = [10, 20, 0]
    other = [15, 5, 30]
    one_heap = FibonacciHeap(*one)
    other_heap = FibonacciHeap(*other)
    one_heap.union(other_heap)
    for i in xrange(0, len(one_heap)):
        print(one_heap.extract_min())


if __name__ == "__main__":
    main()
