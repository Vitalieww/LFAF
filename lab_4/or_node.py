import random
from regex_ast import RegexAST


class Or(RegexAST):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def generate(self):
        return random.choice([self.left, self.right]).generate()

    def __repr__(self):
        return f"Or({self.left}, {self.right})"
