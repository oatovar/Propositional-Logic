#!/usr/bin/env python2
from pysmt.shortcuts import Symbol, And, Not, Or, Implies, Iff, is_sat

P = Symbol("P")
Q = Symbol("Q")

prop1 = Not(P)
prop2 = And(Q, Not(P))
prop3 = Not(And(Q, Not(P)))
prop4 = And(P, Not(And(Q, Not(P))))
prop5 = Not(And(P, Not(And(Q, Not(P)))))

f = Iff(Q, Not(And(P, Not(And(Q, Not(P))))))

print is_sat(f)
