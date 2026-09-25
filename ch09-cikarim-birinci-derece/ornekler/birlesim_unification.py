#!/usr/bin/env python3
"""Eğitim amaçlı birleştirme (unification) — sabit, değişken, f(x) terimleri.

MGU üretir; occurs-check vardır. Tam FOL motoru değildir.
Resmi referans: https://aima.cs.berkeley.edu/ · https://github.com/aimacode
"""
from __future__ import annotations

from typing import Dict, List, Optional, Tuple, Union

# Terim: str (sabit veya ?degisken) | (functor, [arg,...])
Term = Union[str, Tuple[str, List["Term"]]]
Subst = Dict[str, Term]


def degisken_mi(t: Term) -> bool:
    return isinstance(t, str) and t.startswith("?")


def sabit_mi(t: Term) -> bool:
    return isinstance(t, str) and not degisken_mi(t)


def compound_mi(t: Term) -> bool:
    return isinstance(t, tuple)


def yaz(t: Term) -> str:
    if isinstance(t, str):
        return t
    ad, args = t
    return f"{ad}({', '.join(yaz(a) for a in args)})"


def occurs(var: str, t: Term, theta: Subst) -> bool:
    t = gercek(t, theta)
    if t == var:
        return True
    if compound_mi(t):
        return any(occurs(var, a, theta) for a in t[1])
    return False


def gercek(t: Term, theta: Subst) -> Term:
    if degisken_mi(t):
        assert isinstance(t, str)
        if t in theta:
            return gercek(theta[t], theta)
        return t
    if compound_mi(t):
        ad, args = t
        return (ad, [gercek(a, theta) for a in args])
    return t


def unify(x: Term, y: Term, theta: Optional[Subst] = None) -> Optional[Subst]:
    """x ve y'yi birleştir. Başarısızsa None, başarıda birleştirici sözlük."""
    if theta is None:
        theta = {}
    x = gercek(x, theta)
    y = gercek(y, theta)

    if x == y:
        return theta

    if degisken_mi(x):
        assert isinstance(x, str)
        return _var_bind(x, y, theta)
    if degisken_mi(y):
        assert isinstance(y, str)
        return _var_bind(y, x, theta)

    if compound_mi(x) and compound_mi(y):
        if x[0] != y[0] or len(x[1]) != len(y[1]):
            return None
        for a, b in zip(x[1], y[1]):
            theta = unify(a, b, theta)
            if theta is None:
                return None
        return theta

    return None  # farklı sabitler veya karışık uyumsuzluk


def _var_bind(var: str, t: Term, theta: Subst) -> Optional[Subst]:
    if occurs(var, t, theta):
        return None  # occurs-check
    yeni = dict(theta)
    yeni[var] = t
    return yeni


def subst_yaz(theta: Optional[Subst]) -> str:
    if theta is None:
        return "BAŞARISIZ"
    if not theta:
        return "{ } (boş birleştirici)"
    parcalar = [f"{k}/{yaz(v)}" for k, v in sorted(theta.items())]
    return "{ " + ", ".join(parcalar) + " }"


def demo() -> None:
    print("=== Birleştirme (unify) demosu ===\n")

    vakalar: List[Tuple[str, Term, Term]] = [
        ("Aynı sabitler", "Ankara", "Ankara"),
        ("Farklı sabitler", "Ankara", "Izmir"),
        ("Değişken ↔ sabit", "?x", "Ankara"),
        ("İki değişken", "?x", "?y"),
        ("f(x) ↔ f(A)", ("f", ["?x"]), ("f", ["Ankara"])),
        ("f(x) ↔ f(y)", ("f", ["?x"]), ("f", ["?y"])),
        ("f(x) ↔ g(x)", ("f", ["?x"]), ("g", ["?x"])),
        ("Occurs-check: x ↔ f(x)", "?x", ("f", ["?x"])),
        (
            "İç içe: p(f(x), x) ↔ p(f(A), A) — atom değil terim çifti olarak argümanlar",
            ("p", [("f", ["?x"]), "?x"]),
            ("p", [("f", ["Ankara"]), "Ankara"]),
        ),
        (
            "Çelişki: p(f(x), x) ↔ p(f(A), B)",
            ("p", [("f", ["?x"]), "?x"]),
            ("p", [("f", ["Ankara"]), "Bursa"]),
        ),
    ]

    for baslik, a, b in vakalar:
        sonuc = unify(a, b)
        print(f"• {baslik}")
        print(f"    unify({yaz(a)}, {yaz(b)}) → {subst_yaz(sonuc)}")
        print()

    print("Not: Eğitim birleştiricisi; karmaşık term indeksleri / occurs optimizasyonu yok.")


if __name__ == "__main__":
    demo()
