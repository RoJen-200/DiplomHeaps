import matplotlib.pyplot as plt
import numpy as np

def plot_dijkstra_results():
    """График для макро-бенчмарка (Дейкстра) - Раздел 4.4"""
    labels = ['Разреженный граф\n(E/V = 10)', 'Плотный граф\n(E/V = 250)']
    
    # Данные из Таблицы 4.4
    bh_times = [0.0033, 0.0031]
    fh_times = [0.0125, 0.0591]
    ph_times = [0.0094, 0.0532]

    x = np.arange(len(labels))
    width = 0.25

    fig, ax = plt.subplots(figsize=(8, 6))
    rects1 = ax.bar(x - width, bh_times, width, label='Биномиальная куча (BH)', color='#4C72B0')
    rects2 = ax.bar(x, fh_times, width, label='Фибоначчиева куча (FH)', color='#DD8452')
    rects3 = ax.bar(x + width, ph_times, width, label='Парная куча (PH)', color='#55A868')

    ax.set_ylabel('Время выполнения, сек', fontsize=12)
    ax.set_title('Результаты алгоритма Дейкстры (V=1000)', fontsize=14, pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=11)
    ax.legend(fontsize=11)
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    fig.tight_layout()
    plt.savefig('dijkstra_chart.png', dpi=300)
    print("График Дейкстры сохранен как 'dijkstra_chart.png'")

def plot_cache_locality():
    """График для кэш-локальности (Малые графы) - Раздел 4.3"""
    # Данные из Таблицы 4.3
    sizes = [100, 500, 1000]
    bh_lat = [0.0020, 0.0024, 0.0027]
    fh_lat = [0.0020, 0.0020, 0.0021]
    ph_lat = [0.0010, 0.0016, 0.0016]

    fig, ax = plt.subplots(figsize=(8, 6))
    
    ax.plot(sizes, bh_lat, marker='o', linewidth=2, markersize=8, label='Биномиальная куча (BH)', color='#4C72B0')
    ax.plot(sizes, fh_lat, marker='s', linewidth=2, markersize=8, label='Фибоначчиева куча (FH)', color='#DD8452')
    ax.plot(sizes, ph_lat, marker='^', linewidth=2, markersize=8, label='Парная куча (PH)', color='#55A868')

    ax.set_xlabel('Количество элементов (n)', fontsize=12)
    ax.set_ylabel('Средняя латентность операции, мс', fontsize=12)
    ax.set_title('Латентность базовых операций на малых объемах данных', fontsize=14, pad=15)
    ax.set_xticks(sizes)
    ax.legend(fontsize=11)
    ax.grid(linestyle='--', alpha=0.7)

    fig.tight_layout()
    plt.savefig('cache_chart.png', dpi=300)
    print("График кэш-локальности сохранен как 'cache_chart.png'")

if __name__ == "__main__":
    plot_dijkstra_results()
    plot_cache_locality()