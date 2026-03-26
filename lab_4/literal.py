from regex_ast import RegexAST


class Literal(RegexAST):
    def __init__(self, char):
        self.char = char

    def generate(self):
        return self.char

    def __repr__(self):
        return f"Literal('{self.char}')"
