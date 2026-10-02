#!/usr/bin/env python3
"""Küçük Bayes ağı: enumeration ile P(sorgu | kanıt).

Senaryo (özgün): Ofis yangın alarmı
  Yangin, SigaraDumanı → Alarm → MudurArar

Exact çıkarım: tüm gizli atamaları dolaş, joint çarp, normalleştir.
Resmi referans: https://aima.cs.berkeley.edu/ · https://github.com/aimacode
"""
from __future__ import annotations

from itertools import product
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

Var = str
Assignment = Dict[Var, bool]

# --- Ağ tanımı ---
ORDER: List[Var] = ["Yangin", "SigaraDumanı", "Alarm", "MudurArar"]

# P(X=True | parents) — parents sırası sabit
CPT = {
    "Yangin": {(): 0.01},
    "SigaraDumanı": {(): 0.05},
    "Alarm": {
        (True, True): 0.95,    # Yangin, Sigara
        (True, False): 0.88,
        (False, True): 0.70,
        (False, False): 0.001,
    },
    "MudurArar": {
        (True,): 0.80,   # Alarm
        (False,): 0.05,
    },
}

PARENTS: Dict[Var, Tuple[Var, ...]] = {
    "Yangin": (),
    "SigaraDumanı": (),
    "Alarm": ("Yangin", "SigaraDumanı"),
    "MudurArar": ("Alarm",),
}


def p_true_given_parents(var: Var, asg: Assignment) -> float:
    key = tuple(asg[p] for p in PARENTS[var])
    return CPT[var][key]


def factor(var: Var, asg: Assignment) -> float:
    """P(var=asg[var] | parents) tek faktör."""
    pt = p_true_given_parents(var, asg)
    return pt if asg[var] else 1.0 - pt


def joint(asg: Assignment) -> float:
    return 1.0 * __import__("functools").reduce(
        lambda a, b: a * b, (factor(v, asg) for v in ORDER), 1.0
    )


def enumerate_ask(query: Var, evidence: Assignment) -> Dict[bool, float]:
    """P(query | evidence) — enumeration (küçük ağ)."""
    hidden = [v for v in ORDER if v != query and v not in evidence]
    weights = {True: 0.0, False: 0.0}

    for qval in (True, False):
        total = 0.0
        for hid_vals in product([False, True], repeat=len(hidden)):
            asg: Assignment = dict(evidence)
            asg[query] = qval
            for v, val in zip(hidden, hid_vals):
                asg[v] = val
            total += joint(asg)
        weights[qval] = total

    z = weights[True] + weights[False]
    if z == 0:
        raise ZeroDivisionError("kanıt olasılığı sıfır")
    return {True: weights[True] / z, False: weights[False] / z}


def fmt_bool(b: bool) -> str:
    return "T" if b else "F"


def yazdir_dag() -> None:
    print("Ağ yapısı:")
    print("  Yangin ──┐")
    print("           ├─→ Alarm ─→ MudurArar")
    print("  SigaraDumanı ─┘")
    print()


def main() -> None:
    print("Bayes ağı — enumeration demosu (özgün eğitim)\n")
    yazdir_dag()

    # Önce P(Yangin) kontrol (önsel)
    p_y = enumerate_ask("Yangin", {})
    print(f"P(Yangin=T) = {p_y[True]:.4f}  (önsel, kanıt yok)")
    print()

    senaryolar = [
        ("Mudür aradı — yangın olasılığı?", "Yangin", {"MudurArar": True}),
        ("Alarm çaldı — yangın?", "Yangin", {"Alarm": True}),
        ("Alarm + müdür aradı — yangın?", "Yangin", {"Alarm": True, "MudurArar": True}),
        ("Alarm çaldı — sigara?", "SigaraDumanı", {"Alarm": True}),
        ("Alarm çaldı, yangın yok — sigara?", "SigaraDumanı", {"Alarm": True, "Yangin": False}),
        ("Alarm çaldı, yangın var — sigara?", "SigaraDumanı", {"Alarm": True, "Yangin": True}),
        ("Hiçbir şey yokken müdür arar mı?", "MudurArar", {}),
    ]

    for baslik, query, evidence in senaryolar:
        dist = enumerate_ask(query, evidence)
        ev_str = ", ".join(f"{k}={fmt_bool(v)}" for k, v in evidence.items()) or "∅"
        print(f"• {baslik}")
        print(f"  Kanıt: {{{ev_str}}}")
        print(f"  P({query}=T | e) = {dist[True]:.4f}")
        print(f"  P({query}=F | e) = {dist[False]:.4f}")
        print()

    print("Nedenler arası akıl yürütme: Alarm çaldığında yangın ve sigara birbiriyle yarışan iki açıklamadır.")
    print("Yangının OLDUĞUNU öğrenmek sigara olasılığını düşürür ('açıklayıp götürme', explaining away);")
    print("yangının OLMADIĞINI öğrenmek ise sigarayı neredeyse tek açıklama yapar.")


if __name__ == "__main__":
    main()
