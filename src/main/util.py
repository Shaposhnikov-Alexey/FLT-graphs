from pygraphblas import *


def transitive_closure(matrix) -> Matrix:
    result = matrix.dup()
    continue_mul = True

    while continue_mul:
        old_number = result.nvals
        with semiring.LOR_LAND_BOOL:
            result += result @ matrix
        new_number = result.nvals

        if new_number == old_number:
            break

    return result

# def transitive_closure(matrix) -> Matrix:
#     result = matrix.dup()
#     continue_mul = True
#
#     while continue_mul:
#         old_number = result.nvals
#         with semiring.LOR_LAND_BOOL:
#             result += result @ result
#         new_number = result.nvals
#
#         if new_number == old_number:
#             break
#
#     return result
