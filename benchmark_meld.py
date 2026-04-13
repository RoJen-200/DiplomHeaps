import time
import gc
import json

# Импортируем ваши структуры данных
from binomial import BinomialHeap
from fibonacci import FibonacciHeap
from pairing import PairingHeap

def benchmark_cascading_meld(K=1000, heap_size=10, runs=10):
    heap_classes = [BinomialHeap, FibonacciHeap, PairingHeap]
    results = {cls.__name__: [] for cls in heap_classes}

    for heap_class in heap_classes:
        for run in range(runs):
            gc.collect()
            gc.disable() # Отключаем сборщик мусора [cite: 1661]
            
            # Подготовка K независимых куч 
            heaps = []
            for i in range(K):
                h = heap_class()
                for j in range(heap_size):
                    key = (i * heap_size + j) % 50 
                    h.insert(key, f"val_{i}_{j}")
                heaps.append(h)
            
            # Измерение времени слияния
            main_heap = heaps[0]
            start_time = time.perf_counter()
            
            for i in range(1, K):
                main_heap.meld(heaps[i])
                
            end_time = time.perf_counter()
            gc.enable()
            
            results[heap_class.__name__].append(round(end_time - start_time, 6))

    # Вычисляем медиану [cite: 1755]
    median_results = {}
    for name, times in results.items():
        sorted_times = sorted(times)
        median_results[name] = sorted_times[len(sorted_times) // 2]

    return median_results

if __name__ == "__main__":
    print("Запуск cascading-meld бенчмарка (H4)...")
    meld_results = benchmark_cascading_meld()
    print(json.dumps(meld_results, indent=4))