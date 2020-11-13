from src.main.grammar import GrammarUtils
from src.query_language.language_helper import check_script_with_cyk

test_input = [('a: term (a) star concat term (b)', True),
              ('''
              connect "/src/data"
              ''', True),
              ('''
              a: term (a) star concat term (b)
              c: nonterm (b) star
              f: nonterm (b) alt nonterm (c) star concat term (s)
              ''', True),
              ('''
              select count edges from name "graph" intersect grammar
              ''', True),
              ('''
              select count edges from setStartAndFinal ( range  4 , 5 ; none ) name "graph" intersect name "other_graph"
              ''', True),
              ('''
              select edges from setStartAndFinal ( 1, 2, 3 ; range  4, 5 ) name "graph" intersect name "other_graph"
              ''', True),
              ('''
              select filter edges with (1, edge, 2) satisfies 1 labelIs first from name "graph"
              ''', True),
              ('''
              select filter edges with (1, edge, 2) satisfies isStart 1 and isFinal 2 from name "graph"
              ''', True),
              ('''
              select filter edges with (1, edge, 2) satisfies 1 labelIs first and not 2 labelIs first from name "graph"
              ''', True),
              ('''
              select edges from query nonterm (a) concat nonterm (b) alt term (s) opt alt nonterm (n) star
              ''', True),
              ('''
              select edges from name "graph" intersect query nonterm (a) concat nonterm (b) plus
              ''', True),
              ('''
              connect "src/data"
              select count edges from setStartAndFinal (1, 2, 3 ; 4, 5, 6) name "graph" intersect query term (a) star concat term (b) plus
               ''', True),
              ('''
              connect "src/data"
              s: nonterm (b) star concat term (f) opt
              f: nonterm (a) alt nonterm (b) concat term (q)
              q: nonterm (c) star
              select filter edges with (24, edge, 26) satisfies 24 labelIs first and not 26 labelIs first or isFinal 26 
                from name "graph" intersect grammar
              ''', True),
              # Rest are wrong cases
              ('''
              select count edges from "graph" intersect grammar
              ''', False),
              ('''
              select count edges from setStartAndFinal  range  4 , 5 ; none name "graph" intersect name "other_graph"
              ''', False),
              ('''
              select edges from setStartAndFinal ( 1, 2, 3  range  4, 5 ) name "graph" intersect name "other_graph"
              ''', False),
              ('''
              select filter edges with (1 edge  2) satisfies 1 labelIs first from name "graph"
              ''', False),
              ('''
              select filter edges with (1, edge, 2) satisfies isStart 1  isFinal 2 from name "graph"
              ''', False),
              ('''
              select filter edges with 1, edge, 2 satisfies 1 labelIs first and not 2 labelIs first from name "graph"
              ''', False),
              # there must be empty space before and after parentheses
              ('''
              select edges from query nonterm(a) concat nonterm(b) alt term (s) opt alt nonterm (n) star
              ''', False),
              # there must be concat in regexp
              ('''
              select edges from name "graph" intersect query nonterm (a) nonterm (b) plus
              ''', False),
              # name should be in ""
              ('''
              connect src/data
              select count edges from setStartAndFinal (1, 2, 3 ; 4, 5, 6) name "graph" intersect query term (a) star concat term (b) plus
               ''', False),
              # there must be defined what to select
              ('select from name "graph"', False),
              ('select cont from name "graph"', False),
              ('select edgs from name "graph"', False),
              ('select edges from name "graph" intersect ', False),
              ('select from name "graph"', False),
              # wrong types
              ('''
              select count edges from setStartAndFinal ( range  ab , 5 ; none ) name "graph" intersect name "other_graph"
              ''', False),
              ('''
              select edges from setStartAndFinal ( cat ; range  4, 5 ) name "graph" intersect name "other_graph"
              ''', False),
              ("select edges from query a", False),
              ("select count filter edges from grammar", False),
              # wrong patterns
              ("a -> term (a)", False),
              ("a term (a)", False),
              ("s: term (sss) concat", False),
              ('connect "src/wrong/character*"', False)
]


def test_grammar():
    cfg = GrammarUtils.from_file('src/query_language/query_language_grammar.txt')
    grammar = GrammarUtils.to_cnf(cfg)
    for (script, expected) in test_input:
        assert check_script_with_cyk(grammar, script) == expected
