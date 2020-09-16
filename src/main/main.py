import sys
from os import path

from src.main.graph import Graph

if __name__ == '__main__':
    assert sys.argv[1] is not None and path.isfile(
        sys.argv[1]), f'First argument should be [path_to_graph.txt].'
    assert sys.argv[2] is not None and path.isfile(
        sys.argv[2]), f'Second argument should be [path_to_regexp.txt].'
    # if len(sys.argv) > 3:
    # Parse command arguments: TODO later
    graph = Graph.from_file(sys.argv[1])
    automaton = Graph.from_regexp(sys.argv[2])
    result = graph.intersect_with(automaton)
