class FiniteAutomaton:
    def __init__(self):
        self.initial_state = 'S'
        self.final_states = {'X'}  # This is the 'exit' state

        # This is the map #variant 26
        self.transitions = {
            ('S', 'd'): 'A',
            ('A', 'a'): 'B',
            ('A', 'b'): 'X',
            ('B', 'b'): 'C',
            ('B', 'd'): 'X',
            ('C', 'c'): 'B',
            ('C', 'a'): 'A'
        }

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