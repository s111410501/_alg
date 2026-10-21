# lcs_brute.py
# 最長共同子序列（Longest Common Subsequence, LCS）— 非動態規劃（暴力枚舉子序列）

def is_subsequence(sub, text):
    """
    使用雙指針判斷字串 sub 是否為 text 的子序列（不要求連續）
    
    :param sub: 要檢查的子序列
    :param text: 目標字串
    :return: True 若 sub 是 text 的子序列，否則 False
    """
    i = 0  # 指向 sub
    j = 0  # 指向 text
    len_sub = len(sub)
    len_text = len(text)
    while i < len_sub and j < len_text:
        if sub[i] == text[j]:
            i += 1
        j += 1
    return i == len_sub

def lcs_brute(A, B):
    """
    暴力枚舉：枚舉較短字串的所有子序列，逐一檢查是否為較長字串的子序列，取最長者
    
    注意：此法為窮舉（非 DP），時間複雜度為 O(max(m,n) * 2^(min(m,n)))，
          僅適合極短字串（建議 min(m,n) <= 16~20）使用。
    
    :param A: 第一個字串
    :param B: 第二個字串
    :return: LCS 的長度
    """
    # 選擇較短的字串進行枚舉，以減少子序列數量
    if len(A) <= len(B):
        S, T = A, B
    else:
        S, T = B, A
    
    max_len = 0
    
    def backtrack(index, current):
        nonlocal max_len
        if index == len(S):
            # 已產生完整子序列 current，檢查是否為 T 的子序列
            if is_subsequence(current, T):
                if len(current) > max_len:
                    max_len = len(current)
            return
        
        # 1. 選擇：將 S[index] 納入子序列
        backtrack(index + 1, current + S[index])
        
        # 2. 不選擇：將 S[index] 排除子序列
        backtrack(index + 1, current)
    
    backtrack(0, "")
    return max_len

def main():
    # 測試範例（僅用極短字串，避免指數爆炸）
    test_cases = [
        ("ABC", "AC"),      # LCS 長度 2
        ("AB", "AC"),       # LCS 長度 1
        ("AC", "BD"),       # LCS 長度 0
        ("AG", "GA"),       # LCS 長度 1
    ]
    
    print("=== LCS 非動態規劃（暴力枚舉子序列）解法 ===")
    print("（警告：min(m,n) 較大時將極度耗時，僅供教學觀念用）")
    for A, B in test_cases:
        print(f"A = '{A}', B = '{B}' -> LCS 長度 = {lcs_brute(A, B)}")

if __name__ == "__main__":
    main()
