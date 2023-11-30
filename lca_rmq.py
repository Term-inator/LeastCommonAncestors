class LCARMQ:
    def __init__(self, root, graph):
        self.time = 0
        self.graph = graph
        self.E = []  # Stores the Euler tour of the tree
        self.L = []  # Stores the levels of the nodes during Euler tour
        self.H = {}  # Stores the first occurrence of a node in E
        self.build_euler_tour(root, 0)

        # Preprocess for RMQ
        self.N = len(self.E)
        self.logn = [0] * (self.N + 1)
        self.preprocess_logn()
        self.st = [[0 for _ in range(self.N)] for _ in range(len(self.logn))]
        self.preprocess_rmq()

    def build_euler_tour(self, node, level):
        """ Build Euler tour for the tree. """
        if node is None:
            return
        self.H[node] = self.time
        self.E.append(node)
        self.L.append(level)
        self.time += 1
        for child in self.graph.get(node, []):
            if self.H.get(child, None) is None:
                self.build_euler_tour(child, level + 1)
                self.E.append(node)
                self.L.append(level)
                self.time += 1

    def preprocess_logn(self):
        """ Preprocess log values for RMQ. """
        for i in range(2, self.N + 1):
            self.logn[i] = self.logn[i // 2] + 1

    def preprocess_rmq(self):
        """ Preprocess for range minimum queries. """
        for i in range(self.N):
            self.st[i][0] = i  # Store index instead of level
        j = 1
        while (1 << j) <= self.N:
            i = 0
            while i + (1 << j) - 1 < self.N:
                if self.L[self.st[i][j - 1]] < self.L[self.st[i + (1 << (j - 1))][j - 1]]:
                    self.st[i][j] = self.st[i][j - 1]
                else:
                    self.st[i][j] = self.st[i + (1 << (j - 1))][j - 1]
                i += 1
            j += 1

    def query_rmq(self, L, R):
        """ Query for RMQ in range [L, R]. """
        j = self.logn[R - L + 1]
        if self.L[self.st[L][j]] <= self.L[self.st[R - (1 << j) + 1][j]]:
            return self.E[self.st[L][j]]
        else:
            return self.E[self.st[R - (1 << j) + 1][j]]

    def lca(self, u, v):
        """ Find LCA of nodes u and v. """
        if self.H[u] > self.H[v]:
            u, v = v, u
        return self.query_rmq(self.H[u], self.H[v])
