from pairing import PairingHeap

def main():
    print("=== Тестирование Парной кучи ===")
    heap = PairingHeap()
    
    # Вставляем элементы и сохраняем ссылки на узлы
    print("Добавляем задачи: A(10), B(20), C(5), D(15)")
    node_a = heap.insert(10, "Task A")
    node_b = heap.insert(20, "Task B")
    node_c = heap.insert(5, "Task C")
    node_d = heap.insert(15, "Task D")
    
    print(f"Текущий минимум (должен быть 5): {heap.find_min()}")
    
    # Применяем Decrease Key
    print("\nУменьшаем ключ 'Task B' с 20 до 2...")
    heap.decrease_key(node_b, 2)
    
    print(f"Новый минимум (должен быть 2): {heap.find_min()}")
    
    # Извлекаем элементы до опустошения
    print("\nИзвлекаем все элементы по порядку:")
    while not heap.is_empty():
        key, val = heap.extract_min()
        print(f"Извлечено: Ключ={key}, Значение={val}")
        
    print("Куча пуста. Тест успешно завершен!")

if __name__ == "__main__":
    main()