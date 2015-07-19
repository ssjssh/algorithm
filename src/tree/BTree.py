#!/usr/bin/env python
# -*- coding:UTF-8
from lib.stack import Stack

__author__ = 'shenshijun'


class Node(object):
    def __init__(self, is_leaf, keys, childs=None, parent=None):
        """
        在真实的实现中应该在加上一个数组表示指向真实数据的指针
        keys和childs都是一个数组，分别表示关键字和孩子
        """
        self.keys = list(sorted(keys))
        self.is_leaf = is_leaf
        self.__size = len(self.keys)
        if childs is None:
            self.childs = [None for x in xrange(0, self.__size)]
            self.childs.append(None)
        else:
            self.childs = childs
        self.parent = parent

    def __str__(self):
        return "".join(['Node(keys=', ",".join(map(lambda key: str(key), self.keys)),
                        ',leaf' if self.is_leaf else ',not leaf',
                        ',childs num=', str(len(self.childs)), ')\n'])

    def __len__(self):
        return self.__size

    def append(self, key):
        """
        向B树的节点中插入一个关键字，返回这个关键字的下标
        """
        result = self.__size
        self.__size += 1
        for x in xrange(0, result):
            if self.keys[x] > key:
                self.keys.insert(x, key)
                self.childs.insert(x, None)
                return x
        self.keys.append(key)
        self.childs.append(None)
        return result

    def search_child(self, instance):
        """
        查找小于instance的子树
        """
        for x in xrange(0, self.__size):
            if self.keys[x] > instance:
                return self.childs[x]
        return self.childs[self.__size]


class BTree(object):
    """
    B树实现，注意，不是二叉树
    """

    def __init__(self, load_factor=4, *vargs):
        """Constructor for BTree"""
        self.__root = None
        self.__load_factor = load_factor
        self.__size = len(vargs)
        map(self.insert, vargs)

    def insert(self, key):
        """
        节点插入的时候不需要再检测节点是不是满了，因为load_factor>=2，每次插入节点前调整都是使得节点关键字个数为load_factor-1。
        而插入一个关键字之后节点关键字个数是2*load_factor-1或者load_factor
        :param key:
        :return:
        """
        if self.__root is None:
            self.__root = Node(True, [key])
            return
        cur_node = self.__root
        while not cur_node.is_leaf:
            self.__split(cur_node)
            cur_node = cur_node.search_child(key)
        left_node, right_node = self.__split(cur_node)
        if left_node is None or right_node is None:
            # 返回None表示叶节点没有满
            cur_node.append(key)
        else:
            if left_node.keys[-1] < key:
                # 说明left_node中的所有节点都比key小，所以把新节点插入到右边
                right_node.append(key)
            else:
                left_node.append(key)

    def __split(self, node):
        if self.full(node):
            parent_node = node.parent
            middle_key = node.keys[self.__load_factor - 1]
            if parent_node is None:
                # 处理根节点
                self.__root = Node(False, [])
                parent_node = self.__root
            parent_middle_index = parent_node.append(middle_key)
            left_node = Node(node.is_leaf, node.keys[:self.__load_factor - 1], node.childs[:self.__load_factor],
                             parent_node)
            # 注意设定分裂节点的子节点的父指针
            for child in left_node.childs:
                if child is not None:
                    child.parent = left_node
            right_node = Node(node.is_leaf, node.keys[self.__load_factor:], node.childs[self.__load_factor:],
                              parent_node)
            for child in right_node.childs:
                if child is not None:
                    child.parent = right_node
            parent_node.childs[parent_middle_index] = left_node
            parent_node.childs[parent_middle_index + 1] = right_node
            self.__root.is_leaf = False
            return left_node, right_node
        return None, None

    def search(self, instance):
        return self.__search(self.__root, instance)

    def full(self, node):
        return len(node) >= (self.__load_factor * 2 - 1)

    @classmethod
    def __search(cls, root, instance):
        cur_node = root
        while True:
            cur_len = len(cur_node)
            x = 0
            while x < cur_len and cur_node.keys[x] < instance:
                x += 1
            if cur_node.keys[x] == instance:
                return cur_node, x
            elif cur_node.is_leaf:
                return None, None
            else:
                cur_node = cur_node.childs[x]

    def min(self):
        cur_node = self.__root
        while not cur_node.is_leaf:
            cur_node = cur_node.childs[0]
        return cur_node.keys[0]

    def max(self):
        cur_node = self.__root
        while not cur_node.is_leaf:
            cur_node = cur_node.childs[-1]
        return cur_node.keys[-1]

    def midorder(self, f):
        """
        B树中序遍历
        :param f:
        :return:
        """
        result = []
        stack = Stack()
        cur_node = self.__root
        if cur_node.is_leaf:
            return map(f, cur_node.keys)

        while True:
            if cur_node.is_leaf:
                # 到叶节点了，开始把叶节点的所有关键字都遍历掉
                result.extend(map(f, cur_node.keys))
                # 开始从栈中取元素，遍历下一个节点叶节点
                if stack.empty():
                    return result
                cur_node, i = stack.pop()
                result.append(f(cur_node.keys[i]))
                if i < len(cur_node) - 1:
                    stack.push((cur_node, i + 1))
                cur_node = cur_node.childs[i + 1]
            else:
                stack.push((cur_node, 0))
                cur_node = cur_node.childs[0]
        return result

    def __str__(self):
        return "\n".join(self.midorder(lambda s: str(s)))

    def test(self):
        print "-" * 20
        print self.__root
        print self.__root.childs[0]
        print self.__root.childs[1]


def main():
    btree = BTree(3, 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'R', 'S', 'T', 'U',
                  'V', 'X', 'Y', 'Z')
    print btree
    print btree.max()
    print btree.min()


if __name__ == "__main__":
    main()
