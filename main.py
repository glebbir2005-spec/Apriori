import sys
import time
import matplotlib.pyplot as plt
from apriori import apriori
from load_dataset import load_dataset
from collections import defaultdict

def visualize_results(thresholds, exec_times, length_counts_by_threshold):
    exec_times_ms = [t * 1000 for t in exec_times]

    plt.figure(figsize=(10, 5))
    plt.plot(thresholds, exec_times_ms, marker='o', linestyle='-', color='b', linewidth=2, markersize=8)
    plt.title('Зависимость времени выполнения от порога поддержки', fontsize=14)
    plt.xlabel('Порог поддержки (%)', fontsize=12)
    plt.ylabel('Время выполнения (мс)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(thresholds)
    plt.tight_layout()
    plt.savefig('execution_time_chart.png')
    plt.show()

    all_lengths = set()
    for counts in length_counts_by_threshold.values():
        all_lengths.update(counts.keys())
    all_lengths = sorted(list(all_lengths))

    plt.figure(figsize=(12, 6))
    x_indexes = list(range(len(thresholds)))
    
    num_lengths = len(all_lengths)
    total_width = 0.8
    bar_width = total_width / num_lengths if num_lengths > 0 else total_width

    for i, length in enumerate(all_lengths):
        counts = [length_counts_by_threshold[t].get(length, 0) for t in thresholds]
        
        offset = (i - num_lengths / 2 + 0.5) * bar_width
        x_pos = [x + offset for x in x_indexes]
        
        plt.bar(x_pos, counts, width=bar_width, label=f'Длина {length}', alpha=0.8)

    plt.title('Количество частых наборов различной длины при разных порогах', fontsize=14)
    plt.xlabel('Порог поддержки (%)', fontsize=12)
    plt.ylabel('Количество найденных наборов', fontsize=12)
    plt.xticks(x_indexes, thresholds)
    plt.legend(title="Размер набора")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('itemsets_length_chart.png')
    plt.show()


def run_experiments():
    filename = 'baskets.csv'
    
    print("Загрузка данных...")
    transactions = load_dataset(filename)
    print(f"Всего загружено транзакций: {len(transactions)}\n")
    
    thresholds = [1, 3, 5, 10, 15]

    execution_times = []
    itemsets_by_length = {}
    
    for threshold in thresholds:
        print(f"{'='*40}")
        print(f"Запуск алгоритма: Порог поддержки = {threshold}%")
        
        start_time = time.perf_counter()
        
        raw_results = apriori(transactions, threshold)
        
        end_time = time.perf_counter()
        exec_time = end_time - start_time
        
        print(f"Найдено частых наборов: {len(raw_results)}")
        print(f"Время выполнения алгоритма: {exec_time:.6f} секунд")

        execution_times.append(exec_time)
        
        length_counts = defaultdict(int)
        for itemset, supp in raw_results:
            length_counts[len(itemset)] += 1
        itemsets_by_length[threshold] = dict(length_counts)

        length_counts = defaultdict(int)
        for itemset, supp in raw_results:
            length_counts[len(itemset)] += 1
        itemsets_by_length[threshold] = dict(length_counts)
        
        formatted_results = []
        for itemset, supp in raw_results:
            sorted_itemset = tuple(sorted(list(itemset)))
            formatted_results.append((sorted_itemset, supp))
            
        formatted_results.sort(key=lambda x: -x[1])
        
        output_filename = f"apriori_results_{threshold}pct.txt"
        with open(output_filename, 'w', encoding='utf-8') as out_file:
            out_file.write(f"=== Результаты алгоритма Apriori ===\n")
            out_file.write(f"Порог поддержки: {threshold}%\n")
            out_file.write(f"Всего найдено частых наборов: {len(formatted_results)}\n")
            out_file.write(f"Чистое время выполнения: {exec_time:.6f} сек.\n")
            out_file.write("="*40 + "\n\n")
            
            out_file.write("--- Сортировка по убыванию поддержки ---\n")
            for itemset, supp in formatted_results:
                itemset_str = "{" + ", ".join(itemset) + "}"
                out_file.write(f"Набор: {itemset_str:<30} | Поддержка: {supp:.2f}%\n")
                
        print(f"Результаты сохранены в файл: {output_filename}")
    
    print(f"\n{'='*40}")
    print("Все эксперименты завершены!")

    visualize_results(thresholds, execution_times, itemsets_by_length)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')
    run_experiments()