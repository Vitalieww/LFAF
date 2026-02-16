# Grammar and Finite Automaton Implementation

### Course: Formal Languages & Finite Automata
### Author: Vitalie Vasilean FAF-241

----

## Theory

A **formal grammar**, as I've come to understand it through this lab, is like a set of rules for building valid sentences in a language. It starts with a basic concept (the start symbol) and uses production rules to substitute abstract parts (non-terminals) with either other abstract parts or concrete words (terminals) until a complete, valid string is formed. A **finite automaton**, on the other hand, acts as a validator. It reads a string character by character, moving from one state to another based on what it reads. If it finishes in an "accepting" state, the string is valid. The most fascinating part for me was seeing how these two different ideas—one for generating strings and one for checking them—can perfectly describe the same set of regular languages.

## Objectives

The primary goal of this lab was to turn the theoretical concepts of grammars and automata into working code. I aimed to build a `Grammar` class capable of generating random but valid strings based on its production rules. Alongside this, I needed to implement a `FiniteAutomaton` class that could take a string and determine its validity. The core of the project was to create a conversion function that could automatically transform the grammar into its equivalent automaton, thereby proving their functional equivalence. The final step was to test this entire system by generating strings with the grammar and verifying them with the automaton created from it.

## Implementation description

I began by creating the **`Grammar` class**, which holds the non-terminals, terminals, production rules, and the start symbol. The most challenging part was the `generate_string` method. My implementation iteratively builds a string. It starts with the grammar's start symbol and, in a loop, randomly chooses a production rule for the current non-terminal. It appends any terminal characters from the rule to the output string and updates the current non-terminal if one is present. The process stops when a production rule without a non-terminal is chosen, completing the string.

```python
import random

def generate_string(self):
    word = ""
    current_symbol = self.start_symbol

    while current_symbol in self.non_terminals:
        production = random.choice(self.rules[current_symbol])

        for char in production:
            if char in self.terminals:
                word += char
            if char in self.non_terminals:
                current_symbol = char
                break
        else:
            current_symbol = None
    return word
```

Next, I implemented the **`FiniteAutomaton` class**. Its main logic is in the `validate` method, which simulates the machine's operation. It keeps track of the `current_state`, starting with the initial state. For each character in the input string, it looks for a matching transition. If a valid transition is found, it moves to the next state; otherwise, the string is invalid, and the method returns `False` immediately. If the entire string is processed, the method returns `True` only if the final state is one of the designated accepting states.

```python
def validate(self, input_string):
    current_state = self.initial_state

    for char in input_string:
        if (current_state, char) in self.transitions:
            current_state = self.transitions[(current_state, char)]
        else:
            return False

    return current_state in self.final_states
```

The **conversion from grammar to automaton** was the most insightful part of the implementation. I learned that each non-terminal in the grammar maps directly to a state in the automaton. I introduced a special state, `X`, to serve as the single final (accepting) state. Each production rule becomes a transition. For a rule like `A -> aB`, a transition is created from state `A` on input `a` to state `B`. For a rule that terminates, like `A -> b`, the transition goes from state `A` on input `b` to the final state `X`. This direct mapping made the conversion logic elegant and clear.

```python
from finite_automaton import FiniteAutomaton

def to_finite_automaton(self):
    states = self.non_terminals | {'X'}
    alphabet = self.terminals
    initial_state = self.start_symbol
    final_states = {'X'}
    transitions = {}

    for head, productions in self.rules.items():
        for p in productions:
            char = p[0]
            next_state = p[1] if len(p) > 1 else 'X'
            transitions[(head, char)] = next_state

    return FiniteAutomaton(states, alphabet, transitions, initial_state, final_states)
```

## Personal Experience, Difficulties, and Lessons Learned

This lab was a fantastic exercise in bridging theory and practice. Before this, grammars and automata were abstract concepts from lectures. Implementing them forced me to confront the details and edge cases.

A key difficulty was ensuring the string generation would always terminate. My grammar's rules could potentially lead to infinite loops (e.g., `C -> aA` and `A -> aB -> ... -> cB -> cA`). I addressed this by designing the grammar such that every non-terminal had at least one path to a terminal-only production. A more robust solution for a general-purpose tool would be to add a depth limit to the generation to prevent infinite recursion.

Another challenge arose during testing. Initially, my automaton was rejecting some valid strings. After some debugging, I found a subtle bug in my `to_finite_automaton` logic where I was incorrectly identifying the next state from the production rule. This experience taught me the value of writing small, focused tests for each component before integrating them. It's much easier to find a bug in a single function than in the entire system.

Through this process, I learned that the theoretical equivalence between regular grammars and finite automata has a concrete, algorithmic basis. I also gained practical experience using Python dictionaries to represent abstract structures like transition functions. The most valuable lesson was seeing how a simple, deterministic algorithm in the `validate` method can perform the complex task of language recognition. It demystified the concept for me.

## Conclusions / Results

The final implementation works as expected. The program successfully generates random strings from the grammar, converts that grammar into a finite automaton, and then uses the automaton to validate the generated strings. The output confirms that all generated strings are accepted, while manually crafted invalid strings are correctly rejected.

Example output:
```
--- 5 RANDOM VALID STRINGS ---
Generated: dab
Generated: dabd
Generated: dabaabcbabd
Generated: dababd
Generated: dabcbabcbcbd

--- VALIDATION ---
String 'dab': Valid? True
String 'dabd': Valid? True
String 'dabaabcbabd': Valid? True
String 'dababd': True
String 'dabcbabcbcbd': Valid? True
String 'abc': Valid? False
```

The results clearly show the grammar's structure in action—for instance, every valid string starts with 'd', as dictated by the initial production `S -> dA`. This project solidified my understanding of regular languages and gave me practical skills in implementing and testing formal language concepts. The hands-on experience of debugging the conversion process was particularly valuable and taught me more than reading a textbook alone ever could.

## References

1. Hopcroft, J. E., Motwani, R., & Ullman, J. D. (2006). *Introduction to Automata Theory, Languages, and Computation*. Pearson.
2. Sipser, M. (2012). *Introduction to the Theory of Computation*. Cengage Learning.