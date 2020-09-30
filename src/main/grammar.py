from pyformlang.cfg import CFG, Variable, Terminal, Production
from pygraphblas import Matrix, BOOL

from src.main.graph import Graph


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
    def cfpq(grammar: CFG, graph: Graph):
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
