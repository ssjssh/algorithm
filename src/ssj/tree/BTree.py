#!/usr/bin/env python
# -*- coding:UTF-8
from ssj.lib.stack import Stack

__author__ = 'shenshijun'


class Node(object):
    def __init__(self, is_leaf, keys, childs=None, parent=None):
        """
        在真实的实现中应该在加上一个数组表示指向真实数据的指针
        keys和childs都是一个数组，分别表示关键字和孩子
        """
        self.keys = list(sorted(keys))
        self.is_leaf = is_leaf
        self.__size = len(self.keys)
        if not self.is_leaf and childs is None:
            self.childs = [None for x in xrange(0, self.__size + 1)]
        else:
            self.childs = childs
        self.parent = parent

    def __str__(self):
        return "".join(['Node(keys=', ",".join(map(lambda key: str(key), self.keys)),
                        ',Leaf' if self.is_leaf else ',Not Leaf',
                        ',childs num=', '0' if self.is_leaf else str(len(self.childs)), ')\n'])

    def __len__(self):
        return self.__size

    def append(self, key):
        """
        向B树的节点中插入一个关键字，返回这个关键字的下标
        """
        result = self.__size
        self.__size += 1

        for x in xrange(0, result):
            if self.keys[x] > key:
                self.keys.insert(x, key)
                if not self.is_leaf:
                    self.childs.insert(x, None)
                return x
        self.keys.append(key)
        if not self.is_leaf:
            self.childs.append(None)
        return result

    def search_child(self, instance):
        """
        查找小于instance的子树
        """
        for x in xrange(0, self.__size):
            if self.keys[x] > instance:
                return self.childs[x]
        return self.childs[self.__size]

    def leaf_remove(self, index):
        if self.is_leaf:
            del self.keys[index]
            self.__size -= 1


