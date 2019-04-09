#!/usr/bin/env python2

import subprocess
import string

class CodeGenerator:
    def __init__(self, tokens):
        self.tokens = tokens
        self.imports = list()
    
    def isOperator(self, token):
        if token.kind in ['NOT', 'AND', 'OR', 'IMPLIES', 'IFF', 'COMMA', 'LPAR', 'RPAR']:
            return True
        else:
            return False

    def precedence(self, token):
        if token.kind in ['COMMA']:
            return 3
        elif token.kind in ['AND', 'OR', 'IMPLIES', 'IFF']:
            return 2
        elif token.kind == 'NOT':
            return 1
        else:
            return 0

    def infixToPostfix(self, input):
        postfix = list()
        stack = list()
        for item in input:
            if not self.isOperator(item):
                postfix.append(item)
            elif item.kind == 'LPAR':
                stack.append(item)
            elif item.kind == 'RPAR':
                while len(stack) > 0 and stack[-1].kind != 'LPAR':
                    a = stack.pop()
                    postfix.append(a)
                if (len(stack) > 0 and stack[-1].kind != 'LPAR'):
                    return -1
                elif (len(stack) > 0):
                    stack.pop()
                else:
                    return -1
            else:
                while (len(stack) > 0 and self.precedence(item) <= self.precedence(stack[-1])):
                    postfix.append(stack.pop())
                stack.append(item)
                
        while (len(stack) > 0):
            postfix.append(stack.pop())

        return postfix
    
    def parse(self, input):
        result = "" # Result to return
        stack = list() # Stack used for postfix parsing
        props = list() # Props that have been parsed
        a = None
        b = None
        for i in input:
            if i.kind == "ID":
                stack.append(i.value)
            elif i.kind == "AND":
                a = stack.pop()
                b = stack.pop()
                prop = "And(" + a + ", " + b + ")"
                props.append(prop)
            elif i.kind == "OR":
                a = stack.pop()
                b = stack.pop()
                prop = "Or(" + a + ", " + b + ")"
                props.append(prop)
            elif i.kind == "NOT":
                if len(stack) > 0:
                    a = stack.pop()
                else:
                    a = props[-1]
                prop = "Not(" + a + ")"
                props.append(prop)
            elif i.kind == "IFF":
                if len(stack) > 0:
                    a = stack.pop()
                    b = stack.pop()
                else:
                    a = props[-1]
                    b = props[-2]
                prop = "Iff(" + a + ", " + b + ")"
                props.append(prop)
            elif i.kind == "IMPLIES":
                if len(stack) > 0:
                    a = stack.pop()
                    b = stack.pop()
                else:
                    a = props[-1]
                    b = props[-2]
                prop = "Implies(" + a + ", " + b + ")"
                props.append(prop)
            elif i.kind == "COMMA":
                if len(stack) > 0:
                    a = stack.pop()
                    b = stack.pop()
                else:
                    a = props[-1]
                    b = props[-2]
                prop = "And(" + a + ", " + b + ")"
                props.append(prop)
            else:
                pass

        for i, prop in enumerate(props):
            if i < len(props)-1:
                result += "prop" + str(i + 1) + " = " + prop + "\n"
            else:
                result += "\n"
                result += "f = " + prop + "\n"
                result += "\n"

        if (len(props) < 1):
            result += "f = " + stack[-1] + "\n"
        result += "print is_sat(f)\n"
        return result
    
    def generate(self):
        # Open the file handle that we will write to
        file = open("constraints.py", "w")

        file.write("#!/usr/bin/env python2\n")


        file.write('from pysmt.shortcuts import Symbol, And, Not, Or, Implies, Iff, is_sat\n\n')
        
        symbols = list()
        # First Write out the Symbols necessary for the function
        for token in self.tokens:
            if token.kind == "ID" and token.value not in symbols:
                file.write(str(token.value) + ' = ' + 'Symbol("' + token.value + '")\n')
                symbols.append(token.value)

        # Strictly used for pretty printing
        file.write("\n")

        # Convert the tokens into postfix notation
        result = self.infixToPostfix(self.tokens)
        if (result != -1):
            result = self.parse(result)
            file.write(result)
        else:
            print("False")

UPPER_CASE = set(string.ascii_uppercase)

class Location:
    def __init__(self, line, col):
        self.col = col
        self.line = line


class TokenKind:
    ID = "ID" # identifier [A-Z]+
    LPAR = "LPAR" # (
    RPAR = "RPAR" # )
    NOT = "NOT" # !
    AND = "AND"  # /\
    OR = "OR" # \/
    IMPLIES = "IMPLIES"  # =>
    IFF = "IFF" # <=>
    COMMA = "COMMA" # ,
    UNKNOWN = "UNKNOWN" # Anything that is not a token



class Token:
    def __init__(self, loc, kind, value):
        self.loc = loc
        self.kind = kind
        self.value = value

    def __str__(self):
        return str(self.kind)


