# 解决数据流中第k大（小）元素问题
# 使用heapq库 import heapq


class KthLargest:
    def __init__(self, k, nums):
        self.heap = Heap()
        self.k = k
        for num in nums:
            self.heap.push(num)
            if self.heap.size > k:
                self.heap.pop()

    def add(self, val):
        self.heap.push(val)
        if self.heap.size > self.k:
            self.heap.pop()
        return self.heap.top()


# 手写堆
class Heap:
    """
    初始化，默认创建一个小根堆
    """
    def __init__(self, desc=False):
        self.heap = []
        self.desc = desc

    @property
    def size(self):
        return len(self.heap)

    def top(self):
        if self.size:
            return self.heap[0]
        return None

    """
    添加元素
    第一步把元素加入到数组末尾
    第二步将末尾元素向上调整
    """
    def push(self, val):
        self.heap.append(val)
        self._sift_up(self.size - 1)

    """
    弹出堆顶
    第一步，记录堆顶元素的值
    第二步，交换堆顶元素与末尾元素
    第三步，删除数组末尾元素
    第四步，新的堆顶元素向下调整
    第五步，返回答案
    """
    def pop(self):
        if self.size == 0:
            raise IndexError('pop from an empty heap')
        val = self.heap[0]
        self._swap(0, self.size - 1)
        self.heap.pop()
        self._sift_down(0)
        return val

    def _smaller(self, lhs, rhs):
        return lhs > rhs if self.desc else lhs < rhs

    """
    向上调整
    如果父节点和当前节点满足交换的关系
    （对于小顶堆是父节点元素更大，对于大顶堆是父节点更小），
    则持续将当前节点向上调整
    """
    def _sift_up(self, index):
        while index:
            parent = (index - 1) // 2
            if self._smaller(self.heap[parent], self.heap[index]):
                break

            self._swap(parent, index)
            index = parent

    """
    向下调整
    如果子节点和当前节点满足交换的关系
    （对于小顶堆是子节点元素更小，对于大顶堆是子节点更大），
    则持续将当前节点向下调整
    """
    def _sift_down(self, index):
        while index * 2 + 1 < self.size:
            smallest = index
            left = index * 2 + 1
            right = index * 2 + 2

            if self._smaller(self.heap[left], self.heap[smallest]):
                smallest = left
            if right < self.size and self._smaller(self.heap[right], self.heap[smallest]):
                smallest = right

            if smallest == index:
                break

            self._swap(smallest, index)
            index = smallest

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]


if __name__ == '__main__':
    k = 3
    arr = [4, 5, 8, 2]
    kthLargest = KthLargest(k, arr)
    print(kthLargest.add(3))
    print(kthLargest.add(5))
    print(kthLargest.add(10))
    print(kthLargest.add(9))
    print(kthLargest.add(4))
