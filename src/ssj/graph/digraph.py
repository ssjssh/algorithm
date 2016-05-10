#!/usr/bin/env python
# -*- coding:UTF-8

__author__ = 'shenshijun'
from ssj.lib.queue import Queue
from ssj.graph import GraphError


class Vertex(object):
    def __init__(self, key, weight=None):
        """
        adjust_list 表示邻接节点
        """
        self.key = key
        self.weight_list = []
        self.adjust_list = []
        self.in_degree = 0
        self.backup_in_degree = self.in_degree
        self.out_degree = 0
        self.backup_out_degree = self.out_degree
        self.dist = 0

    def add_adjust(self, to_vertex):
        self.adjust_list.append(to_vertex)
        self.out_degree += 1
        self.backup_out_degree += 1


class Digraph(object):
    def __init__(self):
        self._vertexes = {}

    def add_vertex(self, key):
        """
        Args:
        :param key:顶点关键字
        Returns:
        :rtype: bool
        """
        if key in self._vertexes:
            return False
        else:
            self._vertexes[key] = Vertex(key)
            return True

    def add_edge(self, from_key, to_key):
        # 首先把两个节点查入到图中
        self.add_vertex(from_key)
        self.add_vertex(to_key)
        self._vertexes[from_key].add_adjust(self._vertexes[to_key])
        self._vertexes[to_key].in_degree += 1
        self._vertexes[to_key].backup_in_degree += 1

    def top_sort(self, func):
        zero_in_degree_queue = Queue()

        # 首先找到所有入度为0的顶点,遍历从这里开始
        for key, vertex in self._vertexes.iteritems():
            vertex.backup_in_degree = vertex.in_degree
            if vertex.in_degree is 0:
                zero_in_degree_queue.enter(vertex)

        if zero_in_degree_queue.empty():
            raise GraphError('图中有环,无法执行图的拓扑排序')

        result = []
        while not zero_in_degree_queue.empty():
            zero_vertex = zero_in_degree_queue.exit()
            result.append(func(zero_vertex.key))
            for vertex in zero_vertex.adjust_list:
                vertex.in_degree -= 1
                if vertex.in_degree is 0:
                    zero_in_degree_queue.enter(vertex)

        # 恢复
        for key, vertex in self._vertexes.iteritems():
            vertex.in_degree = vertex.backup_in_degree
        return result

    def bfs(self, key, func):
        next_vertex_queue = Queue()
        for k, vertex in self._vertexes.iteritems():
            vertex.dist = -1

        result = []
        self._vertexes[key].dist = 0
        next_vertex_queue.enter(self._vertexes[key])

        while not next_vertex_queue.empty():
            vertex = next_vertex_queue.exit()
            result.append(func(vertex.key, vertex.dist))
            for adjust_vertex in vertex.adjust_list:
                if adjust_vertex.dist is -1:
                    adjust_vertex.dist = vertex.dist + 1
                    next_vertex_queue.enter(adjust_vertex)

        for k, vertex in self._vertexes.iteritems():
            if vertex.dist is -1:
                result.extend(self.bfs(vertex.key, func))
        return result


def main():
    graph = Digraph()
    graph.add_edge('v1', 'v2')
    graph.add_edge('v1', 'v3')
    graph.add_edge('v1', 'v4')
    graph.add_edge('v2', 'v4')
    graph.add_edge('v4', 'v3')
    graph.add_edge('v4', 'v7')
    graph.add_edge('v4', 'v6')
    graph.add_edge('v3', 'v6')
    graph.add_edge('v2', 'v5')
    graph.add_edge('v5', 'v4')
    graph.add_edge('v5', 'v7')
    graph.add_edge('v7', 'v6')
    print graph.top_sort(lambda key: key)
    print graph.bfs('v1', lambda key, dist: (key, dist))


if __name__ == "__main__":
    main()
