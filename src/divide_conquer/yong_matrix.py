#!/usr/bin/env python 
# -*- coding:utf-8 -*-



def extract_min(matrix, w, h):
    """
    算法按照阶梯的形式走下去总体的复杂度是:O(n+m)
    """
    min_node = matrix[0]
    empty_index = 0
    while True:
        left = empty_index + w
        right = empty_index + 1
        # 1，矩阵碰到右边界的时候
        # 2，右边的值是None，表示没有元素
        print "left :", left
        print "right :", right
        if left > (w * h - 1) and right % w is 0:
            matrix[empty_index] = None
            break

        if left <= (w * h - 1) and (right % w is 0 or matrix[right] is None or matrix[left] <= matrix[right]):
            matrix[empty_index] = matrix[left]
            empty_index = left
        # 1，判断矩阵碰到左边界的时候
        # 2，左边的值是None，表示值是None
        elif left > (w * h - 1) or matrix[left] is None or matrix[left] > matrix[right]:
            matrix[empty_index] = matrix[right]
            empty_index = right
        # 到最终节点的时候
        else:
            matrix[empty_index] = None
            break
    return min_node


def main():
    young_matrix = [i for i in xrange(1, 26)]
    weight = 5
    height = 5
    # print young_matrix[25]
    extract_min(young_matrix, weight, height)
    min_node = extract_min(young_matrix, weight, height)
    print young_matrix


if __name__ == '__main__':
    main()
