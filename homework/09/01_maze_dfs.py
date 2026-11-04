import sys

MAZE = [
    "###########",
    "#S..#...#.#",
    "###.#.#.#.#",
    "#.#...#.#.#",
    "#.#####.#.#",
    "#.#...#...#",
    "#.#.#.###.#",
    "#.#.#...#.#",
    "#.#.###.#.#",
    "#.....#..E#",
    "###########",
]

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
DIRECTION_NAMES = {
    (-1, 0): "上",
    (1, 0): "下",
    (0, -1): "左",
    (0, 1): "右",
}


def find_position(maze, target):
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == target:
                return x, y
    return None


def solve_maze_dfs(maze):
    start = find_position(maze, "S")
    goal = find_position(maze, "E")
    height = len(maze)
    width = len(maze[0])
    visited = set()
    parent = {}
    explored = 0
    sys.setrecursionlimit(10000)

    def dfs(current):
        nonlocal explored
        visited.add(current)
        explored += 1

        if current == goal:
            return True

        x, y = current
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if not (0 <= nx < width and 0 <= ny < height):
                continue
            if maze[ny][nx] == "#":
                continue
            neighbor = (nx, ny)
            if neighbor in visited:
                continue
            parent[neighbor] = current
            if dfs(neighbor):
                return True
        return False

    found = dfs(start)
    if not found:
        return None, explored

    path = []
    current = goal
    while True:
        path.append(current)
        if current == start:
            break
        current = parent[current]
    path.reverse()
    return path, explored


def render_maze(maze, path):
    grid = [list(row) for row in maze]
    for x, y in path:
        if grid[y][x] not in ("S", "E"):
            grid[y][x] = "*"
    return "\n".join("".join(row) for row in grid)


def describe_path(path):
    steps = []
    for index in range(1, len(path)):
        x1, y1 = path[index - 1]
        x2, y2 = path[index]
        steps.append(DIRECTION_NAMES[(x2 - x1, y2 - y1)])
    return steps


def main():
    print("=== 老鼠走迷宮問題（DFS 深度優先搜尋）===")
    print("\n迷宮：")
    print("\n".join(MAZE))

    path, explored = solve_maze_dfs(MAZE)

    if path is None:
        print("\n找不到從 S 到 E 的路徑。")
        print(f"總共探索 {explored} 個格子。")
        return

    print("\nDFS 找到的路徑：")
    print(render_maze(MAZE, path))
    print(f"\n路徑長度（格子數）：{len(path)}")
    print(f"移動步數：{len(path) - 1}")
    print(f"探索格子數：{explored}")
    print(f"移動順序：{''.join(describe_path(path))}")
    print(f"路徑座標：{path}")


if __name__ == "__main__":
    main()
