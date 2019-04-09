#!/usr/bin/env python2
from pysmt.shortcuts import Symbol, And, Not, Or, Implies, Iff, is_sat

P = Symbol("P")
Q = Symbol("Q")

prop1 = And(P, Not(Q))
prop2 = Iff(Not(Q), Not(P))

f = And(Iff(Not(Q), Not(P)), And(P, Not(Q)))

print is_sat(f)
