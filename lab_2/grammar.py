class Grammar:
    def __init__(self, non_terminals=None, terminals=None, rules=None, start=None):
        if non_terminals is None:
            # Default grammar from lab 1 variant
            self.non_terminals = {'S', 'A', 'B', 'C'}
            self.terminals = {'a', 'b', 'c'}
            self.start = 'S'
            self.rules = {
                'S': ['aA'],
                'A': ['bA', 'aB'],
                'B': ['bB', 'aC', 'c'],
                'C': ['cC', 'c'],
            }
        else:
            self.non_terminals = set(non_terminals)
            self.terminals = set(terminals)
            self.rules = dict(rules)
            self.start = start

    def generate_string(self):
        import random
        current = self.start
        result = ""
        while True:
            if current not in self.rules:
                break
            production = random.choice(self.rules[current])
            for ch in production:
                if ch in self.terminals:
                    result += ch
                elif ch in self.non_terminals:
                    current = ch
                    break
            else:
                # No non-terminal found in production, we're done
                break
        return result

    def to_finite_automaton(self):
        from finite_automaton import FiniteAutomaton

        states = set(self.non_terminals) | {'X'}
        alphabet = set(self.terminals)
        start_state = self.start
        final_states = {'X'}
        transitions = {}

        for lhs, productions in self.rules.items():
            for prod in productions:
                if len(prod) == 2 and prod[0] in self.terminals and prod[1] in self.non_terminals:
                    key = (lhs, prod[0])
                    if key not in transitions:
                        transitions[key] = []
                    transitions[key].append(prod[1])
                elif len(prod) == 1 and prod[0] in self.terminals:
                    key = (lhs, prod[0])
                    if key not in transitions:
                        transitions[key] = []
                    transitions[key].append('X')

        return FiniteAutomaton(states, alphabet, transitions, start_state, final_states)

    def classify_chomsky(self):
        is_type3_right = True
        is_type3_left = True
        is_type2 = True
        is_type1 = True
        has_epsilon = False

        for lhs, productions in self.rules.items():
            # Type 2 and Type 3 require a single non-terminal on the left side
            if len(lhs) != 1 or lhs not in self.non_terminals:
                is_type2 = False
                is_type3_right = False
                is_type3_left = False

            for prod in productions:
                # Check for epsilon productions
                if prod == '' or prod == 'ε':
                    has_epsilon = True
                    # Type 1 doesn't allow epsilon (except S -> ε if S not on RHS)
                    if lhs != self.start:
                        is_type1 = False
                    continue

                # Type 1: |lhs| <= |rhs|
                if len(lhs) > len(prod):
                    is_type1 = False

                # Type 3 right-linear: A -> a or A -> aB
                if is_type3_right:
                    if len(prod) == 1:
                        if prod[0] not in self.terminals:
                            is_type3_right = False
                    elif len(prod) == 2:
                        if prod[0] not in self.terminals or prod[1] not in self.non_terminals:
                            is_type3_right = False
                    else:
                        is_type3_right = False

                # Type 3 left-linear: A -> a or A -> Ba
                if is_type3_left:
                    if len(prod) == 1:
                        if prod[0] not in self.terminals:
                            is_type3_left = False
                    elif len(prod) == 2:
                        if prod[0] not in self.non_terminals or prod[1] not in self.terminals:
                            is_type3_left = False
                    else:
                        is_type3_left = False

        if is_type3_right or is_type3_left:
            return "Type 3 (Regular Grammar)"
        elif is_type2:
            return "Type 2 (Context-Free Grammar)"
        elif is_type1:
            return "Type 1 (Context-Sensitive Grammar)"
        else:
            return "Type 0 (Unrestricted Grammar)"

    def print_rules(self):
        for lhs, productions in self.rules.items():
            for prod in productions:
                print(f"  {lhs} -> {prod}")
