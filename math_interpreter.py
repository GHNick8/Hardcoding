# Hardcoding my own language, writing some of the building blocks 

# Token types 
# Defines different symbols recognized in the langauge, including numbers, operators, parentheses, and end-of-file. 
NUMBER = 'NUMBER'
PLUS = 'PLUS'
MINUS = 'MINUS'
MULTIPLY = 'MULTIPLY'
DIVIDE = 'DIVIDE'
LPAREN = 'LPAREN' # Left parenthesis (
RPAREN = 'RPAREN' # Right parenthesis )
EOF = 'EOF' # End-of-file is a condition in a computer operating system where no more data can be read from a data source. 
IDENTIFIER = 'IDENTIFIER'
ASSIGN = 'ASSIGN'
FUNC_DEF = 'FUNC_DEF'
FUNC_CALL = 'FUNC_CALL'

# Custom len function
def my_len(iterable):
    count = 0
    for _ in iterable:
        count += 1
    return count

# Custom append function 
def my_append(lst, item):
    lst += [item]

# Custom isdigit function
def my_isdigit(char):
    return '0' <= char <= '9'

# Custom isalpha function
def my_isalpha(char):
    return ('a' <= char <= 'z') or ('A' <= char <= 'Z')

# Custom isspace function 
def my_isspace(char):
    return char == ' ' or char == '\t' or char == '\n' or char == '\r'

# Custom position increment function
def increment_pos(interpreter):
    interpreter.pos += 1

# Custom function to get current token
def current_token(interpreter):
    return interpreter.tokens[interpreter.pos]

# Custom function to get character at position
def get_char(expression, position):
    return expression[position]

# Custom string concatenation function
def concat_strings(s1, s2):
    return s1 + s2

# Tokenizer without regex
def tokenize(expression):
    tokens = []
    position = 0
    while position < my_len(expression):
        char = get_char(expression, position)
        if my_isdigit(char):
            num = char
            position += 1
            while position < my_len(expression) and my_isdigit(get_char(expression, position)):
                num = concat_strings(num, get_char(expression, position))
                position += 1
            my_append(tokens, (NUMBER, num))
        elif my_isalpha(char):
            ident = char
            position += 1
            while position < my_len(expression) and (my_isalpha(get_char(expression, position)) or my_isdigit(get_char(expression, position))):
                ident = concat_strings(ident, get_char(expression, position))
                position += 1
            my_append(tokens, (IDENTIFIER, ident))
        elif char == '=':
            my_append(tokens, (ASSIGN, char))
            position += 1
        elif char == '+':
            my_append(tokens, (PLUS, char))
            position += 1
        elif char == '-':
            my_append(tokens, (MINUS, char))
            position += 1
        elif char == '*':
            my_append(tokens, (MULTIPLY, char))
            position += 1
        elif char == '/':
            my_append(tokens, (DIVIDE, char))
            position += 1
        elif char == '(':
            my_append(tokens, (LPAREN, char))
            position += 1
        elif char == ')':
            my_append(tokens, (RPAREN, char))
            position += 1
        elif my_isspace(char):
            position += 1  # Ignore whitespace
        else:
            raise ValueError(f'Unexpected character: {char}')
    my_append(tokens, (EOF, None))
    return tokens

# Parser & Evaluator
variables = {}

class Interpreter:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def eat(self, token_type):
        if current_token(self)[0] == token_type:
            increment_pos(self)
        else:
            raise ValueError(f'Expected {token_type}, got {current_token(self)[0]}')

    def factor(self):
        token = current_token(self)
        if token[0] == NUMBER:
            self.eat(NUMBER)
            return int(token[1])
        elif token[0] == IDENTIFIER:
            self.eat(IDENTIFIER)
            return variables.get(token[1], 0)
        elif token[0] == LPAREN:
            self.eat(LPAREN)
            result = self.expr()
            self.eat(RPAREN)
            return result
    
    def term(self):
        result = self.factor()
        while current_token(self)[0] in (MULTIPLY, DIVIDE):
            if current_token(self)[0] == MULTIPLY:
                self.eat(MULTIPLY)
                result *= self.factor()
            elif current_token(self)[0] == DIVIDE:
                self.eat(DIVIDE)
                result /= self.factor()
        return result
    
    def expr(self):
        if current_token(self)[0] == IDENTIFIER and self.tokens[self.pos + 1][0] == ASSIGN:
            var_name = current_token(self)[1]
            self.eat(IDENTIFIER)
            self.eat(ASSIGN)
            variables[var_name] = self.expr()
            return variables[var_name]
        
        result = self.term()
        while current_token(self)[0] in (PLUS, MINUS):
            if current_token(self)[0] == PLUS:
                self.eat(PLUS)
                result += self.term()
            elif current_token(self)[0] == MINUS:
                self.eat(MINUS)
                result -= self.term()
        return result

# Run REPL
def main():
    while True:
        try:
            expression = input("calc> ")
            if expression.lower() in ('exit', 'quit'):
                break
            tokens = tokenize(expression)
            interpreter = Interpreter(tokens)
            result = interpreter.expr()
            print(result)
        except Exception as e:
            print(f'Error: {e}')

if __name__ == "__main__":
    main()
