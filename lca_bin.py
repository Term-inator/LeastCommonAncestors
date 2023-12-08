class LCABinaryLifting:
    def __init__(self, root, tree):
        self.n = len(tree)  # number of nodes
        self.lg = max(1, self.n.bit_length())  # maximum depth
        self.tree = tree
        self.up = [[-1 for _ in range(self.lg)] for _ in range(self.n + 1)]  # stores 2^i th ancestor
        self.depth = [0] * (self.n + 1)  # stores depth of each node
        self.dfs(root, -1)

    def dfs(self, node, parent):
        """ Perform DFS to populate `up` and `depth` arrays. """
        self.up[node][0] = parent
        for i in range(1, self.lg):
            if self.up[node][i - 1] != -1:
                self.up[node][i] = self.up[self.up[node][i - 1]][i - 1]

        for child in self.tree.get(node, []):
            if child != parent:
                self.depth[child] = self.depth[node] + 1
                self.dfs(child, node)

    def lca(self, a, b):
        """ Find the LCA of nodes `a` and `b`. """
        if self.depth[a] < self.depth[b]:
            a, b = b, a

        # to same depth
        for i in range(self.lg - 1, -1, -1):
            if self.depth[a] - (1 << i) >= self.depth[b]:
                a = self.up[a][i]

        if a == b:
            return a

        for i in range(self.lg - 1, -1, -1):
            if self.up[a][i] != self.up[b][i]:
                a = self.up[a][i]
                b = self.up[b][i]

        return self.up[a][0]