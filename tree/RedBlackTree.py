#!/usr/bin/env python
# -*- coding:UTF-8
__author__ = 'shenshijun'

from tree.BSTree import Stack


class RedBlackTree(object):
    """
    红黑树实现,红黑树的特性保证树的高度<=2lg(n+1),进而保证树中各个操作的性能.
    """

    class Node(object):
        """
        实现二叉树中的节点
        """

        def __init__(self, key, left, right, parent, color):
            """
            color:true表示红色,false表示黑色
            """
            self.key = key
            self.left = left
            self.right = right
            self.parent = parent
            self.color = color

        def __cmp__(self, other):
            return cmp(self.key, other.key)

        def __eq__(self, other):
            return (self.key == other.key) and (other.color == self.color)

        def is_red(self):
            return self.color

        def is_black(self):
            return not self.color

        def __str__(self):
            return "".join(
                ["Node(key=", str(self.key), ", color=",
                 'Red)' if self.color else 'Black)'])

    def __init__(self, *vargs):
        """"""
        self.Nil = self.Node(None, None, None, None, False)  # 用Nil代替None可以简化逻辑
        self.__root = self.Nil
        self.__size = 0
        map(self.insert, vargs)

    def __len__(self):
        return self.__size

    def __left_rotate(self, node):
        """
        二叉搜索树左旋操作
        :param node:要旋转的分支的父节点
        :return:None
        """
        right_child = node.right
        right_child_left = right_child.left
        parent = node.parent
        if right_child is self.Nil:
            raise NotImplementedError("没有右叶节点不支持左旋转")

        # 判断node是parent的左节点还是右节点
        if parent is not self.Nil:
            if parent.left is node:
                parent.left = right_child
            else:
                parent.right = right_child
        else:
            self.__root = right_child
        node.right = right_child_left
        node.parent = right_child
        right_child.left = node

    def __right_rotate(self, node):
        """
        二叉搜索树右旋操作
        :param node:要被旋转的分子的父节点
        :return:None
        """
        left_child = node.left
        left_right_child = left_child.right
        parent = node.parent
        if left_child is self.Nil:
            raise NotImplementedError('没有左节点不支持右旋转')
        # 判断这个节点是在父节点的那个分支上
        if parent is not self.Nil:
            if parent.left is node:
                parent.left = left_child
            else:
                parent.right = left_child
        else:
            # 如果选择的正好是根节点,那么就需要宠幸设置根节点了
            self.__root = left_child
        node.left = left_right_child
        left_child.right = node
        node.parent = left_child

    def insert(self, key):
        cur_node = self.__root
        node = self.Node(key, self.Nil, self.Nil, self.Nil, True)
        if cur_node is self.Nil:  # 根节点不存在的时候设置根节点
            self.__root = node
        else:
            parent_node = cur_node
            while cur_node is not self.Nil:
                parent_node = cur_node
                if cur_node >= node:
                    cur_node = cur_node.left
                else:
                    cur_node = cur_node.right
            if parent_node >= node:
                parent_node.left = node
            else:
                parent_node.right = node
            node.parent = parent_node
            self.__insert_fixup(node)

    def __insert_fixup(self, node):
        # 首先判断节点是不是根节点或者父节点是不是根节点
        if node.parent is self.Nil or node.parent.parent is self.Nil:
            self.__root.color = False
            return

        cur_node = node
        while cur_node.parent.is_red():
            # 首先需要分清父节点在哪个分支
            parent_node = cur_node.parent
            grand_node = parent_node.parent
            if parent_node is grand_node.left:
                if grand_node.right.is_red():  # 情况1:只需要调整颜色,祖父节点设置成红色,父节点和叔节点设置成黑色,满足了特性3
                    grand_node.color = True
                    parent_node.color = False
                    grand_node.right.color = False
                    cur_node = grand_node  # 这个时候只有祖父节点可能会违反特性3,所有再调节这个节点
                elif parent_node.right is cur_node:  # 情况2:需要左旋
                    self.__left_rotate(parent_node)
                    cur_node = parent_node  # 左旋之后,父节点一定会违背特性3,所以需要调节父节点
                else:  # 情况3:右旋加重新设色
                    grand_node.color = True
                    parent_node.color = False
                    self.__right_rotate(grand_node)
                    break
            else:  # 和上面的情况类似,只是这个时候所有的操作都反了
                if grand_node.left.is_red():
                    grand_node.color = True
                    parent_node.color = False
                    grand_node.left.color = False
                    cur_node = grand_node
                elif parent_node.left is cur_node:
                    self.__right_rotate(parent_node)
                    cur_node = parent_node
                else:
                    grand_node.color = True
                    parent_node.color = False
                    self.__left_rotate(grand_node)
                    break
        self.__root.color = False  # 根节点必须被设置为黑色

    def __delete__(self, instance):
        pass

    def __delete_fixup(self, node):
        pass

    def midorder(self, f):
        """
        中序遍历
        :param f:访问一个节点的时候要对节点进行处理的函数
        :return:
        """
        result = []
        stack = Stack(self.__root)
        cur_node = self.__root.left
        # 第一个阶段首先把所有树左边的节点放进栈里,这个时候并不遍历
        # 第二个阶段的时候由于左节点遍历了之后,再遍历右节点
        while not stack.empty() or cur_node is not self.Nil:
            # 第二个判断条件比较重要,因为如果根节点没有左子树,这个时候栈就是空的,会直接退出循环
            if cur_node is not self.Nil:
                stack.push(cur_node)
                cur_node = cur_node.left
            else:
                cur_node = stack.pop()
                result.append(f(cur_node))
                cur_node = cur_node.right
        return result

    def print_tree(self):
        print self.__root
        print self.__root.left
        print self.__root.right
        self.__right_rotate(self.__root)
        print "after rotate"
        print self.__root
        print self.__root.right
        print self.__root.parent

    def __str__(self):
        return "\t".join(self.midorder(lambda s: str(s)))


def main():
    tree = RedBlackTree(7, 2, 1, 5, 4, 8, 11, 14, 15)
    print tree


if __name__ == "__main__":
    main()
