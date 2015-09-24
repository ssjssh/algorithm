#!/usr/bin/env python
# -*- coding:UTF-8
__author__ = 'shenshijun'
import random


class Node(object):
    """"""

    def __init__(self, value, prev, next, up, down):
        """
        跳跃表中元素的节点
        """
        self.value = value
        self.prev = prev
        self.next = next
        self.up = up
        self.down = down

    def __str__(self):
        return "".join(["Node(value=%s)" % self.value])

    def __cmp__(self, other):
        return cmp(self.value, other.value)

    def __eq__(self, other):
        return self.value == other.value

    def have_down(self):
        return self.down is not None

    def have_next(self):
        return self.next is not None

    def have_up(self):
        return self.up is not None

    def have_prev(self):
        return self.prev is not None


class SkipList(object):
    """
    跳跃表实现,跳跃表实现了lgn的各种操作,足以替代平衡树
    """

    def __init__(self, *vargs):
        """
        """
        self.__top = self.head_node()
        self.__levels = 0  # 跳跃表中层的个数
        self.__size = 0
        self.__lists = [self.__top]
        map(self.insert, vargs)

    def insert(self, value):
        self.__size += 1
        node = self.node(value)
        cur_node = self.__top
        while True:
            if cur_node is not None and cur_node <= node:
                # 一直往右走直到大于这一层的节点为止
                prev_node = cur_node
                cur_node = cur_node.next
            elif prev_node.have_down():
                # 在一层走到尽头的时候进入下一层
                cur_node = prev_node.down
            else:
                # prev就是现在需要插入节点的位置
                self.__insert_node(prev_node, None, node)
                self.__insert_to_up(node)
                break

    def __insert_to_up(self, node):
        up_count = self.up(self.__levels + 1)
        down_node = node
        # 从第一层开始插入,因为在最底层已经把这个元素插入了
        if up_count > self.__levels:  # 添加一个新的层级
            self.__levels = up_count
            new_top = self.head_node()
            self.__top.up = new_top
            new_top.down = self.__top
            self.__top = new_top
            self.__lists.append(self.__top)

        now_level = 0
        while now_level < up_count:  # 在存在的等级上面插入元素
            now_node = self.node(node.value)
            up_node = self.prev_up_node(down_node)
            self.__insert_node(up_node, down_node, now_node)
            down_node = now_node
            now_level += 1

    def get(self, value):
        node = self.__search(value)
        return node.value if node is not None else node

    def delete(self, value):
        node = self.__search(value)
        while True:
            self.delete_node(node)
            if node.up is not None:
                node = node.up
            elif node.down is not None:
                node = node.down
            else:
                break
        return node.value if node is not None else None

    @classmethod
    def delete_node(cls, node):
        prev_node = node.prev
        next_node = node.next
        if prev_node is not None:
            prev_node.next = next_node
        if next_node is not None:
            next_node.prev = prev_node

    def __search(self, value):
        cur_node = self.__top
        while True:
            if cur_node is not None and cur_node.value <= value:
                # 一直往右走直到大于这一层的节点为止
                prev_node = cur_node
                cur_node = cur_node.next
                if prev_node.value == value:
                    return prev_node
            elif prev_node.have_down():
                # 在一层走到尽头的时候进入下一层
                cur_node = prev_node.down
            else:
                # 既不能右行也不能下行的时候查询失败
                return None

    @classmethod
    def __insert_node(cls, prev_node, down_node, node):
        next_node = prev_node.next
        node.next = next_node
        prev_node.next = node
        node.prev = prev_node
        if next_node is not None:
            next_node.prev = node
        node.down = down_node
        if down_node is not None:
            down_node.up = node

    @classmethod
    def prev_up_node(cls, node):
        """
        方法的目的是找到某一层一个节点的上一层的最近的一个节点
        :param node:
        :return:
        """
        cur_node = node
        while not cur_node.have_up():
            cur_node = cur_node.prev
        return cur_node.up

    @classmethod
    def up(cls, max_len):
        """
        判断需要把一个节点移动到第几层的随机函数
        :return:
        """
        judge_count = max_len
        count = 0
        while judge_count > 0 and random.choice([0, 1]) is 1:
            count += 1
            judge_count -= 1
        return count

    @classmethod
    def head_node(cls):
        return Node(float('-inf'), None, None, None, None)

    @classmethod
    def node(cls, value):
        return Node(value, None, None, None, None)

    def __len__(self):
        return self.__size

    def __str__(self):
        result = []
        cur_level = 0
        for head in self.__lists:
            cur_node = head
            cur_level_result = ['levels %s: ' % cur_level]
            while cur_node is not None:
                cur_level_result.append(str(cur_node))
                cur_node = cur_node.next
            result.append("\t".join(cur_level_result))
            cur_level += 1
        return "\n".join(reversed(result))


def main():
    skip_list = SkipList(1, 23, 429, 0, 1, 2, 3, 1928, 29)
    print skip_list
    print skip_list.get(429)
    print skip_list.delete(429)
    print "after delete"
    print skip_list


if __name__ == "__main__":
    main()
