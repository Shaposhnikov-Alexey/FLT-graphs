from pyformlang.regular_expression import Regex
from pygraphblas import *

from src.main.util import *


class Graph:
    def __init__(self):
        self.size = 0
        # unless it is set the other way, start and final states include all of the vertices
        self.start_states = []
        self.final_states = []
        # label_dictionary matches boolean matrix to a label
        self.label_dictionary = {}

    def intersect_with(self, other):
        resulted_graph = Graph()

        # fill result matrix with labels' intersection
        for label in self.label_dictionary:
            if label in other.label_dictionary:
                #  tensor multiplication
                resulted_graph.label_dictionary[label] = self.label_dictionary[label].kronecker(
                                                                         other.label_dictionary[label])

        resulted_graph.size = self.size * other.size

        for i in self.start_states:
            for j in other.start_states:
                resulted_graph.start_states.append(i * self.size + j)
        for i in self.final_states:
            for j in other.final_states:
                resulted_graph.final_states.append(i * self.size + j)

        for label in resulted_graph.label_dictionary:
            print(label, ": ", resulted_graph.label_dictionary[label].nvals)
        print("\n\n")
        return resulted_graph

    def get_reachability(self, args):
        # create null matrix and adjust labels' matrices to its size
        output = Matrix.random(BOOL, self.size, self.size, 0).full(0)
        for label in self.label_dictionary:
            if self.label_dictionary[label].nrows < self.size:
                self.label_dictionary[label].resize(self.size, self.size)
            output = output | self.label_dictionary[label]
        output = transitive_closure(output)

        if args["type"] == 2:  # from sources to all reachability
            sources = args["from"]
            for i in range(self.size):
                if i not in sources:
                    output.assign_row(i, Vector.sparse(BOOL, self.size).full(0))
            return output
        elif args["type"] == 3:  # from sources to destination reachability
            sources = args.sources
            destinations = args.destinations
            for i in range(self.size):
                if i not in sources:
                    output.assign_row(i, Vector.sparse(BOOL, self.size).full(0))
                if i not in destinations:
                    output.assign_col(i, Vector.sparse(Bool, self.size).full(0))
            return output
        else:  # all-to-all reachability
            return output

    @staticmethod
    def from_file(path):
        graph = Graph()
        with open(path, 'r') as file:
            for line in file:
                (from_, label, to) = line.split(' ')
                from_ = int(from_)
                to = int(to)

                if max(from_, to) + 1 > graph.size:
                    graph.size = max(from_, to) + 1
                size = graph.size

                if label in graph.label_dictionary:
                    graph.label_dictionary[label].resize(size, size)
                    graph.label_dictionary[label][from_, to] = 1
                else:
                    boolean_matrix = Matrix.sparse(BOOL, size, size)
                    boolean_matrix[from_, to] = 1
                    graph.label_dictionary[label] = boolean_matrix
        for vertex in range(graph.size):
            graph.start_states.append(vertex)
            graph.final_states.append(vertex)

        file.close()
        return graph

    @staticmethod
    def from_regexp(path):
        graph = Graph()
        with open(path, 'r') as file:
            dfa = Regex.from_python_regex(file.read()).to_epsilon_nfa().to_deterministic().minimize()
        file.close()

        state_counter = 0
        dfa_states = {}
        for state in dfa._states:
            if state not in dfa_states:
                dfa_states[state] = state_counter
                state_counter += 1
        graph.size = state_counter

        for state in dfa._states:
            for symbol in dfa._input_symbols:
                reachable_states = dfa._transition_function(state, symbol)
                for out_state in reachable_states:
                    # add all edges in boolean matrix
                    if symbol in graph.label_dictionary:
                        graph.label_dictionary[symbol][dfa_states[state], dfa_states[out_state]] = 1
                    else:
                        boolean_matrix = Matrix.sparse(BOOL, graph.size, graph.size)
                        boolean_matrix[dfa_states[state], dfa_states[out_state]] = 1
                        graph.label_dictionary[symbol] = boolean_matrix

        # sync start and final states
        graph.start_states = [dfa_states[dfa.start_state]]
        for final_state in dfa._final_states:
            graph.final_states.append(dfa_states[final_state])

        return graph
