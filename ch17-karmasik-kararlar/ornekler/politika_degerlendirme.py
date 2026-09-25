#!/usr/bin/env python3
"""Sabit politika değerlendirme + bir iyileştirme adımı.

Aynı 3×2 gridworld. π₀ = hep doğu; değerlendir; açgözlü iyileştir → π₁.

https://aima.cs.berkeley.edu/ · https://github.com/aimacode
"""
from __future__ import annotations

from typing import Dict, List, Tuple

State = Tuple[int, int]
Action = str

W, H = 3, 2
ACTIONS = ["K", "D", "B", "G"]
DELTA = {"K": (0, 1), "D": (1, 0), "B": (-1, 0), "G": (0, -1)}
LEFT = {"K": "B", "D": "K", "B": "G", "G": "D"}
RIGHT = {"K": "D", "D": "G", "B": "K", "G": "B"}
TERM: Dict[State, float] = {(2, 1): 1.0, (2, 0): -1.0}
STEP = -0.04
GAMMA = 0.9
THETA = 1e-4


def states() -> List[State]:
    return [(x, y) for y in range(H) for x in range(W)]


def clip(x: int, y: int) -> State:
    return max(0, min(W - 1, x)), max(0, min(H - 1, y))


def move(s: State, a: Action) -> State:
    dx, dy = DELTA[a]
    return clip(s[0] + dx, s[1] + dy)


def transitions(s: State, a: Action) -> List[Tuple[float, State]]:
    if s in TERM:
        return [(1.0, s)]
    raw = [(0.8, move(s, a)), (0.1, move(s, LEFT[a])), (0.1, move(s, RIGHT[a]))]
    tot: Dict[State, float] = {}
    for p, sp in raw:
        tot[sp] = tot.get(sp, 0.0) + p
    return [(p, sp) for sp, p in tot.items()]


def reward(s: State, a: Action, sp: State) -> float:
    if s in TERM:
        return 0.0
    if sp in TERM and sp != s:
        return TERM[sp]
    return STEP


def fixed_policy() -> Dict[State, Action]:
    pi = {s: "D" for s in states()}
    for t in TERM:
        pi[t] = "·"
    return pi


def evaluate(pi: Dict[State, Action], max_iter: int = 200) -> Dict[State, float]:
    V = {s: 0.0 for s in states()}
    for s in TERM:
        V[s] = TERM[s]
    for _ in range(max_iter):
        delta = 0.0
        Vn = dict(V)
        for s in states():
            if s in TERM:
                continue
            a = pi[s]
            v = sum(p * (reward(s, a, sp) + GAMMA * V[sp]) for p, sp in transitions(s, a))
            Vn[s] = v
            delta = max(delta, abs(v - V[s]))
        V = Vn
        if delta < THETA:
            break
    return V


def improve(V: Dict[State, float]) -> Dict[State, Action]:
    pi: Dict[State, Action] = {}
    for s in states():
        if s in TERM:
            pi[s] = "·"
            continue
        best_a, best_q = ACTIONS[0], -1e9
        for a in ACTIONS:
            q = sum(p * (reward(s, a, sp) + GAMMA * V[sp]) for p, sp in transitions(s, a))
            if q > best_q:
                best_a, best_q = a, q
        pi[s] = best_a
    return pi


def show_pi(pi: Dict[State, Action], title: str) -> None:
    print(title)
    for y in reversed(range(H)):
        print("  " + " ".join(f"  {pi[(x, y)]}  " for x in range(W)))


def show_v(V: Dict[State, float], title: str) -> None:
    print(title)
    for y in reversed(range(H)):
        print("  " + " ".join(f"{V[(x, y)]:+6.3f}" for x in range(W)))


def main() -> None:
    print("Politika değerlendirme + bir iyileştirme adımı\n")
    pi0 = fixed_policy()
    show_pi(pi0, "π₀ (hep doğu):")
    V0 = evaluate(pi0)
    show_v(V0, "\nV^{π₀}:")
    pi1 = improve(V0)
    show_pi(pi1, "\nπ₁ (bir açgözlü iyileştirme):")
    V1 = evaluate(pi1)
    show_v(V1, "\nV^{π₁}:")
    print(f"\nBaşlangıç (0,0): V0={V0[(0, 0)]:+.3f} → V1={V1[(0, 0)]:+.3f}")
    print("Bitti. Kaynak: aima.cs.berkeley.edu · aimacode")


if __name__ == "__main__":
    main()
