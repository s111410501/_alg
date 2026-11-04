import heapq
import time
from collections import deque

WIDTH = 20
HEIGHT = 12

BASE_MAP = [
    ".....~........~.....",
    "..####....####......",
    "..#..........#......",
    "..#..####....#......",
    ".....#..#...........",
    "..#..#..#..####.....",
    "..#..####...........",
    "..#...~......#......",
    "..####....####......",
    "........~...........",
    "....####....####....",
    "....~..........~....",
]

NETS = [
    ("A", (0, 0), (19, 2)),
    ("B", (0, 5), (19, 6)),
    ("C", (0, 11), (19, 9)),
]

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def cell_cost(position):
    x, y = position
    return 3 if BASE_MAP[y][x] == "~" else 1


def build_blocked():
    blocked = set()
    for y, row in enumerate(BASE_MAP):
        for x, cell in enumerate(row):
            if cell == "#":
                blocked.add((x, y))
    return blocked


def neighbors(position, blocked):
    x, y = position
    for dx, dy in DIRECTIONS:
        nx, ny = x + dx, y + dy
        if not (0 <= nx < WIDTH and 0 <= ny < HEIGHT):
            continue
        if (nx, ny) in blocked:
            continue
        yield (nx, ny)


def reconstruct(parent, start, goal):
    path = []
    current = goal
    while current is not None:
        path.append(current)
        if current == start:
            break
        current = parent[current]
    path.reverse()
    if not path or path[0] != start:
        return None
    return path


def route_bfs(start, goal, blocked):
    if start == goal:
        return [start], 0

    queue = deque([start])
    parent = {start: None}
    expanded = 0

    while queue:
        current = queue.popleft()
        expanded += 1

        for neighbor in neighbors(current, blocked):
            if neighbor in parent:
                continue
            parent[neighbor] = current
            if neighbor == goal:
                return reconstruct(parent, start, goal), expanded
            queue.append(neighbor)

    return None, expanded


def route_dfs(start, goal, blocked):
    stack = [start]
    parent = {start: None}
    expanded = 0

    while stack:
        current = stack.pop()
        expanded += 1

        if current == goal:
            return reconstruct(parent, start, goal), expanded

        for neighbor in neighbors(current, blocked):
            if neighbor in parent:
                continue
            parent[neighbor] = current
            stack.append(neighbor)

    return None, expanded


def route_dijkstra(start, goal, blocked):
    distance = {start: 0}
    parent = {start: None}
    heap = [(0, start)]
    expanded = 0

    while heap:
        current_distance, current = heapq.heappop(heap)
        if current_distance != distance.get(current):
            continue

        expanded += 1

        if current == goal:
            break

        for neighbor in neighbors(current, blocked):
            new_distance = current_distance + cell_cost(neighbor)
            if new_distance >= distance.get(neighbor, float("inf")):
                continue
            distance[neighbor] = new_distance
            parent[neighbor] = current
            heapq.heappush(heap, (new_distance, neighbor))

    if goal not in distance:
        return None, expanded
    return reconstruct(parent, start, goal), expanded


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def route_astar(start, goal, blocked):
    g_score = {start: 0}
    parent = {start: None}
    heap = [(heuristic(start, goal), 0, start)]
    counter = 1
    closed = set()
    expanded = 0

    while heap:
        _, _, current = heapq.heappop(heap)

        if current in closed:
            continue
        closed.add(current)
        expanded += 1

        if current == goal:
            break

        for neighbor in neighbors(current, blocked):
            if neighbor in closed:
                continue
            tentative_g = g_score[current] + cell_cost(neighbor)
            if tentative_g >= g_score.get(neighbor, float("inf")):
                continue
            g_score[neighbor] = tentative_g
            parent[neighbor] = current
            f_score = tentative_g + heuristic(neighbor, goal)
            heapq.heappush(heap, (f_score, counter, neighbor))
            counter += 1

    if goal not in g_score:
        return None, expanded
    return reconstruct(parent, start, goal), expanded


ALGORITHMS = {
    "BFS": route_bfs,
    "DFS": route_dfs,
    "Dijkstra": route_dijkstra,
    "A*": route_astar,
}


def path_cost(path):
    return sum(cell_cost(position) for position in path[1:])


def route_all(algorithm_name):
    blocked = build_blocked()
    results = []
    total_length = 0
    total_cost = 0
    total_expanded = 0
    success = 0

    for name, start, goal in NETS:
        path, expanded = ALGORITHMS[algorithm_name](start, goal, blocked)
        total_expanded += expanded

        if path is None:
            results.append((name, None))
            continue

        success += 1
        total_length += len(path) - 1
        total_cost += path_cost(path)
        results.append((name, path))
        for position in path:
            blocked.add(position)

    return {
        "results": results,
        "success": success,
        "length": total_length,
        "cost": total_cost,
        "expanded": total_expanded,
    }


def render(result):
    grid = [list(row) for row in BASE_MAP]
    for name, path in result["results"]:
        if path is None:
            continue
        for x, y in path:
            grid[y][x] = name
    return "\n".join("".join(row) for row in grid)


def main():
    print("=== IC 設計中的電路繞線問題（多種搜尋方法比較）===")
    print("\n晶片繞線網格：")
    print("\n".join(BASE_MAP))
    print("\n圖例：#=障礙物，~=壅塞區（成本 3），.=一般區域（成本 1）")
    print("待繞線的連線（Net）：")
    for name, start, goal in NETS:
        print("  Net {}：{} -> {}".format(name, start, goal))

    summary = []
    for algorithm_name in ALGORITHMS:
        started_at = time.perf_counter()
        result = route_all(algorithm_name)
        elapsed = time.perf_counter() - started_at
        summary.append((algorithm_name, result, elapsed))

    print("\n=== 各演算法比較（依 Net 順序逐一繞線，已完成的線視為障礙）===")
    print("{:<10}{:<10}{:<12}{:<12}{:<14}{:<12}".format(
        "演算法", "成功數", "總線長", "總成本", "展開節點數", "執行時間(ms)"
    ))
    print("-" * 70)
    for algorithm_name, result, elapsed in summary:
        print("{:<10}{:<10}{:<12}{:<12}{:<14}{:<12.3f}".format(
            algorithm_name,
            "{}/{}".format(result["success"], len(NETS)),
            result["length"],
            result["cost"],
            result["expanded"],
            elapsed * 1000,
        ))

    best_name, best_result, _ = min(
        summary,
        key=lambda item: (
            -item[1]["success"],
            item[1]["cost"],
            item[1]["expanded"],
        ),
    )

    print("\n=== 最佳結果（{}）的繞線圖 ===".format(best_name))
    print(render(best_result))
    print("\nNet 路徑：")
    for name, path in best_result["results"]:
        if path is None:
            print("  Net {}：無法完成繞線".format(name))
        else:
            print("  Net {}：長度 {}，成本 {}，路徑 {}".format(
                name, len(path) - 1, path_cost(path), path
            ))

    print("\n說明：BFS 追求最少格子數，Dijkstra 追求最低成本，")
    print("A* 使用曼哈頓距離啟發函數，DFS 只保證找到一條可行路徑。")


if __name__ == "__main__":
    main()
