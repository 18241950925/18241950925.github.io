import sys
from collections import deque

# 增加递归深度，防止深搜或特殊情况爆栈（虽然这里主要用迭代）
sys.setrecursionlimit(200000)

inf  = 10**9

class Edge:
    def __init__(self, to, cap, cost, rev):
        self.to = to
        self.cap = cap
        self.cost = cost
        self.rev = rev  # 反向边在 nodes[to] 中的下标

def spfa(nodes):
    queue = deque([0])
    in_queue = [False] * len(nodes)
    in_queue[0] = True
    dist = [inf] * len(nodes)
    dist[0] = 0
    prev_node = [-1] * len(nodes)
    prev_edge = [-1] * len(nodes)   
    cost = 0
    while queue:
        u = queue.popleft()
        in_queue[u] = False
        for i, e in enumerate(nodes[u]):
            if e.cap > 0 and dist[e.to] > dist[u] + e.cost:
                dist[e.to] = dist[u] + e.cost
                nodes[e.to][e.rev].cost = -e.cost
                prev_node[e.to] = u
                prev_edge[e.to] = i
                if not in_queue[e.to]:
                    queue.append(e.to)
                    in_queue[e.to] = True
    max_flow = inf
    v = len(nodes) - 1
    if dist[v] == inf:
        return 0, 0
    while v != 0:
        u = prev_node[v]
        e = nodes[u][prev_edge[v]]
        max_flow = min(max_flow, e.cap)
        v = u
    v = len(nodes) - 1
    while v != 0:
        u = prev_node[v]
        e = nodes[u][prev_edge[v]]
        e.cap -= max_flow
        nodes[v][e.rev].cap += max_flow
        v = u
    cost += dist[len(nodes) - 1] * max_flow
    return max_flow, cost

def solve():
    n,m = map(int, input().split())
    need = list(map(int, input().split()))
    nodes = [[] for _ in range(m+2)]
    for _ in range(m):
        u,v,w = map(int, input().split())
        nodes[u].append(Edge(v+1, inf, w, len(nodes[v+1])))
        nodes[v+1].append(Edge(u, 0, -w, len(nodes[u]) - 1))
    for i in range(1,m+2):
        nodes[i].append(Edge(i+1, inf - need[i-1], 0, len(nodes[i+1])))
        nodes[i+1].append(Edge(i, 0, 0, len(nodes[i]) - 1))
    nodes[0].append(Edge(1, inf, 0, len(nodes[1])))
    nodes[1].append(Edge(0, 0, 0, len(nodes[0]) - 1))

    total_cost = 0
    cur_cost = 0
    while True:
        flow, cost = spfa(nodes)
        if flow == 0:
            break
        total_cost += cost
    print(total_cost)

    

if __name__ == '__main__':
    solve()