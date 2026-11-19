import math
import random
import time


def derivative_forward(f, x, h=1e-5):
    return (f(x + h) - f(x)) / h


def derivative_backward(f, x, h=1e-5):
    return (f(x) - f(x - h)) / h


def derivative_central(f, x, h=1e-5):
    return (f(x + h) - f(x - h)) / (2 * h)


def riemann_integral(f, low, high, steps=10000):
    if steps < 1:
        raise ValueError("steps 必須為正整數")
    dx = (high - low) / steps
    total = 0.0
    for i in range(steps):
        total += f(low + (i + 0.5) * dx)
    return total * dx


def monte_carlo_integral(f, low, high, samples=100000, seed=None):
    rng = random.Random(seed)
    width = high - low
    total = 0.0
    total_sq = 0.0
    for _ in range(samples):
        value = f(low + rng.random() * width)
        total += value
        total_sq += value * value
    mean = total / samples
    variance = max(0.0, total_sq / samples - mean * mean)
    estimate = width * mean
    error = width * math.sqrt(variance / samples)
    return estimate, error


def f_square(x):
    return x * x


def f_sin(x):
    return math.sin(x)


def f_exp(x):
    return math.exp(x)


def show_derivatives():
    cases = [
        ("x^2", f_square, 3.0, lambda x: 2 * x),
        ("sin(x)", f_sin, math.pi / 4, math.cos),
        ("exp(x)", f_exp, 0.0, math.exp),
    ]
    print("=== 單變數數值微分（有限差分，h = 1e-5）===")
    print(f"{'函數':10s} {'點 x':>10s} {'解析解':>12s} {'前向':>12s} {'後向':>12s} {'中心':>12s}")
    for name, f, x, exact_f in cases:
        exact = exact_f(x)
        forward = derivative_forward(f, x)
        backward = derivative_backward(f, x)
        central = derivative_central(f, x)
        print(f"{name:10s} {x:10.5f} {exact:12.8f} {forward:12.8f} {backward:12.8f} {central:12.8f}")
    print()
    print("中心差分誤差最小：前向/後向截斷誤差為 O(h)，中心差分為 O(h^2)。")
    print()

    print("=== 步長 h 對中心差分精度的影響（f(x)=x^2, x=3）===")
    for h in [1e-2, 1e-4, 1e-6, 1e-8, 1e-10, 1e-12]:
        value = derivative_central(f_square, 3.0, h)
        print(f"h = {h:.0e}  近似值 = {value:.12f}  誤差 = {abs(value - 6.0):.3e}")
    print("h 太小會被浮點數減法溢出主導，因此並非越小越好。")
    print()


def show_integrals():
    cases = [
        ("x^2", f_square, 0.0, 1.0, 1 / 3),
        ("sin(x)", f_sin, 0.0, math.pi, 2.0),
        ("exp(x)", f_exp, 0.0, 1.0, math.e - 1),
    ]
    print("=== 單變數數值積分（黎曼中點法 vs 蒙地卡羅）===")
    print(f"{'函數':10s} {'區間':>14s} {'解析解':>12s} {'黎曼':>12s} {'黎曼誤差':>11s} {'蒙地卡羅':>12s} {'±誤差':>10s}")
    for name, f, low, high, exact in cases:
        start = time.perf_counter()
        riemann = riemann_integral(f, low, high, steps=10000)
        riemann_time = time.perf_counter() - start
        start = time.perf_counter()
        mc, err = monte_carlo_integral(f, low, high, samples=100000, seed=42)
        mc_time = time.perf_counter() - start
        interval = f"[{low:.3f}, {high:.3f}]"
        print(f"{name:10s} {interval:>14s} {exact:12.8f} {riemann:12.8f} "
              f"{abs(riemann - exact):11.2e} {mc:12.8f} {err:10.2e}")
        print(f"{'':10s} {'黎曼耗時':>14s} {riemann_time:12.6f}s {'蒙地卡羅耗時':>14s} {mc_time:.6f}s")
    print()
    print("黎曼中點法誤差為 O(1/n^2)；蒙地卡羅不會比它快，但在高維度時優勢很大（見第二支程式）。")
    print()


if __name__ == "__main__":
    show_derivatives()
    show_integrals()
