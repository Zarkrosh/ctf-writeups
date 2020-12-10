# https://tailcall.net/blog/cracking-randomness-lcgs/

from functools import *
from math import gcd

def crack_unknown_increment(states, modulus, multiplier):
    increment = (states[1] - states[0]*multiplier) % modulus
    return modulus, multiplier, increment


def crack_unknown_multiplier(states, modulus):
    multiplier = (states[2] - states[1]) * inverse_mod(states[1] - states[0], modulus) % modulus
    return crack_unknown_increment(states, modulus, multiplier)

def crack_unknown_modulus(states):
    diffs = [s1 - s0 for s0, s1 in zip(states, states[1:])]
    zeroes = [t2*t0 - t1*t1 for t0, t1, t2 in zip(diffs, diffs[1:], diffs[2:])]
    modulus = gcdl(zeroes)
    return crack_unknown_multiplier(states, modulus)

def gcdl(L):
    return reduce(gcd, L)

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x)

def inverse_mod(b, n):
    g, x, _ = egcd(b, n)
    if g == 1:
        return x % n

import requests, json

def get_year():
	r = requests.get("http://docker.hackthebox.eu:30357/next_year")
	return json.loads(r.text)["year"]

states = []

for i in range(50):
	states.append(int(get_year()))

modulus, multiplier, increment = crack_unknown_modulus(states)

# sage ints not serializable, we calculate with sage and then get the flag without it
modulus, multiplier, increment = 2147483647, 48271, 0

next_year = (states[-1]*multiplier + increment)%modulus
r = requests.post("http://docker.hackthebox.eu:30357/predict_year", json = {'year': next_year})
print(r.text)
# we receive this message {"msg": "*Tardis trembles*\nDoctor this is Amy! I am with Rory in year 2020. You need to rescue us within exactly 876578 hops. Tardis bug has damaged time and space.\nRemeber, 876578 hops or the universes will collapse!"}
hops = 876578

# seed*m^hops % mod = 2020, since c is 0 in this case

seed = 2020*inverse_mod(multiplier**hops, modulus) % modulus
#print(seed)

r = requests.post("http://docker.hackthebox.eu:30357/travelTo2020", json = {'seed': seed})
print(r.text)