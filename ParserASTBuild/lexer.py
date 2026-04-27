import re
from typing import List
from token_ import Token
from token_type import TokenType, KEYWORDS, FUNCTIONS
from lexer_error import LexerError


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.tokens: List[Token] = []

        # Define regex patterns. Order is important (e.g., ** before *)
        self.rules = [
            (re.compile(r'\n'), TokenType.NEWLINE),
            (re.compile(r'[ \t\r]+'), None),  # Skip whitespace
            (re.compile(r'#.*'), None),  # Skip single-line comments
            (re.compile(r'/\*.*?\*/', re.DOTALL), None),  # Skip multi-line comments
            (re.compile(r'\d+\.\d+([eE][+-]?\d+)?'), TokenType.FLOAT),
            (re.compile(r'\d+'), TokenType.INTEGER),
            (re.compile(r'"[^"\\]*(\\.[^"\\]*)*"'), TokenType.STRING),
            (re.compile(r'[a-zA-Z_]\w*'), TokenType.IDENTIFIER),
            (re.compile(r'\*\*'), TokenType.POWER),
            (re.compile(r'=='), TokenType.EQUAL),
            (re.compile(r'!='), TokenType.NOT_EQUAL),
            (re.compile(r'>='), TokenType.GREATER_EQUAL),
            (re.compile(r'<='), TokenType.LESS_EQUAL),
            (re.compile(r'>'), TokenType.GREATER_THAN),
            (re.compile(r'<'), TokenType.LESS_THAN),
            (re.compile(r'='), TokenType.ASSIGN),
            (re.compile(r'\+'), TokenType.PLUS),
            (re.compile(r'-'), TokenType.MINUS),
            (re.compile(r'\*'), TokenType.MULTIPLY),
            (re.compile(r'/'), TokenType.DIVIDE),
            (re.compile(r'%'), TokenType.MODULO),
            (re.compile(r'\('), TokenType.LPAREN),
            (re.compile(r'\)'), TokenType.RPAREN),
            (re.compile(r':'), TokenType.COLON),
            (re.compile(r','), TokenType.COMMA),
        ]

    def tokenize(self) -> List[Token]:
        pos = 0
        line = 1

        while pos < len(self.source):
            match = None
            for regex, token_type in self.rules:
                match = regex.match(self.source, pos)

                if match:
                    value = match.group(0)

                    if token_type == TokenType.NEWLINE:
                        line += 1
                        self.tokens.append(Token(token_type, '\\n', line, pos))
                    elif token_type == TokenType.IDENTIFIER:
                        # Check if identifier is actually a keyword or function
                        if value in KEYWORDS:
                            self.tokens.append(Token(KEYWORDS[value], value, line, pos))
                        elif value in FUNCTIONS:
                            self.tokens.append(Token(FUNCTIONS[value], value, line, pos))
                        else:
                            self.tokens.append(Token(token_type, value, line, pos))
                    elif token_type:
                        self.tokens.append(Token(token_type, value, line, pos))

                    # Update line count if a multi-line comment spans multiple lines
                    if not token_type and '\n' in value:
                        line += value.count('\n')

                    pos = match.end()
                    break

            if not match:
                raise LexerError(f"Unexpected character: {self.source[pos]}", line, pos)

        self.tokens.append(Token(TokenType.EOF, '', line, pos))
        return self.tokens
