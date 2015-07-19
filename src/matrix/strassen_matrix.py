#!/usr/bin/env python
# -*- coding:utf-8 -*-
import copy

"""
使用了strassen矩阵乘法。复杂度是n**lg7。
可以处理一个细节：如果矩阵的规模不是偶数的时候，给矩阵添加一行一列都是0的行，在计算的最后去掉就可以了。
例如：
1 2 3 0
4 5 6 0
7 8 9 0
0 0 0 0 
"""


class Matrix(object):
    def __init__(self, height, weight, matrix=None):
        if matrix is None:
            self.__height = 0
            self.__weight = 0
            self.__matrix = []
        else:
            self.__height = height
            self.__weight = weight
            self.__matrix = matrix

    def com_op(self, other, op):
        if other.__weight != self.__weight or other.__height != self.__height:
            raise ValueError("when do common operations on matrixs,two matrix must have equal lenght and weight")
        if other.__matrix is None or self.__matrix is None:
            raise ValueError("matrix is Empty")
        else:
            result = [[] for i in xrange(0, self.__weight)]
            for x in xrange(0, self.__weight):
                for y in xrange(0, self.__height):
                    result[x].append(op(self.__matrix[x][y], other.__matrix[x][y]))
        return Matrix(self.__height, self.__weight, result)

    def __add__(self, other):
        return self.com_op(other, lambda x, y: x + y)

    def __sub__(self, other):
        return self.com_op(other, lambda x, y: x - y)

    def __str__(self):
        return "".join(
            ["weight:", str(self.__weight), "\theight:", str(self.__height), "\nmatrix:\n", str(self.__matrix)])

    def __mul__(self, other):
        if self.__weight != other.__height:
            raise ValueError("muti matrix must have equal weight and height with other matrix")
        elif self.__weight is 0:
            return []
        return self.__strassen_method(other)

    @classmethod
    def __add_zero(cls, obj):
        """
        处理矩阵的长宽不是偶数的情况，在矩阵没有变化的时候返回原矩阵，变化了则是一个新的矩阵
        """
        if obj.__weight % 2 is 1 or obj.__height % 2 is 1:
            result = copy.copy(obj.__matrix)
            weight = obj.__weight
            height = obj.__height
            if obj.__weight % 2 is 1:
                result.append([0 for x in xrange(0, obj.__height)])
                weight = weight + 1

            if obj.__height % 2 is 1:
                height += 1
                for x in xrange(0, weight):
                    result[x].append(0)
            return Matrix(height, weight, result)
        else:
            return obj

    @classmethod
    def __divide_matrix(cls, obj):
        arr = Matrix.__add_zero(obj).__matrix
        arr11 = copy.deepcopy(arr[:obj.__weight / 2])
        for col in arr11:
            col[:] = col[:obj.__height / 2]
        arr12 = copy.deepcopy(arr[obj.__weight / 2:])
        for col in arr12:
            col[:] = col[:obj.__height / 2]
        arr21 = copy.deepcopy(arr[:obj.__weight / 2])
        for col in arr21:
            col[:] = col[obj.__height / 2:]
        arr22 = copy.deepcopy(arr[obj.__weight / 2:])
        for col in arr22:
            col[:] = col[obj.__height / 2:]
        divide_len = obj.__weight / 2
        divide_height = obj.__height / 2
        return (Matrix(divide_len, divide_height, arr11), Matrix(divide_len, divide_height, arr12),
                Matrix(divide_len, divide_height, arr21), Matrix(divide_len, divide_height, arr22))

    @classmethod
    def __combine_matrix(cls, m11, m12, m21, m22):
        result = copy.copy(m11.__matrix)
        result.extend(m21.__matrix)
        for x in xrange(0, m11.__weight + m21.__weight):
            temp = m12[x] if x < m11.__weight else m22[x]
            result[x].extend(temp)
        return Matrix(m11.__weight + m12.__weight, m11.__height + m21.__height, result)

    def __strassen_method(self, other):
        # 首先需要保证矩阵可以分割
        a11, a12, a21, a22 = Matrix.__divide_matrix(self)
        b11, b12, b21, b22 = Matrix.__divide_matrix(other)
        # print b11
        # print b12
        # print b21
        # print b22
        s1 = b12 - b22
        s2 = a11 + a12
        s3 = a21 + a22
        s4 = b21 - b11
        s5 = a11 + a22
        s6 = b11 + b22
        s7 = a12 - a22
        s8 = b21 + b22
        s9 = a11 - a21
        s10 = b11 + b12
        print "a11*s1"
        print a11
        print s1
        p1 = a11 * s1
        print "p1: %s" % p1
        p2 = s2 * b22
        p3 = s3 * b11
        p4 = a22 * s4
        p5 = s5 * s6
        p6 = s7 * s8
        p7 = s9 * s10
        c11 = p5 + p4 - p2 + p6
        c12 = p1 + p2
        c21 = p3 + p4
        c22 = p5 + p1 - p3 - p7
        return Matrix.__combine_matrix(c11, c12, c21, c22)


def main():
    a = Matrix(2, 2, [[1, 7], [3, 5]])
    b = Matrix(2, 2, [[6, 4], [8, 2]])
    # print a+b
    # print a-b
    print a * b


if __name__ == '__main__':
    main()
