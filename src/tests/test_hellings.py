from pygraphblas import *

from src.main.grammar import CFPQ
from src.main.graph import Graph


def get_reachable(matrix):
    return zip(*matrix.select(lib.GxB_NONZERO).to_lists()[:2])


def test_hellings_brackets():
    cfg = CFPQ.from_file("src/data/test_hellings_grammar_brackets.txt")
    graph = Graph.from_file("src/data/test_hellings_graph.txt")

    expected = [(3, 3, True),
                (0, 4, True),
                (1, 3, True),
                (2, 4, True),
                (0, 0, True),
                (1, 1, True),
                (2, 2, True),
                (3, 3, True),
                (4, 4, True)]
    result = CFPQ.hellings(cfg, graph)
    assert set(result) == set(expected)


def test_hellings_empty():
    cfg = CFPQ.from_file("src/data/test_hellings_grammar_brackets.txt")
    result = CFPQ.hellings(cfg, Graph())

    assert set() == set(get_reachable(result))
