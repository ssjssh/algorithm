#!/usr/bin/env python
# -*- coding:UTF-8
__author__ = 'shenshijun'


class OpenAddressMap(object):
    """
    使用二次哈希解决冲突,分别使用乘法哈希函数和除法哈希函数
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

        def __init__(self, key, value, first_hash, second_hash):
            """
            """
            self.key = key
            self.value = value
            self.first_hash = first_hash
            self.second_hash = second_hash

        def __cmp__(self, other):
            return cmp(self.key, other.key)

        def __str__(self):
            return "".join(["Node(key=", str(self.key), ",value=",
                            str(self.value), ",first_hash=", str(self.first_hash),
                            ",second_hash=", str(self.second_hash), ")"])

        def __unicode__(self):
            return self.__str__()

    def __init__(self):
        """"""
        self.__power = OpenAddressMap.DEFAULT_SIZE_POWER
        self.__load_factor = 0
        self.__size = 0
        self.__cap = OpenAddressMap.DEFAULT_SIZE
        self.__values = [None for x in xrange(0, self.__cap)]

    def __setitem__(self, key, value):
        """
        加入节点
        :param key:
        :param value:
        :return:
        """
        node = self.Node(key, value, self.multiply_hash(key), self.bit_hash(key))
        times = 0
        while True:
            index = self.hash(node.first_hash, node.second_hash, times)
            print "node=%s,index=%s" % (node, index)
            if self.__values[index] is not None and self.__values[index] != node:
                times += 1
            else:
                self.__size += 1
                self.__values[index] = node
                break
        self.__load_factor = float(self.__size) / self.__cap
        self.__resize()

    def __resize(self):
        if self.__load_factor > OpenAddressMap.DEFAULT_LOAD_FACTOR:
            # 如果哈希表太满了,则把原来的所有元素都重新插入到哈希表中去
            self.__cap *= 2
            self.__power += 1
            old_values = self.__values
            self.__values = [None for x in xrange(0, self.__cap)]
            self.__size = 0
            self.__load_factor = 0
            for node in old_values:
                self.__setitem__(node.key, node.value)

    def __getitem__(self, item):
        node = self.__get(item)
        return None if node is None else node.value

    def __contains__(self, item):
        node = self.__get(item)
        return False if node is None else True

    def __get(self, key):
        """
        :param key:
        :return:
        """
        times = 0
        first_hash = self.multiply_hash(key)
        second_hash = self.bit_hash(key)
        while True:
            index = self.hash(first_hash, second_hash, times)
            if self.__values[index] is not None and self.__values[index].key != key:
                times += 1
            else:
                return self.__values[index]

    def foreach(self, f):
        return map(f, self.__values)

    def __len__(self):
        return self.__size

    @classmethod
    def hash_code(cls, key):
        """
        计算键的hash值,由于Python中的内建对象并没有很好地提供哈希值,因此需要自己计算
        :param key:
        :return:
        """
        return abs(hash(key))

    @classmethod
    def bit_hash(cls, key):
        """
        来自java.util.HashMap的哈希函数,求别告我
        :param key:
        :return:
        """
        h = OpenAddressMap.hash_code(key)
        return 0 if key is None else (h ^ (h >> 16))

    def multiply_hash(self, key):
        return (((OpenAddressMap.hash_code(key)) * OpenAddressMap.HASH_CONST) % (2 ** 32)) >> (32 - self.__power)

    def hash(self, first_hash, second_hash, i):
        """
        实现二次哈希的函数
        :param first_hash:
        :param second_hash:
        :param i:
        :return:
        """
        return (first_hash + second_hash * i) % self.__cap

    def __str__(self):
        return "\n".join(self.foreach(lambda node: str(node)))


def main():
    d = OpenAddressMap()
    for x in xrange(0, 10):
        d["ssh" + str(x)] = x
    print len(d)
    print d['ssh2']
    print d['ssj11']
    print d


if __name__ == "__main__":
    main()
