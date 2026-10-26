import random
import statistics


def generate_data(N, mean_arrival, mean_service, seed):
    random.seed(seed)
    arrivals, services, current_time = [], [], 0.0
    for _ in range(N):
        current_time += random.expovariate(1 / mean_arrival)
        arrivals.append(current_time)
        services.append(random.expovariate(1 / mean_service))
    return arrivals, services


def simulate(arrivals, services, servers, queue_limit):
    server_free = [0.0] * servers
    start = [None] * len(arrivals)
    accepted = [False] * len(arrivals)
    waits, rejected, max_queue = [], 0, 0
    for i, arrival in enumerate(arrivals):
        queue_now = sum(
            1 for k in range(i)
            if accepted[k] and start[k] > arrival)
        max_queue = max(max_queue, queue_now)
        server_index = server_free.index(min(server_free))
        if server_free[server_index] <= arrival:
            start[i] = arrival
            accepted[i] = True
            waits.append(0.0)
            server_free[server_index] = arrival + services[i]
        elif queue_now >= queue_limit:
            rejected += 1
        else:
            start[i] = server_free[server_index]
            accepted[i] = True
            waits.append(start[i] - arrival)
            server_free[server_index] = start[i] + services[i]
            max_queue = max(max_queue, queue_now + 1)
    served_idx = [i for i, ok in enumerate(accepted) if ok]
    total_service = sum(services[i] for i in served_idx)
    last_dep = max(start[i] + services[i] for i in served_idx)
    horizon = last_dep - arrivals[0]
    util = total_service / (servers * horizon) * 100
    return {
        "mean": statistics.mean(waits),
        "max_wait": max(waits),
        "max_queue": max_queue,
        "util": util,
        "rejected": rejected,
        "loss": rejected / len(arrivals) * 100,
        "served": len(served_idx),
    }


N = 180             # число заданий
mean_arrival = 6    # средний интервал, мин
mean_service = 10   # среднее обслуживание, мин
queue_limit = 8     # ёмкость буфера
seed = 42

arrivals, services = generate_data(
    N, mean_arrival, mean_service, seed)
for servers in (1, 2, 3, 4):
    r = simulate(arrivals, services, servers, queue_limit)
    print(servers, round(r["mean"], 2),
          round(r["max_wait"], 2), r["max_queue"],
          round(r["util"], 2), round(r["loss"], 2))
