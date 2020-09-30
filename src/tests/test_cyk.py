from src.main.grammar import CFPQ


def test_cyk_parentheses():
    cfg = CFPQ.from_file("src/data/test_grammar_parentheses.txt")
    grammar = CFPQ.to_cnf(cfg)

    assert CFPQ.cyk(grammar, 'aabbab')
    assert CFPQ.cyk(grammar, 'ab')
    assert CFPQ.cyk(grammar, 'abababababab')
    assert not CFPQ.cyk(grammar, 'aabba')
    assert not CFPQ.cyk(grammar, 'abbab')


def test_cyk_palindrome():
    cfg = CFPQ.from_file("src/data/test_grammar_palindrome.txt")
    grammar = CFPQ.to_cnf(cfg)

    assert CFPQ.cyk(grammar, 'aabbaa')
    assert CFPQ.cyk(grammar, 'aaaa')
    assert not CFPQ.cyk(grammar, 'aba')
    assert not CFPQ.cyk(grammar, 'a')


def test_cyk_b():
    cfg = CFPQ.from_file("src/data/test_grammar_b.txt")
    grammar = CFPQ.to_cnf(cfg)

    # number of 'b's must be even
    assert CFPQ.cyk(grammar, 'ababbb')
    assert CFPQ.cyk(grammar, 'bbbb')
    assert not CFPQ.cyk(grammar, 'ab')
    assert not CFPQ.cyk(grammar, 'abbab')
