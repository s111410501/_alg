import heapq

MAP = [
    "#################",
    "#N#~..#~..#~....#",
    "#.#.###.#.#.#...#",
    "#.#.....#...#.#.#",
    "#..##..#####..#.#",
    "#~..#~...~#~..#.#",
    "###.#####.#.##.##",
    "#.#.#~...~#.#~..#",
    "#.#.#.#####.#.#.#",
    "#.#.#.#~..#~..#.#",
    "#.#.###.#.#####.#",
    "#~...~...~...~.P#",
    "#################",
]

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
TERRAIN_COST = {
    ".": 1,
    "~": 3,
    "N": 1,
    "P": 1,
}


def find_position(grid, target):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == target:
                return x, y
    return None


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def cell_cost(grid, position):
    x, y = position
    return TERRAIN_COST.get(grid[y][x], 1)


def astar(grid, start, goal):
    height = len(grid)
    width = len(grid[0])
    open_heap = [(heuristic(start, goal), 0, start)]
    counter = 1
    g_score = {start: 0}
    parent = {start: None}
    closed = set()
    expanded = 0

    while open_heap:
        _, _, current = heapq.heappop(open_heap)

        if current in closed:
            continue
        closed.add(current)
        expanded += 1

        if current == goal:
            break

        x, y = current
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if not (0 <= nx < width and 0 <= ny < height):
                continue
            if grid[ny][nx] == "#":
                continue

            neighbor = (nx, ny)
            if neighbor in closed:
                continue

            tentative_g = g_score[current] + cell_cost(grid, neighbor)
            if tentative_g >= g_score.get(neighbor, float("inf")):
                continue

            g_score[neighbor] = tentative_g
            parent[neighbor] = current
            f_score = tentative_g + heuristic(neighbor, goal)
            heapq.heappush(open_heap, (f_score, counter, neighbor))
            counter += 1

    if goal not in parent:
        return None, expanded, None

    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = parent[current]
    path.reverse()
    return path, expanded, g_score[goal]


def render_map(grid, path):
    rendered = [list(row) for row in grid]
    for x, y in path:
        if rendered[y][x] not in ("N", "P"):
            rendered[y][x] = "*"
    return "\n".join("".join(row) for row in rendered)


def main():
    start = find_position(MAP, "N")
    goal = find_position(MAP, "P")

    print("=== NPC 搜尋玩家問題（A* 啟發式搜尋）===")
    print("\n地圖：")
    print("\n".join(MAP))
    print("\n圖例：N=NPC，P=玩家，#=障礙物，~=沼澤（移動成本 3），.=平地（移動成本 1）")

    path, expanded, total_cost = astar(MAP, start, goal)

    if path is None:
        print("\nNPC 找不到玩家。")
        print("展開節點數：{}".format(expanded))
        return

    print("\nA* 找到的路徑：")
    print(render_map(MAP, path))
    print("\n路徑長度（格子數）：{}".format(len(path)))
    print("移動步數：{}".format(len(path) - 1))
    print("路徑總成本：{}".format(total_cost))
    print("展開節點數：{}".format(expanded))
    print("路徑座標：{}".format(path))


if __name__ == "__main__":
    main()
