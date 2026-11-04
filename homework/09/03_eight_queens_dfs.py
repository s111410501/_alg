import sys


def solve_n_queens(n, find_all=True):
    solutions = []
    columns = set()
    diagonal_down = set()
    diagonal_up = set()
    placement = []
    explored = 0

    def dfs(row):
        nonlocal explored
        explored += 1

        if row == n:
            solutions.append(placement.copy())
            return not find_all

        for column in range(n):
            if column in columns:
                continue
            if row + column in diagonal_down:
                continue
            if row - column in diagonal_up:
                continue

            columns.add(column)
            diagonal_down.add(row + column)
            diagonal_up.add(row - column)
            placement.append(column)

            should_stop = dfs(row + 1)

            placement.pop()
            columns.remove(column)
            diagonal_down.remove(row + column)
            diagonal_up.remove(row - column)

            if should_stop:
                return True

        return False

    dfs(0)
    return solutions, explored


def render_board(solution):
    n = len(solution)
    lines = []
    for row in range(n):
        cells = []
        for column in range(n):
            cells.append("Q" if solution[row] == column else ".")
        lines.append(" ".join(cells))
    return "\n".join(lines)


def main():
    n = 8
    find_all = True

    for argument in sys.argv[1:]:
        if argument == "--first":
            find_all = False
        else:
            n = int(argument)

    solutions, explored = solve_n_queens(n, find_all=find_all)

    print("=== {} 皇后問題（DFS 深度優先搜尋 + 回溯）===".format(n))
    mode = "找出所有解" if find_all else "找到第一個解就停止"
    print("\n搜尋模式：{}".format(mode))

    if not solutions:
        print("找不到解答。")
        print("總共探索 {} 個遞迴節點。".format(explored))
        return

    print("找到的解答數量：{}".format(len(solutions)))
    print("總共探索 {} 個遞迴節點。\n".format(explored))

    print("第一個解答：")
    print(render_board(solutions[0]))
    print("\n皇后位置（列, 行），行列皆從 1 開始：")
    positions = [(row + 1, column + 1) for row, column in enumerate(solutions[0])]
    print(positions)

    if find_all and len(solutions) > 1:
        print("\n其餘 {} 個解答已省略，可修改程式輸出全部解答。".format(len(solutions) - 1))


if __name__ == "__main__":
    main()
