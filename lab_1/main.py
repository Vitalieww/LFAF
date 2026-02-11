from finite_automaton import FiniteAutomaton
from grammar import Grammar

if __name__ == "__main__":
    # Create the grammar object
    my_grammar = Grammar()

    # 1. Generate 5 valid strings
    print("--- 5 RANDOM VALID STRINGS ---")
    generated_list = []
    for _ in range(5):
        s = my_grammar.generate_string()
        generated_list.append(s)
        print(f"Generated: {s}")

    # 2. Convert grammar to Finite Automaton
    my_fa = my_grammar.to_finite_automaton()

    # 3. Check if the FA likes the strings we just generated
    print("\n--- VALIDATION ---")
    for s in generated_list:
        is_valid = my_fa.validate(s)
        print(f"String '{s}': Valid? {is_valid}")

    # 4. Check an obviously wrong string
    wrong_string = "abc"
    print(f"String '{wrong_string}': Valid? {my_fa.validate(wrong_string)}")