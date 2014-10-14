#!/usr/bin/env python
#-*- coding:utf-8

"""
计数排序算法复杂度是O(n+k)，因此在k比较小的时候算法的性能比较好。
计数排序只适用于有明确范围的类型比较，比如整数。但是也可以比较位
"""
def count_sort(li,k):
	result=[0 for i in li]
	rank=[0 for i in xrange(0,k)]
	for x in li:
		rank[x]+=1

	for i in xrange(1,k):
		rank[i]+=rank[i-1]

	for x in li:
		result[rank[x]-1]=x
		rank[x]-=1
	return result


def main():
	print count_sort([1,6,2,1,2,5,4,1,5,6,1,2,4,3],7)

if __name__ == '__main__':
	main()