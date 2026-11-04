from collections import deque

START = (0, 0, 0, 0)
GOAL = (1, 1, 1, 1)
FARMER, WOLF, GOAT, CABBAGE = 0, 1, 2, 3
ITEM_NAMES = {
    FARMER: "農夫",
    WOLF: "狼",
    GOAT: "羊",
    CABBAGE: "甘藍菜",
}


def side_name(side):
    return "起始岸" if side == 0 else "對岸"


def is_safe(state):
    farmer, wolf, goat, cabbage = state
    for bank in (0, 1):
        if farmer == bank:
            continue
        if wolf == bank and goat == bank:
            return False
        if goat == bank and cabbage == bank:
            return False
    return True


def next_states(state):
    farmer, wolf, goat, cabbage = state
    result = []

    new_state = list(state)
    new_state[FARMER] = 1 - farmer
    result.append((tuple(new_state), "農夫獨自過河"))

    for item in (WOLF, GOAT, CABBAGE):
        if state[item] != farmer:
            continue
        new_state = list(state)
        new_state[FARMER] = 1 - farmer
        new_state[item] = 1 - state[item]
        result.append((tuple(new_state), f"農夫帶{ITEM_NAMES[item]}過河"))

    return [(new_state, action) for new_state, action in result if is_safe(new_state)]


def solve_bfs(start, goal):
    queue = deque([start])
    parent = {start: None}
    action_from_parent = {start: None}
    explored = 0

    while queue:
        current = queue.popleft()
        explored += 1

        if current == goal:
            break

        for new_state, action in next_states(current):
            if new_state in parent:
                continue
            parent[new_state] = current
            action_from_parent[new_state] = action
            queue.append(new_state)

    if goal not in parent:
        return None, explored

    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = parent[current]
    path.reverse()

    actions = []
    for index in range(1, len(path)):
        actions.append(action_from_parent[path[index]])
    return (path, actions), explored


def format_state(state):
    parts = []
    for index in (WOLF, GOAT, CABBAGE):
        parts.append(f"{ITEM_NAMES[index]}={side_name(state[index])}")
    parts.append(f"農夫={side_name(state[FARMER])}")
    return "，".join(parts)


def main():
    print("=== 狼羊甘藍菜過河問題（BFS 廣度優先搜尋）===")
    print("\n規則：農夫一次只能帶一樣東西過河，")
    print("農夫不在時，狼不能和羊單獨在一起，羊不能和甘藍菜單獨在一起。\n")

    result, explored = solve_bfs(START, GOAL)

    if result is None:
        print("找不到解答。")
        print(f"總共探索 {explored} 個狀態。")
        return

    path, actions = result
    print(f"總共探索 {explored} 個狀態。")
    print(f"最少需要 {len(actions)} 次過河。\n")

    print(f"步驟 0：{format_state(path[0])}")
    for index, action in enumerate(actions, start=1):
        print(f"步驟 {index}：{action}")
        print(f"         {format_state(path[index])}")

    print("\n狀態表示法：(農夫, 狼, 羊, 甘藍菜)，0=起始岸，1=對岸")
    print(f"解答狀態序列：{path}")


if __name__ == "__main__":
    main()
