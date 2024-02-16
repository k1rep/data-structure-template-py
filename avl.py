class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1  # 节点的初始高度设置为1


class AVLTree:
    def __init__(self):
        self.root = None

    # 获取树的高度
    def height(self, node):
        if not node:
            return 0
        return node.height

    # 获取树的平衡因子
    def get_balance(self, node):
        if not node:
            return 0
        return self.height(node.left) - self.height(node.right)

    # 右旋转
    def right_rotate(self, z):
        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        z.height = 1 + max(self.height(z.left), self.height(z.right))
        y.height = 1 + max(self.height(y.left), self.height(y.right))

        return y

    # 左旋转
    def left_rotate(self, z):
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self.height(z.left), self.height(z.right))
        y.height = 1 + max(self.height(y.left), self.height(y.right))

        return y

    # 插入节点
    def insert(self, root, key):
        # 标准的BST插入
        if not root:
            return Node(key)
        elif key < root.key:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)

        root.height = 1 + max(self.height(root.left), self.height(root.right))

        balance = self.get_balance(root)

        # 左旋转
        if balance > 1 and key < root.left.key:
            return self.right_rotate(root)

        # 右旋转
        if balance < -1 and key > root.right.key:
            return self.left_rotate(root)

        # 左右旋转
        if balance > 1 and key > root.left.key:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # 右左旋转
        if balance < -1 and key < root.right.key:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root


if __name__ == '__main__':
    avl = AVLTree()
    root = None
    keys = [10, 20, 30, 40, 50, 25]
    for key in keys:
        root = avl.insert(root, key)
    print('根节点的键值为: %d' % root.key)
