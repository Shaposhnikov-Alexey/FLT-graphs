from pygraphblas import *

from src.main.grammar import GrammarUtils
from src.main.graph import Graph


def get_reachable(matrix):
    return zip(*matrix.select(lib.GxB_NONZERO).to_lists()[:2])


def test_cfpq_brackets():
    cfg = GrammarUtils.from_file("src/data/test_cfpq_grammar_brackets.txt")
    graph = Graph.from_file("src/data/test_cfpq_graph.txt")

    expected = [(3, 3, True),
                (0, 4, True),
                (1, 3, True),
                (2, 4, True),
                (0, 0, True),
                (1, 1, True),
                (2, 2, True),
                (3, 3, True),
                (4, 4, True)]
    result = GrammarUtils.cfpq(cfg, graph)
    assert set(result) == set(expected)


def test_cfpq_empty():
    cfg = GrammarUtils.from_file("src/data/test_cfpq_grammar_brackets.txt")
    result = GrammarUtils.cfpq(cfg, Graph())

    assert set() == set(get_reachable(result))
