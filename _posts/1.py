import sys

# 加速 IO
input = sys.stdin.read

inf = 10**9

class Edge:
    def __init__(self, to, cost, cap):
        self.to = to
        self.cost = cost
        self.cap = cap

def spfa():
    pass

def solve():
    N,p,m,f,n,s = map(int, input().split())
    require = []
    for _ in range(N):
        require.append(int(input()))
    nodes = [x for x in range(2*N+2)]
    edges = [[] for _ in range(2*N+2)]
    # 建边
    S = 0
    T = 2*N+1
    for i in range(1,N+1):
        edges[S].append(Edge(i,p,inf))    
        edges[i].append(Edge(T,0,require[i-1]))
    for i in range(N+1,2*N+1):
        edges[S].append(Edge(i,0,require[i-N-1]))  
        if i != 2*N:  
            edges[i].append(Edge(i+1,0,inf))
        if i-N+n<=N:
            edges[i].append(Edge(i-N+n,s,inf))
        if i-N+m<=N:
            edges[i].append(Edge(i-N+m,f,inf))
    spfa()
        
if __name__ == '__main__':
    solve()