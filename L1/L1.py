def russian(a, b):
    x = a; y = b
    z = 0
    while x > 0:
        if x % 2 == 1: z = z + y
        y = y << 1
        x = x >> 1
    return z


def countdown(x):
    y = 0
    while x > 0:
        x = x - 5
        y = y + 1
    print y
    return y


def time(n):
    """ Return the number of steps necessary to calculate `print countdown(n)`"""

    steps = 3 + 2 * (n / 5 + (n % 5 != 0))
    return steps


def rec_russian(a, b):
    if a == 0: return 0
    if a % 2 == 0: return rec_russian(a/2, b) * 2
    return rec_russian((a-1)/2, b) * 2