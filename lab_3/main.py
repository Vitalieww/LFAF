from lexer import Lexer
from lexer_error import LexerError
from utils import print_tokens


if __name__ == "__main__":
    sample_code = """\
# Lexer demonstration program
let x = 3.14
let y = 2e3
let name = "Alice"
let flag = True

def compute(a, b):
    return a ** 2 + b ** 2

def trigonometry(angle):
    s = sin(angle)
    c = cos(angle)
    t = tan(angle)
    return s + c + t

if x > 0 and flag:
    print("Positive!")
elif x == 0:
    print("Zero")
else:
    print("Negative")

while x > 0:
    x = x - 1

result = sqrt(abs(log(exp(1.0))))
/* multi-line comment block ignored */
final = asin(0.5) + acos(0.5) + atan(1.0)
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
    except LexerError as e:
        print(f"\n{e}")