import json
from binomial import BinomialHeap
from fibonacci import FibonacciHeap
from pairing import PairingHeap

# Импортируем базовые функции стенда
from benchmark import run_benchmark, generate_operations

def benchmark_cache_locality(sizes=[100, 500, 1000], runs=10):
    """
    Тестирование влияния кэш-локальности на малых данных (H5).
    Запускаем смешанную нагрузку для n <= 1000.
    """
    heap_classes = [BinomialHeap, FibonacciHeap, PairingHeap]
    results = {}

    for size in sizes:
        results[size] = {}
        # Генерируем фиксированную последовательность для заданного размера
        ops = generate_operations(size, seed=42)
        
        for heap_class in heap_classes:
            times = []
            for _ in range(runs):
                # Запускаем бенчмарк (прогрев внутри уже работает)
                res = run_benchmark(heap_class, ops)
                times.append(res)
            
            # Берем медианное суммарное время для отсева шума
            sorted_times = sorted(times)
            median_total = sorted_times[len(sorted_times) // 2]
            
            # Вычисляем среднюю латентность одной операции в миллисекундах
            latency_ms = (median_total / size) * 1000
            results[size][heap_class.__name__] = round(latency_ms, 5)

    return results

if __name__ == "__main__":
    print("Запуск бенчмарка кэш-локальности (H5)...")
    cache_results = benchmark_cache_locality()
    print(json.dumps(cache_results, indent=4))