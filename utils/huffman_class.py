class HuffNode:

    def __init__(self, value:int=None) -> None:
        self.value = value
        self.left = None
        self.right = None
        self.isLeaf = False

    def __lt__(self, other):
        return self.value < other.value
    
    def __repr__(self) -> str:
        return "<value:{} left:{} right:{}>".format(self.value, self.left, self.right)

    def search(self, code):
        cur = self
        idx = 0
        n = len(code)
        while idx < n:
            if code[idx] == "0":
                cur = cur.left
            else:
                cur = cur.right

            if cur.isLeaf:
                yield cur.left
                cur = self
            
            idx += 1

