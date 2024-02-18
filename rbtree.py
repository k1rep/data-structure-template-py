class Node:
    def __init__(self, data, color="red"):
        self.data = data
        self.parent = None
        self.left = None
        self.right = None
        self.color = color


class RBTree:
    def __init__(self):
        self.TNULL = Node(None, color="black")  # TNULL是颜色为黑的NULL节点
        self.root = self.TNULL
        self.TNULL.left = self.TNULL
        self.TNULL.right = self.TNULL

    """
          parent
          /    
         x     
        / \
       lx   y
           /  \
          ly   ry
    """
    def __rotate_left(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y

    def __rotate_right(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
            y.right.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y

        y.right = x
        x.parent = y

    def __fix_insert(self, k):
        while k.parent.color == "red":
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left
                if u.color == "red":
                    u.color = "black"
                    k.parent.color = "black"
                    k.parent.parent.color = "red"
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.__rotate_right(k)
                    k.parent.color = "black"
                    k.parent.parent.color = "red"
                    self.__rotate_left(k.parent.parent)
            else:
                u = k.parent.parent.right

                if u.color == "red":
                    u.color = "black"
                    k.parent.color = "black"
                    k.parent.parent.color = "red"
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.__rotate_left(k)
                    k.parent.color = "black"
                    k.parent.parent.color = "red"
                    self.__rotate_right(k.parent.parent)
            if k == self.root:
                break
        self.root.color = "black"

    def insert(self, key):
        node = Node(key)
        node.parent = None
        node.data = key
        node.left = self.TNULL
        node.right = self.TNULL
        node.color = "red"

        y = None
        x = self.root

        while x != self.TNULL:
            y = x
            if node.data < x.data:
                x = x.left
            else:
                x = x.right

        node.parent = y
        if y is None:
            self.root = node
        elif node.data < y.data:
            y.left = node
        else:
            y.right = node

        if node.parent is None:
            node.color = "black"
            return

        if node.parent.parent is None:
            return

        self.__fix_insert(node)

    def __transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def __minimum(self, node):
        while node.left != self.TNULL:
            node = node.left
        return node

    def __fix_delete(self, x):
        while x != self.root and x.color == "black":
            if x == x.parent.left:
                s = x.parent.right
                if s.color == "red":
                    s.color = "black"
                    x.parent.color = "red"
                    self.__rotate_left(x.parent)
                    s = x.parent.right

                if s.left.color == "black" and s.right.color == "black":
                    s.color = "red"
                    x = x.parent
                else:
                    if s.right.color == "black":
                        s.left.color = "black"
                        s.color = "red"
                        self.__rotate_right(s)
                        s = x.parent.right

                    s.color = x.parent.color
                    x.parent.color = "black"
                    s.right.color = "black"
                    self.__rotate_left(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == "red":
                    s.color = "black"
                    x.parent.color = "red"
                    self.__rotate_right(x.parent)
                    s = x.parent.left

                if s.right.color == "black" and s.left.color == "black":
                    s.color = "red"
                    x = x.parent
                else:
                    if s.left.color == "black":
                        s.right.color = "black"
                        s.color = "red"
                        self.__rotate_left(s)
                        s = x.parent.left

                    s.color = x.parent.color
                    x.parent.color = "black"
                    s.left.color = "black"
                    self.__rotate_right(x.parent)
                    x = self.root
        x.color = "black"

    def __delete_node_helper(self, node, key):
        z = self.TNULL
        while node != self.TNULL:
            if node.data == key:
                z = node

            if node.data <= key:
                node = node.right
            else:
                node = node.left

        if z == self.TNULL:
            print("Couldn't find key in the tree")
            return

        y = z
        y_original_color = y.color
        if z.left == self.TNULL:
            x = z.right
            self.__transplant(z, z.right)
        elif z.right == self.TNULL:
            x = z.left
            self.__transplant(z, z.left)
        else:
            y = self.__minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.__transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self.__transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == "black":
            self.__fix_delete(x)

    def delete_node(self, data):
        self.__delete_node_helper(self.root, data)

    def inorder(self, node):
        if node != self.TNULL:
            self.inorder(node.left)
            print(node.data, end=" ")
            self.inorder(node.right)

    def preorder(self, node):
        if node != self.TNULL:
            print(node.data, end=" ")
            self.preorder(node.left)
            self.preorder(node.right)

    def postorder(self, node):
        if node != self.TNULL:
            self.postorder(node.left)
            self.postorder(node.right)
            print(node.data, end=" ")

    def levelorder(self, node):
        if node is self.TNULL:
            return
        q = [node]
        while len(q) > 0:
            print(q[0].data, end=" ")
            node = q.pop(0)
            if node.left is not self.TNULL:
                q.append(node.left)
            if node.right is not self.TNULL:
                q.append(node.right)


if __name__ == "__main__":
    rbt = RBTree()

    rbt.insert(55)
    rbt.insert(40)
    rbt.insert(65)
    rbt.insert(60)
    rbt.insert(75)
    rbt.insert(57)
    rbt.insert(58)

    rbt.delete_node(55)
    rbt.delete_node(40)
    rbt.delete_node(65)

    print("Inorder Traversal of the tree")
    rbt.inorder(rbt.root)
    print()
    print("Preorder Traversal of the tree")
    rbt.preorder(rbt.root)
    print()
    print("Postorder Traversal of the tree")
    rbt.postorder(rbt.root)
    print()
    print("Levelorder Traversal of the tree")
    rbt.levelorder(rbt.root)
    print()
