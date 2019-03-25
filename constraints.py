#!/usr/bin/env python2
from pysmt.shortcuts import Symbol, And, Not, Or, Implies, Iff, is_sat

P = Symbol("P")
Q = Symbol("Q")
X = Symbol("X")
Y = Symbol("Y")

prop1 = Or(Q, P)
prop2 = Implies(Y, X)

f = And(Implies(Y, X), Or(Q, P))

print is_sat(f)
