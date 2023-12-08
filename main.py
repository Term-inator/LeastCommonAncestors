import random
import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
import time

from lca import LCANaive
from lca_bin import LCABinaryLifting
from lca_tarjan import LCATarjan
from lca_rmq import LCARMQ


def gen_tree(max_depth, max_children):
    """
    :param max_depth: Maximum depth of the tree.
    :param max_children: Maximum number of children a node can have.
    :return: A dictionary representing the tree structure.
    """
    # Generate the tree level by level, each node has 1 to max_children children
    node_id = 1
    tree_graph = {node_id: []}
    queue = [(node_id, 1)]
    while queue:
        node, depth = queue.pop(0)
        if depth == max_depth:
            continue
        num_children = random.randint(1, max_children)
        for _ in range(num_children):
            node_id += 1
            tree_graph[node].append(node_id)
            tree_graph[node_id] = []
            queue.append((node_id, depth + 1))
    return tree_graph, node_id


def visualize_tree(tree_graph):
    """
    :param tree_graph: A dictionary representing the tree structure.
    """
    # Visualize the tree
    G = nx.Graph()
    for node in tree_graph:
        for child in tree_graph[node]:
            G.add_edge(node, child)
    pos = nx.spring_layout(G)
    nx.draw_networkx(G, pos, with_labels=True)
    plt.show()


def gen_test_cases(node_num, num):
    """
    :param node_num: Number of nodes in the tree.
    :param num: Number of test cases to generate.
    :return: A list of test cases.
    """
    test_cases = []
    while len(test_cases) < num:
        u = random.randint(node_num // 2, node_num)
        v = random.randint(node_num // 2, node_num)
        test_cases.append((u, v))
    return test_cases


def timeit(func, *args, **kwargs):
    """
    :param func: The function to time.
    :param args: Positional arguments to pass to the function.
    :param kwargs: Keyword arguments to pass to the function.
    :return: The time taken to run the function.
    """
    start = time.time()
    r = func(*args, **kwargs)
    end = time.time()
    return end - start, r


def lca_test(lca, test_cases):
    return [lca.lca(u, v) for u, v in test_cases]


lca_mem = {}


def lca_naive(graph, test_cases):
    """
    :param graph: A dictionary representing the tree structure.
    :param test_cases: A list of test cases.
    :return: A list of LCAs.
    """
    if lca_mem.get('naive'):
        t1, lca = 0, lca_mem['naive']
    else:
        t1, lca = timeit(lambda: LCANaive(1, graph))
        lca_mem['naive'] = lca
    t2, r = timeit(lca_test, lca, test_cases)
    return t1, t2, r


def lca_bin(graph, test_cases):
    """
    :param graph: A dictionary representing the tree structure.
    :param test_cases: A list of test cases.
    :return: A list of LCAs.
    """
    if lca_mem.get('bin'):
        t1, lca = 0, lca_mem['bin']
    else:
        t1, lca = timeit(lambda: LCABinaryLifting(1, graph))
        lca_mem['bin'] = lca
    t2, r = timeit(lca_test, lca, test_cases)
    return t1, t2, r


def lca_tarjan(graph, test_cases):
    """
    :param graph: A dictionary representing the tree structure.
    :param test_cases: A list of test cases.
    :return: A list of LCAs.
    """
    t1, lca = timeit(lambda: LCATarjan(graph))
    for u, v in test_cases:
        lca.add_query(u, v)
    t2, r = timeit(lca.lca, 1)
    return t1, t2, r


def lca_rmq(graph, test_cases):
    """
    :param graph: A dictionary representing the tree structure.
    :param test_cases: A list of test cases.
    :return: A list of LCAs.
    """
    if lca_mem.get('rmq'):
        t1, lca = 0, lca_mem['rmq']
    else:
        t1, lca = timeit(lambda: LCARMQ(1, graph))
        lca_mem['rmq'] = lca
    t2, r = timeit(lca_test, lca, test_cases)
    return t1, t2, r


if __name__ == "__main__":
    tree_graph, node_num = gen_tree(8, 5)
    print(tree_graph, node_num)
    print('Tree generated')
    # visualize_tree(tree_graph)

    ns = np.logspace(3, 6, 5, base=10).astype(int)
    res = {
        'naive_init': [],
        'naive_query': [],
        'bin_init': [],
        'bin_query': [],
        'tarjan_init': [],
        'tarjan_query': [],
        'rmq_init': [],
        'rmq_query': []
    }

    for n in ns:
        print(n)
        test_cases = gen_test_cases(node_num, n)
        print('Test cases generated')

        t1_naive, t2_naive, r_naive = lca_naive(tree_graph, test_cases)
        res['naive_init'].append(t1_naive)
        res['naive_query'].append(t2_naive)
        print('Naive LCA initialization time: ', t1_naive)
        print('Naive LCA query time: ', t2_naive)

        t1_bin, t2_bin, r_bin = lca_bin(tree_graph, test_cases)
        res['bin_init'].append(t1_bin)
        res['bin_query'].append(t2_bin)
        print('Binary Lifting LCA initialization time: ', t1_bin)
        print('Binary Lifting LCA query time: ', t2_bin)

        t1_tarjan, t2_tarjan, r_tarjan = lca_tarjan(tree_graph, test_cases)
        res['tarjan_init'].append(t1_tarjan)
        res['tarjan_query'].append(t2_tarjan)
        print('Tarjan LCA initialization time: ', t1_tarjan)
        print('Tarjan LCA query time: ', t2_tarjan)

        t1_rmq, t2_rmq, r_rmq = lca_rmq(tree_graph, test_cases)
        res['rmq_init'].append(t1_rmq)
        res['rmq_query'].append(t2_rmq)
        print('RMQ LCA initialization time: ', t1_rmq)
        print('RMQ LCA query time: ', t2_rmq)
        print()

    plt.plot(ns, res['naive_query'], label='Naive')
    plt.plot(ns, res['bin_query'], label='Doubling')
    plt.plot(ns, res['tarjan_query'], label='Tarjan')
    plt.plot(ns, res['rmq_query'], label='RMQ')
    plt.legend()
    plt.xlabel('Number of test cases')
    plt.ylabel('Time (s)')
    plt.title('Query time')
    plt.show()
