# 模擬退火法（Simulated Annealing）解決 TSP

import math
import random

# 城市座標（範例）
CITIES = [
    (0, 0),      # 城市 0
    (1, 2),      # 城市 1
    (3, 1),      # 城市 2
    (6, 2),      # 城市 3
    (7, 0),      # 城市 4
    (5, -2),     # 城市 5
    (2, -1),     # 城市 6
]

def calc_distance(p1, p2):
    return math.hypot(p1[0]-p2[0], p1[1]-p2[1])

def build_matrix(cities):
    n = len(cities)
    dist = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1,n):
            d = calc_distance(cities[i], cities[j])
            dist[i][j] = dist[j][i] = d
    return dist

def route_distance(route, dist):
    total = 0
    n = len(route)
    for i in range(n):
        total += dist[route[i]][route[(i+1)%n]]
    return total

def random_route(n):
    route = list(range(n))
    random.shuffle(route)
    return route

def swap(route):
    n = len(route)
    a, b = random.sample(range(n), 2)
    new_route = route[:]
    new_route[a], new_route[b] = new_route[b], new_route[a]
    return new_route

def simulated_annealing(dist, initial_temp=1000, cooling_rate=0.995, iterations=10000):
    n = len(dist)
    current = random_route(n)
    current_dist = route_distance(current, dist)
    best = current[:]
    best_dist = current_dist
    temp = initial_temp
    for _ in range(iterations):
        neighbor = swap(current)
        neighbor_dist = route_distance(neighbor, dist)
        delta = neighbor_dist - current_dist
        if delta < 0 or random.random() < math.exp(-delta / temp):
            current = neighbor
            current_dist = neighbor_dist
            if current_dist < best_dist:
                best = current[:]
                best_dist = current_dist
        temp *= cooling_rate
        if temp < 1e-8:
            break
    return best, best_dist

if __name__ == '__main__':
    random.seed(123)
    dist = build_matrix(CITIES)
    route, total = simulated_annealing(dist)
    print("=== 模擬退火法（Simulated Annealing） ===")
    print("路線:", route + [route[0]])
    print(f"總距離: {total:.3f}")
