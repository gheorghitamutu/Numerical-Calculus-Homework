eps = 1e-2
PROBLEMS_COUNT = 1


def get_function_by_index(index):
    if index == 0:
        return default_input  # function pointer used as button callback/handler
    else:
        raise 'Problem #{} does not exist!'.format(index)


def load_matrix(fpath):
    with open(fpath) as fh:
        n = fh.readline()
        lines = fh.readlines()
    lines = [line.strip().split(',') for line in lines]
    if lines[-1] == ['']:
        lines = lines[:-1]
    matrix = dict()
    for l_index, line in enumerate(lines):
        val = float(line[0])
        i = int(line[1])
        j = int(line[2])
        if not matrix.get(i):
            matrix[i] = list()
        aux_line = {elem[1]: elem[0] for elem in matrix[i]}
        if aux_line.get(j):
            index = matrix[i].index([aux_line[j], j])
            matrix[i][index] = [aux_line[j] + val, j]
        else:
            matrix[i].append([val, j])
    matrix = {'i={}'.format(l_index): sorted(matrix[l_index], key=lambda x: x[1]) for l_index in matrix.keys()}
    # for l_index, line in matrix.items():
    #     print(l_index, line)
    #     if len(line) > 10:
    #         print('More than 10 not null values in line {} of matrix {}'.format(l_index, os.path.basename(fpath)))
    return matrix, int(n)


def compute_sum(A, A_n, B, B_n):
    if A_n != B_n:
        raise Exception("Invalid shape of matrices to compute sum!")
    n = A_n
    matrix_sum = dict()
    for i in range(n):
        i = 'i={}'.format(i)
        if A.get(i) and B.get(i):
            aplusb_line = list()
            A_line = {elem[1]: elem[0] for elem in A[i]}
            B_line = {elem[1]: elem[0] for elem in B[i]}
            for j in range(n):
                if A_line.get(j) and B_line.get(j):
                    aplusb_line.append([A_line[j] + B_line[j], j])
                elif A_line.get(j):
                    aplusb_line.append([A_line[j], j])
                elif B_line.get(j):
                    aplusb_line.append([B_line[j], j])
            if aplusb_line:
                matrix_sum[i] = aplusb_line
        elif A.get(i):
            matrix_sum[i] = A[i]
        elif B.get(i):
            matrix_sum[i] = B[i]
    matrix_sum = {l_index: sorted(matrix_sum[l_index], key=lambda x: x[1]) for l_index in
                  matrix_sum.keys()}
    # for l_index, line in matrix_sum.items():
    #     print(l_index, line)
    return matrix_sum


def get_transpose(matrix):
    matrix = {int(key.split('i=')[1]): matrix[key] for key in matrix.keys()}
    matrix_transpose = dict()
    for key in matrix.keys():
        line_key = key
        for (value, column_key) in matrix[key]:
            if not matrix_transpose.get(column_key):
                matrix_transpose[column_key] = list()
            matrix_transpose[column_key].append([value, line_key])
    matrix_transpose = {'j={}'.format(c_index): sorted(matrix_transpose[c_index], key=lambda x: x[1]) for c_index in
                        matrix_transpose.keys()}
    matrix_transpose = [matrix_transpose[key] for key in matrix_transpose.keys()]
    return matrix_transpose


def compute_multiplication(A, A_n, B, B_n):
    if A_n != B_n:
        raise Exception("Invalid shape of matrices to compute mul!")
    n = A_n
    matrix_mul = list()
    A = [A[key] for key in A.keys()]
    B = get_transpose(B)

    for a in A:
        t_line = list()
        for b in B:
            poz = B.index(b)
            line_A = {t[1]: i for i, t in enumerate(a)}
            line_B = {t[1]: i for i, t in enumerate(b)}
            B_keys = list(line_B)
            index = [_ for _ in line_A if _ in line_B]
            if not index: continue
            res = sum([a[line_A[i]][0] * b[line_B[i]][0] for i in index])
            t_line.append([res, poz])
        matrix_mul.append(t_line)
    matrix_mul = {'i={}'.format(l_index): sorted(line, key=lambda x: x[1]) for l_index, line in enumerate(matrix_mul)}
    return matrix_mul


def check_sum(A1, A2):
    if A1.keys() != A2.keys():
        return False
    for key in A1.keys():
        A1_line = {elem[1]: elem[0] for elem in A1[key]}
        A2_line = {elem[1]: elem[0] for elem in A2[key]}
        if A1.keys() != A2.keys():
            return False
        for _key in A1_line.keys():
            if not A2_line.get(_key):
                return False
            if A1_line[_key] - A2_line[_key] > eps:
                return False
    return True


def check_mul(A1, A2):
    if A1.keys() != A2.keys():
        return False
    A1_values = [sorted([elem[0] for elem in A1[key]]) for key in A1]
    A2_values = [sorted([elem[0] for elem in A2[key]]) for key in A2]
    for index, (A1_line, A2_line) in enumerate(zip(A1_values, A2_values)):
        if A1_line not in A2_values or A2_line not in A1_values:
            return False
    return True


def default_input(out_cb):
    """
    Default input for Homework 03 problem.
    :param out_cb: function pointer passed to process/show the output
    :return:
    """
    out_cb('\n------------------------------------ Homework 03 -------------------------------------------------------'
           '\n------------------------------------ Problem  01 -------------------------------------------------------'
           '\n--------------------------------------------------------------------------------------------------------')

    # memorarea matricelor rare
    out_cb('Loading data...')
    A, A_n = load_matrix(r'homework03_data\a.txt')
    B, B_n = load_matrix(r'homework03_data\b.txt')
    AplusB, AplusB_n = load_matrix(r'homework03_data\aplusb.txt')
    AoriB, AoriB_n = load_matrix(r'homework03_data\aorib.txt')

    # calculul sumei
    out_cb('Computing the sum...')
    AplubB_computed = compute_sum(A, A_n, B, B_n)
    out_cb('Computing the product. This will take a while...')
    AoriB_computed = compute_multiplication(A, A_n, B, B_n)

    # verificare suma, produs
    out_cb('Checking results...')
    out_cb("AplusB == AplusB_computed ({})".format(check_sum(AplusB, AplubB_computed)))
    out_cb("AoriB == AoriB_computed ({})".format(check_mul(AoriB, AoriB_computed)))


if __name__ == '__main__':
    default_input(print)  # use print for stdout
