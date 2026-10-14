# Homework 6：Lambda Calculus 解譯器

本文件由 opencode及gemini製作，用來介紹本資料夾中的 Lambda Calculus（λ-演算）解譯器。

gemini對話網址 <https://share.gemini.google/KVShhyksKzC9> 

---

## 1. `01-lambda/lambda_calculus.py` — λ-演算解譯器（有名稱版本）

以 Python 實作的無類型 λ-演算解譯器。支援定義全域名稱（如 `TRUE`、`FALSE`、`ZERO`、`SUCC`、`PLUS` 等），以 β-歸約逐步顯示計算過程，並用 alpha-conversion 避免變數捕獲。

```bash
python 01-lambda/lambda_calculus.py
```

### 抽象語法樹（AST）

所有 λ-項都是 `Expr` 的子類別，用物件樹表示運算式結構。

| 類別 | 意義 | 例子 | `__repr__` |
| :--- | :--- | :--- | :--- |
| `Var(name)` | 變數 | `x` | `x` |
| `Abs(param, body)` | 抽象（函式定義） | `λx. x` | `(λx. x)` |
| `App(func, arg)` | 應用（函式呼叫） | `f x` | `(f x)` |

### 自由變數與代入

```python
def free_vars(expr):
    if isinstance(expr, Var):
        return {expr.name}
    if isinstance(expr, Abs):
        return free_vars(expr.body) - {expr.param}
    if isinstance(expr, App):
        return free_vars(expr.func) | free_vars(expr.arg)
```

- `Var`：自己就是自由變數。
- `Abs`：把被 λ 綁定的 `param` 從自由變數集合中扣掉。
- `App`：兩邊的自由變數取聯集。

`substitute(expr, var_name, replacement)` 負責實際代入 `expr[var := replacement]`：

- 遇到 `Var`：名稱相符就換成 `replacement`。
- 遇到 `Abs`：
  - 若參數就是 `var_name`，代表 `var` 被綁定，不代入。
  - 若參數會**捕獲** `replacement` 的自由變數，就先做 **alpha-conversion**，把參數改名為 `param_N` 再代入。
- 遇到 `App`：對 `func` 與 `arg` 分別遞迴代入。

### β-歸約引擎

`LambdaInterpreter` 保存全域定義 `env`，並提供：

- `define(name, expr)`：新增一個巨集名稱。
- `expand_env(expr)`：把名稱展開成對應的 λ-項（遞迴展開 `Var`）。
- `step(expr)`：執行**一步** β-歸約，採用**正規序（normal order，最外層最左邊優先）**：

```python
if isinstance(expr, App):
    if isinstance(expr.func, Abs):          # 最外層 redex：(λx. E) N -> E[x := N]
        return substitute(expr.func.body, expr.func.param, expr.arg), True
    new_func, reduced = self.step(expr.func)  # 先化簡函式位置
    if reduced:
        return App(new_func, expr.arg), True
    new_arg, reduced = self.step(expr.arg)    # 再化簡參數位置
    ...
```

正規序保證：只要項存在正規形式（normal form），就一定求得出來。

- `eval_and_trace(expr, max_steps)`：先展開全域定義，再逐步 `step` 直到正規形式，印出每一步。若超過 `max_steps` 則視為可能發散（例如 Ω-combinator）。

### 解析器（Parser）

`tokenize` 把字串切成 `(` `)` `.` `λ` `\` 與識別字，`parse_lambda` 用遞迴下降依下列文法解析：

```
expr := app
app  := atom atom*          (左結合，如 (f a b) -> App(App(f, a), b))
atom := ID | '(' expr ')' | 'λ' ID+ '.' expr
```

> 註：Gemini 原版的 tokenizer `\\[a-zA-Z0-9_]*` 會把 `\x` 連同參數名稱切成同一個 token，導致 `λ`/`\` 永遠比對不到而無法解析抽象。這裡將 `\` 與名稱分開成兩個 token 修正。

### 執行範例

`__main__` 定義了 `I`、`TRUE`、`FALSE`、`NOT`、`ZERO`、`ONE`、`TWO`、`SUCC`、`PLUS`，並測試數個運算式。輸出格式如下：

```
>>> 測試 3：後繼函式 (SUCC ZERO) 應得到 ONE
【原始輸入】    : (SUCC ZERO)
【展開全域定義】: (((λn. (λf. (λx. (f ((n f) x))))) (λf. (λx. x)))
  Step 1: => (λf. (λx. (f (((λf_1. (λx_1. x_1)) f) x))))
  Step 2: => (λf. (λx. (f ((λx_1. x_1) x))))
  Step 3: => (λf. (λx. (f x)))  (已達正規形式 Normal Form)
============================================================
```

`Step 1` 中 `ZERO` 內部的 `f`、`x` 被改名為 `f_1`、`x_1`，正是 **alpha-conversion** 解決變數名稱衝突的結果。

---

## 2. 特性總結

- **有名稱 AST**：可直接用 `TRUE`、`ZERO` 等名稱定義與閱讀。
- **正規序 β-歸約**：最外層最左邊優先，能求出存在正規形式的解。
- **Alpha-conversion**：自動重新命名被綁定變數，避免變數捕獲。
- **逐步顯示**：完整印出展開定義與每一步推導過程。
- **安全上限**：`max_steps` 避免發散程式（如 Ω-combinator）無限執行。

---

> 本 README 由 opencode 撰寫。
