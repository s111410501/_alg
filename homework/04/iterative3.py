import sys
import math
if sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout.reconfigure(encoding="utf-8")

# ============================================================================
# 問題自訂：用「迭代法」求方程式 f(x) = x^3 - 2x - 5 = 0 的實根
# ----------------------------------------------------------------------------
# 為什麼要用迭代法？
#   f(x) 是三次方程式，雖然理論上可以用三次方公式硬解，但公式又長又容易算錯；
#   而且很多工程問題（電路、電位、管線流體、統計）根本沒有可用的代數公式。
#   這些問題的共同點是：
#       雖然「一步算完」很難，但「怎麼從舊值推出新值」卻很清楚，
#       於是就從一個初始猜測值出發，反覆修正，一步步逼近答案。
#
# 兩種迭代公式 (g(x) 就是 README 的迭代函式)
#   1) 固定點迭代：把原式變形，寫成 x = g(x)
#        x^3 - 2x - 5 = 0  =>  x^3 = 2x + 5  =>  g(x) = (2x + 5)^(1/3)
#        想法很單純，但 g'(x) 太大時會發散，收斂速度通常只有「一次」(linear)
#
#   2) 牛頓法 (Newton-Raphson)：用「切線」代替曲線，是迭代法最經典的加速技巧
#        g(x) = x - f(x) / f'(x) = x - (x^3 - 2x - 5) / (3x^2 - 2)
#        想法：用「目前這點的切線」與 x 軸的交點當成新的近似值，越靠近根越準，
#              收斂速度是「二次」(quadratic)：每多迭代一次，正確位數幾乎加倍
#
# 停止條件 (Stopping Criterion)
#   |x_{n+1} - x_n| < eps   已經幾乎不會再動了 => 收斂，可以回傳
#   n >= max_iter           安全機制，避免無限迴圈
# ============================================================================

EPS = 1e-12           # 誤差容限
MAX_ITER = 100        # 最大迭代次數（安全機制）
DERIV_EPS = 1e-10      # f'(x) 的下限，太接近 0 代表切線近乎水平，會發散
TRUE_ROOT = 2.0945514815423265   # 已知真值，只用來驗證、算誤差用


def f(x):
    """原方程式的左邊：f(x) = x^3 - 2x - 5"""
    return x**3 - 2 * x - 5


def fp(x):
    """導函式：f'(x) = 3x^2 - 2"""
    return 3 * x**2 - 2


def g_fixed(x):
    """固定點迭代函式：g(x) = (2x + 5)^(1/3)"""
    return (2 * x + 5) ** (1 / 3)


def g_newton(x):
    """牛頓法迭代函式：g(x) = x - f(x) / f'(x)"""
    return x - f(x) / fp(x)


def iterate(g, x0, eps=EPS, max_iter=MAX_ITER):
    """通用的迭代法框架：x_{n+1} = g(x_n)，回傳整條迭代序列與結束原因"""
    xs = [x0]
    for n in range(1, max_iter + 1):
        x = xs[-1]
        if abs(fp(x)) < DERIV_EPS:      # f'(x) ≈ 0，切線近乎水平，沒辦法往下走
            return xs, f"第 {n} 次失敗：f'(x) ≈ 0（切線近乎水平，遠離根）"
        x_new = g(x)
        if not (-1e6 < x_new < 1e6):    # 中途爆掉也視為失敗
            return xs, f"第 {n} 次失敗：x = {x_new:.6e} 已經發散"
        xs.append(x_new)
        if abs(x_new - x) < eps:        # 相鄰兩次迭代的差小於容限 => 收斂
            return xs, f"第 {n} 次迭代後收斂（|x_n - x_{{n-1}}| < {eps:g}）"
    return xs, f"達最大迭代次數 {max_iter}，停止"


def print_table(name, xs, status, order):
    """印出每次迭代的近似值，並列出與真值的誤差及誤差比值
       order=1 一次收斂，看 e_n / e_{n-1} 是否趨近定值
       order=2 二次收斂，看 e_n / e_{n-1}^2 是否趨近定值
    """
    if order == 2:
        head = f"{'n':>3} | {'x_n':>20} | {'|f(x_n)|':>12} | {'誤差 e_n':>12} | {'e_n / e_{n-1}^2':>15}"
    else:
        head = f"{'n':>3} | {'x_n':>20} | {'|f(x_n)|':>12} | {'誤差 e_n':>12} | {'e_n / e_{n-1}':>15}"
    print(f"\n【{name}】  x0 = {xs[0]:.6f}")
    print(head)
    print("-" * 76)
    for n, x in enumerate(xs):
        err = abs(x - TRUE_ROOT)
        if n == 0:
            ratio = "-"
        else:
            prev = abs(xs[n - 1] - TRUE_ROOT)
            if prev == 0 or err == 0 or prev >= 1e-3:
                ratio = "-"      # 誤差還太大或已達到電腦極限，比值沒有意義
            elif order == 2:
                ratio = f"{err / prev**2:15.4f}"
            else:
                ratio = f"{err / prev:15.4f}"
        print(f"{n:3d} | {x:20.15f} | {abs(f(x)):12.3e} | {err:12.3e} | {ratio:>15}")
    print("-" * 76)
    print(f"收斂結果 x ≈ {xs[-1]:.15f}")
    print(f"結束原因：{status}")
    if abs(xs[-1] - TRUE_ROOT) < 1e-9:
        print(f"驗證：與真值 {TRUE_ROOT} 相比，誤差 {abs(xs[-1] - TRUE_ROOT):.3e} ✔")


