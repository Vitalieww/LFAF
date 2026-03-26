from literal import Literal
from concat import Concat
from or_node import Or
from quantifier import Quantifier

def parse_regex(regex_str):
    def parse_expr(chars):
        nodes = []
        while chars:
            c = chars[0]
            if c == '(':
                chars.pop(0)
                nodes.append(parse_expr(chars))
            elif c == ')':
                chars.pop(0)
                break
            elif c == '|':
                chars.pop(0)
                right = parse_expr(chars)
                left = nodes.pop() if nodes else Literal('')
                nodes.append(Or(left, right))
                break
            elif c in '*+?':
                chars.pop(0)
                target = nodes.pop()
                if c == '*': nodes.append(Quantifier(target, 0, 5))
                elif c == '+': nodes.append(Quantifier(target, 1, 5))
                elif c == '?': nodes.append(Quantifier(target, 0, 1))
            else:
                chars.pop(0)
                nodes.append(Literal(c))

        if not nodes:
            return Literal('')

        result = nodes[0]
        for node in nodes[1:]:
            if isinstance(node, Or) and not isinstance(result, Or):
                result = Concat(result, node)
            else:
                result = Concat(result, node)

        return result

    chars = list(regex_str.replace(' ', ''))
    return parse_expr(chars)
