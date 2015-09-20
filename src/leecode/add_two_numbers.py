#!/usr/bin/env python
# -*- coding:UTF-8
__author__ = 'shenshijun'
"""
You are given two linked lists representing two non-negative numbers. The digits are stored in reverse order and each of their nodes contain a single digit. Add the two numbers and return it as a linked list.

Input: (2 -> 4 -> 3) + (5 -> 6 -> 4)
Output: 7 -> 0 -> 8
"""


class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution(object):
    def __addUpDigit(self, node, up_digit):
        last_node = None
        while node is not None and up_digit > 0:
            node.val += up_digit
            if node.val >= 10:
                node.val -= 10
                up_digit = 1
            else:
                up_digit = 0
            last_node = node
            node = node.next
        if up_digit > 0 and last_node:
            last_node.next = ListNode(up_digit)

    def addTwoNumbers(self, l1, l2):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """
        cur_l1 = l1
        cur_l2 = l2
        last_l1 = None
        last_up_digit = 0
        while cur_l1 is not None and cur_l2 is not None:
            this_val = cur_l1.val + cur_l2.val + last_up_digit
            if this_val >= 10:
                cur_l1.val = this_val - 10
                last_up_digit = 1
            else:
                cur_l1.val = this_val
                last_up_digit = 0
            last_l1 = cur_l1
            cur_l1 = cur_l1.next
            cur_l2 = cur_l2.next

        if cur_l1 is None and cur_l2 is None and last_up_digit > 0 and last_l1 is not None:
            last_l1.next = ListNode(last_up_digit)
        self.__addUpDigit(cur_l1, last_up_digit)
        self.__addUpDigit(cur_l2, last_up_digit)

        # 如果l1比较短,需要把l2长的部分合并到l1后面
        if cur_l2 is not None:
            if last_l1 is None:
                return l2
            else:
                last_l1.next = cur_l2

        return l1


def main():
    pass


if __name__ == "__main__":
    main()
