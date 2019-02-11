from lexer import Location, Lexer
import sys

class VariableType:
    PROPOSITIONS = 0
    PROPOSITION  = 1
    ATOMIC       = 2
    MOREPROPOSITIONS = 3
    COMPOUND = 4
    CONNECTIVE = 5



class Parser:
    def __init__(self):
        self.loc = Location(0, 0)
        self.tokens = list()
        self.index = 0

    def parse(self, tokenList):
        self.tokens = tokenList
        t = self.tokens[self.index]
        self.index += 1
        print t.kind
        if (t.kind == "ID" or t.kind == "LPAR" or 
        t.kind == "RPAR" or t.kind == "NOT" or t.kind == "AND"
        or t.kind == "OR" or t.kind == "IMPLIES" or t.kind == "IFF"
        or t.kind == "COMMA" or t.kind == "UNKNOWN"):
            self.propositions()
            self.match(t)
            return self.tokens
        else:
            print("Syntax Error at line " + str(t.loc.line) + " column " +
            str(t.loc.col) + ".")

    def match(self, token):
        print sys._getframe().f_code.co_name
        raise NotImplementedError

    def propositions(self):
        print "propositions"
        self.proposition()
        self.more_proposition()


    def more_proposition(self):
        print sys._getframe().f_code.co_name
        if ()
        self.epsilon()
    
    def proposition(self):
        print sys._getframe().f_code.co_name
        if (token.kind == "LPAR" or token.kind == "IMPLIES" or
        token.kind == "IFF"):
            self.compound()
        else:
            self.atomic()

    def atomic(self):
        print sys._getframe().f_code.co_name

    def compound(self):
        print sys._getframe().f_code.co_name
        # OPTION 1
        self.atomic()
        self.connective()
        self.proposition()
        # OPTION 2
        # LPAR HERE
        self.proposition()
        # MATCH RPAR HERE
        # OPTION 3
        # MATCH NOT HERE
        self.proposition()

    def connective(self):
        print sys._getframe().f_code.co_name
        # MATCH HERE
        
    # add more methods if needed
    def epsilon(self):
        print sys._getframe().f_code.co_name