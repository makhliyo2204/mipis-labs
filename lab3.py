import random
import statistics

# Исходные данные варианта (здесь базовый пример)
N = 220             # количество объектов
mean_arrival = 9    # средний интервал поступления, мин
mean_control = 14   # среднее время контроля, мин
p_defect = 0.10     # вероятность несоответствия
seed = 203          # начальное значение генератора


def generate(N, mean_arrival, mean_control, p_defect, seed):
    """Один и тот же поток объектов для всех вариантов числа постов."""
    random.seed(seed)
    t = 0.0
    objects = []
    for _ in range(N):
        t += random.expovariate(1 / mean_arrival)        # момент прибытия
        control_time = random.expovariate(1 / mean_control)
        defect = random.random() < p_defect              # несоответствие
        objects.append((t, control_time, defect))
    return objects


def simulate(objects, posts):
    free_at = [0.0] * posts      # когда освободится каждый пост
    starts, waits, queue_at_arrival = [], [], []
    busy_time = 0.0
    end_time = 0.0
    for i, (arrival, control_time, defect) in enumerate(objects):
        # сколько объектов ждёт в очереди в момент прибытия
        queue = sum(1 for j in range(i) if starts[j] > arrival)
        queue_at_arrival.append(queue)
        k = min(range(posts), key=lambda j: free_at[j])  # пост, который освободится раньше
        start = max(arrival, free_at[k])
        free_at[k] = start + control_time
        starts.append(start)
        waits.append(start - arrival)
        busy_time += control_time
        end_time = max(end_time, start + control_time)
    load = busy_time / (posts * (end_time - objects[0][0])) * 100
    return {
        "avg_wait": statistics.mean(waits),
        "max_wait": max(waits),
        "max_queue": max(queue_at_arrival),
        "load": load,
        "checked": len(objects),
        "defects": sum(1 for o in objects if o[2]),
    }


objects = generate(N, mean_arrival, mean_control, p_defect, seed)
print("Постов | Ср. ожидание | Макс. ожидание | Макс. очередь | Загрузка, % | Несоответствия")
for posts in (1, 2, 3, 4):
    r = simulate(objects, posts)
    print(f"{posts:6d} | {r['avg_wait']:12.2f} | {r['max_wait']:14.2f} | "
          f"{r['max_queue']:13d} | {r['load']:11.2f} | {r['defects']:14d}")
