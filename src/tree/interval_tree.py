#!/usr/bin/env python
# -*- coding:UTF-8
from lib.queue import Queue
from lib.stack import Stack

__author__ = 'shenshijun'


class Node(object):
    """
    实现二叉树中的节点
    """

    def __init__(self, low, high, sub_max, left, right, parent, color):
        """
        color:true表示红色,false表示黑色
        """
        self.left = left
        self.right = right
        self.parent = parent
        self.color = color
        self.low = low
        self.high = high
        self.sub_max = sub_max

    def __cmp__(self, other):
        return cmp(self.low, other.low)

    def __eq__(self, other):
        return (self.low == other.low) and (other.sub_max == self.sub_max)

    def is_red(self):
        return self.color

    def is_black(self):
        return not self.color

    def __str__(self):
        return "".join(
            ["Node(low=", str(self.low), ',high=', str(self.high), ',max=', str(self.sub_max), ", color=",
             'Red)' if self.color else 'Black)'])

    def restore_max(self):
        if self.not_empty():
            self.sub_max = max([self.left.sub_max, self.right.sub_max])

    def not_empty(self):
        return self.left is not None and self.right is not None

    @property
    def key(self):
        return self.low, self.high


class IntervalTree(object):
    """
    用红黑树实现区间树
    """

    def __init__(self, *vargs):

        """
        使用元组(low,high)来表示一个区间
        """
        self.Nil = Node(None, None, None, None, None, None, False)  # 用Nil代替None可以简化逻辑
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
        node.restore_max()
        right_child.restore_max()

    def __right_rotate(self, node):
        """
        二叉搜索树右旋操作
        可以证明除了涉及到的两个节点，局部局部特性没有被破坏，全局的的特性则在插入或者删除的过程中维护
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
        node.restore_max()
        left_child.restore_max()

    def insert(self, key):
        cur_node = self.__root
        node = Node(key[0], key[1], key[1], self.Nil, self.Nil, self.Nil, True)
        if cur_node is self.Nil:  # 根节点不存在的时候设置根节点
            self.__root = node
        else:
            parent_node = cur_node
            while cur_node is not self.Nil:
                parent_node = cur_node
                # 插入过程中同时维护最大值，这样就不用在插入之后维护最大值了
                if node.high > cur_node.sub_max:
                    cur_node.sub_max = node.high

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
        return parent

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
                replace_node.parent = successor.parent
                if successor is not self.Nil:  # 在处理的过程中不希望改变Nil的值
                    successor.right = node.right
                    successor.right.parent = successor
            self.__transplant(node, successor)
            if successor is not self.Nil:
                successor.left = node.left
                successor.left.parent = successor
                successor.color = node.color
        print "replace node : %s" % replace_node
        print "replace parent node：%s" % replace_node.parent
        self.__fix_sub_max(replace_node)
        if not deleted_color:
            self.__delete_fixup(replace_node)
        if replace_node is self.Nil:
            replace_node.parent = None
            replace_node.left = None
            replace_node.right = None

    def __fix_sub_max(self, node):
        parent_node = node
        while parent_node is not None:
            parent_node.restore_max()
            if parent_node is self.__root:
                break
            parent_node = parent_node.parent

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
                uncle = parent.right
                if uncle.is_red():
                    # 情况一:叔节点是红色,则重新设色并左旋
                    uncle.color = False
                    parent.color = True
                    self.__left_rotate(parent)
                elif uncle.left.is_black() and uncle.right.is_black():
                    # 情况二(1):叔节点和其两个子节点都是黑色.则设置叔节点为红色,这个时候如果parent是红色,那么循环就会退出
                    uncle.color = True
                    cur_node = parent
                elif uncle.right.is_black():
                    uncle.color = True
                    uncle.left.color = False
                    # 情况二(2):叔节点红和其右节点是黑色,那么意味着叔节点的左节点是红色,这个时候叔节点右旋并且父子节点交换颜色
                    self.__right_rotate(uncle)
                else:
                    # 情况二(3):叔节点是黑色,其右节点红色(可以由前面的转换而来),这个时候叔节点设红,其父节点和右子节点设黑并且父节点左旋
                    parent.color = False
                    uncle.color = True
                    uncle.right.color = False
                    self.__left_rotate(parent)
                    # 退出情况
                    cur_node = self.__root
            else:
                uncle = parent.left
                if uncle.is_red():
                    uncle.color = False
                    parent.color = True
                    self.__right_rotate(parent)
                elif uncle.left.is_black() and uncle.right.is_black():
                    uncle.color = True
                    cur_node = parent
                elif uncle.left.is_black():
                    uncle.color = True
                    uncle.right.color = False
                    self.__left_rotate(uncle)
                else:
                    parent.color = False
                    uncle.color = True
                    uncle.left.color = False
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
    tree = IntervalTree((16, 21), (8, 9), (5, 8), (15, 23), (0, 3), (6, 10), (25, 30), (17, 19), (26, 26), (19, 20))
    print tree
    print tree.delete((25, 30))
    tree.print_tree()


if __name__ == "__main__":
    main()
