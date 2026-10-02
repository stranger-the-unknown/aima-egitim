#!/usr/bin/env python3
"""de Finetti'nin argümanı: Olasılık aksiyomlarını çiğneyen inançlar garanti kayba yol açar.

Ajan 1'in inançları (kitaptaki örnek; aksiyomlarla tutarsız):
    P(a) = 0.4,  P(b) = 0.3,  P(a ∧ b) = 0.0,  P(a ∨ b) = 0.8
Dahil etme–dışlama: P(a ∨ b) = P(a) + P(b) − P(a ∧ b) = 0.7 olmalıydı.

Bir inanç p, "q = 1 − p'ye karşı p" oranında bahse girmeyi kabul etmek demektir:
    Ajan 2, a'nın lehine 4$ koyarsa, Ajan 1 6$ ile ¬a'ya bahse girer. Kazanan hepsini alır.
Ajan 2: a'ya 4$, b'ye 3$, ¬(a ∨ b)'ye 2$ yatırır. Ajan 1 her durumda kaybeder:
    (a, b): −11,  (a, ¬b): −1,  (¬a, b): −1,  (¬a, ¬b): −1

Çalıştırma:
    python hollanda_kitabi.py
"""
from __future__ import annotations

import itertools

# Önermeler: sonuç (a, b) → doğru mu?
ONERMELER = {
    "a": lambda a, b: a,
    "b": lambda a, b: b,
    "a∧b": lambda a, b: a and b,
    "a∨b": lambda a, b: a or b,
}


def bahis_kazanci(inanc: float, ajan2_lehine: bool, ajan2_yatirim: float, dogru: bool) -> float:
    """Ajan 1'in bir bahisten kazancı.
    Ajan 1'in inancı p ise, Ajan 2'nin önermenin lehine koyduğu x dolara karşılık Ajan 1,
    x·(1−p)/p dolar koyar (oranlar p : 1−p). Ajan 2 aleyhine bahse girerse tersi."""
    p = inanc if ajan2_lehine else 1 - inanc          # Ajan 2'nin bahis yaptığı olayın Ajan 1'deki olasılığı
    ajan1_yatirim = ajan2_yatirim * (1 - p) / p
    ajan2_kazandi = dogru if ajan2_lehine else not dogru
    return -ajan1_yatirim if ajan2_kazandi else ajan2_yatirim


def kazanc_tablosu(inanclar: dict, bahisler: list[tuple[str, bool, float]]) -> dict:
    """Her (a, b) sonucu için Ajan 1'in toplam kazancı."""
    tablo = {}
    for a, b in itertools.product([True, False], repeat=2):
        tablo[(a, b)] = sum(bahis_kazanci(inanclar[o], lehine, x, ONERMELER[o](a, b))
                            for o, lehine, x in bahisler)
    return tablo


def beklenen_kazanc(tablo: dict, olasiliklar: dict) -> float:
    return sum(tablo[s] * olasiliklar[s] for s in tablo)


def main() -> None:
    inanclar = {"a": 0.4, "b": 0.3, "a∧b": 0.0, "a∨b": 0.8}
    # Ajan 2'nin bahisleri: a lehine 4$, b lehine 3$, (a∨b) aleyhine 2$
    bahisler = [("a", True, 4), ("b", True, 3), ("a∨b", False, 2)]
    print("=== Tutarsız inançlar: P(a)=0.4, P(b)=0.3, P(a∧b)=0, P(a∨b)=0.8 ===")
    tablo = kazanc_tablosu(inanclar, bahisler)
    for (a, b), k in tablo.items():
        print(f"  a={a!s:<5} b={b!s:<5} → Ajan 1'in kazancı {k:+.0f}$")
    print("  Her sonuçta kayıp: bu bir 'Hollanda kitabı' (Dutch book).")

    print("\n=== Tutarlı inançlarla aynı bahisler: P(a∨b) = 0.7 ===")
    tutarli = {**inanclar, "a∨b": 0.7}
    tablo2 = kazanc_tablosu(tutarli, bahisler)
    for (a, b), k in tablo2.items():
        print(f"  a={a!s:<5} b={b!s:<5} → {k:+.2f}$")
    # Ajan 1'in inançlarıyla tutarlı bir dağılım: P(a,b)=0, P(a,¬b)=0.4, P(¬a,b)=0.3, P(¬a,¬b)=0.3
    dagilim = {(True, True): 0.0, (True, False): 0.4, (False, True): 0.3, (False, False): 0.3}
    print(f"  Ajan 1'in kendi dağılımına göre beklenen kazanç: {beklenen_kazanc(tablo2, dagilim):+.2f}$")
    print("  Adil oranlı her bahsin beklenen değeri 0'dır. Toplamın beklentisi de 0 olduğu için")
    print("  her sonuçta negatif olamaz: tutarlı inançlara karşı garanti kazandıran bahis yoktur.")


if __name__ == "__main__":
    main()
