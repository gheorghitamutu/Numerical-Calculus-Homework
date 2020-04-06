PROBLEMS_COUNT = 1


def get_function_by_index(index):
    if index == 0:
        return default_input  # function pointer used as button callback/handler
    else:
        raise 'Problem #{} does not exist!'.format(index)


eps = 10 ** (-10)
k_max = 10000


def get_params(fpath):
    with open(fpath) as fh:
        n = int(fh.readline())
        lines = fh.readlines()
    lines = [line.strip().split(',') for line in lines]
    if lines[-1] == ['']:
        lines = lines[:-1]
    return n, lines


def update_lines(lines_i, n, i):
    for _ in range(i + 1, n + 1):
        lines_i[_] += 1
    return lines_i


def update_matrix(lines_i, lines_j, values, n, aij, i, j):
    lines_i = update_lines(lines_i, n, i)
    lines_j.insert(lines_i[i], j)
    values.insert(lines_i[i], aij)
    return lines_i, lines_j, values


def update_value(lines_i, lines_j, values, aij, i, j):
    for _ in range(lines_i[i], lines_i[i + 1]):
        if lines_j[_] == j: values[_] += aij
    return lines_j


def load_matrix_A(fpath):
    n, lines = get_params(fpath)

    lines_i = [0 for _ in range(n + 1)]
    lines_j = list()
    values = list()

    for line in lines:
        aij, i, j = float(line[0]), int(line[1]), int(line[2])
        if not aij: continue
        if j not in lines_j[lines_i[i]:lines_i[i + 1]]:
            lines_i, lines_j, values = update_matrix(lines_i, lines_j, values, n, aij, i, j)
        else:
            lines_j = update_value(lines_i, lines_j, values, aij, i, j)

    return lines_i, lines_j, values, n


def load_matrix_B(fpath):
    n, lines = get_params(fpath)

    lines_i = [0 for _ in range(n + 1)]
    lines_j = list()
    values = list()

    for i, line in enumerate(lines):
        aij = float(line[0])
        j = 0
        if not aij: continue
        lines_i, lines_j, values = update_matrix(lines_i, lines_j, values, n, aij, i, j)

    return lines_i, lines_j, values, n


def null_diag_check(n, lines_i, lines_j, values):
    for _ in range(n):
        indexes = [lines_j[k] for k in range(lines_i[_], lines_i[_ + 1])]
        if _ not in indexes: return True
    return False


def get_line(i, lines_i, lines_j, values):
    line = [(lines_j[_], values[_]) for _ in range(lines_i[i], lines_i[i + 1])]
    line.sort(key=lambda _: _[0])
    if not len(line): return 0, 0
    return line


def compute_sum(line, i, X_c, X_p, first=True):
    res = 0

    if first:
        for elem in line:
            if elem[0] < i:
                res += elem[1] * X_c[elem[0]]
        return res
    else:
        for elem in line:
            if elem[0] > i:
                res += elem[1] * X_p[elem[0]]
        return res


def get_diag_elem(line, i):
    res = 0
    for elem in line:
        if elem[0] == i:
            res += elem[1]
    return res


def get_X_c(X_c, X_p, A_i, A_j, A_v, A_n, B_i, B_j, B_v, B_n):
    for i in range(A_n):
        line = get_line(i, A_i, A_j, A_v)
        b = get_line(i, B_i, B_j, B_v)[0][1]
        first_sum = compute_sum(line, i, X_c, X_p)
        second_sum = compute_sum(line, i, X_c, X_p, first=False)
        aii = get_diag_elem(line, i)
        X_c[i] = (b - first_sum - second_sum) / aii
    return X_c


def get_delta_x(X_c, X_p):
    res = list()
    for i in range(len(X_c)):
        res.append(X_c[i] - X_p[i])
    return max(res)


def gauss_seidel_method(A_i, A_j, A_v, A_n, B_i, B_j, B_v, B_n):
    if null_diag_check(A_n, A_i, A_j, A_v): raise Exception('Matrix has null values on the main diagonal!')
    X_c = [0 for _ in range(A_n + 1)]
    k = 0
    while True:
        X_p = X_c.copy()
        get_X_c(X_c, X_p, A_i, A_j, A_v, A_n, B_i, B_j, B_v, B_n)
        delta_x = get_delta_x(X_c, X_p)
        k += 1
        if delta_x < eps or delta_x > 10 ** 8 or k > k_max:
            break

    n = len(X_c)
    X_i, X_j, X_v, X_n, X_m = [0 for _ in range(n + 1)], list(), list(), n - 1, 1
    for i, line in enumerate(X_c):
        aij = line
        j = 0
        if not aij: continue
        X_i, X_j, X_v = update_matrix(X_i, X_j, X_v, n, aij, i, j)

    return X_i, X_j, X_v, X_n, X_m


