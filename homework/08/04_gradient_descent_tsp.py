# 梯度下降法（Gradient Descent，透過局部鄰域搜尋近似實作）解決 TSP

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
    if a == b:
        return route[:]
    if a == 0: a += 1
    new_route = route[:a] + list(reversed(route[a:b+1])) + route[b+1:]
    return new_route

def gradient_descent_tsp(dist, learning_rate=0.01, max_iter=10000, patience=100):
    """
    梯度下降法在此以「沿鄰域（2-opt）最陡下降方向」近似實作（TSP 無連續可微函數，
    故採用離散梯度概念：每次考慮鄰域中最小ΔE 的移動，類似 batch/steepest descent）。
    """
    n = len(dist)
    current = random_route(n)
    current_dist = route_distance(current, dist)
    best = current[:]
    best_dist = current_dist
    no_improve = 0
    for _ in range(max_iter):
        # 蒐集鄰域最佳移動
        best_move = None
        best_move_dist = current_dist
        # 採用局部隨機採樣近似計算「梯度」（離散）
        for _ in range(20):  # 採樣 20 個鄰居估算最陡方向
            neighbor = two_opt(current)
            nd = route_distance(neighbor, dist)
            if nd < best_move_dist:
                best_move_dist = nd
                best_move = neighbor
        if best_move is None or best_move_dist >= current_dist - 1e-12:
            no_improve += 1
        else:
            # 沿最陡下降方向移動（學習率此處僅作比例概念，實際採全步移動）
            current = best_move
            current_dist = best_move_dist
            if current_dist < best_dist:
                best = current[:]
                best_dist = current_dist
            no_improve = 0
        if no_improve >= patience:
            break
    return best, best_dist

if __name__ == '__main__':
    random.seed(123)
    dist = build_matrix(CITIES)
    route, total = gradient_descent_tsp(dist)
    print("=== 梯度下降法（Gradient Descent，離散近似） ===")
    print("路線:", route + [route[0]])
    print(f"總距離: {total:.3f}")
