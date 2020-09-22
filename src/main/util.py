from pygraphblas import *


def transitive_closure(matrix) -> Matrix:
    result = matrix.dup()
    continue_mul = True

    while continue_mul:
        continue_mul = False

        old_number = result.nvals
        result += result @ result
        new_number = result.nvals

        if new_number != old_number:
            continue_mul = True

    return result
