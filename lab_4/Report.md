# Regex Parser & Generator

**Course:** Formal Languages & Finite Automata  
**Author:** Vitalie Vasilean — FAF-241

---

## Theory

Parsing regular expressions into an Abstract Syntax Tree (AST) isolates the structure of the expression. By breaking down regular expressions into fundamental operations — concatenation, alternation, and quantification — a program can evaluate or generate matching strings systematically.

An AST represents the hierarchical syntactic structure of a regex. The parser acts as a bridge between the raw character sequence and the structured tree of AST nodes, where each node represents a distinct operation. Evaluating or generating strings is achieved by recursively traversing the tree and resolving each node down to its base primitives (literals).

---

## Objectives

- Understand how regular expressions can be modeled as an Abstract Syntax Tree.
- Implement a parser that handles concatenation, alternation (`|`), quantification (`*`, `+`, `?`), and grouping (`()`).
- Build an AST node hierarchy capable of generating random string examples that conform to parsed regex rules.
- Validate the implementation against complex string patterns.

---

## Project Structure

```
lab_4/
├── regex_ast.py    # Base AST class template
├── literal.py      # Leaf node — character literals
├── concat.py       # Node — sequence concatenation
├── or_node.py      # Node — alternation / choices
├── quantifier.py   # Node — repetitions (*, +, ?)
├── parser.py       # Core logic: parses regex string into AST
└── main.py         # Entry point for testing
```

---

## Implementation

### AST Nodes

All AST nodes inherit from a base `RegexAST` class and implement a `generate()` method.

**`Or` node** — randomly selects between two branches:

```python
import random
from regex_ast import RegexAST

class Or(RegexAST):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def generate(self):
        return random.choice([self.left, self.right]).generate()

    def __repr__(self):
        return f"Or({self.left}, {self.right})"
```

Similarly:
- `Quantifier` evaluates a random integer within a specified bound (`*` → 0–5, `+` → 1–5, `?` → 0–1).
- `Concat` evaluates both children sequentially and joins the result.

### Parser

`parse_regex` in `parser.py` consumes the regex character by character, handling nested groups via recursion and building nodes into a sequence array:

```python
def parse_regex(regex_str):
    def parse_expr(chars):
        nodes = []
        while chars:
            c = chars[0]
            if c == '(':
                chars.pop(0)
                nodes.append(parse_expr(chars))
            elif c == ')':
                chars.pop(0)
                break
            elif c == '|':
                chars.pop(0)
                right = parse_expr(chars)
                left = nodes.pop() if nodes else Literal('')
                nodes.append(Or(left, right))
                break
            elif c in '*+?':
                chars.pop(0)
                target = nodes.pop()
                if c == '*':   nodes.append(Quantifier(target, 0, 5))
                elif c == '+': nodes.append(Quantifier(target, 1, 5))
                elif c == '?': nodes.append(Quantifier(target, 0, 1))
            else:
                chars.pop(0)
                nodes.append(Literal(c))

        if not nodes:
            return Literal('')

        result = nodes[0]
        for node in nodes[1:]:
            result = Concat(result, node)
        return result

    chars = list(regex_str.replace(' ', ''))
    return parse_expr(chars)
```

---

## Results

For the input regex `(a|b)(c|d)E+G?`, the parser builds a nested tree mapping choices, sequences, and repetitions. Calling `.generate()` repeatedly on the resulting AST produces valid strings from the language defined by the regex.

**AST structure:**
```
Concat(
  Concat(
    Concat(
      Or(Literal('a'), Literal('b')),
      Or(Literal('c'), Literal('d'))
    ),
    Quantifier(Literal('E'), 1–5)
  ),
  Quantifier(Literal('G'), 0–1)
)
```

**Sample generated strings:**
```
{'acEE', 'bdEE', 'bcEEEEG', 'bcEEG', 'bdEEEEEG'}
```

All outputs correctly match the subset of strings defined by the input expression.

---

## Key Takeaways

1. **Recursion simplifies parsing.** Handling parentheses by recursively calling the parse function naturally maps to tree construction.
2. **OOP ASTs are extensible.** Adding a new regex feature only requires a new class inheriting from `RegexAST` with its own `generate()` logic.

---

## References

- Course materials — *Formal Languages & Finite Automata*
- Python docs: [`random`](https://docs.python.org/3/library/random.html)