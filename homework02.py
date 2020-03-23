import math

import numpy as np

PROBLEMS_COUNT = 1


def get_function_by_index(index):
    if index == 0:
        return default_input  # function pointer used as button callback/handler
    else:
        raise 'Problem #{} does not exist!'.format(index)


def get_determinant(X):
    return np.linalg.det(X)


def get_LU_decomposition(A, b, eps):
    """
    compute LU decomposition
    Doolitle Algorithm presented here(https://www.geeksforgeeks.org/doolittle-algorithm-lu-decomposition/)
    """

    if not get_determinant(A):
        return None, None, 'ZeroDeterminant'  # LU not possible

    # initialize L, U
    n = len(A)
    L = [[1 if i == j else 0 for i in range(n)] for j in range(n)]  # diagonal is 1
    U = [[0 for _ in range(n)] for _ in range(n)]

    def compose_sum_U():
        sum_U = 0
        for j in range(i):
            sum_U += round(L[i][j] * U[j][k], 2)
        return sum_U

    def compose_sum_L():
        sum_L = 0
        for j in range(i):
            sum_L += round(L[k][j] * U[j][i], 2)
        return sum_L

    # decompose matrix, get L, U
    for i in range(n):
        # U
        for k in range(i, n):
            # L(i, j) * U(j, k)
            sum_U = compose_sum_U()

            # evaluating U(i, k)
            U[i][k] = A[i][k] - sum_U

        # L
        for k in range(i, n):
            # L(k, j) * U(j, i)
            sum_L = compose_sum_L()

            # evaluating L(k, i)
            if math.fabs(U[i][i]) > eps:
                L[k][i] = (A[k][i] - sum_L) / U[i][i]
            else:
                return None, None, 'ZeroDivisionError'

    return L, U, None


def get_LU_decomposition2(A, b, eps):
    # LU decomposition in same matrix
    if not get_determinant(A):
        return None, None, 'ZeroDeterminant'  # LU not possible

    def compose_sum_U():
        sum_U = 0
        for j in range(i):
            sum_U += round(A[i][j] * A[j][k], 2)
        return sum_U

    def compose_sum_L():
        sum_L = 0
        for j in range(i):
            sum_L += round(A[k][j] * A[j][i], 2)
        return sum_L

    n = len(A)
    for i in range(n):
        for k in range(i, n):
            sum_U = compose_sum_U()

            A[i][k] = A[i][k] - sum_U

            if i == k:
                continue

            sum_L = compose_sum_L()

            if math.fabs(A[i][i]) > eps:
                A[k][i] = (A[k][i] - sum_L) / A[i][i]
            else:
                return None, 'ZeroDivisionError'
    return A, None


def get_determinants(A, L, U):
    detA = round(get_determinant(A), 2)
    detL = round(get_determinant(L), 2)
    detU = round(get_determinant(U), 2)
    # det A = detL * detU
    detLU = round(detL * detU, 2)

    return detA, detL, detU, detA == detLU or round(detA) == round(detLU)


def forward_substitution(L, b, eps):
    n = len(b)
    y = list()
    for i in range(n):
        y.append(b[i])
        for j in range(i):
            y[i] = y[i] - (L[i][j] * y[j])
        if math.fabs(L[i][i]) > eps:
            y[i] = y[i] / L[i][i]
        else:
            return None, 'ZeroDivisionError'

    return y, None


def backward_substitution(U, y, eps):
    def compute_sum():
        sum = 0
        for j in range(i + 1, n):
            sum += U[i][j] * x[j]
        return sum

    n = len(y)
    x = [0 for i in range(n)]
    for i in reversed(range(n)):
        sum = compute_sum()

        if math.fabs(U[i][i]) > eps:
            x[i] = (y[i] - sum) / U[i][i]
        else:
            return None, 'ZeroDivisionError'

    return x, None


def solve_system(A, b, eps):
    L, U, err = get_LU_decomposition(A, b, eps)
    if err: return

    y, err = forward_substitution(L, b, eps)  # Ly = b
    if err: raise err

    x, err = backward_substitution(U, y, eps)  # Ux = y
    if err: raise err

    x = [round(_, 2) for _ in x]
    return x


def compute_euclidian_norm_expression_1(A, b, eps):
    # ||A_init * x_LU - b_init||_2
    x = solve_system(A, b, eps)
    # first part of equation
    A = np.array(A)
    x = np.array([_ for _ in x]).reshape(len(x), 1)
    first = np.dot(A, x).tolist()
    first = [_[0] for _ in first]

    res = list()
    for index, (i, j) in enumerate(zip(first, b)):
        res.append(i - j)

    return np.linalg.norm(res, 2)


def get_inv_matrix(A):
    return np.linalg.inv(A)


