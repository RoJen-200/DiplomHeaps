import math
from base import PriorityQueue

class FibonacciNode:
    """Узел фибоначчиевой кучи."""
    __slots__ = ['key', 'value', 'parent', 'child', 'left', 'right', 'degree', 'marked']

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.parent = None
        self.child = None
        # Изначально узел образует циклический список из самого себя
        self.left = self
        self.right = self
        self.degree = 0
        self.marked = False

class FibonacciHeap(PriorityQueue):
    def __init__(self):
        self._min_node = None
        self._size = 0

    def is_empty(self):
        return self._size == 0

    def _insert_into_root_list(self, node):
        """Вспомогательный метод: вставляет узел в корневой циклический список."""
        if self._min_node is None:
            self._min_node = node
            node.left = node
            node.right = node
        else:
            # Вставляем node справа от _min_node
            node.right = self._min_node.right
            node.left = self._min_node
            self._min_node.right.left = node
            self._min_node.right = node

    def _remove_from_list(self, node):
        """Вспомогательный метод: вырезает узел из его текущего циклического списка."""
        node.left.right = node.right
        node.right.left = node.left

    def insert(self, key, value):
        """Вставка за O(1) - просто добавляем в список корней."""
        node = FibonacciNode(key, value)
        self._insert_into_root_list(node)
        if node.key < self._min_node.key:
            self._min_node = node
        self._size += 1
        return node

    def find_min(self):
        return self._min_node.key if self._min_node else None

    def meld(self, other: 'FibonacciHeap'):
        """Ленивое слияние двух куч за O(1)."""
        if other.is_empty():
            return
        if self.is_empty():
            self._min_node = other._min_node
            self._size = other._size
            return

        # Сшиваем два циклических двусвязных списка
        self_min = self._min_node
        other_min = other._min_node

        self_min.right.left = other_min.left
        other_min.left.right = self_min.right
        self_min.right = other_min
        other_min.left = self_min

        if other_min.key < self_min.key:
            self._min_node = other_min

        self._size += other._size
        
        other._min_node = None
        other._size = 0

    def extract_min(self):
        """Извлечение минимума с последующей консолидацией."""
        if self.is_empty():
            return None

        z = self._min_node
        
        # 1. Переносим всех детей удаляемого минимума в корневой список
        if z.child is not None:
            child = z.child
            while True:
                next_child = child.right
                self._insert_into_root_list(child)
                child.parent = None
                if next_child == z.child:
                    break
                child = next_child

        # 2. Удаляем сам минимум из корневого списка
        self._remove_from_list(z)
        
        if z == z.right:
            self._min_node = None
        else:
            self._min_node = z.right
            self._consolidate() # Запускаем тяжелую работу только сейчас

        self._size -= 1
        return z.key, z.value

    def _link(self, y, x):
        """Делает y ребенком x."""
        self._remove_from_list(y)
        y.parent = x
        if x.child is None:
            x.child = y
            y.right = y
            y.left = y
        else:
            y.left = x.child
            y.right = x.child.right
            x.child.right.left = y
            x.child.right = y
        x.degree += 1
        y.marked = False

    def _consolidate(self):
        """Группировка деревьев одинаковой степени."""
        # Максимально возможная степень дерева в фибоначчиевой куче
        max_degree = int(math.log(self._size) * 2.08) + 2
        A = [None] * max_degree

        # Собираем все корни в отдельный массив, чтобы безопасно итерироваться,
        # так как мы будем разрывать циклический список в процессе
        roots = []
        current = self._min_node
        if current is not None:
            while True:
                roots.append(current)
                current = current.right
                if current == self._min_node:
                    break

        for w in roots:
            x = w
            d = x.degree
            while A[d] is not None:
                y = A[d]
                if x.key > y.key:
                    x, y = y, x
                self._link(y, x)
                A[d] = None
                d += 1
            A[d] = x

        # Пересобираем корневой список и находим новый минимум
        self._min_node = None
        for i in range(max_degree):
            if A[i] is not None:
                if self._min_node is None:
                    self._min_node = A[i]
                    A[i].left = A[i]
                    A[i].right = A[i]
                else:
                    self._insert_into_root_list(A[i])
                    if A[i].key < self._min_node.key:
                        self._min_node = A[i]

    def decrease_key(self, node: FibonacciNode, new_key):
        """Уменьшение ключа с каскадными срезами за амортизированное O(1)."""
        if new_key > node.key:
            raise ValueError("Новый ключ больше текущего")

        node.key = new_key
        parent = node.parent

        if parent is not None and node.key < parent.key:
            self._cut(node, parent)
            self._cascading_cut(parent)

        if node.key < self._min_node.key:
            self._min_node = node

    def _cut(self, node, parent):
        """Отрезает узел от родителя и переносит в корень."""
        if node.right == node:
            parent.child = None
        else:
            self._remove_from_list(node)
            if parent.child == node:
                parent.child = node.right
        
        parent.degree -= 1
        self._insert_into_root_list(node)
        node.parent = None
        node.marked = False

    def _cascading_cut(self, node):
        """Рекурсивно отрезает помеченные узлы вверх по дереву."""
        parent = node.parent
        if parent is not None:
            if not node.marked:
                node.marked = True
            else:
                self._cut(node, parent)
                self._cascading_cut(parent)