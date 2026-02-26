# Grammar and Finite Automaton Implementation — Lab 2

### Course: Formal Languages & Finite Automata  
### Author: Vitalie Vasilean FAF-241

----

## Theory

A finite automaton models computation as a set of states and transitions driven by input symbols. Deterministic finite automata (DFA) have exactly one next state for each pair (state, symbol), while non-deterministic finite automata (NDFA or NFA) may have multiple possible next states. The subset-construction algorithm converts an NFA into an equivalent DFA by treating sets of NFA states as single DFA states.

Regular grammars (right- or left-linear) generate exactly the class of regular languages recognized by finite automata. Mapping between automata and grammars is straightforward: states map to non-terminals, transitions labeled by terminals become productions, and terminal-only productions map to transitions to a designated accepting state.

## Objectives

1. Work with the given variant FA and determine if it is deterministic.
2. Convert the finite automaton to a regular grammar.
3. Classify the resulting grammar according to the Chomsky hierarchy.
4. Implement NDFA \-> DFA conversion (subset construction), produce a readable renaming for composite states and preserve accepting conditions.
5. (Optional) Provide graphical representation of both NDFA and DFA.

## Problem instance (summary)

- States: q0, q1, q2, q3  
- Alphabet: a, b, c  
- Start state: q0  
- Accepting state(s): q3  
- Key transitions: q0 on `a` goes to both q0 and q1 (this makes the automaton non-deterministic); q1 has a loop on `b`, q1 on `a` goes to q2, q2 on `c` goes to q3, q3 loops on `c`.

## Implementation description

The project implements two main classes: `Grammar` and `FiniteAutomaton`.

- `FiniteAutomaton` responsibilities:
  - Store states, alphabet, transitions (as a mapping of (state, symbol) -> list of destinations), start and final states.
  - `validate(input_string)`: simulate the FA. For NFA this keeps a set of current states and advances them per symbol.
  - `is_deterministic()`: checks whether any (state, symbol) pair maps to multiple destinations.
  - `to_regular_grammar()`: converts transitions into productions; terminal-only moves become productions to a special terminal-only non-terminal representing acceptance.
  - `to_dfa()`: subset construction that:
    - Represents DFA states as frozensets of NFA states.
    - Builds transitions by unioning destinations for each symbol.
    - Identifies DFA accepting states as any composite containing an original accepting state.
    - Renames composite sets into readable names such as `{q0,q1}`.
    - Optionally omits explicit trap state, or adds it if fuller deterministic transition tables are required.
  - `draw_graph(filename)`: optional Graphviz export that groups labels for readability.

- `Grammar` responsibilities:
  - Hold non-terminals, terminals, productions and start symbol.
  - `classify_chomsky()`: check productions to determine Type 3 / Type 2 / Type 1 / Type 0.
  - `to_finite_automaton()`: inverse mapping that creates a finite automaton from a right-linear grammar (introduces a final sink state for terminal-only productions).
  - `generate_string()`: simple random production walker used for lightweight testing.

Implementation choices and simplifications:
- Transitions are stored as lists on each key to naturally represent nondeterminism.
- When converting NFA \-> DFA, composite states are renamed with braces for human readability.
- Epsilon (\ε) productions are detected by the grammar classifier but are not used in the provided variant.
- The code intentionally avoids external dependencies except Graphviz for optional drawing.

## Example execution summary

- Determinism: The FA is non-deterministic because δ(q0, `a`) = {q0, q1}.
- Grammar conversion: Each FA transition `A -a-> B` becomes `A -> aB`; if `B` is accepting, also add `A -> a`.
- Grammar classification: The produced grammar is Type 3 (regular), since all productions follow `A -> a` or `A -> aB` form.
- NDFA \-> DFA: Subset construction produced composite states (for example `{q0}`, `{q1}`, `{q0,q1}`, etc.). Accepting DFA states are those containing `q3`. Composite-state renaming was added to keep printouts readable.
- Validation tests: The NFA and the produced DFA were exercised on a set of test strings; results matched after conversion (both accept exactly the same language).

## Personal experience, difficulties, and lessons learned

Working on this lab reinforced the connection between theoretical definitions and concrete data structures. The most immediate friction point was choosing a representation that naturally handles nondeterminism while remaining easy to manipulate for the subset construction. Using tuples/frozensets for composite DFA states and lists for NFA destinations simplified transitions and queue processing.

A repeated source of bugs was bookkeeping during the subset-construction: forgetting to mark visited composite states or mishandling empty next-state sets led to incorrect transition tables or missing DFA states. Renaming composite states for readability also introduced off-by-one or ordering errors when generating deterministic transition dictionaries; addressing this improved confidence in test outputs.

Mapping automata to grammars highlighted subtle details: when a transition leads to an accepting state, a production that yields only a terminal must be added. Initially I missed adding those terminal-only productions and observed mismatches between grammar-generated strings and automaton-accepted strings. Writing small unit tests that compare a few generated strings against FA validation fixed this quickly.

The optional Graphviz drawing was helpful for verifying structure visually. Installation friction (Graphviz system binary vs Python package) made it useful to keep the drawing functionality optional and to print clear instructions when the library was missing.

Overall, the lab taught practical steps for:
- Implementing subset construction robustly (queue, visited set, deterministic transitions),
- Keeping the grammar/automaton mappings symmetrical,
- Designing simple tests that exercise the conversion boundaries (terminal-only productions, loops and self-transitions, and composite accepting states).

## Conclusions / Results

- The given FA is non-deterministic. The subset-construction algorithm was implemented to produce an equivalent DFA.
- The regular grammar produced from the FA is Type 3 according to the Chomsky hierarchy.
- Validation by testing several strings showed the NDFA and the converted DFA accept the same language (modulo presence/absence of an explicit trap state).
- The implementation choices (transition representation, composite-state renaming) simplified debugging and produced readable outputs for evaluation.

## References

1. Hopcroft, J. E., Motwani, R., & Ullman, J. D. (2006). Introduction to Automata Theory, Languages, and Computation. Pearson.  
2. Sipser, M. (2012). Introduction to the Theory of Computation. Cengage Learning.

----