class Lexer:
    def __init__(self, text):
        self.text = text
        self.line = 1
        self.col = 1

    def tokenize(self):
        current_match = None
        tokens = list()
        # print "Proposition: " + self.text
        c = 0 # current character index
        while c < len(self.text):
            if self.text[c] in UPPER_CASE:
                current_match = self.text[c]
                while (c + 1 < len(self.text)):
                    if (self.text[c+1] in UPPER_CASE):
                        c += 1
                        current_match += self.text[c]
                    else:
                        break
                # print "Index at " + str(c)
                # print "Appending " + current_match + " " + str(self.col)
                tokens.append(Token(Location(self.line, self.col), TokenKind.ID, current_match))
                # Advancing the column later is necessary so that the original spot is not lost
                self.col = c + 1
            elif self.text[c] == "(":
                current_match = self.text[c]
                tokens.append(Token(Location(self.line, self.col), TokenKind.LPAR, current_match))
            elif self.text[c] == ")":
                current_match = self.text[c]
                tokens.append(Token(Location(self.line, self.col), TokenKind.RPAR, current_match))
            elif self.text[c] == "!":
                current_match = self.text[c]
                tokens.append(Token(Location(self.line, self.col), TokenKind.NOT, current_match))
            elif self.text[c] == "/":
                # Probably good to check if this isn't part of a previous OR
                if (self.text[c-1] == "\\"):
                    c += 1
                    self.col = c + 1
                    continue
                elif (self.text[c+1] == "\\"):
                    current_match = self.text[c] + self.text[c+1]
                    tokens.append(Token(Location(self.line, self.col), TokenKind.AND, current_match))
                else:
                    print("Syntax Error at line " + str(self.line) + " column " + str(self.col) + ".")
                    break
            elif self.text[c] == "\\":
                if (self.text[c-1] == "/"):
                    c += 1
                    self.col = c + 1
                    continue
                elif (self.text[c+1] == "/"):
                    current_match = self.text[c] + self.text[c+1]
                    tokens.append(Token(Location(self.line, self.col), TokenKind.OR, current_match))
                    # Probably good to check if this isn't part of a previous AND
                else:
                    print("Syntax Error at line " + str(self.line) + " column " + str(self.col) + ".")
                    break
            elif self.text[c] == "=":
                # Check to see if this does not belong to a '<=>' token
                # and if it belongs to a '=>' IMPLIES token
                if (c+1 < len(self.text)):
                    if (self.text[c-1] != "<" and self.text[c+1] == ">"):
                        current_match = self.text[c:c+2]
                        tokens.append(Token(Location(self.line, self.col), TokenKind.IMPLIES, current_match))
                        self.col += 2
                    else:
                        print("Syntax Error at line " + str(self.line) + " column " + str(self.col) + ".")
                        break
                else:
                    print("Syntax Error at line " + str(self.line) + " column " + str(self.col) + ".")
                    break
            elif self.text[c] == "<":
                current_match = self.text[c]
                if (c+2 < len(self.text)):
                    # Check to see if the following two characters are '=' and '>'
                    # which would form '<=>', the token we are looking for
                    if (self.text[c+1] == "=" and self.text[c+2] == ">"):
                        current_match = self.text[c:c+3]
                        c += 2
                        tokens.append(Token(Location(self.line, self.col), TokenKind.IFF, current_match))
                        self.col += 3
                    else:
                        # Print an exception and break out of the loop.
                        print("Syntax Error at line " + str(self.line) + " column " + str(self.col) + ".")
                        break
            elif self.text[c] == ">":
                current_match = self.text[c]
                if (self.text[c-1] == "=" and self.text[c] == ">"):
                    pass
                else:
                    print("Syntax Error at line " + str(self.line) + " column " + str(self.col) + ".")
                    break
            elif self.text[c] == " ":
                current_match = None
                pass
            elif self.text[c] == ",":
                current_match = self.text[c]
                tokens.append(Token(Location(self.line, self.col), TokenKind.COMMA, current_match))
            elif self.text[c] == "\n":
                self.line += 1
                self.col = 0
            else:
                current_match = self.text[c]
                print(self.text[c])
                tokens.append(Token(Location(self.line, self.col), TokenKind.UNKNOWN, current_match))
                print("Syntax Error at line " + str(self.line) + " column " + str(self.col) + ".")
                break
            # raise NotImplementedError

            self.col += 1
            c += 1
        # Used to test if the tokens and positions are being grabbed correctly
        # tokenValues = list()
        # tokenPositions = list()
        # for token in tokens:
        #     tokenValues.append(token.value)
        #     tokenPositions.append(token.loc.col)
        # print tokenValues
        # print tokenPositions
        return tokens

if __name__ == '__main__':
    # unittest.main()
    file = open('input.txt', 'r')
    for index, line in enumerate(file):
        print ("Input #" + str(index+1) + ": ")
        print (line)
        lexer = Lexer(line).tokenize()
        # parse_tree = Parser().parse(lexer)

        # Generate the code for pysmt
        generator = CodeGenerator(lexer)
        generator.generate()

        result = subprocess.check_output(["python2", "constraints.py"])
        print(result)
        print("Code generated:")
        code = open('constraints.py', 'r')
        for line in code:
            print(line)
        # print "\n\n"
        # print "-------------------------"