import sys

# 加速 IO
input = sys.stdin.read
class Edge:
    def __init__(self, to, cost, cap):
        self.to = to
        self.cost = cost
        self.cap = cap

def solve():
    N,p,m,f,n,s = map(int, input().split())
    require = []
    for _ in range(N):
        require.append(int(input()))
    nodes = [x for x in range(2*N+2)]
    

if __name__ == '__main__':
    solve()