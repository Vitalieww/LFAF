from parser import parse_regex

if __name__ == "__main__":
    regexes = [
        "(a|b)(c|d)E+G?",
        "p(Q|R|S)T(UV|W|X)*Z+",
        "1(0|1)*2(3|4)*5+6"
    ]

    for pattern in regexes:
        print(f"\nRegex: {pattern}")

        ast = parse_regex(pattern)
        print("AST Processing Sequence:")
        print(ast)

        generated = {ast.generate() for _ in range(5)}
        print(f"Generated examples: {generated}")
