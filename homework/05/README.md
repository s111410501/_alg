# Homework 5：程式碼介紹

本文件由 opencode 製作，用來介紹本資料夾中四個 Python 檔案的程式碼。

---

## 1. `hanoi_recursive.py` — 河內塔（遞迴版）

用**遞迴**解河內塔。核心函式 `hanoi`：

```python
def hanoi(n, source, auxiliary, destination, moves=None):
    if moves is None:
        moves = []
    if n == 1:
        moves.append((source, destination))
        return moves
    hanoi(n - 1, source, destination, auxiliary, moves)
    moves.append((source, destination))
    hanoi(n - 1, auxiliary, source, destination, moves)
    return moves
```

**程式碼說明：**

- `moves=None`：預設參數，第一次呼叫時建立空串列 `moves` 來收集每一步移動，之後遞迴共用同一個串列（可變物件）。
- **基底情況** `n == 1`：只有一個盤子，直接從 `source` 移到 `destination`，記錄 `(source, destination)` 後回傳。
- **遞迴步驟**：
  1. `hanoi(n-1, source, destination, auxiliary, moves)`：先把上面 $n-1$ 個盤子搬到輔助柱（`auxiliary`），此時 `destination` 當輔助柱。
  2. `moves.append((source, destination))`：把最大的盤子從 `source` 移到 `destination`。
  3. `hanoi(n-1, auxiliary, source, destination, moves)`：再把那 $n-1$ 個盤子從輔助柱搬到 `destination`。

**其餘函式：**

- `solve(n)`：以三根柱子 `'A'`、`'B'`、`'C'` 呼叫 `hanoi`，回傳移動清單。
- `print_moves(moves)`：用 `enumerate(moves, 1)` 逐行印出「編號. 來源 -> 目標」，最後印出總步數 `len(moves)`。
- `__main__` 區塊：從命令列參數讀取盤子數 `n`（`sys.argv[1]`），沒給則預設 `3`。

```bash
python hanoi_recursive.py 3
```

---

## 2. `hanoi_iterative.py` — 河內塔（迭代版）

同樣解河內塔，但**不用遞迴**，改用**堆疊 `stack`** 模擬遞迴的呼叫堆疊。

```python
def hanoi_iterative(n, source, auxiliary, destination):
    moves = []
    if n < 1:
        return moves
    stack = [(n, source, auxiliary, destination)]
    while stack:
        num, src, aux, dst = stack.pop()
        if num == 1:
            moves.append((src, dst))
            continue
        stack.append((num - 1, aux, src, dst))
        stack.append((1, src, aux, dst))
        stack.append((num - 1, src, dst, aux))
    return moves
```

**程式碼說明：**

- `n < 1`：盤子數小於 1 時直接回傳空的 `moves`。
- `stack` 初始放入一個任務 `(n, source, auxiliary, destination)`。
- `stack.pop()`：取出最上層任務 `(num, src, aux, dst)`。
- **`num == 1`**：只需移動一個盤子，記錄 `(src, dst)` 並 `continue`。
- **拆解任務**：把大任務拆成三個子任務，**依相反順序**推回堆疊，這樣 `pop()` 時執行順序才會與遞迴版一致：
  1. `(num-1, aux, src, dst)`：最後才做（先推入，後執行）。
  2. `(1, src, aux, dst)`：中間把最大盤子移過去。
  3. `(num-1, src, dst, aux)`：最先做（後推入，先執行）。

**其餘函式：** `solve(n)`、`print_moves(moves)`、`__main__` 皆與遞迴版相同，因此兩者輸出完全一致，可互相驗證。

---

## 3. `map_filter_reduce_bubble.py` — 函數式程式設計

用**遞迴**自行實作 `map` / `filter` / `reduce`，並用遞迴寫泡泡排序。

### `my_map(func, lst)`

```python
def my_map(func, lst):
    if not lst:
        return []
    head = lst[0]
    tail = lst[1:]
    return [func(head)] + my_map(func, tail)
```

- 空串列回傳 `[]`（基底情況）。
- 否則把串列拆成「頭 `head`」與「尾 `tail`」，對 `head` 套用 `func`，再遞迴處理 `tail`，最後用 `+` 串接。

### `my_filter(func, lst)`

```python
def my_filter(func, lst):
    if not lst:
        return []
    head = lst[0]
    tail = lst[1:]
    if func(head):
        return [head] + my_filter(func, tail)
    return my_filter(func, tail)
```

- 與 `my_map` 類似，但會先判斷 `func(head)`：
  - 為真 → 保留 `head` 並遞迴。
  - 為假 → 丟掉 `head`，只遞迴處理 `tail`。

### `my_reduce(func, lst, initializer=None)`

```python
def my_reduce(func, lst, initializer=None):
    if not lst:
        if initializer is None:
            raise TypeError("reduce() of empty sequence with no initial value")
        return initializer
    if initializer is None:
        head = lst[0]
        tail = lst[1:]
        return my_reduce(func, tail, head)
    head = lst[0]
    tail = lst[1:]
    return my_reduce(func, tail, func(initializer, head))
```

