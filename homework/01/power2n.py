import time

# 方法 1：直接用 Python 內建的乘法算 2**n
def power2n_1(n):
    return 2**n

# 方法 2a：用遞迴 power2n(n-1)+power2n(n-1)
# 每個呼叫會分叉成兩個，呼叫次數為 O(2^n)，n=100 根本跑不完
def power2n_2a(n):
    if n == 0:
        return 1
    return power2n_2a(n - 1) + power2n_2a(n - 1)

# 方法 2b：用遞迴 2*power2n(n-1)
# 每個 n 只呼叫一次，呼叫次數為 O(n)
def power2n_2b(n):
    if n == 0:
        return 1
    return 2 * power2n_2b(n - 1)

# 方法 3：用遞迴 + 查表 (memoization)
# 先用表記住算過的答案，避免重複計算，呼叫次數為 O(n)
memo = {}
def power2n_3(n):
    if n == 0:
        return 1
    if n in memo:
        return memo[n]
    memo[n] = power2n_3(n - 1) + power2n_3(n - 1)
    return memo[n]

def test(name, fn, n):
    t0 = time.time()
    r = fn(n)
    t = time.time() - t0
    print(f"{name:12s} n={n:3d} => {r}, 花費 {t:.6f} 秒")
    return t

if __name__ == "__main__":
    N = 100
    test("方法1 (2**n)", power2n_1, N)
    # 方法 2a 在 n=100 絕對跑不完，改用較小的 n 示範指數爆炸
    for n in [10, 15, 20, 24]:
        test("方法2a (遞迴+遞迴)", power2n_2a, n)
    test("方法2b (2*遞迴)", power2n_2b, N)
    test("方法3 (遞迴+查表)", power2n_3, N)