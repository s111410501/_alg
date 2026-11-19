import itertools
import math
import random
import time

MAX_GRID_POINTS = 2_000_000


def gradient(f, x, h=1e-5):
    x = list(x)
    result = []
    for i in range(len(x)):
        forward = x[:]
        backward = x[:]
        forward[i] += h
        backward[i] -= h
        result.append((f(forward) - f(backward)) / (2 * h))
    return result


def hypervolume(low, high):
    volume = 1.0
    for lo, hi in zip(low, high):
        volume *= hi - lo
    return volume


def integral(f, low, high, steps=8):
    low = list(low)
    high = list(high)
    n = len(low)
    if n != len(high):
        raise ValueError("low 與 high 的維度必須相同")
    if steps < 1:
        raise ValueError("steps 必須為正整數")

    grid_points = steps ** n
    if grid_points > MAX_GRID_POINTS:
        raise ValueError(
            f"黎曼格點數 {grid_points} 超過上限 {MAX_GRID_POINTS}，"
            f"n={n} 且 steps={steps} 時無法計算，請改用蒙地卡羅法"
        )

    axes = []
    for lo, hi in zip(low, high):
        delta = (hi - lo) / steps
        axes.append([lo + (i + 0.5) * delta for i in range(steps)])

    total = 0.0
    for point in itertools.product(*axes):
        total += f(list(point))
    return total * hypervolume(low, high) / grid_points


def monte_carlo_integral(f, low, high, samples=100000, seed=None):
    rng = random.Random(seed)
    low = list(low)
    high = list(high)
    volume = hypervolume(low, high)

    total = 0.0
    total_sq = 0.0
    for _ in range(samples):
        x = [lo + rng.random() * (hi - lo) for lo, hi in zip(low, high)]
        value = f(x)
        total += value
        total_sq += value * value

    mean = total / samples
    variance = max(0.0, total_sq / samples - mean * mean)
    estimate = volume * mean
    error = volume * math.sqrt(variance / samples)
    return estimate, error


def sum_of_squares(x):
    return sum(xi * xi for xi in x)


def report_gradient():
    print("=== n 變數數值微分：梯度（中心差分，h = 1e-5）===")
    print("f(x) = x1^2 + ... + xn^2，取 x = (1, 1, ..., 1)，解析梯度為 (2, 2, ..., 2)")
    for n in [1, 2, 5, 100]:
        x = [1.0] * n
        start = time.perf_counter()
        g = gradient(sum_of_squares, x)
        elapsed = time.perf_counter() - start
        max_error = max(abs(value - 2.0) for value in g)
        head = ", ".join(f"{value:.6f}" for value in g[:3])
        tail = ", ..." if n > 3 else ""
        print(f"n={n:3d}  梯度前幾項 = ({head}{tail})  最大誤差 = {max_error:.3e}  耗時 = {elapsed:.6f}s")
    print()


def report_riemann():
    print("=== n 變數黎曼積分：integral(f, low, high) ===")
    print("f(x) = x1^2 + ... + xn^2，low=(0,...,0)，high=(1,...,1)，解析解 = n/3")
    print(f"{'n':>4s} {'steps':>7s} {'格點數':>14s} {'估計值':>14s} {'誤差':>12s} {'耗時':>12s}")
    settings = [(1, 10000), (2, 300), (5, 10), (100, 1)]
    for n, steps in settings:
        low = [0.0] * n
        high = [1.0] * n
        exact = n / 3
        start = time.perf_counter()
        value = integral(sum_of_squares, low, high, steps=steps)
        elapsed = time.perf_counter() - start
        print(f"{n:4d} {steps:7d} {steps ** n:14d} {value:14.8f} {abs(value - exact):12.2e} {elapsed:11.6f}s")

    print()
    print("100 維若只把 steps 從 1 提高到 2：")
    try:
        integral(sum_of_squares, [0.0] * 100, [1.0] * 100, steps=2)
    except ValueError as error:
        print(f"  {error}")
    print("  2^100 = 1267650600228229401496703205376 個格點，即使每台電腦每秒算 10 億點也需要約 4e13 年。")
    print("  這就是維度災難，因此高維度必須改用蒙地卡羅法。")
    print()


def report_monte_carlo():
    print("=== n 變數蒙地卡羅積分（題目同上一題）===")
    print("f(x) = x1^2 + ... + xn^2，low=(0,...,0)，high=(1,...,1)，解析解 = n/3")
    print(f"{'n':>4s} {'樣本數':>9s} {'估計值':>14s} {'標準誤差':>12s} {'實際誤差':>12s} {'耗時':>12s}")
    for n in [1, 2, 5, 100]:
        low = [0.0] * n
        high = [1.0] * n
        exact = n / 3
        start = time.perf_counter()
        value, error = monte_carlo_integral(sum_of_squares, low, high, samples=100000, seed=2026)
        elapsed = time.perf_counter() - start
        print(f"{n:4d} {100000:9d} {value:14.8f} {error:12.2e} {abs(value - exact):12.2e} {elapsed:11.6f}s")
    print()
    print("蒙地卡羅的誤差約為 O(1/sqrt(N))，與維度 n 無關，因此 100 維仍然可行。")
    print()


if __name__ == "__main__":
    report_gradient()
    report_riemann()
    report_monte_carlo()
