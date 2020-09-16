from pyformlang.finite_automaton import *
from pygraphblas import Matrix


def test_matrix_multiplication():
    a = Matrix.from_lists(
        [0, 0, 1, 1],
        [0, 1, 0, 1],
        [4, 1, 1, 2])

    b = Matrix.from_lists(
        [0, 0, 1, 1],
        [0, 1, 0, 1],
        [7, 1, 3, 1])

    c = Matrix.from_lists(
        [0, 0, 1, 1],
        [0, 1, 0, 1],
        [31, 5, 13, 3])

    result = a @ b
    assert result.iseq(c)


def test_automaton_intersection():
    dfa_1 = DeterministicFiniteAutomaton()
    dfa_2 = DeterministicFiniteAutomaton()

    state0 = State(0)
    state1 = State(1)
    state2 = State(2)
    state3 = State(3)

    symb_a = Symbol("a")
    symb_b = Symbol("b")
    symb_c = Symbol("c")
    symb_d = Symbol("d")

    # Add a start state
    dfa_1.add_start_state(state0)
    dfa_2.add_start_state(state0)

    # Add two final states
    dfa_1.add_final_state(state2)
    dfa_1.add_final_state(state3)
    dfa_2.add_final_state(state2)
    dfa_2.add_final_state(state3)

    # Create transitions
    dfa_1.add_transitions([
        (state0, symb_a, state1),
        (state0, symb_b, state1),
        (state1, symb_a, state0),
        (state1, symb_b, state1),
        (state1, symb_c, state2),
        (state1, symb_d, state3)])
    # Accepts aaac, bbd, abc, etc.
    dfa_2.add_transitions([
        (state0, symb_a, state1),
        (state0, symb_b, state1),
        (state1, symb_b, state1),
        (state1, symb_d, state3)])
    # Doesn't accept aaac, abc

    dfa_intersected = dfa_1 & dfa_2
    assert not dfa_intersected.accepts("aaac")
    assert not dfa_intersected.accepts("abc")
    assert dfa_intersected.accepts("bbd")
    assert dfa_intersected.accepts("ad")
