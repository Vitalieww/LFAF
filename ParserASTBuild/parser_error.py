class ParserError(Exception):
    def __init__(self, message: str, line: int, column: int):
        super().__init__(f"ParserError at line {line}, col {column}: {message}")
        self.line = line
        self.column = column