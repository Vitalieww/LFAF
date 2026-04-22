from typing import Set, Dict, Tuple, Iterable
from collections import defaultdict

class Grammar:
    def __init__(self,
                 Vn: Iterable[str],
                 Vt: Iterable[str],
                 prods: Dict[str, Iterable[Tuple[str, ...]]],
                 start: str):
        self.Vn = set(Vn)
        self.Vt = set(Vt)
        # normalize productions to mapping -> set of tuples
        self.prods = defaultdict(set)
        for A, rhss in prods.items():
            for rhs in rhss:
                # empty rhs represented as empty tuple
                self.prods[A].add(tuple(rhs))
        self.start = start
        self.Vn.update(self.prods.keys())

    def pretty(self) -> str:
        out = []
        for A in sorted(self.prods.keys()):
            for rhs in sorted(self.prods[A]):
                rhs_s = "ε" if rhs == tuple() else "".join(rhs)
                out.append(f"{A} -> {rhs_s}")
        return "\n".join(out)

    def copy(self) -> "Grammar":
        return Grammar(set(self.Vn), set(self.Vt),
                       {A: set(self.prods[A]) for A in self.prods},
                       self.start)