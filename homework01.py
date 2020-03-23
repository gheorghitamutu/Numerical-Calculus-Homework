import math

import numpy

PROBLEMS_COUNT = 3


def get_function_by_index(index):
    if index == 0:
        return problema1
    elif index == 1:
        return problema2
    elif index == 2:
        return problema3_default_input
    else:
        raise 'Problem #{} does not exist!'.format(index)


def problema1():
    power = -1.0
    u = 10.0 ** power  # initially, u = 10 ^ (-1)
    while (1.0 + u) != 1.0:
        power -= 1.0
        u = 10.0 ** power
    else:
        pass
        u = u * 10.0
    return u


def problema2():
    u = problema1()
    x = 1.0
    y, z = u, u

    left_add = (x + y) + z
    right_add = x + (y + z)

    message_assoc = \
        'Adunare asociativa: {} ({}, {})'.format(left_add == right_add, left_add, right_add)

    x = 10 ** (-2)  # schimbam precizie x
    left_mul = (x * y) * z
    right_mul = x * (y * z)

    message_mul = \
        'Inmultire asociativa: {} ({}, {})'.format(left_mul == right_mul, left_mul, right_mul)

    return '{} | {}'.format(message_assoc, message_mul)


def zero_array(shape, dtype=bool):
    return numpy.zeros(shape, dtype=dtype)


def get_new_line(lines, matrix_Bi, i, result):
    new_line = zero_array(result[i].shape)
    for j in lines:
        new_line = numpy.add(new_line, matrix_Bi[j])
    return new_line


def compute_Ci(matrix_Ai, matrix_Bi):
    _shape = numpy.matmul(matrix_Ai, matrix_Bi).shape
    result = zero_array(_shape)

    for i in range(_shape[0]):
        # lista cu indicii elem != 0 din linia i
        result[i] = get_new_line(numpy.argwhere(matrix_Ai[i]).flatten(), matrix_Bi, i, result)

    return result


def adjust(submatrices, n, line, column):
    _axis = 0 if line else 1

    # add new line/column of zeros
    last_submatrix = submatrices[-1].copy()
    while last_submatrix.shape != submatrices[0].shape:
        if line:
            last_submatrix = numpy.append(submatrices[-1], zero_array((1, n)), axis=_axis)
        elif column:
            last_submatrix = numpy.append(submatrices[-1], zero_array((n, 1), dtype=bool), axis=_axis)
    submatrices[-1] = last_submatrix

    return submatrices


def get_main_submatrices(matrix, line=False, column=False):
    _axis = 0 if line else 1

    n = matrix.shape[0]
    m = math.floor(math.log2(n))
    p = n // m

    splits_indexes = range(p, n, p)

    submatrices = numpy.array_split(matrix, splits_indexes, axis=_axis)
    # print(submatrices)

    if submatrices[-1].shape == submatrices[0].shape:
        return submatrices

    submatrices = adjust(submatrices, n, line, column)

    return submatrices


def get_C_matrix(matrix_A, matrix_B):
    matrix_Ci = list()
    for i in range(len(matrix_A)):
        matrix_Ci.append(compute_Ci(matrix_A[i], matrix_B[i]))

    # sum up all Ci
    matrix_C = matrix_Ci[0]
    for i in range(1, len(matrix_Ci)):
        matrix_C = numpy.add(matrix_C, matrix_Ci[i])
    return matrix_C


def get_all_submatrices(matrix_A, matrix_B):
    # to numpy array
    matrix_A = numpy.array(matrix_A)
    matrix_B = numpy.array(matrix_B)
    matrix_A, matrix_B = get_main_submatrices(matrix_A, column=True), get_main_submatrices(matrix_B, line=True)

    matrix_C = numpy.vectorize(lambda x: int(x))(get_C_matrix(matrix_A, matrix_B))

    return matrix_A, matrix_B, matrix_C


def problema3(matrix_A, matrix_B):
    matrix_A, matrix_B, matrix_C = get_all_submatrices(matrix_A, matrix_B)
    return matrix_C


def problema3_default_input():
    matrix_A = [
        [0, 1, 0, 1, 0, 1],
        [0, 1, 1, 0, 1, 1],
        [1, 0, 0, 1, 0, 0],
        [1, 0, 0, 0, 1, 0],
        [0, 0, 0, 1, 1, 0],
        [0, 0, 0, 1, 0, 0]
    ]

    matrix_B = [
        [0, 1, 1, 0, 1, 9],
        [0, 0, 0, 1, 1, 1],
        [1, 0, 1, 0, 0, 0],
        [0, 1, 0, 1, 1, 1],
        [1, 1, 1, 1, 0, 1],
        [0, 0, 0, 0, 0, 0]
    ]

    # print(problema3([[0, 1, 0, 1, 0], [0, 1, 1, 0, 1], [1, 0, 0, 1, 0], [1, 0, 0, 0, 1], [0, 0, 0, 1, 1]],
    #                 [[0, 1, 1, 0, 1], [0, 0, 0, 1, 1], [1, 0, 1, 0, 0], [0, 1, 0, 1, 1], [1, 1, 1, 1, 0]]))
    # print(problema3([[0, 1, 0, 1], [0, 1, 1, 0], [1, 0, 0, 1], [1, 0, 0, 0]],
    #                 [[0, 1, 1, 0], [0, 0, 0, 1], [1, 0, 1, 0], [0, 1, 0, 1]]))

    matrix_resulted = problema3(matrix_A, matrix_B)

    message = '\nMatrix A\n{}\nMatrix B\n{}\nMatrix Resulted\n{}'.format(
        numpy.vectorize(lambda x: int(x))(matrix_A),
        numpy.vectorize(lambda x: int(x))(matrix_B),
        matrix_resulted)

    return message
