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
        self.results = list()
        self.index = 0

    def parse(self, tokenList):
        # Try to parse the tree
        try:
            self.tokens = tokenList
            token_values = list()
            for token in tokenList:
                token_values.append(token.kind)
            print(token_values)
            t = self.tokens[self.index]
            self.loc = t.loc
            if (t.kind == "ID" or t.kind == "LPAR" or 
            t.kind == "RPAR" or t.kind == "NOT" or t.kind == "AND"
            or t.kind == "OR" or t.kind == "IMPLIES" or t.kind == "IFF"
            or t.kind == "COMMA" or t.kind == "UNKNOWN"):
                self.propositions()
                return self.results
            else:
                print("Syntax Error at line " + str(t.loc.line) + " column " +
                str(t.loc.col) + ".")
                return
        # If the parser throws an error then print out the exception
        except Exception as E:
            print E


    def match(self, token):
        # print sys._getframe().f_code.co_name
        raise NotImplementedError

    def propositions(self):
        # print sys._getframe().f_code.co_name
        self.results.append("propositions")
        self.proposition()
        self.more_proposition()


    def more_proposition(self):
        # print sys._getframe().f_code.co_name
        self.results.append("more_proposition")
        if (self.index < len(self.tokens)):
            token = self.tokens[self.index]
            if (token.kind == "COMMA"):
                #print self.tokens[self.index].kind
                self.COMMA()
                self.index += 1
                #print self.tokens[self.index].kind
                self.propositions()
            else:
                self.epsilon()
        else:
            self.epsilon()
    
    def proposition(self):
        # print sys._getframe().f_code.co_name
        self.results.append("proposition")
        if (self.index < len(self.tokens)):
            token = self.tokens[self.index]
            #print(token.kind)
            if (token.kind == "LPAR" or token.kind == "NOT"):
                self.compound()
            elif (token.kind == "ID" and self.index < len(self.tokens) - 1):
                if (self.tokens[self.index+1].kind in ("AND", "OR", "IMPLIES", "IFF")):
                    self.compound()
                else:
                    self.atomic()
                    self.index += 1
            else:
                print("Syntax Error at line "+ str(token.loc.line) + " column " + str(token.loc.col) + ".")
                return
        else:
            token = self.tokens[self.index]
            print("Syntax Error at line "+ str(token.loc.line) + " column " + str(token.loc.col) + ".")
            return

    def atomic(self):
        # print sys._getframe().f_code.co_name
        self.results.append("atomic")
        if (self.index < len(self.tokens)):
            token = self.tokens[self.index]
            if (token.kind == "ID"):
                self.ID()
                self.index += 1
            else:
                print("Syntax Error at line "+ str(token.loc.line) + " column " + str(token.loc.col) + ".")
                return
        else:
            token = self.tokens[self.index]
            print("Syntax Error at line "+ str(token.loc.line) + " column " + str(token.loc.col) + ".")
            return

    def compound(self):
        # print sys._getframe().f_code.co_name
        self.results.append("compound")
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
                print("Syntax Error at line "+ str(token.loc.line) + " column " + str(token.loc.col) + ".")
                return
        else:
            token = self.tokens[self.index]
            print("Syntax Error at line "+ str(token.loc.line) + " column " + str(token.loc.col) + ".")
            return

    def connective(self):
        # print sys._getframe().f_code.co_name
        self.results.append("connective")
        # PRINT TOKEN HERE SINCE CONNECTIVE LEADS TO TERMINAL STATES
        if (self.index < len(self.tokens)):
            token = self.tokens[self.index]
        else:
            print("Syntax Error at line "+ str(token.loc.line) + " column " + str(token.loc.col) + ".")
            return
        if (token.kind == "AND"):
            self.AND()
            self.index += 1
        elif(token.kind == "OR"):
            self.OR()
            self.index += 1
        elif(token.kind == "IMPLIES"):
            self.IMPLIES()
            self.index += 1
        elif(token.kind == "IFF"):
            self.IFF()
            self.index += 1
        else:
            token = self.tokens[self.index]
            print("Syntax Error at line "+ str(token.loc.line) + " column " + str(token.loc.col) + ".")
            return
    
    # prints ID
    def ID(self):
        # print sys._getframe().f_code.co_name
        self.results.append("ID")

    # prints epsilon
    def epsilon(self):
        # print sys._getframe().f_code.co_name
        self.results.append("epsilon")
    
    # prints LPAR
    def LPAR(self):
        # print sys._getframe().f_code.co_name
        self.results.append("LPAR")
    
    # prints RPAR
    def RPAR(self):
        # print sys._getframe().f_code.co_name
        self.results.append("RPAR")

    # prints NOT
    def NOT(self):
        # print sys._getframe().f_code.co_name
        self.results.append("NOT")

    # prints COMMA
    def COMMA(self):
        # print sys._getframe().f_code.co_name
        self.results.append("COMMA")
        print("COMMA REACHED")

    # prints AND
    def AND(self):
        # print sys._getframe().f_code.co_name
        self.results.append("AND")

    # prints OR
    def OR(self):
        # print sys._getframe().f_code.co_name
        self.results.append("OR")
    
    # prints IMPLIES
    def IMPLIES(self):
        # print sys._getframe().f_code.co_name
        self.results.append("IMPLIES")

    # IFF
    def IFF(self):
        # print sys._getframe().f_code.co_name
        self.results.append("IFF")