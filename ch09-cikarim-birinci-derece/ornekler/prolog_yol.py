#!/usr/bin/env python3
"""Mantık programlamanın bir tuzağı: kural sırası ve sonsuz döngü.

Bir graf ve iki tanım (Prolog gösterimiyle):

    (a) yol(X, Z) :- bag(X, Z).                     (b) yol(X, Z) :- yol(X, Y), bag(Y, Z).
        yol(X, Z) :- yol(X, Y), bag(Y, Z).              yol(X, Z) :- bag(X, Z).

Mantıksal olarak ikisi aynıdır (aynı modeller). Ama Prolog'un derinlik öncelikli
geri zincirlemesi (b)'de `yol(X, Y)` alt hedefini hemen yeniden açar ve sonsuza
kadar iner. İleri zincirleme ise iki durumda da sonlu sayıda adımda durur.

Kitaptaki çözüm önerileri: kural sırasına dikkat etmek, ileri zincirleme ya da
**tablolama** (daha önce sorulmuş alt hedefleri hatırlamak).

Çalıştırma:
    python prolog_yol.py
"""
from __future__ import annotations

from fol_cikarim import geri_zincirleme, ileri_zincirleme, tamamla, terim, yaz

BAGLAR = [("A", "B"), ("B", "C"), ("C", "D"), ("A", "E")]
OLGULAR = [terim(f"bag({a}, {b})") for a, b in BAGLAR]
TABAN = ([terim("bag(x, z)")], terim("yol(x, z)"))
OZYINELI = ([terim("yol(x, y)"), terim("bag(y, z)")], terim("yol(x, z)"))


def geri_dene(kurallar, sorgu: str, sinir: int) -> tuple[list[str], int]:
    """Derinlik sınırlı geri zincirleme. Döner: (ilk yanıtlar, İLK yanıttan önce açılan alt hedef)."""
    iz: list[str] = []
    yanitlar = []
    ilk_yanita_kadar = None
    for teta in geri_zincirleme(kurallar, OLGULAR, terim(sorgu), iz=iz, sinir=sinir):
        if ilk_yanita_kadar is None:
            ilk_yanita_kadar = len(iz)
        yanitlar.append(yaz(tamamla(teta).get("q", "?")))
        if len(yanitlar) >= 4:
            break
    return yanitlar, ilk_yanita_kadar


def main() -> None:
    print("Bağlar:", ", ".join(f"{a}→{b}" for a, b in BAGLAR))

    print("\n(a) Taban kural önce: yol(A, q)?")
    for sinir in (6, 12, 18):
        y, n = geri_dene([TABAN, OZYINELI], "yol(A, q)", sinir=sinir)
        print(f"    derinlik sınırı {sinir:>2}: ilk yanıtlar {y}, ilk yanıttan önce açılan alt hedef: {n}")

    print("\n(b) Özyineli kural önce: yol(A, q)?")
    for sinir in (6, 12, 18):
        y, n = geri_dene([OZYINELI, TABAN], "yol(A, q)", sinir=sinir)
        print(f"    derinlik sınırı {sinir:>2}: ilk yanıtlar {y}, ilk yanıttan önce açılan alt hedef: {n}")
    print("    (a)'da ilk yanıt sınırdan bağımsız olarak hemen gelir. (b)'de ise arama önce"
          "\n    yol(A, y) → yol(A, y') → … zincirinde sınıra kadar iner; ilk yanıt ancak sınıra"
          "\n    çarpıp geri dönünce gelir. Gerçek Prolog'da sınır yoktur: ilk yanıt HİÇ gelmez,"
          "\n    program sonsuza kadar iner (yığın taşar).")

    print("\nİleri zincirleme (kural sırası fark etmez):")
    for ad, kurallar in (("(a)", [TABAN, OZYINELI]), ("(b)", [OZYINELI, TABAN])):
        _, turlar = ileri_zincirleme(kurallar, OLGULAR)
        yollar = sorted(yaz(f) for tur in turlar for f in tur)
        print(f"  {ad}: {len(turlar)} turda {len(yollar)} yol türetildi → {', '.join(yollar)}")


if __name__ == "__main__":
    main()
