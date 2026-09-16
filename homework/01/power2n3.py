memo = {}
def power2n_3(n):
    if n == 0:
        return 1
    if n in memo:
        return memo[n]
    memo[n] = power2n_3(n - 1) + power2n_3(n - 1)
    return memo[n]

print(power2n_3(100))