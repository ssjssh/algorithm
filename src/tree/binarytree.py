# /usr/bin/env python
# -*- coding:utf-8 -*-
import Queue


class Stack(object):
    """
    实现上还是有些问题的，因为没有考虑栈空间不够的时候扩展的问题
    """

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


class Btree(object):
    """
    实现一个通用的二叉树，这个二叉树并不包含任何别的性质
    """

    class Node(object):
        """docstring for Node"""

        def __init__(self, key, left, right):
            self.key = key
            self.left = left
            self.right = right

        def __str__(self):
            return "".join(["key: ", str(self.key)])

    def __init__(self, nodes, root_index=0):
        """
        node是一个元祖列表，默认第一个是根节点，例如[(key=12,left=7,right=3),(key=15,left=8,right=None)]
        """
        super(Btree, self).__init__()
        self.__root, self.__nodes = self.build_tree(nodes, root_index)
        self.__size = len(nodes)

    def build_tree(self, nodes, root_index=0):
        tree_nodes = [self.Node(ele[0], ele[1], ele[2]) for ele in nodes]
        for node in tree_nodes:
            node.left = tree_nodes[node.left] if node.left is not None else None
            node.right = tree_nodes[node.right] if node.right is not None else None
        return (tree_nodes[root_index], tree_nodes)

    def depth_walk(self, f):
        """
        使用栈实现深度遍历，每次都是把右节点放进栈里，这样的保证每次都是优先访问左节点
        """
        result = []
        stack = Stack(self.__size)
        stack.push(self.__root)
        while not stack.empty():
            cur_node = stack.pop()
            result.append(f(cur_node.key))
            if cur_node.right is not None:
                stack.push(cur_node.right)

            if cur_node.left is not None:
                stack.push(cur_node.left)
        return result

    def breadth_walk(self, f):
        """
        使用堆实现广度遍历
        """
        result = []
        q = Queue.Queue(maxsize=-1)
        q.put(self.__root)
        while not q.empty():
            cur_node = q.get()
            result.append(f(cur_node.key))
            # 注意：这儿的顺序比较讲究，不能调换
            if cur_node.left is not None:
                q.put(cur_node.left)

            if cur_node.right is not None:
                q.put(cur_node.right)
        return result

    def __str__(self):
        return "\t".join(self.depth_walk(lambda key: str(key)))


def main():
    nodes = [(12, 6, 2), (15, 7, None), (4, 9, None), (10, 4, 8), (2, None, None), (18, 0, 3), (7, None, None),
             (14, 5, 1), (21, None, None), (5, None, None)]
    btree = Btree(nodes, 5)
    print btree


if __name__ == '__main__':
    main()