class BTree(object):
    """
    B树实现，注意，不是二叉树
    """

    def __init__(self, load_factor=4, *vargs):
        """Constructor for BTree"""
        self.__root = None
        self.__load_factor = load_factor
        self.__size = 0
        map(self.insert, vargs)

    def insert(self, key):
        """
        插入一个节点
        :param key:
        :return:
        """
        if self.__root is None:
            self.__root = Node(True, [key])
            return

        cur_node = self.__root
        while not cur_node.is_leaf:
            self.__split(cur_node)
            # 这个地方cur_node并没有被改变，所以是可以继续搜索的。
            cur_node = cur_node.search_child(key)

        left_node, right_node = self.__split(cur_node)
        if left_node is None or right_node is None:
            # 返回None表示叶节点没有满
            cur_node.append(key)
        else:
            # 找到左右节点的共同关键字
            parent_key = None
            parent = left_node.parent
            for i in xrange(len(parent)):
                if parent.childs[i] is left_node:
                    parent_key = parent.keys[i]

            if parent_key <= key:
                # 说明left_node中的所有节点都比key小，所以把新节点插入到右边
                right_node.append(key)
            else:
                left_node.append(key)

        self.__size += 1

    def __split(self, node):
        """
        在节点满的时候分裂节点。要注意两个问题：
        1，根节点分裂的时候需要重新设置根节点
        2，叶节点是没有子节点的，一次要时刻判断
        :param node:
        :return:
        """
        if self.full(node):
            parent_node = node.parent
            middle_key = node.keys[self.__load_factor - 1]
            if parent_node is None:
                # 处理根节点
                parent_node = self.__root = Node(False, [])

            parent_middle_index = parent_node.append(middle_key)
            left_node = Node(node.is_leaf, node.keys[:self.__load_factor - 1],
                             None if node.is_leaf else node.childs[:self.__load_factor],
                             parent_node)

            right_node = Node(node.is_leaf, node.keys[self.__load_factor:],
                              None if node.is_leaf else node.childs[self.__load_factor:],
                              parent_node)

            # 注意设定分裂节点的子节点的父指针，因为如果node是叶节点，那么两个子节点肯定都是叶节点，反之同理
            if not node.is_leaf:
                for child in left_node.childs:
                    if child is not None:
                        child.parent = left_node
                for child in right_node.childs:
                    if child is not None:
                        child.parent = right_node

            parent_node.childs[parent_middle_index] = left_node
            parent_node.childs[parent_middle_index + 1] = right_node
            self.__root.is_leaf = False
            return left_node, right_node
        return None, None

    def search(self, instance):
        """
        查找一个元素的位置，位置使用一个tuple表示，前面一个元素是Node，后面一个元素是元素的位置
        :param instance:
        :return:(Node, index)
        """
        return self.__search(self.__root, instance)

    def full(self, node):
        return len(node) >= (self.__load_factor * 2 - 1)

    @classmethod
    def __search(cls, root, instance):
        """
        搜索树中节点
        :param root:
        :param instance:
        :return:
        """
        cur_node = root
        while True:
            cur_len = len(cur_node)
            x = 0
            while x < cur_len and cur_node.keys[x] < instance:
                x += 1
            if x < cur_len and cur_node.keys[x] == instance:
                return cur_node, x
            elif cur_node.is_leaf:
                return None, None
            else:
                cur_node = cur_node.childs[x]

    def min(self):
        """
        取出树中最小值
        :return:
        """
        cur_node = self.__root
        while not cur_node.is_leaf:
            cur_node = cur_node.childs[0]
        return cur_node.keys[0]

    def max(self):
        """
        取出树中最大值
        :return:
        """
        cur_node = self.__root
        while not cur_node.is_leaf:
            cur_node = cur_node.childs[-1]
        return cur_node.keys[-1]

    def mid_order(self, f):
        """
        B树中序遍历
        :param f:
        :return:
        """
        result = []
        stack = Stack()
        cur_node = self.__root
        if cur_node.is_leaf:
            return map(f, cur_node.keys)

        while True:
            if cur_node.is_leaf:
                # 到叶节点了，开始把叶节点的所有关键字都遍历掉
                result.extend(map(f, cur_node.keys))
                # 开始从栈中取元素，遍历下一个节点叶节点
                if stack.empty():
                    return result
                cur_node, i = stack.pop()
                result.append(f(cur_node.keys[i]))
                if i < len(cur_node) - 1:
                    stack.push((cur_node, i + 1))
                cur_node = cur_node.childs[i + 1]
            else:
                stack.push((cur_node, 0))
                cur_node = cur_node.childs[0]
        return result

    def delete(self, key):
        """
        删除一个关键字
        :param key:
        :return:
        """
        node, index = self.search(key)
        if node is None:
            return False

        return self.__delete(node, index)

    def __delete(self, node, index):
        if node is None:
            return False

        if node.is_leaf:
            self.__size -= 1

            if self.will_starve(node):
                # 检查是否能从兄弟节点借一个元素，会检查左右两个节点。如果不能从兄弟节点借，那么就只能和兄弟节点合并了
                change_index, bro_node, bro_index = self.__check_brother_borrow(node)
                if bro_node is None:
                    del node.keys[index]

                    self.__merge_brother(node)
                else:
                    parent = node.parent
                    node.keys[index] = parent.keys[change_index]
                    parent.keys[change_index] = bro_node.keys[bro_index]
                    bro_node.leaf_remove(bro_index)
            else:
                # 删除之后节点还是有效的B树节点，因此直接从B树中删除元素
                node.leaf_remove(index)
        else:
            # 如果节点删除发生在内部节点上，那么先把后继节点上的关键字移动到被删除的元素的位置上，然后把后继节点删除
            succ, succ_index = self.__successor(node, index)
            node.keys[index] = succ.keys[succ_index]
            # 因为调用了自己，所有并没有把size减一
            return self.__delete(succ, succ_index)
        return True

    def __successor(self, node, i):
        """
        查找在node的i处的节点的关键字的后继节点,位置使用一个元祖表示，前面的一个元素是node,后面的是index
        如果返回None表示没有后继，也就是说是最大元素
        :param node:
        :param i:
        :return:(Node,index)|None
        """
        if not node.is_leaf:
            child_node = node.childs[i + 1]
            while not child_node.is_leaf:
                child_node = child_node.childs[0]
            return self.__successor(child_node, -1)
        else:
            if i < len(node) - 1:
                return node, i + 1
            else:
                return None, None

    def will_starve(self, node):
        """
        检查一个节点的元素是否小于load_factor,这样的话如果在删除一个关键字节点就不符合B树的节点定义了
        :param node:
        :return:
        """
        return len(node) < self.__load_factor

    def successor(self, key):
        """
        查找关键字的后继节点,位置使用一个元祖表示，前面的一个元素是node,后面的是index
        如果返回None表示没有后继，也就是说是最大元素
        :param key:
        :return:(Node,index)|None
        """
        node, index = self.search(key)
        if node is None:
            return None, None
        return self.__successor(node, index)

    def __str__(self):
        return "\n".join(self.mid_order(lambda s: str(s)))

    def test(self):
        node = self.successor('0')
        print(node)

    def __check_brother_borrow(self, node):
        """
        检查左右的兄弟节点是否能够借出节点
        int:父节点中交换元素的位置
        Node:要借出元素的节点
        int：借出元素的位置

        如果不能借出，那么返回(None,None,None)
        :param node:
        :return:(int,Node,int)|(None,None,None)
        """
        parent = node.parent
        node_index = -1
        # 寻找node在parent的位置
        for i in xrange(len(parent.childs)):
            if parent.childs[i] is node:
                node_index = i

        # 先从左边的兄弟节点借
        if node_index >= 1 and not self.will_starve(parent.childs[node_index - 1]):
            return node_index - 1, parent.childs[node_index - 1], -1

        if node_index >= 0 and not self.will_starve(parent.childs[node_index + 1]):
            return node_index, parent.childs[node_index + 1], 0

        return None, None, None

    def __merge_brother(self, node):
        parent = node.parent
        if parent is self.__root and len(parent.keys) > 0:
            return

        node_index = -1
        # 寻找node在parent的位置
        for i in xrange(len(parent.childs)):
            if parent.childs[i] is node:
                node_index = i

        # 合并只和长度较小的节点合并
        smaller_node = None
        is_left = True
        if node_index >= 1:
            smaller_node = parent.childs[node_index - 1]

        if node_index >= 0 and (smaller_node is None or len(smaller_node) > parent.childs[node_index + 1]):
            smaller_node = parent.childs[node_index + 1]
            is_left = False

        # 只有在必要的时候才合并
        if len(smaller_node) < self.__load_factor - 1 or len(node) < self.__load_factor - 1:
            if is_left:
                new_keys = smaller_node.keys
                new_keys.append(parent.keys[node_index - 1])
                new_keys.extend(node.keys)
            else:
                new_keys = node.keys
                new_keys.append(parent.keys[node_index - 1])
                new_keys.extend(smaller_node.keys)

            new_childs = None
            if not node.is_leaf:
                if is_left:
                    new_childs = smaller_node.childs
                    new_childs.extend(node.childs)
                else:
                    new_childs = node.childs
                    new_childs.extend(smaller_node.childs)

            new_node = Node(node.is_leaf, new_keys, new_childs, parent)

            # 从父节点中删除被拿到子节点的节点
            if is_left:
                del parent.childs[node_index - 1]
                del parent.keys[node_index - 1]
                parent.childs[node_index - 1] = new_node
            else:
                del parent.childs[node_index + 1]
                del parent.keys[node_index + 1]
                parent.childs[node_index] = new_node

            # 处理根节点,然后调用递归调用合并父节点
            if parent is self.__root and len(parent.keys):
                new_node.parent = None
                self.__root = new_node
            else:
                self.__merge_brother(parent)


def main():
    import random
    test = ['O', 'J', 'S', 'Y', 'C', 'M', 'B', 'R', 'N', 'F', 'L', 'Z', 'U', 'Q', 'A', 'G', 'V', 'E', 'D', 'W', 'I',
            'H', 'T', 'K', 'X', 'P']

    random.shuffle(test)
    btree = BTree(3, *test)
    print(btree.delete('O'))
    print(btree)


if __name__ == "__main__":
    main()
