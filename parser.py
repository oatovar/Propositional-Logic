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
        # Try to parse the tree
        try:
            self.tokens = tokenList
            t = self.tokens[self.index]
            self.loc = t.loc
            if (t.kind == "ID" or t.kind == "LPAR" or 
            t.kind == "RPAR" or t.kind == "NOT" or t.kind == "AND"
            or t.kind == "OR" or t.kind == "IMPLIES" or t.kind == "IFF"
            or t.kind == "COMMA" or t.kind == "UNKNOWN"):
                self.propositions()
                return self.tokens
            else:
                print("Syntax Error at line " + str(t.loc.line) + " column " +
                str(t.loc.col) + ".")
        # If the parser throws an error then print out the exception
        except Exception as E:
            print E


    def match(self, token):
        print sys._getframe().f_code.co_name
        raise NotImplementedError

    def propositions(self):
        print sys._getframe().f_code.co_name
        self.proposition()
        self.more_proposition()


    def more_proposition(self):
        print sys._getframe().f_code.co_name
        if (self.index < len(self.tokens)):
            token = self.tokens[self.index]
            if (token.kind == "COMMA"):
                self.COMMA()
                self.index += 1
                self.propositions()
            else:
                self.epsilon()
        else:
            self.epsilon()
    
    def proposition(self):
        print sys._getframe().f_code.co_name
        if (self.index < len(self.tokens)):
            token = self.tokens[self.index]
            if (token.kind == "LPAR" or token.kind == "NOT"):
                self.compound()
            elif (token.kind == "ID"):
                self.atomic()
            else:
                raise Exception("Syntax Error at line "+ str(token.loc.line) + " column " + str(token.loc.col) + ".")
        else:
            token = self.tokens[self.index]
            raise Exception("Syntax Error at line "+ str(token.loc.line) + " column " + str(token.loc.col) + ".")

    def atomic(self):
        print sys._getframe().f_code.co_name
        if (self.index < len(self.tokens)):
            token = self.tokens[self.index]
            if (token.kind == "ID"):
                self.ID()
                self.index += 1
            else:
                raise Exception("Syntax Error at line "+ str(token.loc.line) + " column " + str(token.loc.col) + ".")
        else:
            token = self.tokens[self.index]
            raise Exception("Syntax Error at line "+ str(token.loc.line) + " column " + str(token.loc.col) + ".")

    def compound(self):
        print sys._getframe().f_code.co_name
        if (self.index < len(self.tokens)):
            token = self.tokens[self.index]
             # OPTION 1
            if (token.kind == "ID"):
                self.atomic()
                self.connective()
                self.proposition()
            # OPTION 2
            # LPAR HERE
            elif (token.kind == "LPAR"):
                self.LPAR()
                self.index += 1
                self.proposition()
                self.RPAR()
                self.index +=1
            # MATCH RPAR HERE
            # OPTION 3
            # MATCH NOT HERE
            elif (token.kind == "NOT"):
                self.NOT()
                self.index += 1
                self.proposition()
            else:
                raise Exception("Syntax Error at line "+ str(token.loc.line) + " column " + str(token.loc.col) + ".")
        else:
            token = self.tokens[self.index]
            raise Exception("Syntax Error at line "+ str(token.loc.line) + " column " + str(token.loc.col) + ".")

    def connective(self):
        print sys._getframe().f_code.co_name
        # PRINT TOKEN HERE SINCE CONNECTIVE LEADS TO TERMINAL STATES
        if (self.index < len(self.tokens)):
            token = self.tokens[self.index]
        else:
            raise Exception("Syntax Error at line "+ str(token.loc.line) + " column " + str(token.loc.col) + ".")
        if (token.kind == "AND"):
            self.AND()
        elif(token.kind == "OR"):
            self.OR()
        elif(token.kind == "IMPLIES"):
            self.IMPLIES()
        elif(token.kind == "IFF"):
            self.IFF()
        else:
            token = self.tokens[self.index]
            raise Exception("Syntax Error at line "+ str(token.loc.line) + " column " + str(token.loc.col) + ".")
    
    # prints ID
    def ID(self):
        print sys._getframe().f_code.co_name

    # prints epsilon
    def epsilon(self):
        print sys._getframe().f_code.co_name
    
    # prints LPAR
    def LPAR(self):
        print sys._getframe().f_code.co_name
    
    # prints RPAR
    def RPAR(self):
        print sys._getframe().f_code.co_name

    # prints NOT
    def NOT(self):
        print sys._getframe().f_code.co_name

    # prints COMMA
    def COMMA(self):
        print sys._getframe().f_code.co_name

    # prints AND
    def AND(self):
        print sys._getframe().f_code.co_name

    # prints OR
    def OR(self):
        print sys._getframe().f_code.co_name
    
    # prints IMPLIES
    def IMPLIES(self):
        print sys._getframe().f_code.co_name

    # IFF
    def IFF(self):
        print sys._getframe().f_code.co_name