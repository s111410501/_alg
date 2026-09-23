import sys
if sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout.reconfigure(encoding="utf-8")

# 用「系統性列舉真值表」的方式暴力求解 SAT 問題
# SAT (布林可滿足性問題): 找出一個讓布林公式為真的變數指派
# 概念: n 個變數只有 2^n 種組合，全部列出來檢查即可，這是最暴力的方法

# 資料結構定義 (以 CNF 合取範式表示公式)
#   變數   : 以數字 0, 1, ..., n-1 代表 x0, x1, ...
#   文字   : (var, neg)  -- neg=False 代表 x[var], neg=True 代表 ~x[var]
#   子句   : 一組文字，任一文字為真即滿足 (OR)
#   公式   : 一組子句，全部子句都為真才滿足 (AND)

def eval_literal(lit, truth):
    var, neg = lit
    v = truth[var]
    return (not v) if neg else v

def eval_clause(clause, truth):
    return any(eval_literal(lit, truth) for lit in clause)

def eval_formula(formula, truth):
    return all(eval_clause(c, truth) for c in formula)

# 系統性列舉真值表: 把 0..2^n-1 當成 n 位元計數器
# code 的第 i 位元 (bit i) 就是變數 xi 的值
def truth_table(n, formula):
    rows = []
    for code in range(2**n):
        truth = [((code >> v) & 1) == 1 for v in range(n)]
        if eval_formula(formula, truth):
            rows.append(truth)
    return rows

# 印出真值表: 含每個子句的結果與最終 SAT 判定
def print_table(n, formula):
    print(f"共有 {2**n} 組指派，真值表如下:")
    head = "  ".join(f"x{i}" for i in range(n)) + "  |  "
    head += "  ".join(f"C{j}" for j in range(len(formula))) + "  |  SAT"
    print(head)
    print("-" * len(head))
    for code in range(2**n):
        truth = [((code >> v) & 1) == 1 for v in range(n)]
        row = "  ".join("1" if t else "0" for t in truth) + "  |  "
        row += "  ".join("1" if eval_clause(c, truth) else "0" for c in formula)
        row += "  |  " + ("1" if eval_formula(formula, truth) else "0")
        print(row)

def show(n, formula):
    print_table(n, formula)
    sat = truth_table(n, formula)
    if sat:
        print(f"\n有解! 找到 {len(sat)} 組滿足指派:")
        for truth in sat:
            print("  " + "  ".join(f"x{i}={1 if truth[i] else 0}" for i in range(n)))
    else:
        print("\n無解! ")

if __name__ == "__main__":
    # 範例1: (x0 OR x1) AND (~x0 OR ~x1)  => 僅當兩變數相反時為真
    f1 = [ [(0, False), (1, False)], [(0, True), (1, True)] ]
    print("公式1: (x0 或 x1) 且 (~x0 或 ~x1)")
    show(2, f1)

    # 範例2: (x0 OR x1) AND (~x0 OR x1) AND (x0 OR ~x1)  => 僅 x1=1, x0=0 為真
    f2 = [ [(0, False), (1, False)], [(0, True), (1, False)], [(0, False), (1, True)] ]
    print("\n公式2: (x0 或 x1) 且 (~x0 或 x1) 且 (x0 或 ~x1)")
    show(2, f2)

    # 範例3: (x0 OR x1) AND (x0 OR ~x1) AND (~x0 OR x1) AND (~x0 OR ~x1)
    #        四個子句涵蓋所有可能 => 恆假，無解
    f3 = [
        [(0, False), (1, False)],
        [(0, False), (1, True)],
        [(0, True), (1, False)],
        [(0, True), (1, True)],
    ]
    print("\n公式3: 四個子句涵蓋所有組合 => 恆假")
    show(2, f3)

    # 範例4: 3 變數，恆真公式 (每個子句都含 x AND ~x)
    f4 = [ [(0, False), (0, True)], [(1, False), (1, True)], [(2, False), (2, True)] ]
    print("\n公式4: 恆真(tautology)，含 x 與 ~x 的子句必真")
    show(3, f4)