def steps_to(x0, g, target=1e-8, max_iter=MAX_ITER):
    """從 x0 出發，迭代到誤差小於 target 為止，共花了幾次迭代"""
    xs, _ = iterate(g, x0, eps=target, max_iter=max_iter)
    return len(xs) - 1


def main():
    print("=" * 76)
    print("迭代法求解：f(x) = x^3 - 2x - 5 = 0  的實根")
    print("=" * 76)
    print("真值參考： x = 2.0945514815423265")

    # 實驗 1：固定點迭代 x_{n+1} = (2x_n + 5)^(1/3)
    xs, status = iterate(g_fixed, 2.0)
    print_table("實驗1  固定點迭代  x_{n+1} = (2x_n + 5)^(1/3)", xs, status, order=1)
    print("觀察：e_n / e_{n-1} 趨近 0.152 ≈ |g'(x*)| => 一次收斂 (linear)")
    print("      誤差每輪大約只剩前輪的 15%，要很多輪才能逼近")

    # 實驗 2：牛頓法 x_{n+1} = x_n - f(x_n)/f'(x_n)
    xs, status = iterate(g_newton, 2.0)
    print_table("實驗2  牛頓法  x_{n+1} = x_n - f(x_n)/f'(x_n)", xs, status, order=2)
    print("觀察：e_n / e_{n-1}^2 趨近定值 => 二次收斂 (quadratic)")
    print("      正確位數 2 碼 -> 5 碼 -> 11 碼，加倍成長，所以只需 4 步")

    # 實驗 3：初始值對收斂速度的影響（牛頓法）
    print("\n" + "=" * 76)
    print("實驗3  同一個迭代公式，不同初始值 (牛頓法)")
    print("=" * 76)
    print(f"{'x0':>10} | {'迭代次數':>8} | {'x_n':>20} | {'|f(x_n)|':>12} | 結果")
    print("-" * 76)
    bad = math.sqrt(2 / 3)     # f'(x) = 3x^2 - 2 = 0 的地方，切線完全水平
    for x0 in [1.0, 1.5, 2.0, 2.5, 3.0, 5.0, 0.0, -3.0, 0.8165, bad]:
        xs, status = iterate(g_newton, x0)
        ok = abs(xs[-1] - TRUE_ROOT) < 1e-9
        label = f"{x0:.4f}" if x0 != bad else f"{x0:.4f}*"
        print(f"{label:>10} | {len(xs) - 1:8d} | {xs[-1]:20.15f} | "
              f"{abs(f(xs[-1])):12.3e} | {'✔ 收斂' if ok else '✘ ' + status}")
    print("-" * 76)
    print("觀察：初始值越接近根，收斂越快；離根遠通常也救得回來，")
    print("      但 x0 = sqrt(2/3) 時 f'(x0) = 0，切線與 x 軸平行 => 迭代失敗；")
    print("      x0 = 0.8165 只是「幾乎」等於它，於是走了 36 輪才回來 ——")
    print("      這就是「初始值選得好很重要」的原因")

    # 實驗 4：比較兩種迭代公式的效率（都從 x0 = 5.0 出發，遠離根）
    print("\n" + "=" * 76)
    print("實驗4  兩種迭代公式的效率比較（都從 x0 = 5.0 出發，遠離根）")
    print("=" * 76)
    print(f"{'迭代公式':<32} | {'收斂型態':<10} | {'達誤差<1e-8':>12} | {'收斂所需次數':>12}")
    print("-" * 76)
    for name, g, kind in [
        ("固定點迭代 (2x+5)^(1/3)", g_fixed, "一次 linear"),
        ("牛頓法 x - f(x)/f'(x)", g_newton, "二次 quadratic"),
    ]:
        steps = steps_to(5.0, g)
        print(f"{name:<32} | {kind:<10} | {'1e-8':>12} | {steps:12d}")
    print("-" * 76)
    print("結論：同樣是迭代法，選對迭代函式 g(x) 就能快好幾倍 ——")
    print("      牛頓法把 f(x)=0 的資訊（用導數）塞進 g(x)，所以收斂快得多。")


if __name__ == "__main__":
    main()