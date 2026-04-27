from typing import List
from token_ import Token


def print_tokens(tokens: List[Token]):
    print(f"\n{'─' * 65}")
    print(f"{'TYPE':<25} {'VALUE':<20} {'LINE':<6} {'COL'}")
    print(f"{'─' * 65}")
    for token in tokens:
        print(f"{token.type.name:<25} {token.value!r:<20} {token.line:<6} {token.column}")
    print(f"{'─' * 65}\n")