# Programming language focused on lean syntax and high performance 
# Lexer also known as tokenizer
# Convert a math expression string into a list of tokens that our parser can then use 
def tokenize(input_str):
    tokens = []
    i = 0
    while i < len(input_str):
        char = input_str[i]
        # Handle numbers including decimals
        if char.isdigit() or char == '.':
            num = char
            i += 1
            while i < len(input_str) and (input_str[i].isdigit() or input_str[i] == '.'):
                num += input_str[i]
                i += 1
            tokens.append(('NUMBER', float(num)))
        # Handle operators
        elif char in '+-*/^':
            tokens.append(('OPERATOR', char))
            i += 1
        # Handel parentheses
        elif char in '()':
            tokens.append(('PAREN', char))
            i += 1
        # Ignore whitespace
        elif char.isspace():
            i += 1
        else: 
            raise ValueError(f"Unexpected character: {char}")
    return tokens

if __name__ == '__main__':
    expression = "3 + 4 * (2 - 1)"
    tokens = tokenize(expression)
    print("Tokens:", tokens)

# Parser and AST Implementation
class ASTNode:
    pass

class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return f"NumberNode({self.value})"
    
class BinOpNode(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op # '+' / '-' / '*' / '/' / '^'
        self.right = right

    def __repr__(self):
        return f"BinOpNode({self.left}, '{self.op}', {self.right})"
    
# Parser class to build the AST from tokens
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None
    
    def eat(self, expected_type=None, expected_value=None):
        token = self.current_token()
        if token is None:
            raise Exception("Unexpected end of input")
        token_type, token_value = token
        if expected_type and token_type != expected_type:
            raise Exception(f"Expected token type {expected_type}, got {token_type}")
        if expected_value and token_value != expected_value:
            raise Exception(f"Expected token value {expected_value}, got {token_value}")
        self.pos += 1
        return token

    def parse(self):
        node = self.parse_expression()
        if self.current_token() is not None:
            raise Exception("Unexpected token at end of input")
        return node

    def parse_expression(self):
        # expression → term (("+" | "-") term)*
        node = self.parse_term()
        while self.current_token() and self.current_token()[0] == 'OPERATOR' and self.current_token()[1] in ('+', '-'):
            op = self.eat('OPERATOR')[1]
            right = self.parse_term()
            node = BinOpNode(node, op, right)
        return node

    def parse_term(self):
        # term → factor (("*" | "/") factor)*
        node = self.parse_factor()
        while self.current_token() and self.current_token()[0] == 'OPERATOR' and self.current_token()[1] in ('*', '/'):
            op = self.eat('OPERATOR')[1]
            right = self.parse_factor()
            node = BinOpNode(node, op, right)
        return node

    def parse_factor(self):
        # factor → primary ("^" factor)?
        node = self.parse_primary()
        # Exponentiation is right-associative
        while self.current_token() and self.current_token()[0] == 'OPERATOR' and self.current_token()[1] == '^':
            op = self.eat('OPERATOR')[1]
            right = self.parse_factor()
            node = BinOpNode(node, op, right)
        return node

    def parse_primary(self):
        # primary → NUMBER | "(" expression ")"
        token = self.current_token()
        if token is None:
            raise Exception("Unexpected end of input")
        
        token_type, token_value = token
        if token_type == 'NUMBER':
            self.eat('NUMBER')
            return NumberNode(token_value)
        elif token_type == 'PAREN' and token_value == '(':
            self.eat('PAREN', '(')
            node = self.parse_expression()
            self.eat('PAREN', ')')
            return node
        else:
            raise Exception(f"Unexpected token: {token}")

# Example usage:
if __name__ == '__main__':
    # Assume tokenize() from our previous step is available
    expression = "3 + 4 * (2 - 1) ^ 2"
    tokens = tokenize(expression)
    print("Tokens:", tokens)

    parser = Parser(tokens)
    ast = parser.parse()
    print("AST:", ast)

def evaluate(node):
    if isinstance(node, NumberNode):
        return node.value
    elif isinstance(node, BinOpNode):
        left_val = evaluate(node.left)
        right_val = evaluate(node.right)
        if node.op == '+':
            return left_val + right_val
        elif node.op == '-':
            return left_val - right_val
        elif node.op == '*':
            return left_val * right_val
        elif node.op == '/':
            return left_val / right_val
        elif node.op == '^':
            return left_val ** right_val
        else:
            raise Exception(f"Unknown operator: {node.op}")
    else:
        raise Exception("Invalid AST Node")

# Example integration with the lexer and parser
if __name__ == '__main__':
    expression = "3 + 4 * (2 - 1) ^ 2"
    tokens = tokenize(expression)
    print("Tokens:", tokens)
    
    parser = Parser(tokens)
    ast = parser.parse()
    print("AST:", ast)
    
    result = evaluate(ast)
    print("Result:", result)
