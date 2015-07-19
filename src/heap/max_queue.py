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
        while true break是一个比较方便的把递归转换成循环的方法，因为在while的时候不用判断任何条件，判断都在break里面，避免了在while
        中设置复杂的条件
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

    def __len__(self):
        return self.length

    def __getitem__(self, index):
        return self.__array[index]

    def append(self, value):
        self.__array.append(value)
        insert_index = self.length
        while True:
            parent = (insert_index - 1) / 2
            # 这儿需要判断使得parent不会越界
            if parent >= 0 and self.__array[insert_index] > self.__array[parent]:
                self.__array[parent], self.__array[insert_index] = self.__array[insert_index], self.__array[parent]
                insert_index = parent
            else:
                break
        self.length += 1

    def append_with_one_assign(self, value):
        """
        添加了一项优化，就是在移动节点的时候不要交换值，而是仅仅移动父节点，在最后空出来的节点上面插入值.
        这样的好处是仅需要赋值一次。减低了算法中的常数项。
        """
        self.__array.append(value)
        insert_index = self.length
        while True:
            parent = (insert_index - 1) / 2
            # 这儿需要判断使得parent不会越界
            if parent >= 0 and value > self.__array[parent]:
                self.__array[insert_index] = self.__array[parent]
                insert_index = parent
            else:
                break
        self.__array[insert_index] = value
        self.length += 1

    def __setitem__(self, index, value):
        self.__array[index] = value

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

    @classmethod
    def heap_sort(cls, list):
        new_heap = Heap(*list)
        result = new_heap.__array
        i = len(result) - 1
        while True:
            result[0], result[i] = result[i], result[0]
            new_heap.length -= 1
            i -= 1
            if i is 2:
                break
            new_heap.loop_heapify(0)
        return result

    def pop(self, index=-1):
        node = self.__array.pop(index)
        self.length -= 1
        """这里也可以使用比较复杂的逻辑支持移动一个元素(O(lgn))，但是调用这个方法比较方便
        复杂度:O(n)
        """
        self.__build_heap()
        return node

    def pop_max(self):
        """
        这个方法仅仅支持pop首元素，因此可以直接调用loop_heapify。上面的不可以
        复杂度:O(lgn)
        """
        max_node = self.__array[0]
        self.length -= 1
        self.__array[0] = self.__array.pop()
        self.loop_heapify(0)
        return max_node


class MaxQueue(object):
    """使用堆实现最大优先堆"""

    class Node(object):
        """优先队列里面的节点"""

        def __init__(self, key, obj):
            super(MaxQueue.Node, self).__init__()
            self.key = key
            self.obj = obj

        def __str__(self):
            return "".join(["Key: ", str(self.key), "\tObject:", str(self.obj)])

        def __cmp__(self, other):
            if self.key < other.key:
                return -1
            elif self.key > other.key:
                return 1
            else:
                return 0

    def __init__(self, kargs):
        super(MaxQueue, self).__init__()
        values = [MaxQueue.Node(kargs[obj], obj) for obj in kargs]
        self.__heap = Heap(*values)
        self.length = self.__heap.length

    def max(self):
        return self.__heap[0].obj

    def pop_max(self):
        if self.length < 1:
            return None
        self.length -= 1
        return self.__heap.pop_max()

    def __setitem__(self, key, value):
        node = MaxQueue.Node(key, value)
        self.__heap.append_with_one_assign(node)

    def __str__(self):
        return str(self.__heap)


def main():
    queue = MaxQueue({16: 16, 4: 4, 10: 10, 14: 14, 7: 7, 9: 9, 3: 3, 2: 2, 8: 8, 1: 1})
    print queue
    print queue.pop_max()
    print queue
    queue[16] = 16
    print queue


if __name__ == '__main__':
    main()
