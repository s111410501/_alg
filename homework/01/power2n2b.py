def power2n_2b(n):
    if n == 0:
        return 1
    return 2 * power2n_2b(n - 1)

print(power2n_2b(100))