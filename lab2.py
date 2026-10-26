import random
import statistics

# Исходные данные (базовый пример)
N = 200             # количество автобусов
mean_arrival = 10   # средний интервал прибытия, мин
mean_service = 15   # среднее время обслуживания, мин
seed = 42           # начальное значение генератора


def generate(N, mean_arrival, mean_service, seed):
    """Один и тот же поток автобусов для всех вариантов числа постов."""
    random.seed(seed)
    t = 0.0
    arrivals, services = [], []
    for _ in range(N):
        t += random.expovariate(1 / mean_arrival)        # момент прибытия
        arrivals.append(t)
        services.append(random.expovariate(1 / mean_service))
    return arrivals, services


def simulate(arrivals, services, posts):
    free_at = [0.0] * posts      # когда освободится каждый пост
    starts, waits = [], []
    max_queue = 0
    busy_time = 0.0
    end_time = 0.0
    for i, arrival in enumerate(arrivals):
        # сколько автобусов уже ждёт в очереди в момент прибытия
        queue = sum(1 for j in range(i) if starts[j] > arrival)
        k = min(range(posts), key=lambda j: free_at[j])  # пост, который освободится раньше
        start = max(arrival, free_at[k])
        free_at[k] = start + services[i]
        # если автобус встал в очередь, он тоже входит в её длину
        max_queue = max(max_queue, queue + 1 if start > arrival else queue)
        starts.append(start)
        waits.append(start - arrival)
        busy_time += services[i]
        end_time = max(end_time, start + services[i])
    load = busy_time / (posts * (end_time - arrivals[0])) * 100
    return {
        "avg_wait": statistics.mean(waits),
        "max_wait": max(waits),
        "max_queue": max_queue,
        "load": load,
        "served": len(arrivals),
    }


arrivals, services = generate(N, mean_arrival, mean_service, seed)
print("Постов | Ср. ожидание | Макс. ожидание | Макс. очередь | Загрузка, %")
for posts in (1, 2, 3, 4):
    r = simulate(arrivals, services, posts)
    print(f"{posts:6d} | {r['avg_wait']:12.2f} | {r['max_wait']:14.2f} | "
          f"{r['max_queue']:13d} | {r['load']:11.2f}")
