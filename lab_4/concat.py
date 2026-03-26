from regex_ast import RegexAST


class Concat(RegexAST):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def generate(self):
        return self.left.generate() + self.right.generate()

    def __repr__(self):
        return f"Concat({self.left}, {self.right})"
