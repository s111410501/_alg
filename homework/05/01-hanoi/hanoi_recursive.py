def hanoi(n, source, auxiliary, destination, moves=None):
    if moves is None:
        moves = []
    if n == 1:
        moves.append((source, destination))
        return moves
    hanoi(n - 1, source, destination, auxiliary, moves)
    moves.append((source, destination))
    hanoi(n - 1, auxiliary, source, destination, moves)
    return moves


def solve(n):
    return hanoi(n, 'A', 'B', 'C')


def print_moves(moves):
    for i, (frm, to) in enumerate(moves, 1):
        print(f"{i:2d}. {frm} -> {to}")
    print(f"Total: {len(moves)} moves")


if __name__ == '__main__':
    import sys
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    print_moves(solve(n))
