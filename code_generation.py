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
                result += "f = " + prop + "\n"

        result += "print is_sat(f)\n"
        return result
    
    def generate(self):
        # Open the file handle that we will write to
        file = open("constraints.txt", "w")

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
                file.write(str(token.value) + ' = ' + 'Symbol("' + token.value + '")\n')
                symbols.append(token.value)

        # Strictly used for pretty printing
        file.write("\n")

        # Convert the tokens into postfix notation
        result = self.infixToPostfix(self.tokens)
        if (result != -1):
            for key in result:
                print(str(key.value)),
            print('\n')

            result = self.parse(result)
            file.write(result)
            print(result)