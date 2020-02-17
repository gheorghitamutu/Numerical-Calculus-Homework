def problema1():
    power = -1.0
    u = 10.0 ** power  # initially, u = 10 ^ (-1)
    while (1.0 + u) != 1.0:
        power -= 1.0
        u = 10.0 ** power
    else:
        u *= 10.0
    return u


def problema2():
    u = problema1()
    x = 1.0
    y = u
    z = u
    left_add = (x + y) + z
    right_add = x + (y + z)

    message_assoc = \
        'Adunare asociativa: {} ({}, {})'.format(left_add == right_add, left_add, right_add)

    x = 10 ** (-2)  # schimbam precizie x
    left_mul = (x * y) * z
    right_mul = x * (y * z)

    message_mul = \
        'Inmultire asociativa: {} ({}, {})'.format(left_mul == right_mul, left_mul, right_mul)

    return '{}{}\n'.format(message_assoc, message_mul)
