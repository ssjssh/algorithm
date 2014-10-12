#!/usr/bin/env python 
#-*- coding:utf-8 -*-

def partition(li,start,end):
	x=li[start]
	i=start
	j=end
	while True:
		while li[j]>x:
			j-=1

		while li[i]<x:
			i+=1

		if i<j:
			li[i],li[j]=li[j],li[i]
		else:
			return j

def quick_sort(li,start,end):
	li_len=end-start
	if li_len<2:
		return li
	middle=partition(li,start,end)
	quick_sort(li,start,middle-1)
	quick_sort(li,middle+1,end)
	return li

def main():
	li=[13,19,9,5,12,8,7,4,11,2,6,21]
	# print partition(li,0,11)
	# print li
	print quick_sort(li,0,11)

if __name__ == '__main__':
	main()