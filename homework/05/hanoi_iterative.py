def hanoi_iterative(n, source, auxiliary, destination):
    moves = []
    if n < 1:
        return moves
    stack = [(n, source, auxiliary, destination)]
    while stack:
        num, src, aux, dst = stack.pop()
        if num == 1:
            moves.append((src, dst))
            continue
        stack.append((num - 1, aux, src, dst))
        stack.append((1, src, aux, dst))
        stack.append((num - 1, src, dst, aux))
    return moves


def solve(n):
    return hanoi_iterative(n, 'A', 'B', 'C')


def print_moves(moves):
    for i, (frm, to) in enumerate(moves, 1):
        print(f"{i:2d}. {frm} -> {to}")
    print(f"Total: {len(moves)} moves")


if __name__ == '__main__':
    import sys
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    print_moves(solve(n))
