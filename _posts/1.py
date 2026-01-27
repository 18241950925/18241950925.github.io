import sys
from collections import deque

# 增加递归深度，防止深搜或特殊情况爆栈（虽然这里主要用迭代）
sys.setrecursionlimit(200000)

class Edge:
    def __init__(self, to, cap, cost, rev):
        self.to = to
        self.cap = cap
        self.cost = cost
        self.rev = rev  # 反向边在 nodes[to] 中的下标

def solve():
    # --- 1. 修复输入处理 ---
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        p = int(next(iterator))
        m = int(next(iterator))
        f = int(next(iterator))
        n = int(next(iterator))
        s = int(next(iterator))
        require = [int(next(iterator)) for _ in range(N)]
    except StopIteration:
        return

    # 源点 S, 汇点 T
    S = 0
    T = 2 * N + 1
    graph = [[] for _ in range(T + 2)]

    # --- 2. 修复加边逻辑（必须添加反向边） ---
    def add_edge(u, v, cap, cost):
        # 正向边: graph[u] 的最后一个元素
        # 反向边: graph[v] 的最后一个元素
        graph[u].append([v, cap, cost, len(graph[v])])
        graph[v].append([u, 0, -cost, len(graph[u]) - 1])

    # 建图
    for i in range(1, N + 1):
        ri = require[i-1]
        # 节点定义：
        # i: 第i天晚上（产出脏资源）
        # i+N: 第i天早上（需要新资源）
        
        supply_node = i
        demand_node = i + N

        # 1. 源点 -> 脏资源 (接收脏餐巾)
        add_edge(S, supply_node, ri, 0)
        
        # 2. 新资源 -> 汇点 (必须满足需求)
        add_edge(demand_node, T, ri, 0)
        
        # 3. 源点 -> 新资源 (直接购买)
        add_edge(S, demand_node, float('inf'), p)
        
        # 4. 脏资源延期 (留到明天)
        if i < N:
            add_edge(supply_node, supply_node + 1, float('inf'), 0)
            
        # 5. 快洗
        if i + m <= N:
            add_edge(supply_node, demand_node + m, float('inf'), f)
            
        # 6. 慢洗
        if i + n <= N:
            add_edge(supply_node, demand_node + n, float('inf'), s)

    # --- 3. 标准 SPFA + MCMF ---
    min_cost = 0
    max_flow = 0
    
    while True:
        dist = [float('inf')] * (T + 2)
        parent_node = [-1] * (T + 2)
        parent_edge_idx = [-1] * (T + 2)
        in_queue = [False] * (T + 2)
        
        queue = deque([S])
        dist[S] = 0
        in_queue[S] = True
        
        # SPFA 找最短路
        while queue:
            u = queue.popleft()
            in_queue[u] = False
            
            for idx, (v, cap, cost, rev) in enumerate(graph[u]):
                if cap > 0 and dist[v] > dist[u] + cost:
                    dist[v] = dist[u] + cost
                    parent_node[v] = u
                    parent_edge_idx[v] = idx
                    if not in_queue[v]:
                        queue.append(v)
                        in_queue[v] = True
        
        if dist[T] == float('inf'):
            break
            
        # 寻找增广路上的最小流量
        flow = float('inf')
        curr = T
        while curr != S:
            p_node = parent_node[curr]
            edge_idx = parent_edge_idx[curr]
            flow = min(flow, graph[p_node][edge_idx][1]) # 1 is cap
            curr = p_node
            
        # 更新流量和费用
        max_flow += flow
        min_cost += flow * dist[T]
        
        curr = T
        while curr != S:
            p_node = parent_node[curr]
            edge_idx = parent_edge_idx[curr]
            
            # 更新正向边
            graph[p_node][edge_idx][1] -= flow
            
            # 更新反向边 (通过 rev 索引直接找到)
            rev_idx = graph[p_node][edge_idx][3]
            graph[curr][rev_idx][1] += flow
            
            curr = p_node

    print(min_cost)

if __name__ == '__main__':
    solve()