#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lambda Calculus 解譯器（有名稱版本 / Named Lambda Calculus）

以 Python 實作無類型 λ-演算 (untyped lambda calculus) 的解譯器：
  * 支援定義全域名稱 (如 TRUE, FALSE, ZERO, SUCC, PLUS ...)
  * 使用正規序 (normal order) 的 β-歸約，並逐步顯示計算過程
  * 以 alpha-conversion 重新命名，避免變數捕獲 (variable capture)
  * 語法：λx.body 或 \\x.body，應用寫成 (f x)，多參數 λxy.body

用法：
  python lambda_calculus.py
"""

import re
import sys


# ---------------------------------------------------------------------------
# 1. AST (抽象語法樹)
# ---------------------------------------------------------------------------
class Expr:
    """所有 λ-項的基底類別。"""


class Var(Expr):
    """變數 (Variable)：x"""

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return isinstance(other, Var) and self.name == other.name

    def __hash__(self):
        return hash(("Var", self.name))


class Abs(Expr):
    """抽象 (Abstraction)：λparam. body"""

    def __init__(self, param, body):
        self.param = param
        self.body = body

    def __repr__(self):
        return f"(λ{self.param}. {self.body})"


class App(Expr):
    """應用 (Application)：(func arg)"""

    def __init__(self, func, arg):
        self.func = func
        self.arg = arg

    def __repr__(self):
        return f"({self.func} {self.arg})"


# ---------------------------------------------------------------------------
# 2. 自由變數與代入 (Substitution)
# ---------------------------------------------------------------------------
def free_vars(expr):
    """取得項中的自由變數 (free variables)。"""
    if isinstance(expr, Var):
        return {expr.name}
    if isinstance(expr, Abs):
        return free_vars(expr.body) - {expr.param}
    if isinstance(expr, App):
        return free_vars(expr.func) | free_vars(expr.arg)
    return set()


def substitute(expr, var_name, replacement, fresh_idx=None):
    """
    把 expr 中自由出現的 var_name 換成 replacement，
    並用 alpha-conversion 避免變數捕獲。
    """
    if fresh_idx is None:
        fresh_idx = [0]

    if isinstance(expr, Var):
        return replacement if expr.name == var_name else expr

    if isinstance(expr, Abs):
        # var 被此 λ 綁定，內部出現的 var 不是自由的，不代入
        if expr.param == var_name:
            return expr
        # 參數名稱會捕獲 replacement 的自由變數，先改名 (alpha-conversion)
        if expr.param in free_vars(replacement):
            fresh_idx[0] += 1
            new_param = f"{expr.param}_{fresh_idx[0]}"
            renamed_body = substitute(expr.body, expr.param, Var(new_param), fresh_idx)
            return Abs(new_param, substitute(renamed_body, var_name, replacement, fresh_idx))
        return Abs(expr.param, substitute(expr.body, var_name, replacement, fresh_idx))

    # App
    return App(
        substitute(expr.func, var_name, replacement, fresh_idx),
        substitute(expr.arg, var_name, replacement, fresh_idx),
    )


# ---------------------------------------------------------------------------
# 3. β-歸約引擎
# ---------------------------------------------------------------------------
class LambdaInterpreter:
    def __init__(self):
        self.env = {}

    def define(self, name, expr):
        """定義一個全域名稱 (巨集)。"""
        self.env[name] = expr

    def expand_env(self, expr):
        """把自訂名稱展開成它對應的 λ-項。"""
        if isinstance(expr, Var):
            if expr.name in self.env:
                return self.expand_env(self.env[expr.name])
            return expr
        if isinstance(expr, Abs):
            return Abs(expr.param, self.expand_env(expr.body))
        if isinstance(expr, App):
            return App(self.expand_env(expr.func), self.expand_env(expr.arg))
        return expr

    def step(self, expr):
        """
        執行單步 β-歸約（正規序：最外層、最左邊的 redex 優先）。
        回傳 (新項, 是否發生歸約)。
        """
        if isinstance(expr, Var):
            return expr, False

        if isinstance(expr, App):
            # 最外層 redex：(λx. E) N  ->  E[x := N]
            if isinstance(expr.func, Abs):
                reduced = substitute(expr.func.body, expr.func.param, expr.arg)
                return reduced, True
            # 否則先化簡函式位置
            new_func, reduced = self.step(expr.func)
            if reduced:
                return App(new_func, expr.arg), True
            # 再化簡參數位置
            new_arg, reduced = self.step(expr.arg)
            if reduced:
                return App(expr.func, new_arg), True
            return expr, False

        if isinstance(expr, Abs):
            new_body, reduced = self.step(expr.body)
            if reduced:
                return Abs(expr.param, new_body), True
            return expr, False

    def eval_and_trace(self, expr, max_steps=40):
        """展開名稱後逐步歸約，印出完整的計算過程。"""
        print(f"【原始輸入】    : {expr}")
        current = self.expand_env(expr)
        print(f"【展開全域定義】: {current}")

        step_count = 0
        while step_count < max_steps:
            next_expr, reduced = self.step(current)
            if not reduced:
                print(f"  Step {step_count}: {current}  (已達正規形式 Normal Form)")
                break
            step_count += 1
            print(f"  Step {step_count}: => {next_expr}")
            current = next_expr

        if step_count == max_steps:
            print(f"已達步數上限 ({max_steps})，可能不會終止（例如 Ω-combinator）。")
        print("=" * 60)


# ---------------------------------------------------------------------------
# 4. 解析器 (Parser)：字串 -> AST
# ---------------------------------------------------------------------------
def tokenize(text):
    tokens = re.findall(r"\(|\)|\.|λ|\\|[A-Za-z0-9_]+", text)
    tokens.append(None)  # EOF 標記
    return tokens


def parse_lambda(text):
    """
    文法：
        expr := app
        app  := atom atom*            (左結合)
        atom := ID | '(' expr ')' | 'λ' ID+ '.' expr
    """
    tokens = tokenize(text)
    pos = [0]

    def peek():
        return tokens[pos[0]]

    def parse_app():
        parts = [parse_atom()]
        while peek() is not None and peek() not in (")", "."):
            parts.append(parse_atom())
        result = parts[0]
        for part in parts[1:]:
            result = App(result, part)
        return result

    def parse_atom():
        token = peek()
        if token == "(":
            pos[0] += 1
            expr = parse_app()
            if peek() != ")":
                raise SyntaxError("缺少 ')'")
            pos[0] += 1
            return expr
        if token in ("λ", "\\"):
            pos[0] += 1
            params = []
            while peek() is not None and peek() not in (".", ")", "("):
                params.append(peek())
                pos[0] += 1
            if peek() != ".":
                raise SyntaxError("λ 之後缺少 '.'")
            pos[0] += 1
            body = parse_app()
            for param in reversed(params):
                body = Abs(param, body)
            return body
        if token is None or token in (")", "."):
            raise SyntaxError(f"非預期的符號: {token!r}")
        pos[0] += 1
        return Var(token)

    expr = parse_app()
    if peek() is not None:
        raise SyntaxError(f"多餘的符號: {peek()!r}")
    return expr


# ---------------------------------------------------------------------------
# 5. 主程式：定義常用項並測試
# ---------------------------------------------------------------------------
def main():
    interp = LambdaInterpreter()

    # 恆等函式
    interp.define("I", parse_lambda(r"(\x. x)"))

    # Church 布林
    interp.define("TRUE", parse_lambda(r"(\x. (\y. x))"))
    interp.define("FALSE", parse_lambda(r"(\x. (\y. y))"))
    interp.define("NOT", parse_lambda(r"(\b. ((b FALSE) TRUE))"))

    # Church 數
    interp.define("ZERO", parse_lambda(r"(\f. (\x. x))"))
    interp.define("ONE", parse_lambda(r"(\f. (\x. (f x)))"))
    interp.define("TWO", parse_lambda(r"(\f. (\x. (f (f x))))"))
    interp.define("SUCC", parse_lambda(r"(\n. (\f. (\x. (f ((n f) x)))))"))
    interp.define("PLUS", parse_lambda(r"(\m. (\n. (\f. (\x. ((m f) ((n f) x))))))"))

    tests = [
        ("測試 1：恆等應用 (I a)", r"(I a)"),
        ("測試 2：布林選擇 ((TRUE A) B) 應得到 A", r"((TRUE A) B)"),
        ("測試 3：後繼函式 (SUCC ZERO) 應得到 ONE", r"(SUCC ZERO)"),
        ("測試 4：加法 ((PLUS ONE) TWO) 應得到 THREE", r"((PLUS ONE) TWO)"),
        ("測試 5：布林反運算 (NOT FALSE) 應得到 TRUE", r"(NOT FALSE)"),
    ]

    for title, expr in tests:
        print(f"\n>>> {title}")
        interp.eval_and_trace(parse_lambda(expr))


if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    main()
