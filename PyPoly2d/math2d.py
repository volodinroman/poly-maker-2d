import math

def binomial(i, n):
    """Binomial coefficient"""
    return math.factorial(n) / float(math.factorial(i) * math.factorial(n - i))
    

def bernstein(t, i, n):
    """Bernstein basis polynomial"""
    return binomial(i, n) * (t ** i) * ((1 - t) ** (n - i))


def bezier(t, points):
    """Per each iteration calculate curve point coordinates"""
    n = len(points) - 1
    x = 0
    y = 0
    for i, pos in enumerate(points):
        b = bernstein(t, i, n)
        x += pos[0] * b
        y += pos[1] * b
        
    return round(x,4), round(y,4)


def bezierCurve(n, points):
    """Bezier curve points generator"""
    for i in range(n):
        t = i / float(n - 1)
        yield bezier(t, points)


def cross3D(a = None, b = None):
    """Finds vector cross product"""
    c = [a[1]*b[2] - a[2]*b[1],
         a[2]*b[0] - a[0]*b[2],
         a[0]*b[1] - a[1]*b[0]]

    return c


def vectorMagnitude(vector = None):
    """Calculates the length of the vector"""
    return math.sqrt(pow(vector[0],2) + pow(vector[1],2) + pow(vector[2], 2))


def vectorNormalized(vector = None):
    """Normalizes vector """
    length = vectorMagnitude(vector = vector) #get vector magnitude
    return [vector[0] / length, vector[1] / length, vector[2] / length]
