#!/usr/bin/env python3
"""Alıştırma 7 çözümü: Eş ilişkisi ile yeğen, enişte ve yenge.

    ∀x,y Yeğen(x, y)  ⇔ ∃k Kardeş(k, y) ∧ Ebeveyn(k, x)
    ∀x,y Enişte(x, y) ⇔ Erkek(x) ∧ ∃w Eş(x, w) ∧ (Hala(w, y) ∨ Teyze(w, y) ∨ (Kardeş(w, y) ∧ Kadın(w)))
    ∀x,y Yenge(x, y)  ⇔ Kadın(x) ∧ ∃h Eş(x, h) ∧ (Amca(h, y) ∨ Dayı(h, y) ∨ (Kardeş(h, y) ∧ Erkek(h)))
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ornekler"))

from akrabalik_turkce import (ERKEK, KADIN, KISILER, amca, dayi, ebeveyn,  # noqa: E402
                              hala, kardes, teyze)

# Evlilikler (simetrik)
_ES = {("Ahmet", "Elif"), ("Zeynep", "Ali"), ("Hasan", "Fatma")}
ES = _ES | {(b, a) for a, b in _ES}


def es(x, y) -> bool:
    return (x, y) in ES


def yegen(x, y) -> bool:
    return any(kardes(k, y) and ebeveyn(k, x) for k in KISILER)


def eniste(x, y) -> bool:
    return x in ERKEK and any(
        es(x, w) and (hala(w, y) or teyze(w, y) or (kardes(w, y) and w in KADIN)) for w in KISILER)


def yenge(x, y) -> bool:
    return x in KADIN and any(
        es(x, h) and (amca(h, y) or dayi(h, y) or (kardes(h, y) and h in ERKEK)) for h in KISILER)


def main() -> None:
    print("Evlilikler: " + ", ".join(f"Eş({a}, {b})" for a, b in sorted(_ES)))
    for ad, f in (("Yeğen", yegen), ("Enişte", eniste), ("Yenge", yenge)):
        ciftler = [(x, y) for x in KISILER for y in KISILER if f(x, y)]
        print(f"\n{ad}:")
        for x, y in ciftler:
            print(f"  {ad}({x}, {y})")
    print("\nNot: Ali, Zeynep'in eşidir. Zeynep; Deniz ve Can'ın halası, Ahmet ve Mehmet'in kız kardeşidir."
          "\nBu yüzden Ali dördünün de eniştesi olur. Türkçede 'enişte' hem halanın/teyzenin"
          "\nkocasını hem de kız kardeşin kocasını kapsar.")


if __name__ == "__main__":
    main()
