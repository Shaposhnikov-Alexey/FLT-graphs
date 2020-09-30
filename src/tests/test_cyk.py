from src.main.grammar import GrammarUtils


def test_cyk_parentheses():
    cfg = GrammarUtils.from_file("src/data/test_cyk_grammar_parentheses.txt")
    grammar = GrammarUtils.to_cnf(cfg)

    assert GrammarUtils.cyk(grammar, 'aabbab')
    assert GrammarUtils.cyk(grammar, 'ab')
    assert GrammarUtils.cyk(grammar, 'abababababab')
    assert not GrammarUtils.cyk(grammar, 'aabba')
    assert not GrammarUtils.cyk(grammar, 'abbab')


def test_cyk_palindrome():
    cfg = GrammarUtils.from_file("src/data/test_cyk_grammar_palindrome.txt")
    grammar = GrammarUtils.to_cnf(cfg)

    assert GrammarUtils.cyk(grammar, 'aabbaa')
    assert GrammarUtils.cyk(grammar, 'aaaa')
    assert not GrammarUtils.cyk(grammar, 'aba')
    assert not GrammarUtils.cyk(grammar, 'a')


def test_cyk_b():
    cfg = GrammarUtils.from_file("src/data/test_cyk_grammar_b.txt")
    grammar = GrammarUtils.to_cnf(cfg)

    # number of 'b's must be even
    assert GrammarUtils.cyk(grammar, 'ababbb')
    assert GrammarUtils.cyk(grammar, 'bbbb')
    assert not GrammarUtils.cyk(grammar, 'ab')
    assert not GrammarUtils.cyk(grammar, 'abbab')
