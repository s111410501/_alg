# lcs_dp.py
# 最長共同子序列（Longest Common Subsequence, LCS）— 動態規劃解法

def lcs_dp(A, B):
    """
    使用動態規劃計算兩個字串 A 和 B 的最長共同子序列（LCS）長度
    
    :param A: 第一個字串
    :param B: 第二個字串
    :return: LCS 的長度
    """
    m = len(A)
    n = len(B)
    
    # 建立 (m+1) x (n+1) 的 dp 表
    # dp[i][j] = A[0..i-1] 與 B[0..j-1] 的 LCS 長度
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if A[i - 1] == B[j - 1]:
                # 當前字元相等：左上角 + 1
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                # 當前字元不相等：取上方或左方的最大值
                if dp[i - 1][j] >= dp[i][j - 1]:
                    dp[i][j] = dp[i - 1][j]
                else:
                    dp[i][j] = dp[i][j - 1]
    
    return dp[m][n]

def main():
    # 測試範例
    test_cases = [
        ("AGGTAB", "GXTXAYB"),  # LCS = "GTAB", 長度 4
        ("ABCBDAB", "BDCAB"),   # LCS 長度 4
        ("ABCD", "ACBD"),       # LCS 長度 3
        ("ABC", "AC"),          # LCS 長度 2
    ]
    
    print("=== LCS 動態規劃（DP）解法 ===")
    for A, B in test_cases:
        print(f"A = '{A}', B = '{B}' -> LCS 長度 = {lcs_dp(A, B)}")
    
    print("\n（提示：此解法時間複雜度 O(mn)，適合中等長度字串）")

if __name__ == "__main__":
    main()
