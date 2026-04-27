from abc import ABC


class ASTNode(ABC):
    pass


class LiteralNode(ASTNode):
    def __init__(self, value, token_type):
        self.value = value
        self.token_type = token_type

    def __repr__(self):
        return f"Literal({self.value})"

class BinOpNode(ASTNode):
    def __init__(self, left: ASTNode, op: str, right: ASTNode):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"BinOp({self.left}, {self.op}, {self.right})"

class IdentifierNode(ASTNode):
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"Identifier({self.name})"

class AssignNode(ASTNode):
    def __init__(self, target: IdentifierNode, value: ASTNode):
        self.target = target
        self.value = value

    def __repr__(self):
        return f"Assign({self.target}, {self.value})"

class FunctionCallNode(ASTNode):
    def __init__(self, name: str, arguments: list):
        self.name = name
        self.arguments = arguments

    def __repr__(self):
        return f"FunctionCall({self.name}, {self.arguments})"

class BlockNode(ASTNode):
    def __init__(self, statements: list):
        self.statements = statements

    def __repr__(self):
        return f"Block({self.statements})"

class IfNode(ASTNode):
    def __init__(self, condition: ASTNode, true_branch: ASTNode, false_branch: ASTNode = None):
        self.condition = condition
        self.true_branch = true_branch
        self.false_branch = false_branch

    def __repr__(self):
        return f"If({self.condition}, {self.true_branch}, {self.false_branch})"

class WhileNode(ASTNode):
    def __init__(self, condition: ASTNode, body: ASTNode):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"While({self.condition}, {self.body})"

class FunctionDefNode(ASTNode):
    def __init__(self, name: str, params: list, body: ASTNode):
        self.name = name
        self.params = params
        self.body = body

    def __repr__(self):
        return f"FunctionDef({self.name}, {self.params}, {self.body})"