from dataclasses import dataclass
from token_type import TokenType


@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int

    def __repr__(self):
        return (f"Token({self.type.name}, {self.value!r}, "
                f"line={self.line}, col={self.column})")