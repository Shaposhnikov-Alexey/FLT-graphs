from pygraphblas import *

from src.main.grammar import GrammarUtils
from src.main.graph import Graph
from src.main.util import get_reachable

expected_brackets = [(3, 3, True),
                     (0, 4, True),
                     (1, 3, True),
                     (2, 4, True),
                     (0, 0, True),
                     (1, 1, True),
                     (2, 2, True),
                     (3, 3, True),
                     (4, 4, True)]

expected_simple = [(0, 0, True),
                   (1, 1, True),
                   (0, 2, True),
                   (3, 3, True),
                   (2, 2, True)]

expected_triple = [(0, 1, True), (4, 4, True), (2, 4, True), (1, 2, True),
                   (0, 4, True), (3, 4, True), (0, 0, True), (4, 3, True),
                   (1, 1, True), (0, 3, True), (1, 4, True), (2, 3, True),
                   (0, 2, True), (3, 3, True), (2, 2, True), (1, 3, True)]


# hellings tests
def test_cfpq_hellings_brackets():
    cfg = GrammarUtils.from_file("src/data/test_cfpq_grammar_brackets.txt")
    graph = Graph.from_file("src/data/test_cfpq_graph.txt")

    result = GrammarUtils.cfpq_hellings(cfg, graph)
    assert set(result) == set(expected_brackets)


def test_cfpq_hellings_empty():
    cfg = GrammarUtils.from_file("src/data/test_cfpq_grammar_brackets.txt")
    result = GrammarUtils.cfpq_hellings(cfg, Graph())

    assert set() == set(get_reachable(result))


# matrix multiplication tests
def test_cfpq_matrix_brackets():
    cfg = GrammarUtils.from_file("src/data/test_cfpq_grammar_brackets.txt")
    grammar = GrammarUtils.to_cnf(cfg)
    graph = Graph.from_file("src/data/test_cfpq_graph.txt")

    result = GrammarUtils.cfpq_matrix(graph, grammar)
    assert set(result) == set(expected_brackets)


def test_cfpq_matrix_simple():
    cfg = GrammarUtils.from_file("src/data/test_cfpq_grammar_simple.txt")
    grammar = GrammarUtils.to_cnf(cfg)
    graph = Graph.from_file("src/data/test_cfpq_graph_simple.txt")

    result = GrammarUtils.cfpq_matrix(graph, grammar)
    assert set(result) == set(expected_simple)


def test_cfpq_matrix_triple():
    cfg = GrammarUtils.from_file("src/data/test_cfpq_grammar_triple.txt")
    grammar = GrammarUtils.to_cnf(cfg)
    graph = Graph.from_file("src/data/test_cfpq_graph_triple.txt")

    result = GrammarUtils.cfpq_matrix(graph, grammar)
    assert set(result) == set(expected_triple)


def test_cfpq_matrix_empty():
    cfg = GrammarUtils.from_file("src/data/test_cfpq_grammar_brackets.txt")
    result = GrammarUtils.cfpq_matrix(Graph(), cfg)

    assert set() == set(get_reachable(result))


# tensor production tests
def test_cfpq_tensor_brackets():
    cfg = GrammarUtils.from_file("src/data/test_cfpq_grammar_brackets.txt")
    graph = Graph.from_file("src/data/test_cfpq_graph.txt")

    result = GrammarUtils.cfpq_tensor(graph, cfg)
    assert set(result) == set(expected_brackets)


def test_cfpq_tensor_simple():
    cfg = GrammarUtils.from_file("src/data/test_cfpq_grammar_simple.txt")
    graph = Graph.from_file("src/data/test_cfpq_graph_simple.txt")

    result = GrammarUtils.cfpq_tensor(graph, cfg)
    assert set(result) == set(expected_simple)


def test_cfpq_tensor_triple():
    cfg = GrammarUtils.from_file("src/data/test_cfpq_grammar_triple.txt")
    graph = Graph.from_file("src/data/test_cfpq_graph_triple.txt")

    result = GrammarUtils.cfpq_tensor(graph, cfg)
    assert set(result) == set(expected_triple)


def test_cfpq_tensor_empty():
    cfg = GrammarUtils.from_file("src/data/test_cfpq_grammar_brackets.txt")
    result = GrammarUtils.cfpq_tensor(Graph(), cfg)

    assert set() == set(get_reachable(result))
