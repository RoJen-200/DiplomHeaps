import random
import time
import gc
from binomial import BinomialHeap
from fibonacci import FibonacciHeap
from pairing import PairingHeap

def generate_operations(num_operations, seed=42):
    random.seed(seed)
    operations = []
    inserted_nodes = []
    
    initial_inserts = num_operations // 2
    for _ in range(initial_inserts):
        key = random.randint(1, 1000000)
        operations.append(('insert', key, f"val_{key}"))
        inserted_nodes.append(key)
        
    for _ in range(num_operations - initial_inserts):
        chance = random.random()
        if chance < 0.3 and inserted_nodes:
            operations.append(('extract_min', None, None))
        elif chance < 0.6 and inserted_nodes:
            target = random.choice(inserted_nodes)
            new_key = target - random.randint(1, 50)
            operations.append(('decrease_key', target, new_key))
        else:
            key = random.randint(1, 1000000)
            operations.append(('insert', key, f"val_{key}"))
            inserted_nodes.append(key)
            
    return operations

def run_benchmark(heap_class, operations):
    dummy_heap = heap_class()
    for i in range(1000):
        dummy_heap.insert(i, "warmup")
        
    heap = heap_class()
    nodes_map = {}
    
    gc.disable()
    start_time = time.perf_counter()
    
    for op, arg1, arg2 in operations:
        if op == 'insert':
            node = heap.insert(arg1, arg2)
            nodes_map[arg1] = node
            
        elif op == 'extract_min':
            res = heap.extract_min()
            # ИСПРАВЛЕНИЕ: Уничтожаем "зомби"
            # Удаляем извлеченный узел из словаря, чтобы decrease_key его больше не трогал
            if res is not None:
                extracted_key, _ = res
                if extracted_key in nodes_map:
                    del nodes_map[extracted_key]
                    
        elif op == 'decrease_key':
            node = nodes_map.get(arg1)
            if node and arg2 < node.key:
                heap.decrease_key(node, arg2)
                # Обновляем словарь, так как ключ узла изменился
                del nodes_map[arg1]
                nodes_map[arg2] = node 
                
    end_time = time.perf_counter()
    gc.enable()
    
    return round(end_time - start_time, 4)

def main():
    print("Генерация 50,000 операций...")
    ops = generate_operations(50000, seed=42)
    
    heaps = [BinomialHeap, FibonacciHeap, PairingHeap]
    print("\n--- Запуск Бенчмарка ---")
    
    for heap in heaps:
        time_taken = run_benchmark(heap, ops)
        print(f"{heap.__name__:<15}: {time_taken:.4f} сек.")

if __name__ == "__main__":
    main()