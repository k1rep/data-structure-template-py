import heapq


# huffman-tree-node
class Node:
    def __init__(self, char=None, freq=None):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


# huffman-tree
class HuffmanTree:
    def __init__(self, char_weights):
        self.leaves = [Node(char, freq) for char, freq in char_weights]
        heapq.heapify(self.leaves)  # 初始化优先队列
        while len(self.leaves) > 1:
            left = heapq.heappop(self.leaves)
            right = heapq.heappop(self.leaves)
            merged = Node(freq=(left.freq + right.freq))
            merged.left = left
            merged.right = right
            heapq.heappush(self.leaves, merged)
        self.root = self.leaves[0]

    # 左0右1编码
    def _encode(self, node, prefix='', code=None):
        if code is None:
            code = {}
        if node is not None:
            if node.char is not None:
                code[node.char] = prefix
            self._encode(node.left, prefix + '0', code)
            self._encode(node.right, prefix + '1', code)
        return code

    def get_code(self):
        return self._encode(self.root)


if __name__ == '__main__':
    char_weights = [('a', 5), ('b', 9), ('c', 12), ('d', 13), ('e', 16), ('f', 45)]
    tree = HuffmanTree(char_weights)
    codes = tree.get_code()
    for character, coden in codes.items():
        print(f'{character}: {coden}')