- 空串列：有 `initializer` 就回傳它；否則拋出 `TypeError`。
- 沒有 `initializer` 時，先取第一個元素 `head` 當作初始累加值，再遞迴處理剩下的 `tail`。
- 有 `initializer` 時，每次用 `func(initializer, head)` 合併頭元素，遞迴直到串列耗盡。

### 泡泡排序

```python
def _bubble_pass(arr, index=0):
    if index >= len(arr) - 1:
        return arr
    if arr[index] > arr[index + 1]:
        new_arr = list(arr)
        new_arr[index], new_arr[index + 1] = new_arr[index + 1], new_arr[index]
        return _bubble_pass(new_arr, index + 1)
    return _bubble_pass(arr, index + 1)

def bubble_sort(arr):
    data = list(arr)
    n = len(data)
    def _sort(lst, count):
        if count <= 1:
            return lst
        lst_after_pass = _bubble_pass(lst)
        return _sort(lst_after_pass, count - 1)
    return _sort(data, n)
```

- `_bubble_pass`：一趟掃描，從 `index` 開始比較相鄰兩元素；若前者較大就**複製串列**後交換，再往右繼續。
- `bubble_sort`：先複製輸入（不改到原串列），用內部的 `_sort` 重複執行 `_bubble_pass`，共 `n - 1` 趟。

`__main__` 區塊示範了排序，以及用 `lambda` 搭配 `map`（乘 2）、`filter`（取偶數）、`reduce`（求和、求積）。

---

## 4. `sym_diff_recursive.py` — 符號微分（遞迴）

對以 **tuple 運算式樹**表示的數學式做**遞迴求導**。

### 輔助判斷函式

```python
def is_number(e):
    return isinstance(e, (int, float)) and not isinstance(e, bool)

def is_var(e):
    return e == 'x'
```

- `is_number`：判斷是否為數值（並排除 `bool`，因為 `True/False` 也是 `int`）。
- `is_var`：判斷是否為變數 `'x'`。

### `sym_diff(expr)` — 求導主函式

```python
def sym_diff(expr):
    if is_number(expr):
        return 0
    if is_var(expr):
        return 1
    if not isinstance(expr, tuple):
        raise ValueError(f"Unsupported expression type: {expr}")
    op = expr[0]
    ...
```

- **常數** → 導數為 `0`。
- **變數 `x`** → 導數為 `1`。
- 其他非 tuple 就丟出 `ValueError`。
- 依照運算子 `op = expr[0]` 分派到對應的微分法則：

| 運算子 | 法則 | 程式碼 |
| :--- | :--- | :--- |
| `+` / `-` | 逐項微分 | `('+', du, dv)` / `('-', du, dv)` |
| `*` | 乘積法則 | `('+', ('*', du, v), ('*', u, dv))` |
| `/` | 商法則 | 分子 `du*v - u*dv`，分母 `v^2` |
| `^` / `**` | 冪次法則 | 次方為常數：`n * u^(n-1) * du`；否則用一般式 `u^n * (n/u*du + ln(u)*dn)` |
| `neg` | 負號 | `('neg', sym_diff(u))` |
| `sin` / `cos` / `tan` | 三角微分 | `cos(u)*du`、`-sin(u)*du`、`du / cos(u)^2` |
| `exp` / `ln` / `sqrt` | 指對數與根號 | `exp(u)*du`、`du/u`、`du / (2*sqrt(u))` |

每個分支都遵循**連鎖律**：先算內層 `du = sym_diff(u)`，再乘上外層導數。遇到不支援的運算子則 `raise ValueError`。

### `_prec(op)` — 運算子優先序

```python
def _prec(op):
    if op == 'neg': return 5
    if op in ('^', '**'): return 4
    if op == '*' or op == '/': return 3
    if op == '+' or op == '-': return 2
    return 0
```

用來判斷輸出字串時是否需要補括號（數字越大優先序越高）。

### `expr_to_str(expr)` — 樹轉字串

- 數值：若為整數值的浮點數（如 `2.0`）就轉成 `2`。
- `neg`：若子表達式優先序不低於 `neg`，外面要加括號，例如 `-(...)`。
- 單元運算（`len==2`，如 `sin`）：輸出 `op(...)`。
- 二元運算（`len==3`）：
  - `^`：右運算元是 tuple 要括號；左運算元優先序不夠時也要括號。
  - `* / + -`：子運算元優先序低於目前運算子時，用括號包起來，避免改變計算順序。

### `sym_diff_str(expr)`

```python
def sym_diff_str(expr):
    return expr_to_str(sym_diff(expr))
```

先 `sym_diff` 求導，再用 `expr_to_str` 轉成字串。

`__main__` 區塊對多組範例（`x^2`、`x^3`、`x*5`、`sin(x)*cos(x)`、`sin(x^2)`、`ln(x)`、`exp(x)`、`sin(x)/x`、`sqrt(x)` 等）印出 `d/dx ... = ...` 的結果。

```bash
python sym_diff_recursive.py
```

---

> 本 README 由 opencode 撰寫。
