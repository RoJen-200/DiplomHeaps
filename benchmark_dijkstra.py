import time
import gc
import json
import random
from binomial import BinomialHeap
from fibonacci import FibonacciHeap
from pairing import PairingHeap

def generate_graph(V, E, seed=42):
    """Генерирует взвешенный ориентированный граф (список смежности)."""
    random.seed(seed)
    adj = {i: [] for i in range(V)}
    
    # Гарантируем базовую связность (путь 0 -> 1 -> ... -> V-1)
    for i in range(V - 1):
        adj[i].append((i + 1, random.randint(1, 100)))
        
    edges_added = V - 1
    # Добиваем случайными ребрами до нужной плотности
    while edges_added < E:
        u = random.randint(0, V - 1)
        v = random.randint(0, V - 1)
        if u != v:
            adj[u].append((v, random.randint(1, 100)))
            edges_added += 1
            
    return adj

def run_dijkstra_benchmark(V, E, runs=5):
    heap_classes = [BinomialHeap, FibonacciHeap, PairingHeap]
    results = {}
    
    # Генерируем один и тот же граф для честного сравнения всех куч
    adj = generate_graph(V, E, seed=42)
    
    for heap_class in heap_classes:
        times = []
        for _ in range(runs):
            gc.collect()
            gc.disable()
            
            # --- Начало алгоритма Дейкстры ---
            start_time = time.perf_counter()
            
            heap = heap_class()
            nodes_map = {}
            distances = {i: float('inf') for i in range(V)}
            distances[0] = 0
            
            # Инициализация кучи всеми вершинами
            for i in range(V):
                node = heap.insert(distances[i], i)
                nodes_map[i] = node
                
            while True:
                res = heap.extract_min()
                if res is None:
                    break
                    
                current_dist, u = res
                
                # Удаляем посещенную вершину из словаря
                if u in nodes_map:
                    del nodes_map[u]
                    
                if current_dist == float('inf'):
                    break
                    
                # Релаксация ребер (вызов decrease_key)
                for v, weight in adj[u]:
                    if v in nodes_map: # Если сосед еще в куче
                        new_dist = current_dist + weight
                        if new_dist < distances[v]:
                            distances[v] = new_dist
                            heap.decrease_key(nodes_map[v], new_dist)
                            
            end_time = time.perf_counter()
            # --- Конец алгоритма ---
            
            gc.enable()
            times.append(round(end_time - start_time, 4))
            
        # Медиана для отсева системного шума
        sorted_times = sorted(times)
        results[heap_class.__name__] = sorted_times[len(sorted_times) // 2]
        
    return results

if __name__ == "__main__":
    print("Запуск макро-бенчмарка (Дейкстра)...")
    
    # Сценарий 1 (Н1): Разреженный граф (V=1000, E=10000). E/V = 10.
    print("Генерация разреженного графа...")
    sparse_res = run_dijkstra_benchmark(V=1000, E=10000)
    
    # Сценарий 2 (Н3): Экстремально плотный граф (V=1000, E=250000). 
    # Здесь E/V = 250, что в точности равно V/4 (1000/4 = 250).
    print("Генерация экстремально плотного графа...")
    dense_res = run_dijkstra_benchmark(V=1000, E=250000)
    
    final_results = {
        "Sparse_H1": sparse_res,
        "Dense_H3": dense_res
    }
    
    print("\nРезультаты:")
    print(json.dumps(final_results, indent=4))