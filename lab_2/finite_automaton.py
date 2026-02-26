class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, start_state, final_states):
        self.states = set(states)
        self.alphabet = set(alphabet)
        # transitions: dict of (state, symbol) -> list of states
        self.transitions = {}
        for key, dests in transitions.items():
            if isinstance(dests, list):
                self.transitions[key] = list(dests)
            else:
                self.transitions[key] = [dests]
        self.start_state = start_state
        self.final_states = set(final_states)

    def validate(self, input_string):
        current_states = {self.start_state}

        for symbol in input_string:
            next_states = set()
            for state in current_states:
                key = (state, symbol)
                if key in self.transitions:
                    next_states.update(self.transitions[key])
            if not next_states:
                return False
            current_states = next_states

        return bool(current_states & self.final_states)

    def is_deterministic(self):
        # Check if any (state, symbol) pair has more than one destination
        seen_keys = {}
        for (state, symbol), dests in self.transitions.items():
            if len(dests) > 1:
                return False
            # Also check if same (state, symbol) appears multiple times
            key = (state, symbol)
            if key in seen_keys:
                return False
            seen_keys[key] = True
        return True

    def to_regular_grammar(self):
        from grammar import Grammar

        rules = {}
        for state in self.states:
            rules[state] = []

        for (src, symbol), destinations in self.transitions.items():
            for dest in destinations:
                # A -> aB
                rules[src].append(symbol + dest)
                # If dest is a final state, also add A -> a
                if dest in self.final_states:
                    rules[src].append(symbol)

        # Remove states with no productions (except if they appear on RHS)
        non_terminals = set(self.states)
        terminals = set(self.alphabet)

        return Grammar(
            non_terminals=non_terminals,
            terminals=terminals,
            rules=rules,
            start=self.start_state
        )

    def to_dfa(self):
        if self.is_deterministic():
            print("FA is already deterministic.")
            return self

        dfa_start = frozenset([self.start_state])
        dfa_states = set()
        dfa_transitions = {}
        queue = [dfa_start]
        visited = set()

        while queue:
            current = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)
            dfa_states.add(current)

            for symbol in sorted(self.alphabet):
                next_states = set()
                for state in current:
                    key = (state, symbol)
                    if key in self.transitions:
                        next_states.update(self.transitions[key])

                if next_states:
                    next_frozen = frozenset(next_states)
                    dfa_transitions[(current, symbol)] = [next_frozen]
                    if next_frozen not in visited:
                        queue.append(next_frozen)
                # If next_states is empty, we could add a dead/trap state
                # For simplicity, we just don't add a transition

        # Determine final states: any composite state containing an original final state
        dfa_final = set()
        for state_set in dfa_states:
            if state_set & self.final_states:
                dfa_final.add(state_set)

        # Rename composite states for readability
        state_list = sorted(dfa_states, key=lambda s: sorted(s))
        state_mapping = {}
        for i, state_set in enumerate(state_list):
            name = "{" + ",".join(sorted(state_set)) + "}"
            state_mapping[state_set] = name

        new_states = set(state_mapping.values())
        new_start = state_mapping[dfa_start]
        new_final = {state_mapping[s] for s in dfa_final}
        new_transitions = {}
        for (src, symbol), dests in dfa_transitions.items():
            new_transitions[(state_mapping[src], symbol)] = [state_mapping[dests[0]]]

        return FiniteAutomaton(
            states=new_states,
            alphabet=self.alphabet,
            transitions=new_transitions,
            start_state=new_start,
            final_states=new_final
        )

    def draw_graph(self, filename="fa_graph"):
        try:
            from graphviz import Digraph
        except ImportError:
            print("graphviz not installed. Run: pip install graphviz")
            print("Also install Graphviz system package: https://graphviz.org/download/")
            return

        dot = Digraph(comment="Finite Automaton")
        dot.attr(rankdir='LR', size='10')

        # Invisible start arrow
        dot.node("__start__", shape="none", label="")
        dot.edge("__start__", str(self.start_state))

        for state in self.states:
            state_str = str(state)
            if state in self.final_states:
                dot.node(state_str, shape="doublecircle")
            else:
                dot.node(state_str, shape="circle")

        # Group transitions with same src->dest to show multiple labels
        edge_labels = {}
        for (src, symbol), dests in self.transitions.items():
            for dest in dests:
                key = (str(src), str(dest))
                if key not in edge_labels:
                    edge_labels[key] = []
                edge_labels[key].append(symbol)

        for (src, dest), symbols in edge_labels.items():
            label = ",".join(sorted(symbols))
            dot.edge(src, dest, label=label)

        dot.render(filename, format="png", cleanup=True)
        print(f"Graph saved to {filename}.png")
