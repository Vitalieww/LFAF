from enum import Enum, auto


class TokenType(Enum):
    # Literals
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()
    BOOLEAN = auto()

    # Identifiers & Keywords
    IDENTIFIER = auto()
    KEYWORD = auto()

    # Arithmetic Operators
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MODULO = auto()
    POWER = auto()

    # Comparison Operators
    EQUAL = auto()
    NOT_EQUAL = auto()
    LESS_THAN = auto()
    GREATER_THAN = auto()
    LESS_EQUAL = auto()
    GREATER_EQUAL = auto()

    # Logical Operators
    AND = auto()
    OR = auto()
    NOT = auto()

    # Assignment
    ASSIGN = auto()

    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    COMMA = auto()
    SEMICOLON = auto()
    COLON = auto()
    DOT = auto()

    # Trigonometric Functions
    SIN = auto()
    COS = auto()
    TAN = auto()
    ASIN = auto()
    ACOS = auto()
    ATAN = auto()

    # Math Functions
    SQRT = auto()
    ABS = auto()
    LOG = auto()
    EXP = auto()

    # Special
    NEWLINE = auto()
    EOF = auto()
    UNKNOWN = auto()


KEYWORDS = {
    'if': TokenType.KEYWORD,
    'else': TokenType.KEYWORD,
    'elif': TokenType.KEYWORD,
    'while': TokenType.KEYWORD,
    'for': TokenType.KEYWORD,
    'return': TokenType.KEYWORD,
    'def': TokenType.KEYWORD,
    'class': TokenType.KEYWORD,
    'import': TokenType.KEYWORD,
    'from': TokenType.KEYWORD,
    'in': TokenType.KEYWORD,
    'not': TokenType.NOT,
    'and': TokenType.AND,
    'or': TokenType.OR,
    'True': TokenType.BOOLEAN,
    'False': TokenType.BOOLEAN,
    'None': TokenType.KEYWORD,
    'pass': TokenType.KEYWORD,
    'break': TokenType.KEYWORD,
    'continue': TokenType.KEYWORD,
    'let': TokenType.KEYWORD,
    'var': TokenType.KEYWORD,
    'const': TokenType.KEYWORD,
    'print': TokenType.KEYWORD,
}

FUNCTIONS = {
    'sin': TokenType.SIN,
    'cos': TokenType.COS,
    'tan': TokenType.TAN,
    'asin': TokenType.ASIN,
    'acos': TokenType.ACOS,
    'atan': TokenType.ATAN,
    'sqrt': TokenType.SQRT,
    'abs': TokenType.ABS,
    'log': TokenType.LOG,
    'exp': TokenType.EXP,
}