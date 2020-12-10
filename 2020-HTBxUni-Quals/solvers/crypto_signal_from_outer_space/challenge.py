from Crypto.Cipher import AES
from Crypto.Util.number import inverse
from Crypto.Util.Padding import pad, unpad
from collections import namedtuple
from random import randint
import hashlib
import os

# Create a simple Point class to represent the affine points.
Point = namedtuple("Point", "x y")

# The point at infinity (origin for the group law).
O = 'Origin'

def encrypt(secret):
    sha1 = hashlib.sha1()
    sha1.update(str(secret).encode('ascii'))
    key = sha1.digest()[:16]

    dt = open('flag.mp3','rb').read()
    # Encrypt flag
    cipher = AES.new(key, AES.MODE_ECB)

    ciphertext = cipher.encrypt(pad(dt, 16))

    open('flag.enc','wb').write(ciphertext)


def check_point(P: tuple):
    if P == O:
        return True
    else:
        return (P.y**2 - (P.x**3 + a*P.x + b)) % p == 0 and 0 <= P.x < p and 0 <= P.y < p


def point_inverse(P: tuple):
    if P == O:
        return P
    return Point(P.x, -P.y % p)


def point_addition(P: tuple, Q: tuple):
    if P == O:
        return Q
    elif Q == O:
        return P
    elif Q == point_inverse(P):
        return O
    else:
        if P == Q:
            lam = (3*P.x**2 + a)*inverse(2*P.y, p)
            lam %= p
        else:
            lam = (Q.y - P.y) * inverse((Q.x - P.x), p)
            lam %= p
    Rx = (lam**2 - P.x - Q.x) % p
    Ry = (lam*(P.x - Rx) - P.y) % p
    R = Point(Rx, Ry)
    assert check_point(R)
    return R


def double_and_add(P: tuple, n: int):
    Q = P
    R = O
    while n > 0:
        if n % 2 == 1:
            R = point_addition(R, Q)
        Q = point_addition(Q, Q)
        n = n // 2
    assert check_point(R)
    return R


def gen_shared_secret(Q: tuple, n: int):
    S = double_and_add(Q, n)
    return S.x


p = ...
a = ...
b = ...


g_x = ...
g_y = ...
G = Point(g_x, g_y)


n = randint(1, p)

public = double_and_add(G, n)

key = gen_shared_secret(public,n)
encrypt(key)
decrypt(key)
