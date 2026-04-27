from typing import List, Optional
from token_ import Token
from token_type import TokenType
from ast_nodes import ASTNode, LiteralNode, BinOpNode, IdentifierNode, AssignNode
from parser_error import ParserError


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def current_token(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1]

    def eat(self, token_type: TokenType) -> Token:
        token = self.current_token()
        if token.type == token_type:
            self.pos += 1
            return token
        raise ParserError(
            f"Expected {token_type.name}, got {token.type.name}",
            token.line,
            token.column
        )

    def parse(self) -> List[ASTNode]:
        statements = []
        while self.current_token().type != TokenType.EOF:
            if self.current_token().type == TokenType.NEWLINE:
                self.eat(TokenType.NEWLINE)
                continue

            statements.append(self.statement())

        return statements

    def statement(self) -> ASTNode:
        token = self.current_token()

        if token.type == TokenType.KEYWORD:
            if token.value == 'if':
                return self.if_statement()
            elif token.value == 'while':
                return self.while_statement()
            elif token.value == 'def':
                return self.function_def_statement()

        return self.assignment_statement()

    def while_statement(self) -> ASTNode:
        self.eat(TokenType.KEYWORD)  # Eat 'while'

        condition = self.expression()
        self.eat(TokenType.COLON)

        if self.current_token().type == TokenType.NEWLINE:
            self.eat(TokenType.NEWLINE)

        body = self.statement()

        from ast_nodes import WhileNode
        return WhileNode(condition, body)

    def function_def_statement(self) -> ASTNode:
        self.eat(TokenType.KEYWORD)  # Eat 'def'

        name_token = self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.LPAREN)

        params = []
        if self.current_token().type != TokenType.RPAREN:
            params.append(self.eat(TokenType.IDENTIFIER).value)
            while self.current_token().type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                params.append(self.eat(TokenType.IDENTIFIER).value)

        self.eat(TokenType.RPAREN)
        self.eat(TokenType.COLON)

        if self.current_token().type == TokenType.NEWLINE:
            self.eat(TokenType.NEWLINE)

        body = self.statement()

        from ast_nodes import FunctionDefNode
        return FunctionDefNode(name_token.value, params, body)

    def if_statement(self) -> ASTNode:
        self.eat(TokenType.KEYWORD)  # Eat 'if'

        # Parse the condition expression
        condition = self.expression()

        # Expect a colon
        self.eat(TokenType.COLON)

        # Parse the body (for simplicity, a single statement)
        if self.current_token().type == TokenType.NEWLINE:
            self.eat(TokenType.NEWLINE)
        true_branch = self.statement()

        # OVERCOME THE ERROR: Eat possible newline after the true branch
        if self.current_token().type == TokenType.NEWLINE:
            self.eat(TokenType.NEWLINE)

        false_branch = None
        # Check for 'else'
        token = self.current_token()
        if token.type == TokenType.KEYWORD and token.value == 'else':
            self.eat(TokenType.KEYWORD)
            self.eat(TokenType.COLON)
            if self.current_token().type == TokenType.NEWLINE:
                self.eat(TokenType.NEWLINE)
            false_branch = self.statement()

        from ast_nodes import IfNode
        return IfNode(condition, true_branch, false_branch)

    def assignment_statement(self) -> ASTNode:
        # Existing assignment logic
        if self.current_token().type in (TokenType.KEYWORD, TokenType.IDENTIFIER):
            if self.current_token().value in ('let', 'var', 'const'):
                self.eat(TokenType.KEYWORD)

            if self.current_token().type == TokenType.IDENTIFIER:
                # Need to look ahead to see if it's an assignment or just an expression
                # (Assuming standard let x = 5 format for this step)
                ident_token = self.current_token()
                self.eat(TokenType.IDENTIFIER)
                if self.current_token().type == TokenType.ASSIGN:
                    self.eat(TokenType.ASSIGN)
                    expr = self.expression()
                    return AssignNode(IdentifierNode(ident_token.value), expr)
                else:
                    self.pos -= 1  # Backtrack if not assignment

        return self.expression()

    def expression(self) -> ASTNode:
        """The new entry point for expressions handles logical OR first."""
        return self.logical_or()

    def logical_or(self) -> ASTNode:
        node = self.logical_and()
        while self.current_token().type == TokenType.OR:
            op_token = self.current_token()
            self.eat(op_token.type)
            node = BinOpNode(node, op_token.value, self.logical_and())
        return node

    def logical_and(self) -> ASTNode:
        node = self.comparison()
        while self.current_token().type == TokenType.AND:
            op_token = self.current_token()
            self.eat(op_token.type)
            node = BinOpNode(node, op_token.value, self.comparison())
        return node

    def comparison(self) -> ASTNode:
        node = self.math_expression()
        ops = (
            TokenType.EQUAL, TokenType.NOT_EQUAL,
            TokenType.LESS_THAN, TokenType.GREATER_THAN,
            TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL
        )
        while self.current_token().type in ops:
            op_token = self.current_token()
            self.eat(op_token.type)
            node = BinOpNode(node, op_token.value, self.math_expression())
        return node

    def math_expression(self) -> ASTNode:
        """This replaces the old expression() method."""
        node = self.term()
        while self.current_token().type in (TokenType.PLUS, TokenType.MINUS):
            op_token = self.current_token()
            self.eat(op_token.type)
            node = BinOpNode(node, op_token.value, self.term())
        return node

    def term(self) -> ASTNode:
        node = self.factor()
        while self.current_token().type in (TokenType.MULTIPLY, TokenType.DIVIDE):
            op_token = self.current_token()
            self.eat(op_token.type)
            node = BinOpNode(node, op_token.value, self.factor())
        return node

    def factor(self) -> ASTNode:
        token = self.current_token()

        # Check for numeric or string literals
        if token.type in (TokenType.INTEGER, TokenType.FLOAT, TokenType.STRING, TokenType.BOOLEAN):
            self.eat(token.type)
            return LiteralNode(token.value, token.type)

        # Handle identifiers and function calls
        elif token.type in (TokenType.IDENTIFIER, TokenType.SIN, TokenType.COS, TokenType.TAN):
            func_or_ident_token = self.eat(token.type)

            # If the next token is a parenthesis, it's a function call
            if self.current_token().type == TokenType.LPAREN:
                self.eat(TokenType.LPAREN)
                args = []
                if self.current_token().type != TokenType.RPAREN:
                    args.append(self.expression())
                    while self.current_token().type == TokenType.COMMA:
                        self.eat(TokenType.COMMA)
                        args.append(self.expression())
                self.eat(TokenType.RPAREN)
                # Need to import FunctionCallNode at the top of parser_.py
                from ast_nodes import FunctionCallNode
                return FunctionCallNode(func_or_ident_token.value, args)

            return IdentifierNode(func_or_ident_token.value)

        # Handle parentheses for groupings
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expression()
            self.eat(TokenType.RPAREN)
            return node

        raise ParserError(f"Unexpected token {token.value}", token.line, token.column)

