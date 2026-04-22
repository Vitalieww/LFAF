from typing import List, Tuple, Dict, Set
from collections import defaultdict, deque
from itertools import combinations
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
        # find nullable nonterminals
        changed = True
        while changed:
            changed = False
            for A, rhss in P.items():
                if A in nullable:
                    continue
                for rhs in rhss:
                    if rhs == tuple():
                        nullable.add(A); changed = True; break
                    # rhs nullable if all symbols are nonterminals and nullable
                    if all(self._is_nonterminal(s) and s in nullable for s in rhs):
                        nullable.add(A); changed = True; break

        new_prods = defaultdict(set)
        for A, rhss in P.items():
            for rhs in rhss:
                if rhs == tuple():
                    continue
                positions = [i for i, s in enumerate(rhs) if self._is_nonterminal(s) and s in nullable]
                # create combinations of removing nullable nonterminals
                for r in range(len(positions) + 1):
                    for comb in combinations(positions, r):
                        rem = set(comb)
                        new_rhs = tuple(rhs[i] for i in range(len(rhs)) if i not in rem)
                        new_prods[A].add(new_rhs)
        # handle start nullable: create new start S0 if needed
        start = self.G.start
        if start in nullable:
            S0 = start + "_0"
            self.G.Vn.add(S0)
            new_prods[S0].add((start,))
            new_prods[S0].add(tuple())
            start = S0
        # remove explicit epsilons except possibly new start
        for A in list(new_prods.keys()):
            if A != start and tuple() in new_prods[A]:
                new_prods[A].remove(tuple())

        return Grammar(self.G.Vn, self.G.Vt, new_prods, start)

    def remove_unit(self, G: Grammar) -> Grammar:
        P = G.prods
        units = defaultdict(set)
        for A in P.keys():
            # find all B where A -*> B via unit productions
            q = deque([A])
            visited = {A}
            while q:
                X = q.popleft()
                for rhs in P.get(X, set()):
                    if len(rhs) == 1 and rhs[0] in G.Vn:
                        B = rhs[0]
                        if B not in visited:
                            visited.add(B); q.append(B)
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
                            reachable.add(s); changed = True
        newP = defaultdict(set)
        for A in reachable:
            for rhs in G.prods.get(A, set()):
                # keep production only if all nonterminals in rhs are reachable
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
                        productive.add(A); changed = True; break
        newP = defaultdict(set)
        for A in productive:
            for rhs in G.prods[A]:
                if all((s in G.Vt) or (s in productive) for s in rhs):
                    newP[A].add(rhs)
        return Grammar(productive, G.Vt, newP, G.start)

    def convert_to_cnf(self, G: Grammar) -> Grammar:
        prods = G.prods
        term_map: Dict[str, str] = {}
        newP = defaultdict(set)
        # helper to create fresh vars
        def fresh(prefix="X"):
            v = f"{prefix}_{self.next_var_index}"
            self.next_var_index += 1
            G.Vn.add(v)
            return v

        # map terminals in mixed rhs to vars
        for A, rhss in prods.items():
            for rhs in rhss:
                if rhs == tuple():
                    newP[A].add(rhs)
                    continue
                rhs_list = list(rhs)
                # replace terminals by T_<t> if length>1
                if len(rhs_list) > 1:
                    for i, s in enumerate(rhs_list):
                        if s in G.Vt:
                            if s not in term_map:
                                tv = f"T_{s}"
                                term_map[s] = tv
                                G.Vn.add(tv)
                                newP[tv].add((s,))
                            rhs_list[i] = term_map[s]
                # now break to binaries
                if len(rhs_list) <= 2:
                    newP[A].add(tuple(rhs_list))
                else:
                    left = rhs_list[0]
                    for i in range(1, len(rhs_list)-1):
                        nxt = fresh()
                        newP[left].add((left, nxt)) if False else None  # noop to keep readable
                        # build chain: for first step create A -> left nxt, then chain nxt -> rhs[i] nxt2 ...
                        if i == 1:
                            newP[A].add((left, nxt))
                        else:
                            newP[prev].add((left, nxt))
                        prev = nxt
                        left = rhs_list[i]
                    # last chain variable points to last two symbols
                    newP[prev].add((rhs_list[-2], rhs_list[-1])) if 'prev' in locals() else None
                    # cleanup: simpler, regenerate chain correctly
                    # simpler reliable implementation below
        # The above attempted chain-building is verbose; implement clear splitting:
        finalP = defaultdict(set)
        for A, rhss in prods.items():
            for rhs in rhss:
                if rhs == tuple():
                    finalP[A].add(rhs); continue
                symbols = list(rhs)
                # replace terminals when necessary
                if len(symbols) > 1:
                    for i, s in enumerate(symbols):
                        if s in G.Vt:
                            if s not in term_map:
                                tv = f"T_{s}"
                                term_map[s] = tv
                                G.Vn.add(tv)
                            symbols[i] = term_map[s]
                # now split into binaries
                if len(symbols) == 1:
                    finalP[A].add((symbols[0],))
                else:
                    cur = A
                    for i in range(len(symbols)-2):
                        nxt = fresh()
                        finalP[cur].add((symbols[i], nxt))
                        cur = nxt
                    finalP[cur].add((symbols[-2], symbols[-1]))
        # add terminal rules
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