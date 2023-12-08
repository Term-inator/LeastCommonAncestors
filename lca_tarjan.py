from collections import defaultdict


class LCATarjan:
    def __init__(self, tree):
        self.tree = tree
        self.ancestor = {}  # stores the ancestor of each node
        self.visited = set()
        self.parent = {}
        self.results = defaultdict(int)
        self.queries = defaultdict(list)

    def find(self, node):
        if self.parent[node] != node:
            self.parent[node] = self.find(self.parent[node])
        return self.parent[node]

    def union(self, node1, node2):
        root1 = self.find(node1)
        root2 = self.find(node2)
        if root1 != root2:
            self.parent[root2] = root1

    def add_query(self, node1, node2):
        self.queries[node1].append(node2)
        self.queries[node2].append(node1)

    def lca(self, node):
        self.parent[node] = node
        self.ancestor[node] = node
        for child in self.tree[node]:
            self.lca(child)
            self.union(node, child)
            self.ancestor[self.find(node)] = node
        self.visited.add(node)
        for other in self.queries[node]:
            if other in self.visited:
                self.results[(node, other)] = self.ancestor[self.find(other)]