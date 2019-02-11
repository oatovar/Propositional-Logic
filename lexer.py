import string
UPPER_CASE = set(string.ascii_uppercase)

class Location:
    def __init__(self, line, col):
        self.col = col
        self.line = line


class TokenKind:
    ID = "ID" # identifier
    LPAR = "LPAR" # (
    RPAR = "RPAR" # )
    NOT = "NOT" # !
    AND = "AND"  # /\
    OR = "OR" # \/
    IMPLIES = "IMPLIES"  # =>
    IFF = "IFF" # <=>
    COMMA = "COMMA" # ,
    UNKNOWN = "UNKNOWN" # Anything that is not a state



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
        print self.text
        for c in self.text:
            current_type = None
            if c in UPPER_CASE:
                if (current_type == TokenKind.ID):
                    current_match += c
                    continue
                current_match = c
                current_type = TokenKind.ID
                tokens.append(Token(Location(self.line, self.col), TokenKind.ID, current_match))
            elif c == "(":
                current_match = c
                current_type = TokenKind.LPAR
                tokens.append(Token(Location(self.line, self.col), TokenKind.RPAR, current_match))
            elif c == ")":
                current_match = c
                current_type = TokenKind.RPAR
                tokens.append(Token(Location(self.line, self.col), TokenKind.RPAR, current_match))
            elif c == "!":
                current_match = c
                current_type = TokenKind.NOT
                tokens.append(Token(Location(self.line, self.col), TokenKind.NOT, current_match))
            elif c == "/":
                if (self.text[self.col] == "\\"):
                    current_match = c + self.text[self.col]
                    tokens.append(Token(Location(self.line, self.col), TokenKind.AND, current_match))
                else:
                    raise Exception("Syntax Error at line " + str(self.line) + " column " + str(self.col) + ".")
            elif c == "\\":
                if (self.text[self.col] == "/"):
                    current_match = c + self.text[self.col]
                    tokens.append(Token(Location(self.line, self.col), TokenKind.OR, current_match))
                else:
                    raise Exception("Syntax Error at line " + str(self.line) + " column " + str(self.col) + ".")
            elif c == "=":
                current_match = c
                tokens.append(Token(Location(self.line, self.col), TokenKind.IMPLIES, current_match))
            elif c == "<":
                current_match = c
                tokens.append(Token(Location(self.line, self.col), TokenKind.IFF, current_match))
            elif c == " ":
                current_match = None
                pass
            elif c == ",":
                current_match = c
                tokens.append(Token(Location(self.line, self.col), TokenKind.COMMA, current_match))
            elif c == "\n":
                self.line += 1
                self.col = 1
            else:
                current_match = c
                tokens.append(Token(Location(self.line, self.col), TokenKind.UNKNOWN, current_match))
                raise Exception("Syntax Error at line " + self.line + " column " + self.col + ".")
            # raise NotImplementedError

            self.col += 1
        return tokens