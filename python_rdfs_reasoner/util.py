def diff(first, second):
    x = [tuple(y) for y in first]
    z = [tuple(y) for y in second]
    return set(x) - set(z)
