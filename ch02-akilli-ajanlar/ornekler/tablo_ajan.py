#!/usr/bin/env python3
"""Tabloya dayalı ajan: ajan fonksiyonunu doğrudan tablo olarak yazmak neden işe yaramaz?

Tabloya dayalı ajan, algı geçmişinin *tamamını* anahtar olarak kullanır ve
eylemi tablodan okur. Kavramsal olarak her ajan fonksiyonunu temsil edebilir,
ama tablo boyutu yaşam süresiyle üstel büyür:

    satır sayısı = |P|^1 + |P|^2 + ... + |P|^T      (|P| = olası algı sayısı)

Bu script:
  1. Süpürge dünyası için küçük bir tabloya dayalı ajan çalıştırır.
  2. Farklı algı sayıları ve yaşam süreleri için tablo boyutunu hesaplar.

Çalıştırma:
    python tablo_ajan.py
"""
from __future__ import annotations

import math
from itertools import product

ALGILAR = [("A", "Temiz"), ("A", "Kirli"), ("B", "Temiz"), ("B", "Kirli")]


def refleks_kurali(algi: tuple[str, str]) -> str:
    konum, durum = algi
    if durum == "Kirli":
        return "Süpür"
    return "Sağ" if konum == "A" else "Sol"


def tablo_olustur(T: int) -> dict[tuple, str]:
    """Uzunluğu T'ye kadar olan *her* algı dizisi için bir satır.

    Eylemi basit refleks kuralıyla dolduruyoruz (yalnızca son algıya bakıyor),
    ama tablo yine de tüm geçmişleri anahtar olarak tutmak zorunda.
    """
    tablo = {}
    for t in range(1, T + 1):
        for gecmis in product(ALGILAR, repeat=t):
            tablo[gecmis] = refleks_kurali(gecmis[-1])
    return tablo


class TabloAjani:
    def __init__(self, tablo: dict[tuple, str]) -> None:
        self.tablo = tablo
        self.gecmis: list[tuple[str, str]] = []

    def __call__(self, algi: tuple[str, str]) -> str:
        self.gecmis.append(algi)
        return self.tablo[tuple(self.gecmis)]


def tablo_boyutu(algi_sayisi: int, T: int) -> int:
    """Σ_{t=1}^{T} |P|^t (geometrik seri)."""
    if algi_sayisi == 1:
        return T
    return (algi_sayisi ** (T + 1) - algi_sayisi) // (algi_sayisi - 1)


def main() -> None:
    T = 4
    tablo = tablo_olustur(T)
    print(f"Süpürge dünyası: |P| = {len(ALGILAR)} algı, yaşam süresi T = {T}")
    print(f"Tablo satır sayısı: {len(tablo)}  (formül: {tablo_boyutu(4, T)})\n")

    ajan = TabloAjani(tablo)
    for algi in [("A", "Kirli"), ("A", "Temiz"), ("B", "Kirli"), ("B", "Temiz")]:
        print(f"  algı={algi} → {ajan(algi)}")
    print("  (5. algıda tablo biter: ajan ne yapacağını bilemez.)\n")

    print("Tablo boyutu nasıl büyüyor?")
    print(f"{'|P|':>8} {'T':>6} {'satır sayısı (≈10^k)':>24}")
    for P, T_ in [(4, 10), (4, 100), (4, 1000), (1000, 100), (10**6, 3600)]:
        k = math.log10(tablo_boyutu(P, T_)) if P ** T_ < 10**300 else T_ * math.log10(P)
        print(f"{P:>8} {T_:>6} {'10^' + format(k, '.0f'):>24}")
    print(
        "\nKarşılaştırma: gözlemlenebilir evrendeki atom sayısı ≈ 10^80."
        "\nBu yüzden asıl soru, *küçük bir programla* rasyonel davranış üretmektir:"
        "\nrefleks kuralları, iç model, hedefler, fayda ve öğrenme bunun yollarıdır."
    )


if __name__ == "__main__":
    main()
