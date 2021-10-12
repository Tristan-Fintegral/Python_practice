print('these are examples on args and kwargs')

c = []

def my_func(a, b, c=None):
    c = c or []
    print(f'a={a}, b={b}, c={c}')
    return c


def my_func(b, a):
    print(f'a={a}, b={b}')
    if a:
        return 'a string'
    if b:
        return 1111


def calculate_var(vector, percentile=None):
    percentile = percentile or 0.99

