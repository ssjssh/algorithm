#!/usr/bin/env python
# -*- coding:UTF-8
from lib.queue import Queue

__author__ = 'shenshijun'
"""
一个使用邻接链表实现的带权有有向图
"""


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


class Edge(object):
    """
    """

    def __init__(self, from_node, to_node):
        self.from_node = from_node
        self.to_node = to_node

    def __eq__(self, other):
        return self.from_node == other.from_node and self.to_node == other.to_node

    def __hash__(self):
        return hash(hash(self.from_node) * hash(self.to_node))

    def __str__(self):
        return "=>".join([str(self.from_node), str(self.to_node)])


class WeightedGraph(object):
    """"""

    def __init__(self):
        """
        首先用一个set来存储所有节点，而在图中仅仅保存了指向这些节点的指针
        :return:
        """
        self.__adj_list = {}
        self.__size = 0

    def __len__(self):
        return self.__size

    def insert_edge(self, from_v, to_v, weight):
        if from_v in self.__adj_list:
            self.__adj_list[from_v].append(Node(to_v, weight))
        else:
            self.__adj_list[from_v] = [Node(to_v, weight)]

    def __str__(self):
        graph_list = []
        for key, v_list in self.__adj_list.iteritems():
            graph_list.extend([str(key), ' => '])
            graph_list.extend(map(lambda node: str(node) + ',', v_list))
            graph_list.append('\n')
        return "".join(graph_list)

    def __dfs_multiple(self, node, func):
        pass

    def bfs(self):
        pass

    def lws(self, from_node, to_node):
        """
        在有向无环带权图里面查找最长路径
        令list(s,t)是从s到t的最长带权路径。
        那么可以使用递归式表示这个问题
        list(s,t) = max(list(s,t-1))+list(t-1,t)(唯一)
        用动态规划自下而上解决，因为自上而下解决首先遇到的问题就是
        查找指向一个节点的节点在邻接表中比较困难
        :param from_node:
        :param to_node:
        :return:
        """
        __lws = {}
        # 为了计算方便，这里把开始节点到开始节点插入字典中，
        zero_edge = Edge(from_node, from_node)
        __lws[zero_edge] = 0
        graph_stack = Queue()
        graph_stack.enter(from_node)
        while not graph_stack.empty():
            cur_node = graph_stack.exit()
            cur_edge_list = self.__adj_list.get(cur_node)
            if cur_edge_list is None:
                print ",".join(map(lambda edge: str(edge), __lws.iteritems()))
                print ",".join(map(lambda edge: str(edge), __lws))
                return __lws[Edge(from_node, to_node)]
            for edge_end_node in cur_edge_list:
                graph_stack.enter(edge_end_node.key)
                last_weighted_length = __lws[Edge(from_node, cur_node)]
                cur_edge = Edge(from_node, edge_end_node.key)
                cur_weight_length = last_weighted_length + edge_end_node.weight
                # 如果不存在这个边，那么就插入
                if cur_edge not in __lws:
                    __lws[cur_edge] = cur_weight_length
                # 如果存在，那么就把最大值插入
                elif cur_weight_length > __lws[cur_edge]:
                    __lws[cur_edge] = cur_weight_length
        print ",".join(map(lambda edge: str(edge), __lws.iteritems()))
        print ",".join(map(lambda edge: str(edge), __lws))
        return __lws[Edge(from_node, to_node)]

    def test(self):
        pass


def main():
    graph = WeightedGraph()
    graph.insert_edge('A', 'B', 2)
    graph.insert_edge('A', 'H', 7)
    graph.insert_edge('B', 'C', 3)
    graph.insert_edge('B', 'H', 6)
    graph.insert_edge('C', 'F', 4)
    graph.insert_edge('D', 'E', 9)
    graph.insert_edge('E', 'F', 10)
    graph.insert_edge('D', 'C', 5)
    graph.insert_edge('H', 'D', 11)
    graph.insert_edge('F', 'M', 0)
    print graph.lws('A', 'F')
    print graph


if __name__ == "__main__":
    main()
