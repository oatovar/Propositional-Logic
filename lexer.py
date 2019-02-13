import string
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
        print "Proposition: " + self.text
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