# A Practical Implementation of a Lexical Analyzer

**Course:** Formal Languages & Finite Automata  
**Author:** Vitalie Vasilean FAF-241

---

## Theory

This laboratory was my first practical dive into the world of compilers, starting with the foundational step: lexical analysis. Before this, `lexing` and `parsing` were just abstract terms. I learned that a lexer's job is simple in concept but detailed in execution: it scans raw source code character by character and groups them into meaningful **tokens**. It felt similar to how we read text: first we recognize individual symbols, then we group them into words and punctuation before thinking about meaning.

The key insight for me was the difference between a **lexeme** (the exact text slice like `let`) and a **token** (a structured object like `KEYWORD("let")` plus metadata). The lexer is basically a bridge between an unstructured character stream and a structured token stream that a parser can consume. Without tokenization, implementing grammar rules would be messy, because every parser rule would need to deal with raw characters.

What stood out during the lab was how much time goes into edge cases: floats vs integers, scientific notation, distinguishing operators like `=` vs `==`, and making sure comments don't break everything. At the same time, it made the finite automaton idea much more concrete: each "reader" function in the lexer behaves like a small DFA.

---

## Objectives

- Understand lexical analysis and why it is the first stage in most language processors.
- Implement a lexer in Python that recognizes literals, identifiers, keywords, operators, delimiters, and built-in math functions.
- Track line and column positions for every token to enable useful error reporting (via `LexerError`).
- Demonstrate the lexer on a non-trivial sample program and print the resulting token table.

---

## Implementation Description

### Project Structure

I split the implementation into small, focused modules. This helped me debug faster because each file has a clear responsibility, and issues were easier to isolate.

```
lab3/
├── token_type.py   # TokenType enum + KEYWORDS / FUNCTIONS maps
├── token_.py       # Token dataclass (+ readable __repr__)
├── lexer_error.py  # Custom LexerError exception with line/column
├── lexer.py        # Core Lexer class (scanner/tokenizer)
├── utils.py        # Token pretty-printer table output
└── main.py         # Demo entry point using sample_code
```

### `token_type.py` — Token Catalogue

This file defines the full set of token categories as an `Enum` (`TokenType`). I also used two dictionaries: `KEYWORDS` for language keywords (like `if`, `while`, `return`, `let`) and `FUNCTIONS` for math/trig functions (like `sin`, `sqrt`). This made recognition in the lexer straightforward and fast via dictionary lookup.

```python
from enum import Enum, auto

class TokenType(Enum):
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()
    BOOLEAN = auto()
    IDENTIFIER = auto()
    KEYWORD = auto()
    # ... operators, delimiters, functions, etc.

KEYWORDS = {
    "if": TokenType.KEYWORD,
    "while": TokenType.KEYWORD,
    "and": TokenType.AND,
    "True": TokenType.BOOLEAN,
    # ...
}

FUNCTIONS = {
    "sin": TokenType.SIN,
    "sqrt": TokenType.SQRT,
    # ...
}
```

### `token_.py` — Token Data Structure

Tokens are stored as a `@dataclass` with `type`, `value`, `line`, and `column`. Adding `line` and `column` early was one of the best decisions in this lab, because it makes both debugging and error messages precise. I also kept a readable `__repr__` so printing tokens during testing is clean.

```python
from dataclasses import dataclass
from token_type import TokenType

@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int
```

### `lexer_error.py` — Custom Exception

This file defines `LexerError`, which stores the error message along with the exact position. Having errors formatted as `line` and `col` made it much easier to understand what broke in the input without guessing.

```python
class LexerError(Exception):
    def __init__(self, message: str, line: int, column: int):
        super().__init__(f"LexerError at line {line}, col {column}: {message}")
        self.line = line
        self.column = column
```

### `lexer.py` — Core Scanner

This is the heart of the project. The `Lexer` walks through the source string using a position index and tracks `line`/`column` in `advance()`. The main `tokenize()` loop skips whitespace, checks for comments/newlines, and then dispatches to specialized routines:

- `read_number()`: reads integers, floats, and scientific notation.
- `read_string()`: reads quoted strings and raises errors if unterminated.
- `read_identifier_or_keyword()`: reads identifiers, then decides if the result is a function, keyword, boolean, or plain identifier.
- Operator handling: supports both two-character operators (like `==`, `!=`, `<=`) and single-character ones (like `+`, `-`, `(`, `)`).

A concrete snippet that shows the style of the main loop:

```python
def tokenize(self) -> List[Token]:
    while self.pos < len(self.source):
        self.skip_whitespace()
        char = self.current_char()

        if char == "#" or (char == "/" and self.peek() == "*"):
            self.skip_comment()
            continue

        if char.isdigit():
            self.tokens.append(self.read_number())
            continue

        if char in ('"', "'"):
            self.tokens.append(self.read_string(char))
            continue

        if char.isalpha() or char == "_":
            self.tokens.append(self.read_identifier_or_keyword())
            continue

        # ... operators / delimiters ...

    self.tokens.append(Token(TokenType.EOF, "", self.line, self.column))
    return self.tokens
```

### `utils.py` — Pretty Printer

This helper prints tokens in a table with aligned columns (`TYPE`, `VALUE`, `LINE`, `COL`). I relied on it as a quick "visual debugger": after any change in the lexer, I reran the demo and scanned the table for mistakes.

### `main.py` — Demo Entry Point

The demo defines a larger `sample_code` string that includes variables, numbers (including scientific notation), function calls (`sin`, `cos`, `sqrt`, `abs`, `log`, `exp`), control flow (`if`/`elif`/`else`, `while`), and a block comment `/* ... */`. It then tokenizes and prints results, catching `LexerError` if something goes wrong.

---

## Results

This lab made lexical analysis feel real, not theoretical. The biggest "aha" moment was realizing that each reader method is basically a small state machine, and that tracking position (line/column) is cheap but extremely valuable. Seeing the final token table printed from `main.py` felt like a clear confirmation that the lexer rules were working correctly.

### Sample Output (Abbreviated)

```
TYPE                      VALUE                LINE   COL
KEYWORD                   'let'                2      1
IDENTIFIER                'x'                  2      5
ASSIGN                    '='                  2      7
FLOAT                     '3.14'               2      9
...
EOF                       ''                   ...    ...
```

### Personal Takeaways

1. **Edge cases matter more than the happy path.** Supporting floats and comments took more thought than basic identifiers.
2. **One-character lookahead is powerful.** It solves ambiguities like `/` vs `/*` and `=` vs `==`.
3. **Modular design helps.** Separating token definitions, token objects, errors, and printing made the project easier to maintain.

---

## References

1. Course materials — Formal Languages & Finite Automata (Technical University of Moldova).
2. Robert Nystrom, *Crafting Interpreters* (Scanning): <https://craftinginterpreters.com/scanning.html>
3. Python docs: `enum` — <https://docs.python.org/3/library/enum.html>
4. Python docs: `dataclasses` — <https://docs.python.org/3/library/dataclasses.html>