from finite_automaton import FiniteAutomaton
from grammar import Grammar

if __name__ == "__main__":
    # ========================================
    # Define the FA from the variant
    # ========================================
    # δ(q0,a) = q1
    # δ(q1,b) = q1
    # δ(q1,a) = q2
    # δ(q0,a) = q0   <-- same (q0,a) as above, so NDFA
    # δ(q2,c) = q3
    # δ(q3,c) = q3

    states = {"q0", "q1", "q2", "q3"}
    alphabet = {"a", "b", "c"}
    final_states = {"q3"}
    start_state = "q0"
    transitions = {
        ("q0", "a"): ["q0", "q1"],  # non-deterministic: q0 on 'a' goes to both q0 and q1
        ("q1", "b"): ["q1"],
        ("q1", "a"): ["q2"],
        ("q2", "c"): ["q3"],
        ("q3", "c"): ["q3"],
    }

    fa = FiniteAutomaton(states, alphabet, transitions, start_state, final_states)

    # ========================================
    # 1. Check if FA is deterministic
    # ========================================
    print("=" * 50)
    print("1. DETERMINISM CHECK")
    print("=" * 50)
    det = fa.is_deterministic()
    print(f"Is the FA deterministic? {det}")
    if not det:
        print("Reason: δ(q0, a) has multiple destinations: {q0, q1}")

    # ========================================
    # 2. Convert FA to Regular Grammar
    # ========================================
    print("\n" + "=" * 50)
    print("2. FA -> REGULAR GRAMMAR")
    print("=" * 50)
    reg_grammar = fa.to_regular_grammar()
    print("Production rules:")
    reg_grammar.print_rules()

    # ========================================
    # 3. Classify the grammar (Chomsky Hierarchy)
    # ========================================
    print("\n" + "=" * 50)
    print("3. CHOMSKY HIERARCHY CLASSIFICATION")
    print("=" * 50)
    classification = reg_grammar.classify_chomsky()
    print(f"Grammar type: {classification}")

    # Also classify the default grammar from lab 1
    lab1_grammar = Grammar()  # uses default rules
    print(f"\nLab 1 grammar type: {lab1_grammar.classify_chomsky()}")

    # ========================================
    # 4. Convert NDFA to DFA
    # ========================================
    print("\n" + "=" * 50)
    print("4. NDFA -> DFA CONVERSION")
    print("=" * 50)
    dfa = fa.to_dfa()
    print(f"DFA states: {dfa.states}")
    print(f"DFA start state: {dfa.start_state}")
    print(f"DFA final states: {dfa.final_states}")
    print("DFA transitions:")
    for (src, sym), dests in sorted(dfa.transitions.items(), key=lambda x: (str(x[0][0]), x[0][1])):
        print(f"  δ({src}, {sym}) = {dests[0]}")

    print(f"\nIs the converted DFA deterministic? {dfa.is_deterministic()}")

    # ========================================
    # 5. Validate strings with both NDFA and DFA
    # ========================================
    print("\n" + "=" * 50)
    print("5. STRING VALIDATION")
    print("=" * 50)
    test_strings = ["ac", "aac", "abac", "ababac", "abacc", "abc", "c", "aaac", "ababacc"]
    print(f"{'String':<15} {'NDFA':<10} {'DFA':<10}")
    print("-" * 35)
    for s in test_strings:
        ndfa_result = fa.validate(s)
        dfa_result = dfa.validate(s)
        print(f"{s:<15} {str(ndfa_result):<10} {str(dfa_result):<10}")

    # ========================================
    # 6. Draw graphs (optional, requires graphviz)
    # ========================================
    print("\n" + "=" * 50)
    print("6. GRAPHICAL REPRESENTATION")
    print("=" * 50)
    fa.draw_graph("ndfa_graph")
    dfa.draw_graph("dfa_graph")
