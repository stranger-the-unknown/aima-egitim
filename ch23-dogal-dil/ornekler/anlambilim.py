#!/usr/bin/env python3
"""Artırılmış dilbilgileri ve anlamsal yorum (kitaptaki 23.4).

* Bileşimsel anlambilim: Bir öbeğin anlamı, alt öbeklerinin anlamlarının bir fonksiyonudur.
  Kitaptaki aritmetik dilbilgisi: Exp(op(x, y)) → Exp(x) Operator(op) Exp(y); Exp(x) → ( Exp(x) );
  Exp(x) → Number(x); Number(x) → Digit(x); Number(10x + y) → Number(x) Digit(y).
  "3 + (4 ÷ 2)" ağacının kökü Exp(5).
* İngilizcenin küçük bir parçası için birinci derece mantık: "Ali loves Bo" → Loves(Ali, Bo).
  "loves Bo" → λx Loves(x, Bo); S(pred(obj)) → NP(obj) VP(pred).

Çalıştırma:
    python anlambilim.py
"""
from __future__ import annotations

import operator
from fractions import Fraction

ISLEMLER = {"+": operator.add, "-": operator.sub, "×": operator.mul, "÷": lambda a, b: Fraction(a, b)}
ONCELIK = {"+": 1, "-": 1, "×": 2, "÷": 2}


def sozcukle(metin: str) -> list[str]:
    return [c for c in metin.replace(" ", "")]


class Ayristirici:
    """Özyinelemeli iniş; her kural anlamını alt öbeklerin anlamından kurar ve ağacı da döndürür."""

    def __init__(self, metin: str):
        self.t, self.i = sozcukle(metin), 0

    def bak(self):
        return self.t[self.i] if self.i < len(self.t) else None

    def exp(self, en_az: int = 1):
        sol_anlam, sol_agac = self.birincil()
        while self.bak() in ONCELIK and ONCELIK[self.bak()] >= en_az:
            op = self.t[self.i]
            self.i += 1
            sag_anlam, sag_agac = self.exp(ONCELIK[op] + 1)
            sol_anlam = ISLEMLER[op](sol_anlam, sag_anlam)
            sol_agac = f"Exp({sol_anlam}) [{sol_agac} Operator({op}) {sag_agac}]"
        return sol_anlam, sol_agac

    def birincil(self):
        if self.bak() == "(":
            self.i += 1
            anlam, ic = self.exp()
            assert self.bak() == ")", "kapanış parantezi bekleniyordu"
            self.i += 1
            return anlam, f"Exp({anlam}) [( {ic} )]"
        sayi = 0
        basla = self.i
        while self.bak() is not None and self.bak().isdigit():
            sayi = 10 * sayi + int(self.t[self.i])                 # Number(10x + y) → Number(x) Digit(y)
            self.i += 1
        assert self.i > basla, f"sayı bekleniyordu: {self.bak()}"
        return sayi, f"Exp({sayi}) [Number({sayi})]"


def yorumla(metin: str):
    a = Ayristirici(metin)
    anlam, agac = a.exp()
    assert a.i == len(a.t), "fazla simge"
    return anlam, agac


# --- λ-hesabıyla İngilizce parçası ------------------------------------------------------------
SOZLUK = {
    "ali": ("NP", "Ali"), "bo": ("NP", "Bo"), "wumpus": ("NP", "Wumpus"),
    "loves": ("Verb", lambda nesne: (lambda ozne: f"Loves({ozne}, {nesne})")),
    "sees": ("Verb", lambda nesne: (lambda ozne: f"Sees({ozne}, {nesne})")),
    "stinks": ("IVerb", lambda ozne: f"Stinks({ozne})"),
}


def cumle_anlami(cumle: str) -> str:
    """S(pred(obj)) → NP(obj) VP(pred);  VP(pred(obj)) → Verb(pred) NP(obj);  VP(pred) → IVerb(pred)."""
    s = cumle.lower().split()
    kat, ozne = SOZLUK[s[0]]
    assert kat == "NP"
    if len(s) == 2:
        _, yuklem = SOZLUK[s[1]]                                 # tek yerli fiil
    else:
        _, fiil = SOZLUK[s[1]]
        _, nesne = SOZLUK[s[2]]
        yuklem = fiil(nesne)                                     # "loves Bo" → λx Loves(x, Bo)
    return yuklem(ozne)


def main() -> None:
    print("=== Aritmetik ifadeler: bileşimsel anlambilim ===")
    for ifade in ("3 + (4 ÷ 2)", "3 + 4 × 2", "(3 + 4) × 2", "12 - 2 - 3", "10 ÷ 4"):
        anlam, agac = yorumla(ifade)
        print(f"  {ifade:<12} → {anlam}")
    print(f"  3 + (4 ÷ 2) ağacı: {yorumla('3 + (4 ÷ 2)')[1]}")

    print("\n=== λ-hesabıyla cümle anlamı ===")
    for c in ("Ali loves Bo", "Bo sees wumpus", "wumpus stinks"):
        print(f"  {c:<15} → {cumle_anlami(c)}")


if __name__ == "__main__":
    main()
