# Homework 5：遞迴、迭代與函數式程式設計

本作業使用 opencode 製作。

這個資料夾共包含四個 Python 程式，分別示範**河內塔**（遞迴與迭代兩種寫法）、**函數式程式設計**（自行實作 `map` / `filter` / `reduce` 與泡泡排序），以及**符號微分**（以遞迴對數學運算式求導）。

---

## 檔案總覽

| 檔案 | 主題 | 核心概念 |
| :--- | :--- | :--- |
| `hanoi_recursive.py` | 河內塔（遞迴版） | 分治法、遞迴 |
| `hanoi_iterative.py` | 河內塔（迭代版） | 以堆疊取代遞迴 |
| `map_filter_reduce_bubble.py` | 函數式工具 | `map` / `filter` / `reduce`、泡泡排序 |
| `sym_diff_recursive.py` | 符號微分 | 樹狀結構遞迴、數學求導 |

---

## 一、`hanoi_recursive.py` — 河內塔（遞迴版）

以經典的**遞迴**方式解河內塔：要將 $n$ 個盤子從 `source` 搬到 `destination`，先將上面 $n-1$ 個搬到輔助柱，移動最大的盤子，再把 $n-1$ 個搬回。

```python
def hanoi(n, source, auxiliary, destination, moves=None):
    if n == 1:
        moves.append((source, destination))
        return moves
    hanoi(n - 1, source, destination, auxiliary, moves)
    moves.append((source, destination))
    hanoi(n - 1, auxiliary, source, destination, moves)
    return moves
```

- `solve(n)`：以 `A`、`B`、`C` 三根柱子呼叫 `hanoi`。
- `print_moves(moves)`：逐行印出每一步與總步數（$2^n - 1$ 步）。

執行方式：

```bash
python hanoi_recursive.py 3
```

---

## 二、`hanoi_iterative.py` — 河內塔（迭代版）

同樣解河內塔，但**不使用遞迴**，改用一個**堆疊（stack）**模擬遞迴的呼叫過程。每次取出一個 `(num, src, aux, dst)` 任務，若 `num == 1` 就直接移動，否則把「拆解後的三個子任務」依相反順序推回堆疊，確保執行順序與遞迴版一致。

```python
stack = [(n, source, auxiliary, destination)]
while stack:
    num, src, aux, dst = stack.pop()
    if num == 1:
        moves.append((src, dst))
        continue
    stack.append((num - 1, aux, src, dst))
    stack.append((1, src, aux, dst))
    stack.append((num - 1, src, dst, aux))
```

執行方式：

```bash
python hanoi_iterative.py 3
```

兩個河內塔檔案的輸出完全相同，可互相驗證結果是否正確。

---

## 三、`map_filter_reduce_bubble.py` — 函數式程式設計

這個檔案用**遞迴**自行實作了 Python 內建的 `map` / `filter` / `reduce`，並用遞迴實作泡泡排序。

### 自行實作的三個函式

| 函式 | 功能 | 說明 |
| :--- | :--- | :--- |
| `my_map(func, lst)` | 對串列每個元素套用函式 | 取頭、算結果、遞迴處理尾端 |
| `my_filter(func, lst)` | 保留使函式為真的元素 | 依判斷決定是否保留頭元素 |
| `my_reduce(func, lst, initializer)` | 將串列化簡為單一值 | 支援有無初始值兩種情況；空串列且無初始值時拋出 `TypeError` |

### 泡泡排序（遞迴版）

- `_bubble_pass(arr, index)`：完成一趟掃描，將相鄰較大的元素往後交換。
- `bubble_sort(arr)`：重複執行 `n - 1` 趟掃描，直到排序完成。

執行方式：

```bash
python map_filter_reduce_bubble.py
```

範例輸出包含 `Map (*2)`、`Filter (even)`、`Reduce (sum)`、`Reduce (*)` 等結果。

---

## 四、`sym_diff_recursive.py` — 符號微分（遞迴）

以**運算式樹（expression tree）**表示數學式，並用**遞迴**對其求導。程式支援基本的微分法則：

- **加減法**：`('+', u, v)`、`('-', u, v)`
- **乘法**：乘積法則（product rule）
- **除法**：商法則（quotient rule）
- **次方**：冪次法則與一般式 $\frac{d}{dx}u^n$
- **函式**：`sin`、`cos`、`tan`、`exp`、`ln`、`sqrt`、`neg`（負號）

運算式以 tuple 表示，例如 $x^2$ 寫成 `('^', 'x', 2)`，$\sin(x)\cos(x)$ 寫成 `('*', ('sin', 'x'), ('cos', 'x'))`。

### 主要函式

| 函式 | 功能 |
| :--- | :--- |
| `sym_diff(expr)` | 對運算式樹求導，回傳新的運算式樹 |
| `expr_to_str(expr)` | 將運算式樹轉回可讀字串（會依優先序自動加括號） |
| `sym_diff_str(expr)` | 求導後直接輸出成字串 |

執行方式：

```bash
python sym_diff_recursive.py
```

程式會對多組範例（如 $x^2$、$\sin(x^2)$、$\ln x$、$\sqrt{x}$、$\frac{\sin x}{x}$ 等）印出 `d/dx ... = ...` 的微分結果。

---

## 總結

這四個檔案分別從不同角度展示「重複」與「分解」兩種核心思維：

- **河內塔**示範同一問題的遞迴解與迭代解（以堆疊模擬呼叫堆疊）。
- **函數式工具**示範如何用遞迴取代迴圈來處理串列運算。
- **符號微分**示範如何對樹狀結構做遞迴，將數學法則轉換為程式邏輯。

> 本 README 由 opencode 撰寫。
