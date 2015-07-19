#!/usr/bin/env
# !-*- coding:utf-8 -*-
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


class NTree(object):
    """
    用左孩子右兄弟的方式实现一个n可以有任意个子节点的树
    """

    class Node(object):
        """
        """

        def __init__(self, key, child, brother):
            self.key = key
            self.child = child
            self.brother = brother

        def __str__(self):
            return str(key)

    def __init__(self, nodes, root_index=0):
        """
        nodes是一个元祖列表，最前面的一个元素是节点值，后面的都是子节点的索引。
        如果一个元祖中只有第一个元素，那么就认为这个元祖表示的是一个叶节点
        """
        super(NTree, self).__init__()
        self.__root, self.__nodes = self.build_tree(nodes, root_index)
        self.__size = len(nodes)

    def build_tree(self, nodes, root_index=0):
        tree_nodes = [self.Node(node[0], node[1], node[2]) for node in nodes]
        for node in tree_nodes:
            node.child = tree_nodes[node.child] if node.child is not None else None
            node.brother = tree_nodes[node.brother] if node.brother is not None else None
        return (tree_nodes[root_index], tree_nodes)

    def depth_walk(self, f):
        """
        使用栈来实现深度遍历的时候，首先把兄弟节点进栈，然后把子节点放在栈中.
        """
        result = []
        stack = Stack(self.__size)
        stack.push(self.__root)
        while not stack.empty():
            cur_node = stack.pop()
            result.append(f(cur_node.key))
            if cur_node.brother is not None:
                stack.push(cur_node.brother)

            if cur_node.child is not None:
                stack.push(cur_node.child)
        return result

    def breadth_walk(self, f):
        """
        使用队列实现广度遍历的思路是类似的，在访问到一个父节点的时候把所有的子节点都依次放到队列中
        """
        result = []
        q = Queue.Queue(maxsize=-1)
        q.put(self.__root)
        while not q.empty():
            cur_node = q.get()
            result.append(f(cur_node.key))
            # 注意：这儿的顺序比较讲究，不能调换
            child = cur_node.child
            while child is not None:
                q.put(child)
                child = child.brother
        return result

    def __str__(self):
        return "\t".join(self.depth_walk(lambda key: str(key)))


def main():
    nodes = [(12, 6, 2), (15, 7, None), (4, 9, None), (10, 4, 8), (2, None, None), (18, 0, 3), (7, None, None),
             (14, 5, 1), (21, None, None), (5, None, None)]
    btree = NTree(nodes, 5)
    print btree


if __name__ == '__main__':
    main()
