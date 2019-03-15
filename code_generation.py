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
    
    def generate(self):
        # Open the file handle that we will write to
        file = open("constraints.txt", "w")

        # Proposition Count
        propCount = 1

        # Check to see what imports are needed
        for token in self.tokens:
            if (token.kind == "ID" and "Symbol" not in self.imports):
                self.imports.append("Symbol")
            if (token.kind == "LPAR" or token.kind == "RPAR"):
                continue
            if (token.kind == "NOT" and "Not" not in self.imports):
                self.imports.append("Not")
            if (token.kind == "OR" and "Or" not in self.imports):
                self.imports.append("Or")
            if (token.kind == "AND" and "And" not in self.imports):
                self.imports.append("And")
            if (token.kind == "IMPLIES" and "Implies" not in self.imports):
                self.imports.append("Implies")
            if (token.kind == "IFF" and "Iff" not in self.imports):
                self.imports.append("Iff")
        
        # Write the necessary import statement
        file.write('from pysmt.shortcuts import ')
        index = 0
        while index < len(self.imports):
            file.write(self.imports[index])
            file.write(', ')
            index += 1
        # Delete the index variable that is no longer in use
        del index
        
        # Append the last import which is always 'is_sat'
        file.write('is_sat\n\n')
        
        symbols = list()
        # First Write out the Symbols necessary for the function
        for token in self.tokens:
            if token.kind == "ID" and token.value not in symbols:
                file.write(str(token.value) + ' = ' + 'Symbol("' + token.value + '")\n\n')
                symbols.append(token.value)
            if token.kind == "COMMA":
                propCount += 1
        file.write("# Proposition Count: " + str(propCount) + "\n\n")
        
        # Convert the tokens into postfix notation
        result = self.infixToPostfix(self.tokens)
        if (result != -1):
            for key in result:
                print(str(key.value)),
            print('\n')

