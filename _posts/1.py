import sys

# 加速 IO
input = sys.stdin.read

def solve():
    data = input().split()
    if not data:
        return
    
    n = int(data[0])
    m = int(data[1])
    
    # 预处理 a，转为整数列表
    a = []
    idx = 2
    for _ in range(n):
        a.append(int(data[idx]))
        idx += 1
    
    # dp 数组初始化，使用大数代替 1e15
    INF = 10**15
    dp = [0] * (n + 1)
    
    # dp[1] 单独处理或在循环中自然处理皆可，这里对应 C++ 的 dp[1] = a[0]
    dp[1] = a[0]
    
    for i in range(2, n + 1):
        cur = i
        total = 0
        current_max = a[i-1] 
        min_temp = INF      
        
        while cur >= 1:
            val = a[cur-1]
            total += val
            
            if total > m:
                break
            if val > current_max:
                current_max = val
            cost = dp[cur-1] + current_max
            if cost < min_temp:
                min_temp = cost
            
            cur -= 1
            
        dp[i] = min_temp

    print(dp[n])

if __name__ == '__main__':
    solve()