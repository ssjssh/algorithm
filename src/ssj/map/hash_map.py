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
    DEFAULT_SIZE = 2 << DEFAULT_SIZE_POWER  # aka8
    DEFAULT_LOAD_FACTOR = 0.75  # 默认装载因子0.75

    class Node(object):
        """
        哈希表中存储的节点
        """

        def __init__(self, key, value, hash_code, nex, last_insert, next_insert):
            """
            nex用来解决链表的哈希冲突
            next_insert用来记录下一个插入的元素
            """
            self.key = key
            self.value = value
            self.hash_code = hash_code
            self.nex = nex
            self.last_insert = last_insert
            self.next_insert = next_insert

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
        self.__power = HashMap.DEFAULT_SIZE_POWER  # 把哈希表大小存储为幂数，这样的好处不用在扩展时再从头计算
        self.__cap = HashMap.DEFAULT_SIZE  # 表示哈希表的容量
        self.__head = None
        self.__last_put = None  # 存储上一个插入时的元素，这样便于在插入新元素的时候用指针把他们按照插入顺序连接起来
        self.__values = [None for x in range(0, self.__cap)]  # 主要使用的列表

    def __get_index(self, key):
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
            self.__values = [None for x in xrange(0, self.__cap)]
            self.__size = 0
            self.__load_factor = 0
            self.__last_put = None
            cur_node = self.__head
            self.__head = None
            while cur_node:
                self.__setitem__(cur_node.key, cur_node.value)
                cur_node = cur_node.next_insert

    def foreach(self, f):
        cur_node = self.__head
        while cur_node:
            yield f(cur_node.key, cur_node.value)
            cur_node = cur_node.next_insert

    def __get(self, key):
        index = self.__get_index(key)
        indexed_node = self.__values[index]
        while indexed_node:
            if indexed_node.key == key:
                return indexed_node
            indexed_node = indexed_node.nex
        return None

    def __contains__(self, key):
        node = self.__get(key)
        return node

    def __getitem__(self, item):
        node = self.__get(item)
        return None if node is None else node.value

    def __setitem__(self, key, value):
        index = self.__get_index(key)

        exists_nodes = self.__values[index]
        exists_flag = False
        if exists_nodes:
            cur_node = exists_nodes
            while cur_node:
                if cur_node.key == key:
                    exists_flag = True
                    cur_node.value = value
                    node = cur_node
                    break
                cur_node = cur_node.nex

        if not exists_flag:
            node = self.Node(key, value, HashMap.hash_code(key), exists_nodes, self.__last_put, None)
            self.__values[index] = node
            self.__size += 1

        if self.__last_put:
            self.__last_put.next_insert = node
        self.__last_put = node
        if not self.__head:
            self.__head = node
        self.__resize()

    def __delitem__(self, key):
        old_value = None
        index = self.__get_index(key)
        indexed_node = self.__values[index]
        last_node = None
        while indexed_node:
            if indexed_node.key == key:
                old_value = indexed_node.value
                if last_node:
                    last_node.nex = indexed_node.nex
                else:
                    self.__values[index] = indexed_node.nex
                # 处理哈希表
                self.__size -= 1
                if indexed_node.last_insert:
                    indexed_node.last_insert.next_insert = indexed_node.next_insert

                if indexed_node.next_insert:
                    indexed_node.next_insert.last_insert = indexed_node.last_insert
            last_node = indexed_node
            indexed_node = indexed_node.nex
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
    del d['ssh100']
    print d['ssh100']
    print(len(d))
    print(d)


if __name__ == "__main__":
    main()
