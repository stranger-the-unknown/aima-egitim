#!/usr/bin/env python3
"""Romanya haritasında arama — Bölüm 3. BFS, DFS, UCS, Greedy, A*."""
from __future__ import annotations
import argparse, heapq
from collections import deque
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Tuple

ROMANIA: Dict[str, List[Tuple[str, int]]] = {
    "Arad": [("Zerind", 75), ("Sibiu", 140), ("Timisoara", 118)],
    "Bucharest": [("Fagaras", 211), ("Pitesti", 101), ("Giurgiu", 90), ("Urziceni", 85)],
    "Craiova": [("Dobreta", 120), ("Rimnicu Vilcea", 146), ("Pitesti", 138)],
    "Dobreta": [("Mehadia", 75), ("Craiova", 120)],
    "Eforie": [("Hirsova", 86)],
    "Fagaras": [("Sibiu", 99), ("Bucharest", 211)],
    "Giurgiu": [("Bucharest", 90)],
    "Hirsova": [("Urziceni", 98), ("Eforie", 86)],
    "Iasi": [("Neamt", 87), ("Vaslui", 92)],
    "Lugoj": [("Timisoara", 111), ("Mehadia", 70)],
    "Mehadia": [("Lugoj", 70), ("Dobreta", 75)],
    "Neamt": [("Iasi", 87)],
    "Oradea": [("Zerind", 71), ("Sibiu", 151)],
    "Pitesti": [("Rimnicu Vilcea", 97), ("Craiova", 138), ("Bucharest", 101)],
    "Rimnicu Vilcea": [("Sibiu", 80), ("Craiova", 146), ("Pitesti", 97)],
    "Sibiu": [("Arad", 140), ("Oradea", 151), ("Fagaras", 99), ("Rimnicu Vilcea", 80)],
    "Timisoara": [("Arad", 118), ("Lugoj", 111)],
    "Urziceni": [("Bucharest", 85), ("Hirsova", 98), ("Vaslui", 142)],
    "Vaslui": [("Iasi", 92), ("Urziceni", 142)],
    "Zerind": [("Arad", 75), ("Oradea", 71)],
}
SLD = {"Arad":366,"Bucharest":0,"Craiova":160,"Dobreta":242,"Eforie":161,"Fagaras":176,
       "Giurgiu":77,"Hirsova":151,"Iasi":226,"Lugoj":244,"Mehadia":241,"Neamt":234,
       "Oradea":380,"Pitesti":100,"Rimnicu Vilcea":193,"Sibiu":253,"Timisoara":329,
       "Urziceni":80,"Vaslui":199,"Zerind":374}

@dataclass(order=True)
class N:
    pri: float
    seq: int
    state: str = field(compare=False)
    g: float = field(compare=False)
    parent: Optional["N"] = field(default=None, compare=False)

@dataclass
class R:
    name: str
    path: Optional[List[str]]
    cost: Optional[float]
    expanded: int
    msg: str = ""

def reconstruct(n: N) -> List[str]:
    out = []
    while n:
        out.append(n.state); n = n.parent
    return list(reversed(out))

def neigh(s: str): return ROMANIA.get(s, [])

def bfs(start, goal) -> R:
    if start == goal: return R("BFS", [start], 0.0, 0)
    q = deque([N(0, 0, start, 0.0, None)]); seen = {start}; exp = 0; seq = 1
    while q:
        n = q.popleft(); exp += 1
        for m, c in neigh(n.state):
            if m in seen: continue
            seen.add(m); ch = N(0, seq, m, n.g + c, n); seq += 1
            if m == goal: return R("BFS", reconstruct(ch), ch.g, exp)
            q.append(ch)
    return R("BFS", None, None, exp, "Hedefe ulaşılamadı")

def dfs(start, goal) -> R:
    if start == goal: return R("DFS", [start], 0.0, 0)
    st = [N(0, 0, start, 0.0, None)]; seen = {start}; exp = 0; seq = 1
    while st:
        n = st.pop(); exp += 1
        for m, c in reversed(neigh(n.state)):
            if m in seen: continue
            seen.add(m); ch = N(0, seq, m, n.g + c, n); seq += 1
            if m == goal: return R("DFS", reconstruct(ch), ch.g, exp)
            st.append(ch)
    return R("DFS", None, None, exp, "Hedefe ulaşılamadı")