def compute_mul_value(A_i, A_j, A_v, i, j):
    v = 0
    for k in range(A_i[i], A_i[i + 1]):
        for l in range(X_i[A_j[k]], X_i[A_j[k] + 1]):
            if X_j[l] == j:
                v += A_v[k] * X_v[l]
    return v


def compute_multiplication(A_i, A_j, A_v, A_n, X_i, X_j, X_v, X_n, X_m):
    if A_n != X_n: raise Exception('Invalid shape of matrices to compute mul!')
    Y_n, Y_m = A_n, X_m
    Y_i, Y_j, Y_v = [0 for _ in range(X_n + 1)], list(), list()
    for i in range(A_n):
        for j in range(X_m):
            v = compute_mul_value(A_i, A_j, A_v, i, j)
            if not v: continue
            if j not in Y_j[Y_i[i]:Y_i[i + 1]]:
                Y_i, Y_j, Y_v = update_matrix(Y_i, Y_j, Y_v, Y_n, v, i, j)
            else:
                Y_j = update_value(Y_i, Y_j, Y_v, v, i, j)

    return Y_i, Y_j, Y_v, Y_n, Y_m


def compute_substitution(Y_i, Y_j, Y_v, Y_n, Y_m, B_i, B_j, B_v, B_n, B_m):
    if Y_n != B_n or Y_m != B_m:  raise Exception('Invalid shape of matrices to compute sub!')
    Z_n, Z_m = Y_n, Y_m
    Z_i, Z_j, Z_v = [0 for _ in range(Z_n + 1)], list(), list()
    for k in range(Y_n):
        first = [_ for _ in range(Y_i[k], Y_i[k + 1])]
        second = [_ for _ in range(B_i[k], B_i[k + 1])]

        for v in first:
            if Y_j[v] not in Z_j[Z_i[k]:Z_i[k + 1]]:
                Z_i, Z_j, Z_v = update_matrix(Z_i, Z_j, Z_v, Z_n, Y_v[v], k, Y_j[v])
            else:
                Z_j = update_value(Z_i, Z_j, Z_v, Y_v[v], k, Y_j[v])

        for v in second:
            if B_j[v] not in Z_j[Z_i[k]:Z_i[k + 1]]:
                Z_i, Z_j, Z_v = update_matrix(Z_i, Z_j, Z_v, Z_n, -B_v[v], k, B_j[v])
            else:
                Z_j = update_value(Z_i, Z_j, Z_v, -B_v[v], k, B_j[v])

    return Z_i, Z_j, Z_v, Z_n, Z_m


def get_norm(Z_i, Z_j, Z_v, Z_n):
    res = list()
    for i in range(Z_n):
        s = 0
        for j in range(Z_i[i], Z_i[i + 1]):
            s += Z_v[j]
        s = abs(s)
        res.append(s)
    return max(res)


def default_input(out_cb):
    out_cb('\n------------------------------------ Homework 04 -------------------------------------------------------'
           '\n------------------------------------ Problem  01 -------------------------------------------------------'
           '\n--------------------------------------------------------------------------------------------------------'
           '\nPlease wait - it may take up to 3 minutes...------------------------------------------------------------')

    # in order to avoid rewriting some functions just declare these as global
    global A_i
    global A_j
    global A_v
    global A_n
    global B_i
    global B_j
    global B_v
    global B_n

    global X_i
    global X_j
    global X_v
    global X_n
    global X_m

    global Y_i
    global Y_j
    global Y_v
    global Y_n
    global Y_m

    global Z_i
    global Z_j
    global Z_v
    global Z_n
    global Z_m

    A_i, A_j, A_v, A_n = load_matrix_A(r'homework04_data\a_4.txt')
    B_i, B_j, B_v, B_n = load_matrix_B(r'homework04_data\b_4.txt')

    X_i, X_j, X_v, X_n, X_m = gauss_seidel_method(A_i, A_j, A_v, A_n, B_i, B_j, B_v, B_n)
    Y_i, Y_j, Y_v, Y_n, Y_m = compute_multiplication(A_i, A_j, A_v, A_n, X_i, X_j, X_v, X_n, X_m)
    # print(Y_v)
    Z_i, Z_j, Z_v, Z_n, Z_m = compute_substitution(Y_i, Y_j, Y_v, Y_n, Y_m, B_i, B_j, B_v, B_n, 1)
    # print(Z_v)
    norm = get_norm(Z_i, Z_j, Z_v, Z_n)

    out_cb("Norm: {}\n\n".format(norm))  # norma
    out_cb("X: {}\n\n".format(X_v))  # solutia


if __name__ == '__main__':
    default_input(print)
