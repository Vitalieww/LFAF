# Abstract Syntax Tree (AST) Parser

**Course:** Formal Languages & Finite Automata  
**Author:** Vitalie Vasilean — FAF-241

---

## Theory

A **Parser** is a component of a compiler or interpreter that takes sequential data (such as a stream of tokens produced by a Lexer) and builds a structural representation of the input, verifying that the syntax conforms to a defined formal grammar.

An **Abstract Syntax Tree (AST)** is a tree representation of the abstract syntactic structure of source code. Each node in the tree denotes a construct occurring in the source code. Unlike a parse tree, which contains all syntactic details (like punctuation and delimiters), an AST focuses purely on the structural meaning of the code, making it an ideal intermediate representation for evaluation or compilation.

This project implements a **Recursive Descent Parser** — a top-down parsing technique built from a set of mutually recursive functions where each function implements one of the grammar's production rules.

---

## Objectives

- Understand the theoretical basis of Top-Down Parsing and Abstract Syntax Trees.
- Implement a Lexer capable of tokenizing complex expressions, keywords, and delimiters.
- Build a Recursive Descent Parser that transforms token streams into AST nodes.
- Handle operator precedence by chaining method calls (e.g., logical operators → comparisons → math operators).
- Support control flow structures (`if`/`else`, `while` loops) and function definitions.
- Output the generated AST structure to verify syntactic correctness.

---

## Project Structure

```
ParserASTBuild/
├── ast_nodes.py      # Data classes representing various AST nodes (BinOp, If, While, etc.)
├── lexer.py          # Tokenizer converting raw source code strings into a list of Tokens
├── parser_.py        # Core logic: Recursive descent parser that builds the AST
├── token_type.py     # Enumerations for supported tokens (keywords, operators, etc.)
├── main.py           # Entry point integrating the lexer and parser to print results
└── README.md         # Documentation and report
```

---

## Implementation

### Grammar Model & AST Nodes

The parser translates source code into object-oriented representations defined in `ast_nodes.py`. Nodes range from simple `LiteralNode` and `IdentifierNode` to compound structures like `FunctionDefNode`, `IfNode`, and `WhileNode`.

### Parsing Pipeline and Operator Precedence

The `Parser` class processes tokens linearly. A critical feature is how it enforces the standard order of operations. Rather than parsing all operators inside a single method, the logic is broken into hierarchical methods simulating precedence levels:

#### Precedence Handling Snippet (`parser_.py`)

```python
def expression(self) -> ASTNode:
    """The new entry point for expressions handles logical OR first."""
    return self.logical_or()

def logical_or(self) -> ASTNode:
    node = self.logical_and()
    while self.current_token().type == TokenType.OR:
        op_token = self.current_token()
        self.eat(op_token.type)
        node = BinOpNode(node, op_token.value, self.logical_and())
    return node

def logical_and(self) -> ASTNode:
    node = self.comparison()
    while self.current_token().type == TokenType.AND:
        op_token = self.current_token()
        self.eat(op_token.type)
        node = BinOpNode(node, op_token.value, self.comparison())
    return node

# cascades down to comparison(), math_expression(), term(), and factor()
```

The full precedence chain (lowest → highest) is:

```
logical_or → logical_and → comparison → math_expression → term → factor
```

---

## Results

The parser successfully converts multi-line source strings with varying features into accurately structured trees without raising `ParserError`.

### Input Source Code

```python
# Function definition
def multiply(x, y):
    let result = x * y

# Variable assignments
let a = 10
let b = 5

# Conditionals and logical operators
if a > b and a != 0:
    let max = a
else:
    let max = b

# While loop with comparison
while a > 0:
    a = a - 1

# Function call
let final = multiply(a, b)
```

### Final AST Output

```
AST Nodes:
FunctionDef(multiply, ['x', 'y'], Assign(Identifier(result), BinOp(Identifier(x), *, Identifier(y))))
Assign(Identifier(a), Literal(10))
Assign(Identifier(b), Literal(5))
If(BinOp(BinOp(Identifier(a), >, Identifier(b)), and, BinOp(Identifier(a), !=, Literal(0))),
   Assign(Identifier(max), Identifier(a)),
   Assign(Identifier(max), Identifier(b)))
While(BinOp(Identifier(a), >, Literal(0)), Assign(Identifier(a), BinOp(Identifier(a), -, Literal(1))))
Assign(Identifier(final), FunctionCall(multiply, [Identifier(a), Identifier(b)]))
```

The parsed output confirms that conditions combined with `and`, mathematical expressions inside loops, and if/else branches are all correctly linked to their parent nodes.

---

## Key Takeaways

**Precedence climbing** — Managing standard math and logical operator precedence is solved cleanly by nesting parser functions in reverse precedence order (lowest precedence parsed first).

**Handling complex whitespace** — Processing `NEWLINE` tokens dynamically ensures seamless block transitions, such as safely exiting an `if` branch to parse the subsequent `else` keyword.

---

## References

- Course materials — *Formal Languages & Finite Automata*
- [Abstract Syntax Tree — Wikipedia](https://en.wikipedia.org/wiki/Abstract_syntax_tree)
- [Recursive Descent Parser — Wikipedia](https://en.wikipedia.org/wiki/Recursive_descent_parser)