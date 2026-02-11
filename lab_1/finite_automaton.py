class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, initial_state, final_states):
        self.states = states  # States
        self.alphabet = alphabet  # Alphabet
        self.transitions = transitions  # Transitions: {(state, char): next_state}
        self.initial_state = initial_state  # Initial state
        self.final_states = final_states  # Final states

    def validate(self, input_string):
        current_state = self.initial_state

        for char in input_string:
            # Check if there is a valid move from here
            if (current_state, char) in self.transitions:
                current_state = self.transitions[(current_state, char)]
            else:
                # If we get a character we didn't expect, return False
                return False

        # If we finish the string, are we in the 'exit' state?
        return current_state in self.final_states