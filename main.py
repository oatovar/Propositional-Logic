#!/usr/bin/env python2

import unittest
from lexer import Lexer, TokenKind
from parser import Parser
from code_generation import CodeGenerator

class Test(unittest.TestCase):
    def test1(self):
        l = Lexer('Q').tokenize()
        self.assertEqual(l[0].kind, "ID")

    def test2(self):
        tokelist = Lexer('!Q)P!').tokenize()
        parse_tree = Parser().parse(tokelist)
        self.assertEqual(parse_tree, None)


if __name__ == '__main__':
    # unittest.main()
    file = open('input.txt', 'r')
    for index, line in enumerate(file):
        print ("Input #" + str(index+1) + ": ")
        print (line)
        lexer = Lexer(line).tokenize()
        # parse_tree = Parser().parse(lexer)
        generator = CodeGenerator(lexer)
        generator.generate()
        # print "\n\n"
        # print "-------------------------"