def compute_euclidian_norm_expression_2(A, b, eps):
    # ||x_LU - x_lib||_2
    sol = solve_system(A, b, eps)
    sol_lib = np.linalg.solve(A, b)
    # print('sol_lib', sol_lib)

    res = list()
    for index, (i, j) in enumerate(zip(sol, sol_lib)):
        res.append(i - j)

    return np.linalg.norm(res, 2)


def compute_euclidian_norm_expression_3(A, b, eps):
    # ||x_LU - (A_lib)^(-1) * b_init||_2
    x = solve_system(A, b, eps)
    A_inv = np.linalg.inv(A)

    A_inv = np.array(A_inv)
    b = np.array([_ for _ in b]).reshape(len(b), 1)
    first = np.dot(A_inv, b).tolist()
    first = [_[0] for _ in first]

    res = list()
    for index, (i, j) in enumerate(zip(x, first)):
        res.append(i - j)

    return np.linalg.norm(res, 2)


def get_LU_inv_matrix(A, b, eps):
    L, U, err = get_LU_decomposition(A, b, eps)
    n = len(A)
    A_rev = list()
    for i in range(n):
        e = [0 for i in range(n)]
        e[i] = 1
        A_rev.append(solve_system(A, e, eps))
    return list(zip(*A_rev))


def compute_expression_4(A, b, eps):
    # || (A_LU)^-1 - (A_lib)^-1 ||_1
    A_rev = get_LU_inv_matrix(A, b, eps)
    # print(A_rev)
    A_rev_lib = get_inv_matrix(A)
    # print(A_rev_lib)

    res = list()
    for index, (i, j) in enumerate(zip(A_rev, A_rev_lib)):
        res.append(i - j)

    return np.linalg.norm(res, 1)


def default_input(out_cb):
    """
    Default input for Homework 02 problem.
    :param out_cb: function pointer passed to process/show the output
    :return:
    """

    out_cb('\n------------------------------------ Homework 02 -------------------------------------------------------'
           '\n------------------------------------ Problem  01 -------------------------------------------------------'
           '\n--------------------------------------------------------------------------------------------------------')
    out_cb('1) LU decomposition')
    A = [[1, 1, -1], [1, -2, 3], [2, 3, 1]]
    # A = [[3, 3, 3], [2, 2, 2], [1, 1, 1]]
    b = [4, -6, 7]
    eps = 0
    L, U, err = get_LU_decomposition(A, b, eps)
    if err:
        out_cb('Failed with error: {}'.format(err))
        exit(1)
    else:
        out_cb('L')
        [out_cb(row) for row in L]
        out_cb('U')
        [out_cb(row) for row in U]

    out_cb('\n--------------------------------------------------------------------------------------------------------')
    out_cb('2) detA = detL * detU')
    dets = get_determinants(A, L, U)
    out_cb('detA = {} | detL = {} | detU = {} | detL * detU = detA ({})'.format(dets[0], dets[1], dets[2], dets[3]))

    out_cb('\n--------------------------------------------------------------------------------------------------------')
    out_cb('3) solution x for which Ax=b')
    out_cb(solve_system(A, b, eps))

    out_cb('\n--------------------------------------------------------------------------------------------------------')
    out_cb('4) Checking solution:||A_init * x_LU - b_init||_2')
    out_cb(compute_euclidian_norm_expression_1(A, b, eps))

    out_cb('\n--------------------------------------------------------------------------------------------------------')
    out_cb('5) Same matrix LU decomposition')
    A_, err = get_LU_decomposition2(A, b, eps)
    if err:
        out_cb('Failed with error: {}'.format(err))
        exit(1)
    else:
        out_cb('L & U in same matrix')
        [out_cb(row) for row in A_]

    out_cb('\n--------------------------------------------------------------------------------------------------------')
    out_cb('6)')
    out_cb('Inversed Matrix A')
    out_cb(get_inv_matrix(A))
    A = [[1, 1, -1], [1, -2, 3], [2, 3, 1]]
    # A = [[3, 3, 3], [2, 2, 2], [1, 1, 1]]
    b = [4, -6, 7]
    out_cb('||x_LU - x_lib||_2 -> {}'.format(compute_euclidian_norm_expression_2(A, b, eps)))

    out_cb('||x_LU - (A_lib)^(-1) * b_init||_2 -> {}'.format(compute_euclidian_norm_expression_3(A, b, eps)))

    out_cb('\n--------------------------------------------------------------------------------------------------------')
    out_cb('7)|| (A_LU)^-1 - (A_lib)^-1 ||_1 -> {}'.format(compute_expression_4(A, b, eps)))


if __name__ == '__main__':
    default_input(print)  # use print for stdout
