#!/usr/bin/env python
# -*- coding:UTF-8

import sys

reload(sys)
sys.setdefaultencoding('UTF-8')

from lib import queue
from lib.stack import Stack

__author__ = 'shenshijun'


class Node(object):
    """
    图中存储数据的结点
    """

    def __init__(self, key, color):
        """
        color
        -1:白色
         0:灰色
         1:黑色
        """

        self.key = key
        self.color = color
        self.depth = 0
        self.parent = None
        self.start_time = None
        self.end_time = None

    def set_gray(self):
        self.color = 0

    def set_black(self):
        self.color = 1

    def set_white(self):
        self.color = -1

    def is_gray(self):
        return self.color is 0

    def is_white(self):
        return self.color is -1

    def is_black(self):
        return self.color is 1

    def __eq__(self, other):
        return self.key == other.key and self.color == other.color and self.depth == other.depth

    def __str__(self):
        return "".join(['Node(key=', unicode(self.key),
                        ',depth=', str(self.depth), ',start_time=', str(self.start_time), ',end_time=',
                        str(self.end_time),
                        ',color:', 'white' if self.color is -1 else 'gray' if self.color is 0 else 'black', ')'])


class GeneralGraph(object):
    """
    使用邻接链表法存储一个通用的图结构。
    使用一个元组来表示一个图中的边
    要注意一个实现上的问题：邻接链表中的元素和关键字元素必须指向同一个对象
    """

    def __init__(self, *vargs):
        """ """
        self.__dict = {}
        map(self.insert, vargs)

    def insert(self, edge):
        start_node = self.__find(edge[0])
        end_node = self.__find(edge[1])
        linked_node = self.__dict.setdefault(start_node, [])
        linked_node.append(end_node)

    def delete_edge(self, edge):
        start_node = self.__find(edge[0])
        linked_list = self.__dict.get(start_node, [])
        for x in xrange(0, len(linked_list)):
            if linked_list[x].key == edge[1]:
                del linked_list[x]
                return True
        return False

    def __find(self, instance):
        for key_node in self.__dict.iterkeys():
            if key_node.key == instance:
                return key_node
        node = Node(instance, -1)
        self.__dict[node] = []
        return node

    def bfs(self, instance, gray_func, black_func):
        """
        图的广度遍历
        :param gray_func:当节点在灰色的时候遍历的函数
        :param black_func:当节点在黑色的时候执行的函数
        :return:结果
        """
        gray_list = []
        black_list = []
        node = self.__find(instance)
        if node is None:
            return None
        graph_queue = queue.Queue()
        # 初始化节点
        node.set_white()
        node.depth = 0
        node.parent = None
        for end_node in self.__dict.iterkeys():
            end_node.set_white()
            end_node.depth = 0
            end_node.parent = Node

        # 开始遍历
        node.set_gray()
        graph_queue.enter(node)
        while not graph_queue.empty():
            cur_node = graph_queue.exit()
            gray_list.append(gray_func(cur_node))
            for end_node in self.__dict[cur_node]:
                if end_node.is_white():
                    end_node.set_gray()
                    end_node.depth += cur_node.depth
                    end_node.parent = cur_node
                    graph_queue.enter(end_node)
            cur_node.set_black()
            black_list.append(black_func(cur_node))
        return gray_list, black_list

    def dfs(self, gray_func, black_func):
        """
        图的深度遍历
        :param gray_func:
        :param black_func:
        :return:
        """
        gray_list = []
        black_list = []

        # 初始化
        for key in self.__dict.iterkeys():
            key.start_time = None
            key.end_time = None
            key.set_white()

        # 开始遍历
        counter = 0
        for key in self.__dict.iterkeys():
            if key.is_white():
                dfs_stack = Stack()
                key.set_gray()
                key.start_time = counter
                counter += 1
                dfs_stack.push(key)
                while not dfs_stack.empty():
                    cur_node = dfs_stack.pop()
                    gray_list.append(gray_func(key))
                    for end_node in self.__dict[cur_node]:
                        if end_node.is_white():
                            end_node.set_gray()
                            end_node.start_time = counter
                            counter += 1
                            dfs_stack.push(end_node)
                    cur_node.set_black()
                    black_list.append(black_func(cur_node))
                    cur_node.end_time = counter
                    counter += 1
        return gray_list, black_list

    def topology_sort(self):
        gray_list, black_list = self.dfs(lambda node: node, lambda node: node)
        return reversed(black_list)


def main():
    graph = GeneralGraph(('内裤', '鞋'), ('内裤', '裤子'), ('裤子', '腰带'), ('腰带', '夹克'), ('衬衣', '腰带'), ('衬衣', '领带'), ('袜子', '鞋'),
                         ('手表', '手表'))
    gray_list, black_list = graph.dfs(lambda node: str(node), lambda node: str(node))
    print gray_list
    print black_list


if __name__ == "__main__":
    main()
