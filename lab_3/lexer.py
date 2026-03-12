from typing import List, Optional
from token_type import TokenType, KEYWORDS, FUNCTIONS
from token_ import Token
from lexer_error import LexerError


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []

    def current_char(self) -> Optional[str]:
        if self.pos < len(self.source):
            return self.source[self.pos]
        return None

    def peek(self, offset: int = 1) -> Optional[str]:
        idx = self.pos + offset
        if idx < len(self.source):
            return self.source[idx]
        return None

    def advance(self) -> str:
        char = self.source[self.pos]
        self.pos += 1
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return char

    def skip_whitespace(self):
        while self.current_char() and self.current_char() in ' \t\r':
            self.advance()

    def skip_comment(self):
        if self.current_char() == '#':
            while self.current_char() and self.current_char() != '\n':
                self.advance()
        elif self.current_char() == '/' and self.peek() == '*':
            self.advance()
            self.advance()
            while self.current_char():
                if self.current_char() == '*' and self.peek() == '/':
                    self.advance()
                    self.advance()
                    break
                self.advance()

    def read_number(self) -> Token:
        start_col = self.column
        num_str = ''
        is_float = False

        while self.current_char() and self.current_char().isdigit():
            num_str += self.advance()

        if self.current_char() == '.' and self.peek() and self.peek().isdigit():
            is_float = True
            num_str += self.advance()
            while self.current_char() and self.current_char().isdigit():
                num_str += self.advance()

        if self.current_char() in ('e', 'E'):
            is_float = True
            num_str += self.advance()
            if self.current_char() in ('+', '-'):
                num_str += self.advance()
            if not self.current_char() or not self.current_char().isdigit():
                raise LexerError("Invalid scientific notation", self.line, self.column)
            while self.current_char() and self.current_char().isdigit():
                num_str += self.advance()

        token_type = TokenType.FLOAT if is_float else TokenType.INTEGER
        return Token(token_type, num_str, self.line, start_col)

    def read_string(self, quote_char: str) -> Token:
        start_col = self.column
        self.advance()
        string_val = ''

        while self.current_char() and self.current_char() != quote_char:
            if self.current_char() == '\\':
                self.advance()
                escape = self.advance()
                escape_map = {
                    'n': '\n', 't': '\t', 'r': '\r',
                    '\\': '\\', '"': '"', "'": "'"
                }
                string_val += escape_map.get(escape, escape)
            else:
                string_val += self.advance()

        if self.current_char() != quote_char:
            raise LexerError("Unterminated string literal", self.line, start_col)

        self.advance()
        return Token(TokenType.STRING, string_val, self.line, start_col)

    def read_identifier_or_keyword(self) -> Token:
        start_col = self.column
        ident = ''

        while self.current_char() and (self.current_char().isalnum() or self.current_char() == '_'):
            ident += self.advance()

        if ident in FUNCTIONS:
            return Token(FUNCTIONS[ident], ident, self.line, start_col)
        elif ident in KEYWORDS:
            return Token(KEYWORDS[ident], ident, self.line, start_col)
        else:
            return Token(TokenType.IDENTIFIER, ident, self.line, start_col)

    def tokenize(self) -> List[Token]:
        while self.pos < len(self.source):
            self.skip_whitespace()

            if self.pos >= len(self.source):
                break

            char = self.current_char()
            col = self.column

            if char == '#' or (char == '/' and self.peek() == '*'):
                self.skip_comment()
                continue

            if char == '\n':
                self.tokens.append(Token(TokenType.NEWLINE, '\\n', self.line, col))
                self.advance()
                continue

            if char.isdigit():
                self.tokens.append(self.read_number())
                continue

            if char in ('"', "'"):
                self.tokens.append(self.read_string(char))
                continue

            if char.isalpha() or char == '_':
                self.tokens.append(self.read_identifier_or_keyword())
                continue

            two_char = char + (self.peek() or '')

            if two_char == '//':
                while self.current_char() and self.current_char() != '\n':
                    self.advance()
                continue

            two_char_map = {
                '==': TokenType.EQUAL,
                '!=': TokenType.NOT_EQUAL,
                '<=': TokenType.LESS_EQUAL,
                '>=': TokenType.GREATER_EQUAL,
                '**': TokenType.POWER,
            }

            if two_char in two_char_map:
                self.tokens.append(Token(two_char_map[two_char], two_char, self.line, col))
                self.advance()
                self.advance()
                continue

            single_char_map = {
                '+': TokenType.PLUS,
                '-': TokenType.MINUS,
                '*': TokenType.MULTIPLY,
                '/': TokenType.DIVIDE,
                '%': TokenType.MODULO,
                '<': TokenType.LESS_THAN,
                '>': TokenType.GREATER_THAN,
                '=': TokenType.ASSIGN,
                '(': TokenType.LPAREN,
                ')': TokenType.RPAREN,
                '{': TokenType.LBRACE,
                '}': TokenType.RBRACE,
                '[': TokenType.LBRACKET,
                ']': TokenType.RBRACKET,
                ',': TokenType.COMMA,
                ';': TokenType.SEMICOLON,
                ':': TokenType.COLON,
                '.': TokenType.DOT,
            }

            if char in single_char_map:
                self.tokens.append(Token(single_char_map[char], char, self.line, col))
                self.advance()
                continue

            raise LexerError(f"Unexpected character: {char!r}", self.line, col)

        self.tokens.append(Token(TokenType.EOF, '', self.line, self.column))
        return self.tokens