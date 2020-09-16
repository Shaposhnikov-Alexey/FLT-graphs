from pygraphblas import BOOL, Matrix, Vector

from src.main.graph import Graph


def test_intersect():
    graph = Graph.from_file("src/data/test_graph.txt")
    automaton = Graph.from_regexp("src/data/test_regexp_1.txt")

    result = graph.intersect_with(automaton)

    assert result.label_dictionary["a"].nvals == 2
    assert result.label_dictionary["b"].nvals == 1
    assert result.label_dictionary["c"].nvals == 3
    assert result.size == graph.size * automaton.size


# --> This test works 1 of 4 times because of different final reachability presentation :c
# def test_intersected_reachability():
#     graph = Graph.from_file("typesrc/data/test_graph.txt")
#     automaton = Graph.from_regexp("src/data/test_regexp_2.txt")
#
#     result = graph.intersect_with(automaton)
#     args = {type: 1}
#     paths_matrix = result.get_reachability(args)
#
#     size = result.size
#     for i in range(size):
#         for j in range(4):
#             assert paths_matrix[i][j] == BOOL.zero
#     print(paths_matrix)
#     assert paths_matrix[1][5] == BOOL.one
#     assert paths_matrix[2][5] == BOOL.one
#     assert paths_matrix[1][6] == BOOL.one
#     assert paths_matrix[2][6] == BOOL.one
#     assert paths_matrix[5][6] == BOOL.one


def test_bad_regexp():
    graph = Graph.from_file("src/data/test_graph.txt")
    automaton = Graph.from_regexp("src/data/test_bad_regexp.txt")

    result = graph.intersect_with(automaton)
    args = {"type": 1}
    assert not result.label_dictionary
    assert result.get_reachability(args) == Matrix.dense(BOOL, 20, 20, 0).full(0)


def test_little():
    graph = Graph.from_file("src/data/test_little_graph.txt")
    automaton = Graph.from_regexp("src/data/test_simple_regexp.txt")

    result = graph.intersect_with(automaton)
    args = {"type": 1, "from": [1, 2]}
    paths_matrix = result.get_reachability(args)
    set_of_reachable = [(0, 1), (0, 2), (1, 2)]
    for i in range(result.size):
        for j in range(result.size):
            if (i, j) not in set_of_reachable:
                assert paths_matrix[i][j] == BOOL.zero


def test_little_with_from_parameters():
    graph = Graph.from_file("src/data/test_little_graph.txt")
    automaton = Graph.from_regexp("src/data/test_simple_regexp.txt")

    result = graph.intersect_with(automaton)
    args = {"type": 2, "from": [1]}
    paths_matrix = result.get_reachability(args)
    for i in range(len(paths_matrix)):
        if i in args["from"]:
            assert paths_matrix[0] != Vector.sparse(BOOL, result.size).full(0)
        else:
            assert paths_matrix[0] == Vector.sparse(BOOL, result.size).full(0)