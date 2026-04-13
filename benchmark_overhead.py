import json
from binomial import BinomialHeap
from fibonacci import FibonacciHeap
from pairing import PairingHeap

# Импортируем ваши функции тестирования [cite: 1667]
from benchmark import run_benchmark, generate_operations

def benchmark_fh_overhead(num_operations=50000, runs=10):
    heap_classes = [BinomialHeap, FibonacciHeap, PairingHeap]
    results = {cls.__name__: [] for cls in heap_classes}
    
    # Фиксированный seed для честного сравнения [cite: 1638]
    operations = generate_operations(num_operations, seed=42)
    
    for heap_class in heap_classes:
        for _ in range(runs):
            res = run_benchmark(heap_class, operations)
            results[heap_class.__name__].append(res)
            
    # Вычисляем медиану [cite: 1755]
    median_results = {}
    for name, times in results.items():
        sorted_times = sorted(times)
        median_results[name] = sorted_times[len(sorted_times) // 2]
        
    return median_results

if __name__ == "__main__":
    print("Запуск бенчмарка базового оверхеда (H2)...")
    overhead_results = benchmark_fh_overhead()
    print(json.dumps(overhead_results, indent=4))