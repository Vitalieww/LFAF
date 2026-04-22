# python
from grammar import Grammar
from cnf_transformer import CNFTransformer

def build_variant_26() -> Grammar:
    Vn = {"S", "A", "B", "D"}
    Vt = {"a", "b", "d"}
    start = "S"
    prods = {
        "S": {("a","B","A"), ("A","B")},
        "A": {("d",), ("d","S"), ("A","b","B","A"), tuple()},
        "B": {("a",), ("a","S"), ("A",)},
        "D": {("A","b","a")},
    }
    return Grammar(Vn, Vt, prods, start)

if __name__ == "__main__":
    G = build_variant_26()
    transformer = CNFTransformer(G)
    stages = transformer.transform()
    for label, g in stages:
        print(label + ":")
        print(g.pretty())
        print()