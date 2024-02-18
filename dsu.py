class Dsu:
    def __init__(self, n):
        self.pa = list(range(n, n * 2)) * 2
        self.rank = [1] * n * 2

    def find(self, x):
        if self.pa[x] == x:
            return x
        self.pa[x] = self.find(self.pa[x])
        return self.pa[x]

    def union(self, x, y):
        xr, yr = self.find(x), self.find(y)
        if xr == yr:
            return
        if self.rank[xr] < self.rank[yr]:
            xr, yr = yr, xr
        self.pa[yr] = xr
        self.rank[xr] += self.rank[yr]

    def erase(self, x):
        self.rank[self.find(x)] -= 1
        self.pa[x] = x

    def move(self, x, y):
        fx, fy = self.find(x), self.find(y)
        if fx == fy:
            return
        self.pa[x] = fy
        self.rank[fx] -= 1
        self.rank[fy] += 1
