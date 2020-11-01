from pyformlang.cfg import CFG, Variable, Terminal, Production, Epsilon
from pyformlang.regular_expression import Regex


def get_new_var_num():
    get_new_var_num.calls += 1
    return get_new_var_num.calls


get_new_var_num.calls = 0

EPS_SYM = 'eps'


class GraphWrapper(CFG):
    def __init__(self,
                 variables=None,
                 terminals=None,
                 start_symbol=None,
                 productions=None):
        super(GraphWrapper, self).__init__(
            variables=variables,
            terminals=terminals,
            start_symbol=start_symbol,
            productions=productions
        )

    @staticmethod
    def regex_to_production(regex, head):
        _dict = {}
        production_set = set()

        enfa = regex.to_epsilon_nfa()
        enfa = enfa.minimize()
        transitions = enfa._transition_function._transitions

        for state in enfa.states:
            _dict[state] = Variable(
                '%s#REGEX#%s' % (head.value, get_new_var_num())
            )

        for head_state in transitions:
            for start_state in enfa.start_states:
                start_production = Production(head, [_dict[start_state]])
                production_set.add(start_production)

            for symbol in list(transitions[head_state]):
                body_state = transitions[head_state][symbol]
                inner_head = _dict[head_state]
                inner_body = []

                if symbol.value == EPS_SYM:
                    inner_body.append(Epsilon())
                elif symbol.value.isupper():
                    inner_body.append(Variable(symbol))
                elif symbol.value.islower():
                    inner_body.append(Terminal(symbol))
                else:
                    raise ValueError(f'''Symbol "{symbol}" is not defined as
                                    a terminal or a variable''')

                inner_body.append(_dict[body_state])
                production_set.add(
                    Production(inner_head, inner_body)
                )

                if transitions[head_state][symbol] in enfa.final_states:
                    eps_production = Production(_dict[body_state], [])
                    production_set.add(eps_production)
        return production_set

    @staticmethod
    def from_text(text, start_symbol=Variable("S")):
        lines = text.splitlines()
        production_set = set()

        for line in lines:
            print(line)
            production = line.split(' -> ')
            head = Variable(production[0])
            body_str = production[1].rstrip('\n')

            body_str = body_str.replace('?', f'|{EPS_SYM}')

            production_set |= GraphWrapper.regex_to_production(
                Regex(body_str),
                head
            )

        return CFG(
            start_symbol=start_symbol,
            productions=production_set
        )
