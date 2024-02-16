class Node:
    __slots__ = ["l", "r", "v"]

    def __init__(self, l, r, v):
        self.l = l
        self.r = r
        self.v = v

    def __lt__(self, other):
        return self.l < other.l

    def unpack(self):
        return self.l, self.r, self.v


class ChthollyTree:
    def __init__(self, l, r, v):
        from sortedcontainers import SortedList
        self.tree = SortedList([Node(l, r, v)])

    def split(self, pos):
        """
        在pos位置切分，返回左边界l为pos的线段下标
        """
        tree = self.tree
        p = tree.bisect_left(Node(pos, 0, 0))
        if p != len(tree) and tree[p].l == pos:
            return p
        p -= 1
        l, r, v = tree[p].unpack()
        tree[p].r = pos - 1
        tree.add(Node(pos, r, v))
        return p + 1

    def assign(self, l, r, v):
        """
        将区间[l, r]赋值为v
        """
        tree = self.tree
        p = self.split(l)
        q = self.split(r + 1)
        del tree[p:q]
        tree.add(Node(l, r, v))

    # 区间加
    def add_interval(self, l, r, v):
        tree = self.tree
        p = self.split(l)
        q = self.split(r + 1)
        for i in range(p, q):
            tree[i].v += v

    # 查询区间最小值
    def query_min(self, l, r):
        p = self.split(l)
        q = self.split(r + 1)
        return min(node.v for node in self.tree[p:q])

    # 查询区间最大值
    def query_max(self, l, r):
        p = self.split(l)
        q = self.split(r + 1)
        return max(node.v for node in self.tree[p:q])

    # 查询区间第k小值
    def query_kth(self, l, r, k):
        p = self.split(l)
        q = self.split(r + 1)
        vs = [(node.v, node.r - node.l + 1) for node in self.tree[p:q]]
        for v, d in sorted(vs):  # 逐个丢出去，缩小k
            k -= d
            if k <= 0:
                return v

    # 查询区间x次方的和
    def query_sum_of_pow(self, l, r, x):
        p = self.split(l)
        q = self.split(r + 1)
        return sum((node.r - node.l + 1) * pow(node.v, x) for node in self.tree[p:q])

    # 查询区间内等于v的个数
    def query_count_v(self, l, r, v):
        p = self.split(l)
        q = self.split(r + 1)
        return sum(node.r - node.l + 1 for node in self.tree[p:q] if node.v == v)

    # 查询区间内是否有大于v的数
    def query_has_greater_than_v(self, l, r, v):
        p = self.split(l)
        q = self.split(r + 1)
        return any(node.v > v for node in self.tree[p:q])

    # 查询所有的最大值
    def query_all_max(self):
        p = self.split(0)
        q = self.split(10 ** 9 + 1)
        return max(node.v for node in self.tree[p:q])

    # 查询所有的合并区间
    def query_all_intervals(self):
        tree = self.tree
        lines = []
        l = r = -1
        for node in tree:
            if node.v == 0:
                if l != -1:
                    lines.append([l, r])
                    l = -1
            else:
                if l == -1:
                    l = node.l
                r = node.r
        return lines


# 715. Range 模块
# https://leetcode-cn.com/problems/range-module/
class RangeModule:
    def __init__(self):
        self.tree = ChthollyTree(0, 10 ** 9, 0)

    def addRange(self, left: int, right: int) -> None:
        self.tree.assign(left, right - 1, 1)

    def queryRange(self, left: int, right: int) -> bool:
        return 1 == self.tree.query_min(left, right - 1)

    def removeRange(self, left: int, right: int) -> None:
        self.tree.assign(left, right - 1, 0)


from typing import List


# 729. 我的日程安排表 I
# https://leetcode-cn.com/problems/my-calendar-i/
class MyCalendar:
    def __init__(self):
        self.tree = ChthollyTree(0, 10 ** 9, 0)

    def book(self, start: int, end: int) -> bool:
        if self.tree.query_max(start, end - 1) == 1:
            return False
        self.tree.assign(start, end - 1, 1)
        return True


# 731. 我的日程安排表 II
# https://leetcode-cn.com/problems/my-calendar-ii/
class MyCalendarTwo:
    def __init__(self):
        self.tree = ChthollyTree(0, 10 ** 9, 0)

    def book(self, start: int, end: int) -> bool:
        if self.tree.query_has_greater_than_v(start, end - 1, 1):
            return False
        self.tree.add_interval(start, end - 1, 1)
        return True


# 732. 我的日程安排表 III
# https://leetcode-cn.com/problems/my-calendar-iii/
class MyCalendarThree:
    def __init__(self):
        self.tree = ChthollyTree(0, 10 ** 9, 0)

    def book(self, start: int, end: int) -> int:
        self.tree.add_interval(start, end - 1, 1)
        return self.tree.query_all_max()


# 699. 掉落的方块
# https://leetcode-cn.com/problems/falling-squares/
class FallingSquares:
    def __init__(self):
        self.tree = ChthollyTree(0, 10 ** 9, 0)

    def fallingSquares(self, positions: List[List[int]]) -> List[int]:
        ans = []
        for l, s in positions:
            r = l + s - 1
            h = self.tree.query_max(l, r)
            self.tree.assign(l, r, h + s)
            if not ans:
                ans.append(h + s)
            else:
                ans.append(max(ans[-1], h + s))
        return ans


# 352. 将数据流变为多个不相交区间
# https://leetcode-cn.com/problems/data-stream-as-disjoint-intervals/
class SummaryRanges:
    def __init__(self):
        self.tree = ChthollyTree(0, 10 ** 4 + 1, 0)

    def addNum(self, val: int) -> None:
        self.tree.assign(val, val, 1)

    def getIntervals(self) -> List[List[int]]:
        return self.tree.query_all_intervals()
