import hashlib

from ellipticcurve import CurveFp, Point, INFINITY, jacobi_symbol

class ECCParameters():
    def __init__(self, p, a, b, Gx, Gy, o):
        self.p = p
        self.a = a
        self.b = b
        self.Gx = Gx
        self.Gy = Gy
        self.o = o


ep = ECCParameters(
    p=0xffffffffffffffffffffffffffffffff000000000000000000000001,
    a=0xfffffffffffffffffffffffffffffffefffffffffffffffffffffffe,
    b=0xb4050a850c04b3abf54132565044b0b7d7bfd8ba270b39432355ffb4,
    Gx=0xb70e0cbd6bb4bf7f321390b94a03c1d356c21122343280d6115c1d21,
    Gy=0xbd376388b5f723fb4c22dfe6cd4375a05a07476444d5819985007e34,
    o=0xffffffffffffffffffffffffffff16a2e0b8f03e13dd29455c5c2a3d)


curve_secp224r1 = CurveFp(ep.p, ep.a, ep.b)
G = Point(curve_secp224r1, ep.Gx, ep.Gy, ep.o)

def powMod(x, y, z) -> int:
    # Calculate (x ** y) % z efficiently.
    number = 1
    while y:
        if y & 1:
            number = number * x % z
        y >>= 1  # y //= 2

        x = x * x % z
    return number

def hashToCurve(x):

    #xBytes = hashlib.sha224(h.encode('utf-8')).digest()
    #x = int.from_bytes(xBytes, byteorder='big')
    print("x:\t",x)
    h=x
    for k in range(0, 100):
        # get matching y element for point
        y_parity = 0  # always pick 0,
        a = (powMod(x, 3, ep.p) + 7) % ep.p
        #print("a:\t",a)
        y = powMod(a, (ep.p + 1) // 4, ep.p)
        #print("before parity %x" % (y))
        if y % 2 != y_parity:
            y = ep.p - y

        # If x is always mod P, can R ever not be on the curve?
        try:
            R = Point(curve_secp224r1, x, y, ep.o)
        except Exception:
            x = (x + 1) % ep.p  # % P?
            continue

        if R == INFINITY or R * ep.o != INFINITY:  # is R * O != INFINITY check necessary?  Validation of Elliptic Curve Public Keys says no if cofactor = 1
            x = (x + 1) % ep.p  # % P?
            continue
        return R
    #print('hashToCurve failed for 100 tries')
    return h
