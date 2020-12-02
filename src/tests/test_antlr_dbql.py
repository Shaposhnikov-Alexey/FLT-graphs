from antlr4 import InputStream
from src.antlr.antlr_helper import TreeHelper

test_input = [
    ('''
        def S1: term(a)*.term(b);
         def S2: term(c)?.term(d)*.(nonterm(S1)|term(a))*;
         def S3: (nonterm(S1) | nonterm (S2)) concat (term(final));
              ''', True),
    ('''
        connect "/src/data/graph1.txt";
        select count edges from name "graph1";
        select filter edges with (1, edge, 2) satisfies (1 labelIs first) 
            and (2 labelIs second) and not (isStart 2 or isFinal 1) 
                from name "graph1";
                  ''', True),
    ('''
              connect "/src/data.txt";
              
              
              ''', True),
    ('''
              def a: term (a) star concat term (b);
              def c: nonterm (b) star;
              def f: nonterm (b) alt nonterm (c) star concat term (s);
              select count edges from grammar;
              ''', True),
    ('''
              select count edges from grammar;
              ''', True),
    ('''
              select count edges from setStartAndFinal ( range  4 , 5 ; none ) name "graph";
              ''', True),
    ('''
              select edges from setStartAndFinal ( set(1, 2, 3) ; range  4, 5 ) name "graph";
              ''', True),
    ('''
              select filter edges with (1, edge, 2) satisfies (1 labelIs first) from name "graph";
              ''', True),
    ('''
              select filter edges with (1, edge, 2) satisfies isStart 1 and isFinal 2 from name "graph";
              ''', True),
    ('''
              select filter edges with (1, edge, 2) satisfies (1 labelIs first) and not (2 labelIs first) from name "graph";
              ''', True),
    ('''
              select edges from query nonterm (a) concat nonterm (b) alt term (s) opt alt nonterm (n) star;
              ''', True),
    ('''
              select edges from query nonterm (a) concat nonterm (b) plus;
              ''', True),
    ('''
              connect "src/data";
              select count edges from setStartAndFinal (set(1, 2, 3) ; set(4, 5, 6)) 
                (query term (a) star concat term (b) plus);
               ''', True),
    ('''
              connect "src/data";
              def s: nonterm (b) star concat term (f) opt;
              def f: nonterm (a) alt nonterm (b) concat term (q);
              def q: nonterm (c) star;
              select filter edges with (24, edge, 26) satisfies (24 labelIs first) and not (26 labelIs first or isFinal 26) from name "graph";
              ''', True),
    # Rest are wrong cases
    ('''
              select count edges from name "graph"
              ''', False),
    ('''
              select count edges from setStartAndFinal  (range  4 , 5) name "graph" intersect name "other_graph";
              ''', False),
    ('''
              select count edges from graph;
              ''', False),
    ('''
              select count edges from "graph" intersect grammar;
              ''', False),
    ('''
              select count edges from setStartAndFinal  range  4 , 5 ; none name "graph" intersect name "other_graph";
              ''', False),
    ('''
              select edges from setStartAndFinal ( 1, 2, 3  range  4, 5 ) name "graph" intersect name "other_graph";
              ''', False),
    ('''
              select filter edges with (1 edge  2) satisfies 1 labelIs first from name "graph";
              ''', False),
    ('''
              select filter edges with (1, edge, 2) satisfies isStart 1  isFinal 2 from name "graph";
              ''', False),
    ('''
              select filter edges with 1, edge, 2 satisfies 1 labelIs first and not 2 labelIs first from (name "graph");
              ''', False),
    # missing ':'
    ('''
              connect "src/data";
              def s: nonterm (b) star concat term (f) opt;
              def f: nonterm (a) alt nonterm (b) concat term (q);
              def q: nonterm (c) star
              select filter edges with (24, edge, 26) satisfies (24 labelIs first) and not (26 labelIs first or isFinal 26) from name "graph";
              ''', False),
    ('''
              connect "src/data"
              select count edges from setStartAndFinal (set(1, 2, 3) ; set(4, 5, 6)) 
                (query term (a) star concat term (b) plus);
               ''', False),
    ('''
              connect "src/data";
              select count edges from setStartAndFinal (set(1, 2, 3) ; set(4, 5, 6)); 
                (query term (a) star concat term (b) plus);
               ''', False),
    # there must be concat in regexp
    ('''
              select edges from name query nonterm (a) nonterm (b) plus;
              ''', False),
    ('''
              select edges from name query nonterm(a)*nonterm(b)+;
              ''', False),
    # name should be in ""
    ('''
              connect src/data;
              select count edges from setStartAndFinal (1, 2, 3 ; 4, 5, 6) name "graph" intersect query term (a) star concat term (b) plus;
               ''', False),
    # there must be defined what to select
    ('select from name "graph";', False),
    ('select cont from name "graph";', False),
    ('select edgs from name "graph";', False),
    ('select edges from name intersect ;', False),
    ('select from name "graph"', False),
    # wrong types
    ('''
              select count edges from setStartAndFinal ( range  ab , 5 ; none ) name "graph" intersect name "other_graph";
              ''', False),
    ('''
              select edges from setStartAndFinal ( cat ; range  4, 5 ) name "graph" intersect name "other_graph";
              ''', False),
    ("select edges from query a;", False),
    ("select count filter edges from grammar;", False),
    # wrong patterns
    ("def a -> term (a);", False),
    ("a term (a);", False),
    ("def s: term (sss) concat;", False),
    ('connect "src/wrong/character*";', False)
]


def test_antlr():
    for index, (script, expected) in enumerate(test_input):
        tree_helper = TreeHelper(InputStream(script))
        is_parsed = tree_helper.tree is not None
        assert is_parsed == expected
        print('Yes!\n')
