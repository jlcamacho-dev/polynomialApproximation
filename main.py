######################################################################
# Name: Jose L. Camacho
# Class: CS 3010
# Professor = Edwin Rodríguez
# Assignment 3
######################################################################
import sys


# ---------- file processing functions --------------- #
def preprocess(buff: list) -> list:
    nbuff = list()
    for i in range(len(buff)):
        if buff[i] != '':
            nbuff.append(buff[i])
    return nbuff


def clean(buff: list) -> list:
    nbuff = list()
    for i in range(len(buff)):
        if buff[i] != '':
            nbuff.append(buff[i])
    return nbuff


def strtofloat(buff: list) -> list:
    for i in range(len(buff)):
        buff[i] = float(buff[i])
    return buff


def filepro(filename: str):
    poly = []  # list containing coefficinets for polynomials, index of each element will act as its appropiate power
    q = 0  # variable for file processing control
    numpow = int()

    # begin file proessing
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip('\n')
                line = line.split(' ')
                line = preprocess(line)
                line = clean(line)
                if q == 0:
                    numpow = int(line[0])
                    q += 1
                elif q == 1:
                    poly = strtofloat(line)
                    poly.reverse()
                    q += 1
    except IOError:
        print('I/O error encountered')

    return poly, numpow


# ---------- file processing functions --------------- #
# evaluate polynomial at desired value
def f(poly: list, x: float) -> float:
    total = 0
    for i in range(len(poly)):
        total += poly[i] * (x ** i)
    return total


def derF(x: float, poly: list) -> float:
    # variable to keep running total
    sum = 0.0

    # calculate derivative
    for i in range(0, len(poly)):
        poly[i] = i * poly[i]

    # pop head
    if poly[0] == 0:
        poly.pop(0)

    # evaluae function at given value
    for i in range(0, len(poly)):
        sum += poly[i] * (x ** i)

    return sum


def bisection(a: float, b: float, poly: list, maxIter: int, eps=0.00000001):
    fa = f(poly, a)
    fb = f(poly, b)
    c = float()  # initialize value for c to keep IDE from squaking at me
    if fa * fb > 0:
        print('Inadequate values for a & b')
        return f'Inadequate values for a & b result = {-1}'

    error = b - a

    for it in range(0, maxIter):
        error = error / 2
        c = a + error
        fc = f(poly, c)

        if abs(error) < eps or fc == 0:
            print(f'Algorithm has converged after {it} iterations')
            return f'Algorithm has converged after {it} iterations result is {c}'

        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc
    print(f'Maxed iterations reached without conergence')
    return f'Maxed iterations reached without conergence result = {c}'


def newton(x: float, maxIter: int, poly: list, eps=0.00000001, delta=0.00000000000001):
    fx = f(poly, x)

    for it in range(0, maxIter):
        fd = derF(x, poly)
        if abs(fd) < delta:
            print('small slope')
            return f'small slope result = {x}'
        d = fx / fd
        x -= d
        fx = f(poly, x)

        if abs(d) < eps:
            print(f'Algorithm has converged after #{it} iteratiosn!')
            return f'Algorithm has converged after #{it} iteratiosn! result = {x}'

    print('Max iterations reached without convergance...')
    return f'Max iterations reached without convergance... result: {x}'


def secant(a: float, b: float, poly: list, maxIter=10000, eps=0.00000001):
    fa = f(poly, a)
    fb = f(poly, b)

    if abs(fa) > abs(fb):
        a, b = b, a  # swap
        fa, fb = fb, fa  # swap

    for it in range(0, maxIter):
        if abs(fa) > abs(fb):
            a, b = b, a
            fa, fb = fb, fa

        d = (b - a) / (fb - fa)
        b = a
        fb = fa
        d = d * fa

        if abs(d) < eps:
            print(f'Algorithm has converged after #{it} iterations!')
            result = f'Algorithm has converged after #{it} iterations!'
            return f'{result} result: {a}'

        a = a - d
        fa = f(poly, a)
    print('Maximum number of iteratiosn reached!')
    result = 'Maximum number of iteratiosn reached!'
    return f'{result} result: {a}'


def hybrid(poly: list, a: float, b: float, maxIter: int, eps=0.00000001, delta=0.00000000000001):
    x = bisection(a, b, poly, maxIter - 10)
    return newton(x, maxIter, poly)


def main() -> None:
    arglist = sys.argv
    newt = sec = 0  # initialize values
    maxIter = 10000  # default value
    filename = ''
    bounds = list()

    for i in range(1, len(arglist)):
        if '.pol' in arglist[i]:
            filename = arglist[i]
        elif arglist[i] == '-newt':
            newt = 1
        elif arglist[i] == '-sec':
            sec = 1
        elif arglist[i] == '-maxIter':
            maxIter = int(arglist[i + 1])
        elif arglist[i - 1] != '-maxIter':
            bounds.append(arglist[i])

    # process file and return polynomial and degree of polynomial
    poly, numpow = filepro(filename)

    # assigning initial points
    if newt:
        x = float(bounds[0])
    else:
        a = float(bounds[0])
        b = float(bounds[1])

    # begin operatiosn
    if newt:
        result = newton(x, maxIter, poly)
    elif sec:
        result = secant(a, b, poly, maxIter)
    else:
        result = bisection(a, b, poly, maxIter)

    # create file with solution
    filename = filename.replace('.pol', '.sol')

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(result)

    except IOError:
        print('I/O error encountered')


if __name__ == '__main__':
    main()
