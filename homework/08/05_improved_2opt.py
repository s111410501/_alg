# 改良法（2-opt 改良法，從貪婪解開始反覆優化）解決 TSP

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
    return route, total

def two_opt_improve(route, dist):
    """完整 2-opt 搜尋直到無改善"""
    best = route[:]
    improved = True
    n = len(best)
    while improved:
        improved = False
        for i in range(1, n-1):
            for j in range(i+1, n):
                if j - i == 1: continue
                new_route = best[:i] + list(reversed(best[i:j])) + best[j:]
                # 計算差異更快，但簡單計算全長也夠小規模
                old_dist = dist[best[i-1]][best[i]] + dist[best[j-1]][best[j] if j < n else best[0]]
                # 簡化：直接比較全距離（n 小）
                if route_distance(new_route, dist) < route_distance(best, dist) - 1e-12:
                    best = new_route
                    improved = True
                    break
            if improved: break
    return best

def improved_2opt(dist, start=0):
    route, _ = nearest_neighbor(dist, start)
    best = two_opt_improve(route, dist)
    return best, route_distance(best, dist)

if __name__ == '__main__':
    random.seed(123)
    dist = build_matrix(CITIES)
    route, total = improved_2opt(dist, start=0)
    print("=== 改良法（2-opt 改良） ===")
    print("路線:", route + [route[0]])
    print(f"總距離: {total:.3f}")
