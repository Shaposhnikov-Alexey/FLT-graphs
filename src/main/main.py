import sys
import time
from os import path

from src.main.graph import Graph


def benchmark_test(graph, automaton, regex_name):
    start_intersect = 0
    end_intersect = 0
    start_reachability = 0
    end_reachability = 0
    args = {"type": 1}
    for i in range(5):
        start_intersect += time.time_ns()
        result = graph.intersect_with(automaton)
        end_intersect += time.time_ns()

        start_reachability += time.time_ns()
        matrix = result.get_reachability(args)
        end_reachability += time.time_ns()

    print('{}: {} {} - {}'.format(path.basename(regex_name), (end_intersect - start_intersect) / 5 // 1000000,
                                  (end_reachability - start_reachability) / 5 // 1000000, matrix.nvals))


if __name__ == '__main__':
    assert sys.argv[1] is not None and path.isfile(
        sys.argv[1]), 'First argument should be [{}].'.format(path_to_graph.txt)
    assert sys.argv[2] is not None and path.isfile(
        sys.argv[2]), 'Second argument should be [{}].'.format(path_to_regexp.txt)
    # if len(sys.argv) > 2:
    # Parse command arguments: TODO later
    graph = Graph.from_file(sys.argv[1])
    automaton = Graph.from_regexp(sys.argv[2])
    benchmark_test(graph, automaton, sys.argv[2])
