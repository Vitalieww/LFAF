from typing import List, Tuple, Dict, Set
from collections import defaultdict, deque
from grammar import Grammar

class CNFTransformer:
    def __init__(self, G: Grammar):
        self.G = G.copy()
        self.next_var_index = 1

    def _is_nonterminal(self, sym: str) -> bool:
        return sym in self.G.Vn

    def remove_epsilon(self) -> Grammar:
        P = self.G.prods
        nullable: Set[str] = set()
        changed = True
        while changed:
            changed = False
            for A, rhss in P.items():
                if A in nullable:
                    continue
                for rhs in rhss:
                    if rhs == tuple():
                        nullable.add(A)
                        changed = True
                        break
                    if all(self._is_nonterminal(s) and s in nullable for s in rhs):
                        nullable.add(A)
                        changed = True
                        break

        new_prods = defaultdict(set)
        for A, rhss in P.items():
            for rhs in rhss:
                if rhs == tuple():
                    continue
                positions = [i for i, s in enumerate(rhs) if self._is_nonterminal(s) and s in nullable]
                from itertools import combinations
                for r in range(len(positions) + 1):
                    for comb in combinations(positions, r):
                        rem = set(comb)
                        new_rhs = tuple(rhs[i] for i in range(len(rhs)) if i not in rem)
                        # Ensure no empty tuples make it into the new productions
                        if new_rhs != tuple():
                            new_prods[A].add(new_rhs)

        start = self.G.start
        return Grammar(self.G.Vn, self.G.Vt, new_prods, start)

    def remove_unit(self, G: Grammar) -> Grammar:
        P = G.prods
        units = defaultdict(set)
        for A in P.keys():
            q = deque([A])
            visited = {A}
            while q:
                X = q.popleft()
                for rhs in P.get(X, set()):
                    if len(rhs) == 1 and rhs[0] in G.Vn:
                        B = rhs[0]
                        if B not in visited:
                            visited.add(B)
                            q.append(B)
            units[A] = visited

        newP = defaultdict(set)
        for A in P.keys():
            for B in units[A]:
                for rhs in P.get(B, set()):
                    if not (len(rhs) == 1 and rhs[0] in G.Vn):
                        newP[A].add(rhs)
        return Grammar(G.Vn, G.Vt, newP, G.start)

    def remove_inaccessible(self, G: Grammar) -> Grammar:
        reachable = set([G.start])
        changed = True
        while changed:
            changed = False
            for A in list(reachable):
                for rhs in G.prods.get(A, set()):
                    for s in rhs:
                        if s in G.Vn and s not in reachable:
                            reachable.add(s)
                            changed = True
        newP = defaultdict(set)
        for A in reachable:
            for rhs in G.prods.get(A, set()):
                if all((s not in G.Vn) or (s in reachable) for s in rhs):
                    newP[A].add(rhs)
        return Grammar(reachable, G.Vt, newP, G.start)

    def remove_nonproductive(self, G: Grammar) -> Grammar:
        productive: Set[str] = set()
        changed = True
        while changed:
            changed = False
            for A, rhss in G.prods.items():
                if A in productive:
                    continue
                for rhs in rhss:
                    if all((s in G.Vt) or (s in productive) for s in rhs):
                        productive.add(A)
                        changed = True
                        break
        newP = defaultdict(set)
        for A in productive:
            for rhs in G.prods[A]:
                if all((s in G.Vt) or (s in productive) for s in rhs):
                    newP[A].add(rhs)
        return Grammar(productive, G.Vt, newP, G.start)

    def convert_to_cnf(self, G: Grammar) -> Grammar:
        prods = G.prods
        term_map: Dict[str, str] = {}
        finalP = defaultdict(set)

        def fresh(prefix="X"):
            v = f"{prefix}_{self.next_var_index}"
            self.next_var_index += 1
            return v

        # ensure term var unique and recorded in Vn
        def get_term_var(t: str):
            if t in term_map:
                return term_map[t]
            tv = f"T_{t}"
            # avoid collision with existing names
            while tv in G.Vn or tv in term_map.values():
                tv = f"T_{t}_{self.next_var_index}"
                self.next_var_index += 1
            term_map[t] = tv
            G.Vn.add(tv)
            return tv

        for A, rhss in prods.items():
            for rhs in rhss:
                if rhs == tuple():
                    finalP[A].add(rhs)
                    continue
                symbols = list(rhs)
                # replace terminals in long RHS
                if len(symbols) > 1:
                    for i, s in enumerate(symbols):
                        if s in G.Vt:
                            symbols[i] = get_term_var(s)
                # now split into binaries if needed
                if len(symbols) == 1:
                    finalP[A].add((symbols[0],))
                elif len(symbols) == 2:
                    finalP[A].add((symbols[0], symbols[1]))
                else:
                    # A -> s0 X1
                    cur = A
                    for i in range(len(symbols) - 2):
                        left = symbols[i]
                        nxt = fresh("X")
                        G.Vn.add(nxt)
                        finalP[cur].add((left, nxt))
                        cur = nxt
                    finalP[cur].add((symbols[-2], symbols[-1]))

        # add terminal productions for each terminal helper variable
        for t, var in term_map.items():
            finalP[var].add((t,))

        return Grammar(G.Vn, G.Vt, finalP, G.start)

    def transform(self) -> List[Tuple[str, Grammar]]:
        stages = []
        g0 = self.G.copy()
        stages.append(("Original", g0))
        g1 = self.remove_epsilon()
        stages.append(("After eliminating epsilon-productions", g1))
        g2 = self.remove_unit(g1)
        stages.append(("After removing unit productions", g2))
        g3 = self.remove_inaccessible(g2)
        stages.append(("After removing inaccessible symbols", g3))
        g4 = self.remove_nonproductive(g3)
        stages.append(("After removing non-productive symbols", g4))
        g5 = self.convert_to_cnf(g4)
        stages.append(("Final CNF-like grammar", g5))
        return stages
