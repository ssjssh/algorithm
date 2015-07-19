#!/usr/bin/env python
# -*- coding:UTF-8
from lib.queue import Queue
from lib.stack import Stack

__author__ = 'shenshijun'


class OrderStatisticTree(object):
    """
    红黑树实现,红黑树的特性保证树的高度<=2lg(n+1),进而保证树中各个操作的性能.
    动态集合顺序统计底层使用红黑树实现，实现各个操作的复杂度都是lgn。
    每一个子树的根节点在这个子树的相对顺序是左子节点的子树大小+1。因此根节点的序是根节点的左子节点的子树大小+1。
    """

    class Node(object):
        """
        实现二叉树中的节点
        """

        def __init__(self, key, left, right, parent, color, sub_size=1):
            """
            color:true表示红色,false表示黑色
            """
            self.key = key
            self.left = left
            self.right = right
            self.parent = parent
            self.color = color
            self.sub_size = sub_size

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
                 'Red' if self.color else 'Black',
                 ', sub_size=', str(self.sub_size), ')'])

        def not_empty(self):
            return self.left is not None and self.right is not None

        def inc(self):
            if self.not_empty():
                self.sub_size += 1
            return self.sub_size

        def dec(self):
            if self.not_empty():
                self.sub_size -= 1
            return self.sub_size

        def restore_sub_size(self):
            if self.not_empty():
                self.sub_size = self.left.sub_size + self.right.sub_size + 1

    def __init__(self, *vargs):
        """"""
        self.Nil = self.Node(None, None, None, None, False, 0)  # 用Nil代替None可以简化逻辑
        self.__root = self.Nil
        self.__size = 0
        map(self.insert, vargs)

    def __len__(self):
        return self.__size

    def __left_rotate(self, node):
        """
        二叉搜索树左旋操作
        可以证明旋转并不会影响node的父节点的sub_size，所以不需要修改node的父节点
        :param node:要旋转的分支的父节点
        :return:None
        """
        right_child = node.right
        right_left_child = right_child.left
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
        node.right = right_left_child
        right_child.parent = node.parent
        node.parent = right_child
        right_child.left = node
        node.restore_sub_size()
        right_child.restore_sub_size()

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
        node.restore_sub_size()
        left_child.restore_sub_size()

    def insert(self, key):
        cur_node = self.__root
        node = self.Node(key, self.Nil, self.Nil, self.Nil, True)
        if cur_node is self.Nil:  # 根节点不存在的时候设置根节点
            self.__root = node
        else:
            parent_node = cur_node
            while cur_node is not self.Nil:
                parent_node = cur_node
                cur_node.sub_size += 1
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
        parent.sub_siz = parent.sub_size - old.sub_size + new.sub_size
        if old is parent.left:
            parent.left = new
        else:
            parent.right = new
        if new is not self.Nil:
            new.parent = parent
        if parent is self.Nil:
            self.__root = new

    def delete(self, instance):
        node = self.__walk_find(instance, lambda n: n.dec())
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
            successor = self.__walk_min(node.right, lambda n: n.dec())
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
                successor.restore_sub_size()
                successor.parent.restore_sub_size()
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

    def __walk_find(self, key, func):
        if key is None:
            raise ValueError("None value not allowed in BSTree")
        cur_node = self.__root
        while cur_node is not self.Nil and cur_node.key != key:
            func(cur_node)
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
        return self.__walk_min(root, lambda node: node)

    def __walk_min(self, root, func):
        cur_node = root
        while cur_node.left is not self.Nil:
            func(cur_node)
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

    def os_select(self, index):
        """
        类似于二分查找，只是本来应该转向左边的逻辑变成了转向左子树
        在转向右子树的时候要注意计算这个时候在右子树中的相对顺序
        本质上就是把计算每一个节点的在本树的相对序，然后和需要查找的序对比看看是不是这个节点
        :param index:
        :return:
        """
        find_rank = index
        cur_node = self.__root
        while cur_node is not self.Nil:
            cur_rank = cur_node.left.sub_size + 1
            if cur_rank == find_rank:
                return cur_node.key
            elif cur_rank < find_rank:
                cur_node = cur_node.right
                find_rank -= cur_rank
            else:
                cur_node = cur_node.left
        return cur_node.key

    def os_rank(self, value):
        cur_node = self.__root
        move_right_incr = 0
        while cur_node is not self.Nil:
            cur_rank = cur_node.left.sub_size + 1
            if cur_node.key == value:
                return cur_rank + move_right_incr
            elif cur_node.key >= value:
                cur_node = cur_node.left
            else:
                cur_node = cur_node.right
                # 在往右边移动的时候要记录下相对序和绝对序的差距
                move_right_incr += cur_rank
        return -1


def main():
    tree = OrderStatisticTree(7, 2, 1, 5, 4, 8, 11, 14, 14, 15)
    print tree.os_select(1)
    print tree.os_select(10)
    print tree.os_select(5)
    print tree.os_rank(11)


if __name__ == "__main__":
    main()
