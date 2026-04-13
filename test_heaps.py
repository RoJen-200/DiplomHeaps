import pytest
from binomial import BinomialHeap
from fibonacci import FibonacciHeap
from pairing import PairingHeap

# Список всех наших куч для массовой проверки
HEAP_CLASSES = [BinomialHeap, FibonacciHeap, PairingHeap]

@pytest.mark.parametrize("heap_class", HEAP_CLASSES)
def test_heap_sort_order(heap_class):
    """Проверка правильности извлечения элементов по возрастанию (свойство min-heap)."""
    heap = heap_class()
    elements = [(45, "A"), (12, "B"), (90, "C"), (3, "D"), (22, "E")]
    
    # Вставляем элементы
    for key, val in elements:
        heap.insert(key, val)
        
    # Проверяем, что минимум найден верно без извлечения
    assert heap.find_min() == 3
    
    # Извлекаем все элементы и сохраняем ключи
    extracted = []
    while not heap.is_empty():
        key, val = heap.extract_min()
        extracted.append(key)
        
    # Проверяем, что они вышли в строгом порядке возрастания
    assert extracted == [3, 12, 22, 45, 90], f"Ошибка сортировки в {heap_class.__name__}"

@pytest.mark.parametrize("heap_class", [FibonacciHeap, PairingHeap])
def test_decrease_key_logic(heap_class):
    """Проверка корректности работы decrease_key и обновления минимума."""
    heap = heap_class()
    
    # Сохраняем ссылки на узлы при вставке
    node1 = heap.insert(50, "Task 1")
    node2 = heap.insert(30, "Task 2")
    node3 = heap.insert(40, "Task 3")
    
    # Текущий минимум должен быть 30
    assert heap.find_min() == 30
    
    # Искусственно делаем узел с ключом 50 самым приоритетным (меняем на 10)
    heap.decrease_key(node1, 10)
    
    # Теперь новый минимум должен быть 10
    assert heap.find_min() == 10
    
    # Извлекаем этот минимум и проверяем
    key, val = heap.extract_min()
    assert key == 10 and val == "Task 1"
    
    # После извлечения десятки, следующим минимумом снова должна стать 30
    assert heap.find_min() == 30