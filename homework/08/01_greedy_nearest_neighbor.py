# 貪婪演算法（Nearest Neighbor）解決 TSP

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

def nearest_neighbor(dist, start=0):
    n = len(dist)
    visited = [False] * n
    route = [start]
    visited[start] = True
    current = start
    total = 0
    for _ in range(n-1):
        next_city = -1
        min_d = float('inf')
        for j in range(n):
            if not visited[j] and dist[current][j] < min_d:
                min_d = dist[current][j]
                next_city = j
        route.append(next_city)
        visited[next_city] = True
        total += min_d
        current = next_city
    total += dist[current][start]
    route.append(start)
    return route, total

if __name__ == '__main__':
    random.seed(123)
    dist = build_matrix(CITIES)
    route, total = nearest_neighbor(dist, start=0)
    print("=== 貪婪演算法（Nearest Neighbor） ===")
    print("路線:", route)
    print(f"總距離: {total:.3f}")
