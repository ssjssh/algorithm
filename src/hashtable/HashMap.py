#!/usr/bin/env python
# -*- coding:UTF-8
__author__ = 'shenshijun'


class HashMap(object):
    """
    使用链接法解决哈希冲突,使用乘法哈希哈希函数
    如果空间需要扩充,那么仅仅简单地把存储空间扩展为双倍,然后重新计算一遍哈希函数
    另外类似于LinkedHashMap,哈希表里面的元素有组成了一个链表,用来保持插入顺序
    """
    # 来自算法导论乘法哈希函数的值,暂时仅支持2**32个元素
    HASH_CONST = 2654435769
    DEFAULT_SIZE_POWER = 3
    DEFAULT_SIZE = 2 << DEFAULT_SIZE_POWER  # aka16
    DEFAULT_LOAD_FACTOR = 0.75  # 默认装载因子0.75

    class Node(object):
        """
        哈希表中存储的节点
        """

        def __init__(self, key, value, hash_code, prev, nex):
            """
            """
            self.key = key
            self.value = value
            self.hash_code = hash_code
            self.nex = nex
            self.prev = prev

        def __cmp__(self, other):
            return cmp(self.key, other.key)

        def __str__(self):
            return "".join(["Node(key=", str(self.key), ",value=",
                            str(self.value), ",hash=", str(self.hash_code), ",has_next=",
                            str(True if self.nex is not None else False), ")"])

        def __unicode__(self):
            return self.__str__()

    def __init__(self):
        """"""
        self.__load_factor = 0
        self.__size = 0  # 表示真正存储的元素有几个
        self.__power = HashMap.DEFAULT_SIZE_POWER
        self.__cap = HashMap.DEFAULT_SIZE  # 表示哈希表的容量
        self.__head = None
        self.__last_put = None
        self.__values = [[] for x in range(0, self.__cap)]

    def hash(self, key):
        """
        乘法哈希函数
        :param key:
        :return:
        """
        return (((HashMap.hash_code(key)) * HashMap.HASH_CONST) % (2 ** 32)) >> (32 - self.__power)

    @classmethod
    def hash_code(cls, key):
        """
        计算键的hash值,由于Python中的内建对象并没有很好地提供哈希值,因此需要自己计算
        :param key:
        :return:
        """
        return abs(hash(key))

    def __resize(self):
        if self.__load_factor > HashMap.DEFAULT_LOAD_FACTOR:
            # 如果哈希表太满了,则把原来的所有元素都重新插入到哈希表中去
            self.__cap *= 2
            self.__power += 1
            old_values = self.__values
            self.__values = [[] for x in xrange(0, self.__cap)]
            self.__size = 0
            self.__load_factor = 0
            self.__last_put = None
            cur_node = self.__head
            self.__head = None
            while cur_node is not None:
                self.__setitem__(cur_node.key, cur_node.value)
                cur_node = cur_node.nex

    def foreach(self, f):
        cur_node = self.__head
        while cur_node is not None:
            yield f(cur_node.key, cur_node.value)
            cur_node = cur_node.nex

    def __get(self, key):
        index = self.hash(key)
        indexed_nodes = self.__values[index]
        for node in indexed_nodes:
            if node.key == key:
                return node
        return None

    def __contains__(self, key):
        node = self.__get(key)
        return False if node is None else True

    def __getitem__(self, item):
        node = self.__get(item)
        return None if node is None else node.value

    def __setitem__(self, key, value):
        node = self.Node(key, value, HashMap.hash_code(key), self.__last_put, None)
        index = self.hash(key)
        exists_nodes = self.__values[index]
        exists_flag = False
        for x in range(0, len(exists_nodes)):
            if node == exists_nodes[x]:
                exists_nodes[x] = node
                exists_flag = True
        if not exists_flag:
            exists_nodes.append(node)
            self.__size += 1
        if self.__last_put is not None:
            self.__last_put.nex = node
        self.__last_put = node
        if self.__head is None:
            self.__head = node
        self.__load_factor = float(self.__size) / self.__cap
        self.__resize()

    def __delitem__(self, key):
        old_value = None
        index = self.hash(key)
        indexed_nodes = self.__values[index]
        for x in xrange(len(indexed_nodes)):
            if indexed_nodes[x].key == key:
                old_value = indexed_nodes[x].value
                del indexed_nodes[x]
        return old_value

    def __len__(self):
        return self.__size

    def __str__(self):
        return "\n".join(self.foreach(lambda key, value: "Node(key=%s,value=%s)" % (key, value)))


def main():
    d = HashMap()
    for x in xrange(0, 1000):
        d["ssh" + str(x)] = x
    print len(d)
    print d
    del d['ssj100']
    print d['ssj100']


if __name__ == "__main__":
    main()
