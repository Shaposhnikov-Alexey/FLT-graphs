from pyformlang.cfg import CFG, Variable, Terminal, Production
from pygraphblas import Matrix, BOOL, semiring

from src.main.graph import Graph
from src.main.rfa import RFA
from src.main.util import transitive_closure, get_reachable


class GrammarUtils:
    @staticmethod
    def to_cnf(cfg):
        if cfg.generate_epsilon():
            cfg = cfg.to_normal_form()
            new_start_symbol = Variable(cfg.start_symbol.value + "'")
            cfg.productions.add(Production(new_start_symbol, []))
            res = CFG(variables=cfg.variables,
                      terminals=cfg.terminals,
                      start_symbol=new_start_symbol)
            res.variables.add(new_start_symbol)
            for production in cfg.productions:
                if production.head == cfg.start_symbol:
                    res.productions.add(Production(new_start_symbol, production.body))
                res.productions.add(production)
            return res

        return cfg.to_normal_form()

    @staticmethod
    def from_file(path) -> CFG:
        productions = []

        with open(path, 'r') as file:
            for line in file:
                raw_current_production = line.split()
                current_production = raw_current_production[0] + ' -> ' + ' '.join(raw_current_production[1:])
                productions.append(current_production)

        productions = '\n'.join(productions)
        return CFG.from_text(productions)

    @staticmethod
    def cyk(cnf, word):
        word_size = len(word)
        if word_size == 0:
            return cnf.generate_epsilon()

        table = [
            [set() for _ in range(word_size)]
            for _ in range(word_size)
        ]

        for i in range(word_size):
            for production in cnf.productions:
                if production.body == [Terminal(word[i])]:
                    table[i][i].add(production.head)

        for i in range(word_size):
            for j in range(word_size - i):
                for k in range(i):
                    first = table[j][j + k]
                    second = table[j + k + 1][j + i]
                    for production in cnf.productions:
                        if (len(production.body) == 2 and production.body[0] in first
                                and production.body[1] in second):
                            table[j][j + i].add(production.head)

        return cnf.start_symbol in table[0][word_size - 1]

    @staticmethod
    def cfpq_hellings(grammar: CFG, graph: Graph):
        cfg = GrammarUtils.to_cnf(grammar)
        graph_size = graph.size
        start_sym = cfg.start_symbol
        result = Graph()
        result.size = graph_size
        for variable in cfg.variables:
            result.label_dictionary[variable] = Matrix.sparse(BOOL, graph_size, graph_size)

        for label in graph.label_dictionary:
            terminal = Terminal(label)
            result.label_dictionary[terminal] = graph.label_dictionary[label].dup()
            for from_vertex, to_vertex in graph.get_edges(label):
                for production in cfg.productions:
                    if len(production.body) == 1 and production.body[0] == terminal:
                        head = production.head
                        result.label_dictionary[head][from_vertex, to_vertex] = 1

        if cfg.generate_epsilon():
            for vertex in range(graph_size):
                result.label_dictionary[start_sym][vertex, vertex] = 1

        matrix_changing = True
        while matrix_changing:
            matrix_changing = False
            for production in cfg.productions:
                head = production.head
                body = production.body
                if len(body) == 2:
                    for (i, m) in result.get_edges(body[0]):
                        for (k, j) in result.get_edges(body[1]):
                            if k == m:
                                if (i, j) not in result.get_edges(head):
                                    matrix_changing = True
                                    result.label_dictionary[head][i, j] = 1

        return result.label_dictionary[start_sym]

    @staticmethod
    def cfpq_matrix(graph: Graph, grammar: CFG):
        size = graph.size
        if size == 0:
            return Matrix.sparse(BOOL, size, size)
        result = Graph()
        start_symbol = grammar.start_symbol
        result.size = size
        for variable in grammar.variables:
            result.label_dictionary[variable] = Matrix.sparse(BOOL, size, size)

        for label in graph.label_dictionary:
            terminal = Terminal(label)
            result.label_dictionary[terminal] = graph.label_dictionary[label].dup()

            for from_, to in graph.get_edges(label):
                for production in grammar.productions:
                    if len(production.body) == 1 and production.body[0] == terminal:
                        head = production.head
                        result.label_dictionary[head][from_, to] = 1

        if grammar.generate_epsilon():
            for vertex in graph.vertices:
                result.label_dictionary[start_symbol][vertex, vertex] = 1

        matrix_changing = True
        with semiring.LOR_LAND_BOOL:
            while matrix_changing:
                matrix_changing = False
                for production in grammar.productions:
                    head = production.head
                    body = production.body
                    if len(body) == 2:
                        previous = result.label_dictionary[head].nvals
                        current = result.label_dictionary[body[0]] @ result.label_dictionary[body[1]]
                        result.label_dictionary[head] = result.label_dictionary[head] + current
                        if previous != result.label_dictionary[head].nvals:
                            matrix_changing = True

        return result.label_dictionary[start_symbol]

    @staticmethod
    def cfpq_tensor(graph: Graph, grammar: CFG):
        rfa = RFA().from_cfg(grammar)
        result = Graph()
        result.size = graph.size
        if graph.size == 0:
            return Matrix.sparse(BOOL, graph.size, graph.size)

        for label in graph.label_dictionary:
            result.label_dictionary[label] = graph.label_dictionary[label].dup()

        for label in rfa.label_dictionary:
            if label not in result.label_dictionary:
                result.label_dictionary[label] = Matrix.sparse(BOOL, graph.size, graph.size)

        for term in grammar.terminals:
            if term.value not in result.label_dictionary:
                result.label_dictionary[term.value] = Matrix.sparse(BOOL, graph.size, graph.size)

        for production in grammar.productions:
            if not production.body:
                for vertex in graph.vertices:
                    result.label_dictionary[production.head.value][vertex, vertex] = 1

        matrix_changing = True
        closure = None
        while matrix_changing:
            matrix_changing = False
            dictionary = {}
            size = 0
            for label in rfa.label_dictionary:
                dictionary[label] = result.label_dictionary[label].kronecker(rfa.label_dictionary[label])
                if size == 0:
                    size = dictionary[label].ncols

            intersection = Matrix.sparse(BOOL, size, size)
            with semiring.LOR_LAND_BOOL:
                for label in dictionary:
                    if dictionary[label].nrows < size:
                        dictionary[label].resize(size, size)
                    intersection += dictionary[label]

            if closure is None:
                previous = 0
            else:
                previous = closure.nvals
            closure = transitive_closure(intersection)

            for start, end in get_reachable(closure):
                start_m = start // rfa.size
                start_rfa = start % rfa.size
                end_m = end // rfa.size
                end_rfa = end % rfa.size

                if start_rfa in rfa.start_states and end_rfa in rfa.final_states:
                    label = rfa.head_by_vertices[(start_rfa, end_rfa)]
                    result.label_dictionary[label][start_m, end_m] = 1

            if previous != closure.nvals:
                matrix_changing = True

        return result.label_dictionary[grammar.start_symbol.value]
