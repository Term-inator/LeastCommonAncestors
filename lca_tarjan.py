class LCATarjan:
    def __init__(self, graph):
        self.graph = graph
        self.ancestor = {}
        self.visited = set()
        self.union_find = {}

    def find(self, u):
        if self.union_find[u] != u:
            self.union_find[u] = self.find(self.union_find[u])
        return self.union_find[u]

    def union(self, u, v):
        root_u = self.find(u)
        root_v = self.find(v)
        self.union_find[root_v] = root_u

    def tarjan_lca(self, node, queries, answers):
        self.ancestor[node] = node
        self.visited.add(node)
        for child in self.graph.get(node, []):
            if child not in self.visited:
                self.tarjan_lca(child, queries, answers)
                self.union(child, node)
                self.ancestor[self.find(node)] = node
        for pair in queries:
            u, v = pair
            if node == u and v in self.visited:
                answers[pair] = self.ancestor[self.find(v)]
            elif node == v and u in self.visited:
                answers[pair] = self.ancestor[self.find(u)]

    def lca(self, queries):
        answers = {}
        for node in self.graph:
            self.union_find[node] = node
        self.tarjan_lca(next(iter(self.graph)), queries, answers)
        return [answers[query] for query in queries]