class LexerError(Exception):
    def __init__(self, message: str, line: int, column: int):
        super().__init__(
            f"LexerError at line {line}, col {column}: {message}"
        )
        self.line = line
        self.column = column