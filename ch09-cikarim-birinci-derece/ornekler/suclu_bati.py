#!/usr/bin/env python3
"""Kitaptaki suç bilgi tabanı: Albay West suçlu mu?

"Yasaya göre, bir Amerikalının düşman ülkelere silah satması suçtur. Amerika'nın
düşmanı olan Nono ülkesinin bazı füzeleri vardır ve bu füzelerin hepsini ona
Amerikalı olan Albay West satmıştır."

Kesin tümceler (kitaptaki 9.3–9.10):
    American(x) ∧ Weapon(y) ∧ Sells(x, y, z) ∧ Hostile(z) ⇒ Criminal(x)
    Owns(Nono, M1)        Missile(M1)           ← ∃x Owns(Nono,x) ∧ Missile(x), M1 yeni sabit
    Missile(x) ∧ Owns(Nono, x) ⇒ Sells(West, x, Nono)
    Missile(x) ⇒ Weapon(x)
    Enemy(x, America) ⇒ Hostile(x)
    American(West)        Enemy(Nono, America)

Kitaptaki ileri zincirleme: iki tur yeter.
    1. tur: Sells(West, M1, Nono), Weapon(M1), Hostile(Nono)
    2. tur: Criminal(West)

Çalıştırma:
    python suclu_bati.py
"""
from __future__ import annotations

from fol_cikarim import geri_zincirleme, ileri_zincirleme, tamamla, terim, yaz


def k(oncul: list[str], sonuc: str):
    return ([terim(o) for o in oncul], terim(sonuc))


KURALLAR = [
    k(["American(x)", "Weapon(y)", "Sells(x, y, z)", "Hostile(z)"], "Criminal(x)"),
    k(["Missile(x)", "Owns(Nono, x)"], "Sells(West, x, Nono)"),
    k(["Missile(x)"], "Weapon(x)"),
    k(["Enemy(x, America)"], "Hostile(x)"),
]
OLGULAR = [terim(f) for f in ["Owns(Nono, M1)", "Missile(M1)", "American(West)", "Enemy(Nono, America)"]]


def main() -> None:
    print("=== İleri zincirleme (FOL-FC-ASK) ===")
    teta, turlar = ileri_zincirleme(KURALLAR, OLGULAR, terim("Criminal(x)"))
    for i, yeni in enumerate(turlar, 1):
        print(f"  {i}. tur: {', '.join(yaz(f) for f in yeni)}")
    print(f"  Sorgu Criminal(x) → x = {yaz(tamamla(teta)['x'])}  ({len(turlar)} tur; kitap: 2)")

    print("\n=== Geri zincirleme (FOL-BC-ASK) — kanıt ağacı ===")
    iz: list[str] = []
    cevap = next(geri_zincirleme(KURALLAR, OLGULAR, terim("Criminal(x)"), iz=iz))
    for satir in iz:
        print("  " + satir)
    print(f"  İlk yanıt: x = {yaz(tamamla(cevap)['x'])}")
    print("\nBu bilgi tabanı bir Datalog KB'sidir: fonksiyon sembolü yok. Bu yüzden ileri"
          "\nzincirleme sonlu sayıda turda tüm sonuçları türetir ve durur.")


if __name__ == "__main__":
    main()
