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

# Custom len function
def my_len(iterable):
    count = 0
    for _ in iterable:
        count += 1
        return count
    
# Custom append function
def my_append(lst, item):
    lst += [item]

# Tokenizer 
def tokenize(expression):
    tokens = []
    position = 0
    while position < my_len(expression):
        char = expression[position]
        if char.isdigit():
            num = char
            position += 1
            while position < my_len(expression) and expression[position].isdigit():
                num += expression[position]
                position += 1
                my_append(tokens, (NUMBER, num))