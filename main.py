#!/usr/bin/env python2

import unittest
from lexer import Lexer, TokenKind
from parser import Parser

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
    # test_string = "!Q)P!"
    # lexer = Lexer(test_string).tokenize()
    # parse_tree = Parser().parse(lexer)
    
    file = open('input.txt', 'r')
    for index, line in enumerate(file):
        print ("Input #" + str(index+1) + ": ")
        lexer = Lexer(line).tokenize()
        parse_tree = Parser().parse(lexer)
        print "\n\n"
        print "-------------------------"