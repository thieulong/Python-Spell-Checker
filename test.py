def find_distance(self, check_s, s):
    if s == " ":
        return len(check_s) * self.del_cost

    dp = [[0 for _ in range(len(check_s) + 1)] for _ in range(len(s) + 1)]
    for j in range(len(check_s) + 1):
        for i in range(len(s) + 1):
            if i == 0:
                dp[i][j] = j * self.ins_cost
                continue
            if j == 0:
                dp[i][j] = i * self.del_cost
                continue
            sub_cost = self.sub_cost
            if check_s[j - 1] == s[i - 1]:
                sub_cost = 0
            dp[i][j] = min(dp[i - 1][j] + self.ins_cost, dp[i][j - 1] + self.del_cost, dp[i - 1][j - 1] + sub_cost)
    return dp[-1][-1]

print("ấ")