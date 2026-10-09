import sys
import time
from apriori import apriori
from load_dataset import load_dataset


def run_experiments():
    filename = 'baskets.csv'
    
    print("Загрузка данных...")
    transactions = load_dataset(filename)
    print(f"Всего загружено транзакций: {len(transactions)}\n")
    
    thresholds = [1, 3, 5, 10, 15]
    
    for threshold in thresholds:
        print(f"{'='*40}")
        print(f"Запуск алгоритма: Порог поддержки = {threshold}%")
        
        start_time = time.perf_counter()
        
        raw_results = apriori(transactions, threshold)
        
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        
        print(f"Найдено частых наборов: {len(raw_results)}")
        print(f"Время выполнения алгоритма: {execution_time:.6f} секунд")
        
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
            out_file.write(f"Чистое время выполнения: {execution_time:.6f} сек.\n")
            out_file.write("="*40 + "\n\n")
            
            out_file.write("--- Сортировка по убыванию поддержки ---\n")
            for itemset, supp in formatted_results:
                itemset_str = "{" + ", ".join(itemset) + "}"
                out_file.write(f"Набор: {itemset_str:<30} | Поддержка: {supp:.2f}%\n")
                
        print(f"Результаты сохранены в файл: {output_filename}")
    
    print(f"\n{'='*40}")
    print("Все эксперименты завершены!")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')
    run_experiments()