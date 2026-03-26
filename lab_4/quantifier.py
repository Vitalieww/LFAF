import random
from regex_ast import RegexAST


class Quantifier(RegexAST):
    def __init__(self, node, min_rep, max_rep):
        self.node = node
        self.min_rep = min_rep
        self.max_rep = max_rep

    def generate(self):
        reps = random.randint(self.min_rep, self.max_rep)
        return "".join(self.node.generate() for _ in range(reps))

    def __repr__(self):
        return f"Quantifier({self.node}, {self.min_rep}-{self.max_rep})"
