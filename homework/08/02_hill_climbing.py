# 爬山演算法（Hill Climbing）解決 TSP

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

def two_opt(route):
    n = len(route)
    a, b = sorted(random.sample(range(n), 2))
    if a == 0: a += 1
    new_route = route[:a] + list(reversed(route[a:b+1])) + route[b+1:]
    return new_route

def hill_climbing(dist, iterations=10000):
    n = len(dist)
    current = random_route(n)
    current_dist = route_distance(current, dist)
    best = current[:]
    best_dist = current_dist
    for _ in range(iterations):
        neighbor = two_opt(current)
        neighbor_dist = route_distance(neighbor, dist)
        if neighbor_dist < current_dist:
            current = neighbor
            current_dist = neighbor_dist
            if current_dist < best_dist:
                best = current[:]
                best_dist = current_dist
    return best, best_dist

if __name__ == '__main__':
    random.seed(123)
    dist = build_matrix(CITIES)
    route, total = hill_climbing(dist, iterations=5000)
    print("=== 爬山演算法（Hill Climbing） ===")
    print("路線:", route + [route[0]])
    print(f"總距離: {total:.3f}")
