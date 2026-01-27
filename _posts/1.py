import sys
from collections import deque

# 加速 IO
input = sys.stdin.read

inf = 10**9

class Edge:
    def __init__(self, to, cost, cap):
        self.to = to
        self.cost = cost
        self.cap = cap

def spfa(nodes, edges):
    S = nodes[0]
    T = nodes[-1]
    n = len(nodes)/2-1

    queue = deque([S])
    in_queue = [False] * len(nodes)
    dist = [inf] * len(nodes)
    parent = [-1] * len(nodes)

    dist[S] = 0
    in_queue[S] = True

    while queue:
        u = queue.popleft()
        in_queue[u] = False

        for edge in edges[u]:
            v = edge.to
            if edge.cap > 0 and dist[u] + edge.cost < dist[v]:
                dist[v] = dist[u] + edge.cost
                if not in_queue[v]:
                    queue.append(v)
                    in_queue[v] = True
                parent[v] = u
    max_flow = 100000000
    cur = T
    while parent[cur] != -1:
        prev = parent[cur]
        for edge in edges[prev]:
            if edge.to == cur:
                max_flow = min(max_flow, edge.cap)
        cur = prev
    cur = T
    while parent[cur] != -1:
        prev = parent[cur]
        for edge in edges[prev]:
            if edge.to == cur:
                edge.cap -= max_flow
        for edge in edges[cur]:
            if edge.to == prev:
                edge.cap += max_flow
        cur = prev
    if dist[T] == inf:
        return -1
    return (dist[T] * max_flow)
    

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
    cur_cost = 0
    res = 0
    while True:
        cur_cost = spfa(nodes, edges)
        if cur_cost == -1:
            break
        res += cur_cost
    print(res)
        
if __name__ == '__main__':
    solve()