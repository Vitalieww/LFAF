import random
from finite_automaton import FiniteAutomaton

class Grammar:
    def __init__(self):
        # VN: Non-terminals, VT: Terminals, P: Productions, S: Start symbol
        self.non_terminals = {'S', 'A', 'B', 'C'}
        self.terminals = {'a', 'b', 'c', 'd'}
        self.start_symbol = 'S'
        self.rules = {
            'S': ['dA'],
            'A': ['aB', 'b'],
            'B': ['bC', 'd'],
            'C': ['cB', 'aA']
        }

    def generate_string(self):
        word = ""
        current_symbol = self.start_symbol

        while current_symbol in self.non_terminals:
            # Pick a random rule for the current symbol
            # For example, if current is 'A', it picks 'aB' or 'b'
            production = random.choice(self.rules[current_symbol])

            for char in production:
                if char in self.terminals:
                    word += char
                if char in self.non_terminals:
                    current_symbol = char
                    break
            else:
                # If the rule didn't have a non-terminal (like 'b' or 'd'), we are done
                current_symbol = None
        return word

    def to_finite_automaton(self):
        # Convert Grammar to Finite Automaton
        # Every Non-Terminal becomes a state.
        # We add 'X' as our special 'exit' state.
        states = self.non_terminals | {'X'}
        alphabet = self.terminals
        initial_state = self.start_symbol
        final_states = {'X'}
        transitions = {}

        for head, productions in self.rules.items():
            for p in productions:
                char = p[0]  # The terminal letter (a, b, c, or d)

                # If rule is like 'aB', next state is B.
                if len(p) > 1:
                    next_state = p[1]
                # If rule is like 'b', next state is our final state 'X'
                else:
                    next_state = 'X'

                transitions[(head, char)] = next_state

        return FiniteAutomaton(states, alphabet, transitions, initial_state, final_states)