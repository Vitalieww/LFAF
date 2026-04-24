# Chomsky Normal Form Converter

**Course:** Formal Languages & Finite Automata  
**Author:** Vitalie Vasilean — FAF-241

---

## Theory

A Context-Free Grammar (CFG) is in **Chomsky Normal Form (CNF)** if all its production rules are of the form:

- `A → BC` — a nonterminal generating exactly two nonterminals
- `A → a` — a nonterminal generating a single terminal
- `S → ε` *(optional)* — the start symbol may generate the empty string, provided `S` does not appear on the right-hand side of any rule

Transforming a grammar into CNF standardizes its structure, which is a prerequisite for many computational linguistics algorithms such as the **CYK parsing algorithm**. The transformation involves several strict phases applied in order: eliminating ε-productions, removing unit productions, discarding useless symbols (inaccessible and non-productive), and finally binarizing long right-hand side productions.

---

## Objectives

- Understand the theoretical basis of Chomsky Normal Form.
- Learn the systematic approaches to grammar normalization.
- Implement a CNF converter that accepts arbitrary context-free grammars.
- Encapsulate the logic in well-structured, object-oriented classes.
- Output intermediate transformation stages to illustrate each step of the pipeline.

---

## Project Structure

```
lab_5/
├── grammar.py          # Data structure representing a Context-Free Grammar
├── cnf_transformer.py  # Core logic: pipeline for CNF normalization steps
├── main.py             # Entry point integrating variant rules and printing stages
└── README.md           # Documentation and report
```

---

## Implementation

### Grammar Model

The `Grammar` class encapsulates the four components of a CFG:

| Field | Description |
|-------|-------------|
| `Vn` | Set of nonterminal symbols |
| `Vt` | Set of terminal symbols |
| `prods` | Production rules (dict of sets) |
| `start` | Start symbol |

Empty strings are automatically normalized to empty tuples, and a `pretty()` helper method handles formatted string output.

### Transformation Pipeline

The `CNFTransformer` class accepts a `Grammar` instance and runs it through a multi-stage pipeline of strictly separated passes:

1. `remove_epsilon()` — eliminates all ε-productions
2. `remove_unit()` — removes unit productions (`A → B`)
3. `remove_inaccessible()` — drops symbols unreachable from the start symbol
4. `remove_nonproductive()` — removes symbols that cannot derive any terminal string
5. `convert_to_cnf()` — binarizes long rules and wraps bare terminals in helper variables

#### `convert_to_cnf` — Final Structural Adjustment

```python
def convert_to_cnf(self, G: Grammar) -> Grammar:
    prods = G.prods
    term_map = {}
    finalP = defaultdict(set)

    def get_term_var(t: str):
        if t in term_map: return term_map[t]
        tv = f"T_{t}"
        term_map[t] = tv
        G.Vn.add(tv)
        return tv

    for A, rhss in prods.items():
        for rhs in rhss:
            symbols = list(rhs)
            if len(symbols) > 1:
                for i, s in enumerate(symbols):
                    if s in G.Vt:
                        symbols[i] = get_term_var(s)

            if len(symbols) <= 2:
                finalP[A].add(tuple(symbols))
            else:
                cur = A
                for i in range(len(symbols) - 2):
                    left = symbols[i]
                    nxt = self.fresh("X")
                    G.Vn.add(nxt)
                    finalP[cur].add((left, nxt))
                    cur = nxt
                finalP[cur].add((symbols[-2], symbols[-1]))

    for t, var in term_map.items():
        finalP[var].add((t,))

    return Grammar(G.Vn, G.Vt, finalP, G.start)
```

---

## Results

For **Variant 26**, the transformer prints the grammar at each intermediate stage, making it easy to audit exactly how each pass modifies the rule set.

### Stage-by-Stage Output

**Original grammar:**
```
A -> AbBA
A -> d
A -> dS
A -> ε
B -> A
B -> a
B -> aS
...
```

**After eliminating ε-productions:**
```
A -> AbB
A -> bB
...
```

**After removing unit productions:**
```
B -> AbB
B -> bB
B -> a
...
```

**Final CNF grammar:**
```
A  -> A X_1
A  -> T_d S
B  -> A X_3
B  -> T_a S
S  -> A B
T_a -> a
T_b -> b
X_1 -> T_b X_2
X_2 -> B A
...
```

The resulting grammar preserves the language of the original CFG while strictly adhering to CNF constraints — every rule is either `N → NN` or `N → t`.

---

## Key Takeaways

**Pipeline architecture** — Breaking the CNF conversion into disjoint passes dramatically simplifies both the mental model and the debugging process. Each pass has a single, well-defined responsibility.

**Immutability patterns** — Operating on deep copies of the grammar at each stage isolates state changes, enabling straightforward auditing of intermediate results and preventing subtle cross-stage bugs.

---

## References

- Course materials — *Formal Languages & Finite Automata*
- [Chomsky Normal Form — Wikipedia](https://en.wikipedia.org/wiki/Chomsky_normal_form)
- [Python `collections.defaultdict` documentation](https://docs.python.org/3/library/collections.html#collections.defaultdict)