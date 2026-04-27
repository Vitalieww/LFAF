from lexer import Lexer
from lexer_error import LexerError
from utils import print_tokens
from parser_ import Parser
from parser_error import ParserError

if __name__ == "__main__":
    sample_code = """\
# Function definition
def multiply(x, y):
    let result = x * y

# Variable assignments
let a = 10
let b = 5

# Conditionals and logical operators
if a > b and a != 0:
    let max = a
else:
    let max = b

# While loop with comparison
while a > 0:
    a = a - 1

# Function call
let final = multiply(a, b)
"""

    print("=" * 65)
    print(" Source Code")
    print("=" * 65)
    print(sample_code)

    lexer = Lexer(sample_code)
    try:
        tokens = lexer.tokenize()
        print_tokens(tokens)
        print(f"Total tokens: {len(tokens)}")

        parser = Parser(tokens)
        ast_nodes = parser.parse()

        print("\nAST Nodes:")
        for node in ast_nodes:
            print(node)

    except LexerError as e:
        print(f"\n{e}")
    except ParserError as e:
        print(f"\n{e}")