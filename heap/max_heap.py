
class Heap(object):
	"""最大二叉堆实现"""
	def __init__(self, *arg):
		super(Heap, self).__init__()
		self.__array=arg
		self.length=len(arg)
		self.__make_heap()

	@classmethod
	def make_heap(cls,li):
		return Heap(*li)

	def __make_heap(self):
		pass


	def __heapify(self,parent):
		"""
			
		"""
		largest=parent
		left=parent*2+1
		right=parent*2+2
		if left<self.length and self.__array[parent]<self.__array[left]:
			largest=left

		if right<self.length and self.__array[largest]<self.__array[right]:
			largest=right

		#保证在父元素就是最大值的时候不要移动元素
		if largest!= parent:
			self.__array[largest],self.__array[parent]=self.__array[parent],self.__array[largest]
			self.__heapify(largest)

		