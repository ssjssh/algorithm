#!/usr/bin/env python
# -*- coding:UTF-8
__author__ = 'shenshijun'


class Set(object):
    """
    使用Python的Dict实现一个Set结构,如果一个对象没有实现hash方法，那么这个对象的哈希值基本上就是这个对象
    的内存地址，这个地址是唯一的，不会收对象的属性的变化的影响，因此可以安全地把可变对象存储在Set中
    """

    def __init__(self, *vargs):
        """"""
        self.__dic = {}
        map(self.add, vargs)

    def add(self, instance):
        self.__dic[instance] = instance

    def __contains__(self, item):
        return self.__dic.get(item, False)

    def delete(self, instance):
        if instance in self:
            del self.__dic[instance]

    def __len__(self):
        return len(self.__dic)

    def __getitem__(self, item):
        """
        get有特殊的意义，保证了get得到的对象和instance是同值，
        但是却是set中已经存储在set中的对象。保证不创建新的对象。
        :param item:
        :return:
        """
        result = self.__dic.get(item)
        if result is None:
            self.add(item)
            result = item
        return result

    def __iter__(self):
        return self.__dic.iterkeys()

    def __str__(self):
        return ",".join(map(lambda node: str(node), iter(self)))


def main():
    test_set = Set()
    test_set.add(10)
    test_set.add(10)
    test_set.add(10)
    print test_set


if __name__ == "__main__":
    main()
