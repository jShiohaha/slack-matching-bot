import itertools
import random

# external package imports
from collections import OrderedDict

def build_empty_graph(items):
    graph = OrderedDict()
    for item in items:
        graph[item] = []
    return graph


def build_graph(items, graph=None):
    if graph is None:
        graph = build_empty_graph(items)
    # constant 2 dictates combination size
    for group in list(itertools.combinations(items, 2)):
        n1, n2 = group[0], group[1]
        graph[n1].append(n2)
        graph[n2].append(n1)
    return graph


def remove_bidir_graph_edge(n1, n2, graph):
    if n2 in graph[n1]:
        graph[n1].remove(n2)
    if n1 in graph[n2]:
        graph[n2].remove(n1)
