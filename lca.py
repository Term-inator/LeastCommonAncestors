class LCANaive:
    def __init__(self, root, graph):
        self.graph = graph
        self.root = root
        self.parent = {root: None}  # Store the parent of each node
        self.build_parent_mapping(root)
        print(self.parent)

    def build_parent_mapping(self, node):
        """ Builds a mapping from each node to its parent. """
        for child in self.graph.get(node, []):
            self.parent[child] = node
            self.build_parent_mapping(child)

    def find_path(self, node, path):
        """ Finds the path from the given node to the root. """
        while node is not None:
            path.append(node)
            node = self.parent[node]

    def lca(self, u, v):
        """ Finds the LCA of nodes u and v. """
        path_u = []
        self.find_path(u, path_u)
        path_v = []
        self.find_path(v, path_v)

        # Find the common ancestor
        lca_node = None
        i = len(path_u) - 1
        j = len(path_v) - 1
        while i >= 0 and j >= 0 and path_u[i] == path_v[j]:
            lca_node = path_u[i]
            i -= 1
            j -= 1
        return lca_node