def ucs(start, goal) -> R:
    seq = 0; pq = [N(0.0, seq, start, 0.0, None)]; seq += 1
    best = {start: 0.0}; exp = 0
    while pq:
        n = heapq.heappop(pq)
        if n.g > best.get(n.state, float("inf")): continue
        exp += 1
        if n.state == goal: return R("UCS", reconstruct(n), n.g, exp)
        for m, c in neigh(n.state):
            ng = n.g + c
            if ng < best.get(m, float("inf")):
                best[m] = ng; heapq.heappush(pq, N(ng, seq, m, ng, n)); seq += 1
    return R("UCS", None, None, exp, "Hedefe ulaşılamadı")

def astar(start, goal, h: Callable[[str], float]) -> R:
    seq = 0; pq = [N(h(start), seq, start, 0.0, None)]; seq += 1
    best = {start: 0.0}; exp = 0
    while pq:
        n = heapq.heappop(pq)
        if n.g > best.get(n.state, float("inf")): continue
        exp += 1
        if n.state == goal: return R("A*", reconstruct(n), n.g, exp)
        for m, c in neigh(n.state):
            ng = n.g + c
            if ng < best.get(m, float("inf")):
                best[m] = ng; heapq.heappush(pq, N(ng + h(m), seq, m, ng, n)); seq += 1
    return R("A*", None, None, exp, "Hedefe ulaşılamadı")

def greedy(start, goal, h: Callable[[str], float]) -> R:
    seq = 0; pq = [N(h(start), seq, start, 0.0, None)]; seq += 1
    seen = set(); exp = 0
    while pq:
        n = heapq.heappop(pq)
        if n.state in seen: continue
        seen.add(n.state); exp += 1
        if n.state == goal: return R("Greedy", reconstruct(n), n.g, exp)
        for m, c in neigh(n.state):
            if m in seen: continue
            heapq.heappush(pq, N(h(m), seq, m, n.g + c, n)); seq += 1
    return R("Greedy", None, None, exp, "Hedefe ulaşılamadı")

def h_factory(goal: str) -> Callable[[str], float]:
    if goal == "Bucharest":
        return lambda s: float(SLD.get(s, 0))
    return lambda _s: 0.0

def show(r: R) -> None:
    print(f"\n--- {r.name} ---")
    if r.path is None:
        print(f"  {r.msg or 'Çözüm yok'}"); print(f"  Genişletilen: {r.expanded}"); return
    print(f"  Yol   : {' -> '.join(r.path)}")
    print(f"  Maliyet (km): {r.cost:.0f}")
    print(f"  Genişletilen düğüm: {r.expanded}")

def main() -> None:
    p = argparse.ArgumentParser(description="Romanya haritasında arama")
    p.add_argument("--baslangic", default="Arad"); p.add_argument("--hedef", default="Bucharest")
    a = p.parse_args()
    if a.baslangic not in ROMANIA or a.hedef not in ROMANIA:
        raise SystemExit("Bilinmeyen şehir")
    print("=" * 60)
    print("ROMANYA HARİTASI — ARAMA KARŞILAŞTIRMASI")
    print(f"Başlangıç: {a.baslangic}  ->  Hedef: {a.hedef}")
    print("Sezgisel: SLD(Bucharest)" if a.hedef == "Bucharest" else "Sezgisel: h=0")
    print("=" * 60)
    h = h_factory(a.hedef)
    results = [bfs(a.baslangic, a.hedef), dfs(a.baslangic, a.hedef),
               ucs(a.baslangic, a.hedef), greedy(a.baslangic, a.hedef, h),
               astar(a.baslangic, a.hedef, h)]
    for r in results: show(r)
    print("\n" + "=" * 60)
    print(f"{'Algoritma':12s} | {'Maliyet':>8s} | {'Genişletilen':>12s} | Kenar")
    print("-" * 60)
    for r in results:
        if r.path is None:
            print(f"{r.name:12s} | {'—':>8s} | {r.expanded:12d} | —")
        else:
            print(f"{r.name:12s} | {r.cost:8.0f} | {r.expanded:12d} | {len(r.path)-1}")
    print("=" * 60)
    print("Not: UCS ve A* (iyi h ile) optimal maliyeti bulur; BFS adım sayısını optimize eder.")

if __name__ == "__main__":
    main()
