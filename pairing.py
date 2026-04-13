from base import PriorityQueue

class PairingNode:
    __slots__ = ['key', 'value', 'child', 'sibling', 'prev']

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.child = None
        self.sibling = None
        self.prev = None

class PairingHeap(PriorityQueue):
    def __init__(self):
        self._root = None
        self._size = 0

    def is_empty(self):
        return self._root is None

    def _link(self, first: PairingNode, second: PairingNode) -> PairingNode:
        if second is None: return first
        if first is None: return second

        if first.key <= second.key:
            second.prev = first
            first.sibling = second.sibling
            if first.sibling is not None:
                first.sibling.prev = first
            second.sibling = first.child
            if second.sibling is not None:
                second.sibling.prev = second
            first.child = second
            return first
        else:
            second.prev = first.prev
            first.prev = second
            first.sibling = second.child
            if first.sibling is not None:
                first.sibling.prev = first
            second.child = first
            return second

    def insert(self, key, value):
        node = PairingNode(key, value)
        if self._root is None:
            self._root = node
        else:
            self._root = self._link(self._root, node)
        self._size += 1
        return node

    def meld(self, other: 'PairingHeap'):
        if other.is_empty(): return
        if self.is_empty():
            self._root = other._root
            self._size = other._size
            return

        self._root = self._link(self._root, other._root)
        self._size += other._size
        other._root = None
        other._size = 0

    def find_min(self):
        return self._root.key if self._root else None

    def _merge_pairs(self, first_sibling: PairingNode) -> PairingNode:
        if first_sibling is None or first_sibling.sibling is None:
            return first_sibling

        tree_array = []
        current = first_sibling
        while current is not None:
            tree_array.append(current)
            next_sib = current.sibling
            current.sibling = None 
            current = next_sib

        i = 0
        while i + 1 < len(tree_array):
            tree_array[i] = self._link(tree_array[i], tree_array[i + 1])
            i += 2

        last = i if i < len(tree_array) else i - 2
        result = tree_array[last]
        for j in range(last - 2, -1, -2):
            result = self._link(tree_array[j], result)

        return result

    def extract_min(self):
        if self.is_empty(): return None
        
        min_node = self._root
        if min_node.child is None:
            self._root = None
        else:
            self._root = self._merge_pairs(min_node.child)
            if self._root is not None:
                self._root.prev = None
                
        self._size -= 1
        return min_node.key, min_node.value

    def decrease_key(self, node: PairingNode, new_key):
        if new_key > node.key:
            raise ValueError("Новый ключ больше текущего")
        node.key = new_key
        if node == self._root:
            return

        if node.prev.child == node:
            node.prev.child = node.sibling
        else:
            node.prev.sibling = node.sibling
            
        if node.sibling is not None:
            node.sibling.prev = node.prev

        node.sibling = None
        node.prev = None

        self._root = self._link(self._root, node)