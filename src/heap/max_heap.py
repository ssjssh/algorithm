#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from math import *
import copy


class Heap(object):
    """最大二叉堆实现"""

    def __init__(self, *arg):
        super(Heap, self).__init__()
        self.__array = list(arg)
        self.length = len(arg)
        self.height = int(log(self.length))
        self.__build_heap()

    @classmethod
    def make_heap(cls, li):
        return Heap(*li)

    def __build_heap(self):
        """
        注意：复杂度是n
        """
        for x in reversed(xrange(0, self.length / 2)):
            self.loop_heapify(x)

    def heapify(self, parent):
        """
        基本思路是从一个元素开始，如果这个元素不符合最大堆的规定，那么就把其子节点的元素，提升到父节点上面。
        注意这是一个递归的过程，只有在满足最大堆的条件或者到达堆的叶节点的时候才会退出.
        注意：heapify方法的条件是他的子节点都是最大堆，使用的时候要注意这一点。
        """
        largest = parent
        left = parent * 2 + 1
        right = parent * 2 + 2
        # 这个地方使用left和right比较，是为了防止到了叶节点的时候会出现数组越界。
        if left < self.length and self.__array[parent] < self.__array[left]:
            largest = left

        if right < self.length and self.__array[largest] < self.__array[right]:
            largest = right

        # 保证在父元素就是最大值的时候不要移动元素
        if largest != parent:
            self.__array[largest], self.__array[parent] = self.__array[parent], self.__array[largest]
            self.heapify(largest)

    def loop_heapify(self, parent):
        """
        复杂度:lgn
        while true break是一个比较方便的把递归转换成循环的方法，因为在while的时候不用判断任何条件，判断都在break里面，避免了在while
        中设置复杂的条件。
        """
        while True:
            largest = parent
            left = parent * 2 + 1
            right = parent * 2 + 2
            # 这个地方使用left和right比较，是为了防止到了叶节点的时候会出现数组越界。
            if left < self.length and self.__array[parent] < self.__array[left]:
                largest = left

            if right < self.length and self.__array[largest] < self.__array[right]:
                largest = right

            # 保证在父元素就是最大值的时候不要移动元素
            if largest != parent:
                self.__array[largest], self.__array[parent] = self.__array[parent], self.__array[largest]
                parent = largest
            else:
                break

    def __left(self, parent):
        return parent * 2 + 1

    def __right(self, parent):
        return parent * 2 + 2

    def __wide_walk_through(self, func, start=0):
        for x in xrange(start, self.length):
            func(self.__array[x])

    def __deep_walk_through(self, func, start=0):
        if start >= self.length:
            func(start)
            left = start * 2 + 1
            right = start * 2 + 2
            self.__deep_walk_through(func, left)
            self.__deep_walk_through(func, right)

    def __str__(self):
        title = "Heap Length: %s\n" % self.length
        content_list = [title]
        self.__wide_walk_through(lambda s: content_list.append(str(s)))
        return '\t'.join(content_list)

    def __copy__(self):
        newone = type(self)(*self.__array)
        newone.__dict__.update(self.__dict__)
        return newone

    def __deepcopy__(self):
        newone = type(self)(*self.__array)
        newone.__dict__.update(self.__dict__)
        for x in self.__dict__:
            newone.__dict__[x] = copy.deepcopy(self.__dict__[x])
        return newone


def main():
    heap = Heap(16, 4, 10, 14, 7, 9, 3, 2, 8, 1)
    print heap
    new_heap = copy.copy(heap)
    print new_heap


if __name__ == '__main__':
    main()
