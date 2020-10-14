from pyformlang.cfg import CFG
from pygraphblas import Matrix, BOOL

from src.main.graph import Graph


class RFA(Graph):
    def __init__(self):
        Graph.__init__(self)
        self.head_by_vertices = {}

    def from_cfg(self, cfg: CFG):
        size = 0
        for production in cfg.productions:
            size += 1 + len(production.body)
        self.size = size
        vertex_index = 0
        for production in cfg.productions:
            if production.head.value not in self.label_dictionary:
                self.label_dictionary[production.head.value] = Matrix.sparse(BOOL, self.size, self.size)

            if production.body:
                self.start_states.append(vertex_index)

            self.head_by_vertices[(vertex_index, vertex_index + len(production.body))] = production.head.value

            for body_symbol in production.body:
                symbol = body_symbol.value
                if symbol not in self.label_dictionary:
                    self.label_dictionary[symbol] = Matrix.sparse(BOOL, self.size, self.size)
                self.label_dictionary[symbol][vertex_index, vertex_index + 1] = 1
                self.vertices.add(vertex_index)
                self.vertices.add(vertex_index + 1)
                vertex_index += 1
            self.final_states.append(vertex_index)
            self.vertices.add(vertex_index)
            vertex_index += 1

        return self
