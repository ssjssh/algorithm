#!/usr/bin/env python
# -*- coding:UTF-8
__author__ = 'shenshijun'
"""
动态规划实现活动调度的问题，每个活动都有开始和结束时间，并且有一个权，要求得使得权和最大的活动集合
"""


class Action(object):
    """
    活动对象
    """

    def __init__(self, start_time, end_time, weight):
        self.start_time = start_time
        self.end_time = end_time
        self.weight = weight

    def __cmp__(self, other):
        pass

    def __eq__(self, other):
        return self.start_time == other.start_time and self.end_time == other.end_time

    def __hash__(self):
        return hash(hash(self.start_time) * hash(self.end_time))

    def __str__(self):
        return "".join(["Action(start_time=", str(self.start_time), ",ent_time=", str(self.end_time), ",weight=",
                        str(self.weight), ")"])


__value_dict = {}
__actions_dict = {}


def max_weighted_actions(action_list):
    """
    假设Action是按照end_time排序的。因此在算法里面就不排序了。
    :param action_list:
    :return:
    """
    global __actions_dict
    global __value_dict
    action_len = len(action_list)
    # 循环退出条件
    if action_len is 0:
        return 0

    cur_max_weight = 0
    for k in xrange(action_len):
        left_max_weight = 0
        if k > 0:
            if (action_list[0], action_list[k]) not in __value_dict:
                __value_dict[(action_list[0], action_list[k])] = max_weighted_actions(
                    filter(lambda action: action.end_time <= action_list[k].start_time, action_list[:k]))
            left_max_weight = __value_dict[(action_list[0], action_list[k])]

        right_max_weight = 0
        if k < action_len - 1:
            if (action_list[k], action_list[-1]) not in __value_dict:
                __value_dict[(action_list[k], action_list[-1])] = max_weighted_actions(
                    filter(lambda action: action.start_time >= action_list[k].end_time, action_list[k + 1:]))
            right_max_weight = __value_dict[(action_list[k], action_list[-1])]

        cur_weight = left_max_weight + right_max_weight + action_list[k].weight
        if cur_max_weight < cur_weight:
            cur_max_weight = cur_weight

        __value_dict[(action_list[0], action_list[-1])] = cur_max_weight
    return __value_dict[(action_list[0], action_list[-1])]


def main():
    action_list = [Action(1, 4, 2), Action(3, 5, 1), Action(0, 6, 1), Action(5, 7, 2), Action(3, 9, 1), Action(5, 9, 1),
                   Action(6, 10, 1), Action(8, 11, 2), Action(8, 12, 1), Action(2, 14, 1), Action(2, 16, 2)]
    print(max_weighted_actions(action_list))


if __name__ == "__main__":
    main()
