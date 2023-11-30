class LCABinaryLifting:
    def __init__(self, root, graph, max_depth):
        self.graph = graph
        self.N = len(graph)
        self.max_depth = max_depth
        self.ancestor = [[-1 for _ in range(max_depth)] for _ in range(self.N + 1)]
        self.depth = [0] * (self.N + 1)
        self.preprocess(root, -1)

    def preprocess(self, node, parent):
        self.ancestor[node][0] = parent
        for i in range(1, self.max_depth):
            if self.ancestor[node][i - 1] != -1:
                self.ancestor[node][i] = self.ancestor[self.ancestor[node][i - 1]][i - 1]
        for child in self.graph.get(node, []):
            if child != parent:
                self.depth[child] = self.depth[node] + 1
                self.preprocess(child, node)

    def lca(self, u, v):
        if self.depth[u] < self.depth[v]:
            u, v = v, u
        diff = self.depth[u] - self.depth[v]
        for i in range(self.max_depth):
            if diff & (1 << i):
                u = self.ancestor[u][i]

        if u == v:
            return u
        for i in range(self.max_depth - 1, -1, -1):
            if self.ancestor[u][i] != self.ancestor[v][i]:
                u = self.ancestor[u][i]
                v = self.ancestor[v][i]
        return self.ancestor[u][0]