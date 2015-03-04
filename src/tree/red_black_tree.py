#!/usr/bin/env python
# -*- coding:UTF-8
from lib.queue import Queue
from lib.stack import Stack

__author__ = 'shenshijun'

"""
实际上，在红黑树中使用单例空节点会出现一个根本的问题：也就是父节点没法保存。这是一个大问题。
可能应该用多个对象表示，或者实现没有父节点的红黑树
"""


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
        if node is self.__root:
            self.__root = right_child
            self.__root.parent = self.Nil
        node.right = right_child_left
        right_child.parent = node.parent
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
        if node is self.__root:
            # 如果选择的正好是根节点,那么就需要宠幸设置根节点了
            self.__root = left_child
            self.__root.parent = self.Nil
        node.left = left_right_child
        left_child.parent = node.parent
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

    def __transplant(self, old, new):
        parent = old.parent
        if old is parent.left:
            parent.left = new
        else:
            parent.right = new
        if new is not self.Nil:
            new.parent = parent
        if parent is self.Nil:
            self.__root = new

    def delete(self, instance):
        node = self.__find(instance)
        if node is self.Nil:
            return node
        deleted_color = node.color
        if node.left is self.Nil:
            self.__transplant(node, node.right)
            replace_node = node.right
        elif node.right is self.Nil:
            self.__transplant(node, node.left)
            replace_node = node.left
        else:  # 后继节点移动在右子树中,因为这个时候右子树一定存在
            successor = self.__successor(instance)
            deleted_color = successor.color
            replace_node = successor.right
            if successor.parent is not node:
                self.__transplant(successor, successor.right)
                if replace_node is self.Nil:
                    replace_node.parent = successor.parent
                if successor is not self.Nil:  # 在处理的过程中不希望改变Nil的值
                    successor.right = node.right
                    successor.right.parent = successor
            self.__transplant(node, successor)
            if successor is not self.Nil:
                successor.left = node.left
                successor.left.parent = successor
                successor.color = node.color
        if not deleted_color:
            self.__delete_fixup(replace_node)
        if replace_node is self.Nil:
            replace_node.parent = None
            replace_node.left = None
            replace_node.right = None

    def __find(self, key):
        if key is None:
            raise ValueError("None value not allowed in BSTree")
        cur_node = self.__root
        while cur_node is not self.Nil and cur_node.key != key:
            if cur_node.key < key:
                cur_node = cur_node.right
            else:
                cur_node = cur_node.left
        return cur_node

    def __successor(self, value):
        find_node = self.__find(value)
        if find_node is self.Nil:
            # 处理节点不存在的情况
            return None
        if find_node.right is not self.Nil:
            return self.__min(find_node.right)
        else:
            cur_parent = find_node.parent
            cur_sub = find_node
            while cur_parent is not self.Nil and cur_parent.right is cur_sub:
                # 第一个条件是为了处理没有找到符合条件的父节点的情况,这个时候搜索失败
                cur_parent, cur_sub = cur_parent.parent, cur_parent
            return cur_parent

    def max(self):
        max_node = self.__max(self.__root)
        return max_node.value if max_node is not None else None

    def __max(self, root):
        cur_node = root
        while cur_node.right is not self.Nil:
            cur_node = cur_node.right
        return cur_node

    def __min(self, root):
        cur_node = root
        while cur_node.left is not self.Nil:
            cur_node = cur_node.left
        return cur_node

    def min(self):
        min_node = self.__min(self.__root)
        return min_node.value if min_node is not None else None

    def __delete_fixup(self, node):
        cur_node = node
        while cur_node is not self.__root and cur_node.is_black():
            parent = cur_node.parent
            if parent.left is cur_node:
                # 判断是左支还是右支,仅仅是实现所限
                brother = parent.right
                if brother.is_red():
                    # 情况一:兄弟节点是红色,则重新设色并左旋
                    brother.color = False
                    parent.color = True
                    self.__left_rotate(parent)
                    cur_node = brother
                elif brother.left.is_black() and brother.right.is_black():
                    # 情况二(1):兄弟节点和其两个子节点都是黑色.则设置兄弟节点为红色,这个时候如果parent是红色,那么循环就会退出
                    brother.color = True
                    cur_node = parent
                elif brother.right.is_black():
                    brother.color = True
                    brother.left.color = False
                    # 情况二(2):兄弟节点红和其右节点是黑色,那么意味着兄弟节点的左节点是红色,这个时候兄弟节点右旋并且父子节点交换颜色
                    self.__right_rotate(brother)
                else:
                    # 情况二(3):兄弟节点是黑色,其右节点红色(可以由前面的转换而来),这个时候兄弟节点设红,其父节点和右子节点设黑并且父节点左旋
                    parent.color = False
                    brother.color = True
                    brother.right.color = False
                    self.__left_rotate(parent)
                    # 退出情况
                    cur_node = self.__root
            else:
                brother = parent.left
                if brother.is_red():
                    brother.color = False
                    parent.color = True
                    self.__right_rotate(parent)
                elif brother.left.is_black() and brother.right.is_black():
                    brother.color = True
                    cur_node = parent
                elif brother.left.is_black():
                    brother.color = True
                    brother.right.color = False
                    self.__left_rotate(brother)
                else:
                    parent.color = False
                    brother.color = True
                    brother.left.color = False
                    self.__right_rotate(parent)
                    cur_node = self.__root
        cur_node.color = False

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
        """
        打印树的结构
        :return:
        """
        queue = Queue(self.__root)
        next_level = 1
        now_node_count = 0
        while not queue.empty():
            cur_node = queue.exit()
            print str(cur_node) + "\t",
            now_node_count += 1
            if now_node_count == next_level:
                print
                now_node_count = 0
                next_level *= 2
            if cur_node.left is not None:
                queue.enter(cur_node.left)

            if cur_node.right is not None:
                queue.enter(cur_node.right)

    def test(self):
        print self.__successor(8)

    def __str__(self):
        return "\t".join(self.midorder(lambda s: str(s)))


def main():
    tree = RedBlackTree(7, 2, 1, 5, 4, 8, 11, 14, 14, 15)
    print tree
    print tree.delete(5)
    tree.print_tree()


if __name__ == "__main__":
    main()
