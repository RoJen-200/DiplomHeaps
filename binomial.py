from base import PriorityQueue

class BinomialNode:
    """Узел биномиальной кучи."""
    __slots__ = ['key', 'value', 'parent', 'child', 'sibling', 'degree']

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.parent = None
        self.child = None
        self.sibling = None
        self.degree = 0

class BinomialHeap(PriorityQueue):
    def __init__(self):
        self._roots = []  
        self._min_node = None
        self._size = 0

    def is_empty(self):
        return self._size == 0
        
    def _link(self, min_node, other_node):
        """Связывает два дерева одинаковой степени."""
        other_node.parent = min_node
        other_node.sibling = min_node.child
        min_node.child = other_node
        min_node.degree += 1

    def insert(self, key, value):
        """Вставка: создаем новую кучу из 1 элемента и делаем meld."""
        node = BinomialNode(key, value)
        temp_heap = BinomialHeap()
        temp_heap._roots = [node]
        temp_heap._size = 1
        temp_heap._min_node = node
        self.meld(temp_heap)
        return node

    def find_min(self):
        return self._min_node.key if self._min_node else None

    def meld(self, other):
        """Слияние двух куч."""
        if other.is_empty():
            return
        
        # Сливаем списки корней
        self._roots.extend(other._roots)
        self._size += other._size
        
        # Запускаем консолидацию для восстановления инвариантов
        self._consolidate()
        
        other._roots = []
        other._size = 0

    def _consolidate(self):
        """Группировка деревьев с одинаковой степенью."""
        if not self._roots:
            self._min_node = None
            return

        # Вспомогательный массив для группировки по степеням
        max_degree = int(self._size ** 0.5) + 5 # С запасом
        A = [None] * max_degree

        for x in self._roots:
            d = x.degree
            while A[d] is not None:
                y = A[d]
                if x.key > y.key:
                    x, y = y, x
                self._link(x, y)
                A[d] = None
                d += 1
            A[d] = x

        # Собираем новые корни и находим новый минимум
        self._roots = []
        self._min_node = None
        for node in A:
            if node is not None:
                self._roots.append(node)
                if self._min_node is None or node.key < self._min_node.key:
                    self._min_node = node

    def extract_min(self):
        """Извлечение минимума."""
        if self.is_empty():
            return None
        
        min_node = self._min_node
        self._roots.remove(min_node)
        
        # Математически, при удалении корня размер кучи всегда уменьшается ровно на 1
        self._size -= 1
        
        # Дети удаленного узла становятся новыми корнями
        child = min_node.child
        kids = []
        while child is not None:
            child.parent = None
            next_sibling = child.sibling
            child.sibling = None
            kids.append(child)
            child = next_sibling
            
        # Восстановление порядка: степени должны идти по возрастанию
        kids.reverse()
            
        # Напрямую добавляем детей в массив корней и принудительно запускаем консолидацию
        self._roots.extend(kids)
        self._consolidate()
        
        return min_node.key, min_node.value

    def decrease_key(self, node, new_key):
        """Оставим на потом, для Дейкстры"""
        pass