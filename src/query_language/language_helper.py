from src.main.grammar import GrammarUtils

keywords = {
    'connect',
    'select', 'from', 'edges',
    'intersect',
    'grammar', 'query', 'name',
    'setStartAndFinal',
    'range', 'count', 'none',
    'satisfies', 'filter', 'with',
    'or', 'and',
    'labelIs', 'isStart', 'isFinal',
    'alt', 'concat',
    'opt', 'plus', 'star',
    'term', 'nonterm', 'e'
}


def check_script_with_cyk(grammar, text):
    script = []
    for word in text.split():
        if word in keywords:
            script.append(word)
        else:
            script.extend(word)

    return GrammarUtils.cyk(grammar, script)
