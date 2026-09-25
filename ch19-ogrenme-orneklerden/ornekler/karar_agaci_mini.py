#!/usr/bin/env python3
"""Minik ID3 tarzı karar ağacı — Türkçe kategorik veri.

Özgün eğitim (kitap metni yok). Entropi / bilgi kazancı ile özellik seçimi.

https://aima.cs.berkeley.edu/ · https://github.com/aimacode
"""
from __future__ import annotations

import math
from collections import Counter
from typing import Any, Dict, List, Optional, Tuple

# Özellik adları
OZELLIKLER = ["havadurumu", "sicaklik", "nem", "ruzgar"]

# (özellik değerleri..., etiket) — etiket: oyna / bekle
VERI: List[Tuple[Tuple[str, ...], str]] = [
    (("gunesli", "sicak", "yuksek", "zayif"), "bekle"),
    (("gunesli", "sicak", "yuksek", "kuvvetli"), "bekle"),
    (("bulutlu", "sicak", "yuksek", "zayif"), "oyna"),
    (("yagmurlu", "ilik", "yuksek", "zayif"), "oyna"),
    (("yagmurlu", "serin", "normal", "zayif"), "oyna"),
    (("yagmurlu", "serin", "normal", "kuvvetli"), "bekle"),
    (("bulutlu", "serin", "normal", "kuvvetli"), "oyna"),
    (("gunesli", "ilik", "yuksek", "zayif"), "bekle"),
    (("gunesli", "serin", "normal", "zayif"), "oyna"),
    (("yagmurlu", "ilik", "normal", "zayif"), "oyna"),
    (("gunesli", "ilik", "normal", "kuvvetli"), "oyna"),
    (("bulutlu", "ilik", "yuksek", "kuvvetli"), "oyna"),
    (("bulutlu", "sicak", "normal", "zayif"), "oyna"),
    (("yagmurlu", "ilik", "yuksek", "kuvvetli"), "bekle"),
]


def entropi(etiketler: List[str]) -> float:
    n = len(etiketler)
    if n == 0:
        return 0.0
    toplam = 0.0
    for c in Counter(etiketler).values():
        p = c / n
        toplam -= p * math.log2(p)
    return toplam


def bilgi_kazanci(ornekler: List[Tuple[Tuple[str, ...], str]], oz_idx: int) -> float:
    etiketler = [y for _, y in ornekler]
    baz = entropi(etiketler)
    n = len(ornekler)
    gruplar: Dict[str, List[str]] = {}
    for x, y in ornekler:
        gruplar.setdefault(x[oz_idx], []).append(y)
    kalan = sum((len(g) / n) * entropi(g) for g in gruplar.values())
    return baz - kalan


class Dugum:
    def __init__(
        self,
        etiket: Optional[str] = None,
        ozellik: Optional[str] = None,
        cocuklar: Optional[Dict[str, "Dugum"]] = None,
    ) -> None:
        self.etiket = etiket
        self.ozellik = ozellik
        self.cocuklar = cocuklar or {}


def cogunluk(etiketler: List[str]) -> str:
    return Counter(etiketler).most_common(1)[0][0]


def id3(ornekler: List[Tuple[Tuple[str, ...], str]], kalan_oz: List[int]) -> Dugum:
    etiketler = [y for _, y in ornekler]
    if len(set(etiketler)) == 1:
        return Dugum(etiket=etiketler[0])
    if not kalan_oz:
        return Dugum(etiket=cogunluk(etiketler))

    best = max(kalan_oz, key=lambda i: bilgi_kazanci(ornekler, i))
    dugum = Dugum(ozellik=OZELLIKLER[best])
    degerler = sorted({x[best] for x, _ in ornekler})
    yeni_kalan = [i for i in kalan_oz if i != best]
    for d in degerler:
        alt = [(x, y) for x, y in ornekler if x[best] == d]
        if not alt:
            dugum.cocuklar[d] = Dugum(etiket=cogunluk(etiketler))
        else:
            dugum.cocuklar[d] = id3(alt, yeni_kalan)
    return dugum


def tahmin(dugum: Dugum, x: Tuple[str, ...]) -> str:
    while dugum.etiket is None:
        assert dugum.ozellik is not None
        idx = OZELLIKLER.index(dugum.ozellik)
        deger = x[idx]
        if deger not in dugum.cocuklar:
            # görülmeyen dal — güvenli varsayılan
            return "bekle"
        dugum = dugum.cocuklar[deger]
    return dugum.etiket


def yazdir_agac(dugum: Dugum, girinti: str = "") -> None:
    if dugum.etiket is not None:
        print(f"{girinti}→ {dugum.etiket}")
        return
    print(f"{girinti}[{dugum.ozellik}]")
    for deger, cocuk in dugum.cocuklar.items():
        print(f"{girinti}  {deger}:")
        yazdir_agac(cocuk, girinti + "    ")


def main() -> None:
    print("=== Minik karar ağacı (ID3 tarzı) ===\n")
    print(f"Örnek sayısı: {len(VERI)}")
    print(f"Özellikler: {OZELLIKLER}\n")

    print("Bilgi kazancı (kök adayı):")
    kg = [(OZELLIKLER[i], bilgi_kazanci(VERI, i)) for i in range(len(OZELLIKLER))]
    kg.sort(key=lambda t: -t[1])
    for ad, g in kg:
        print(f"  {ad:12s}  IG={g:.4f}")

    agac = id3(VERI, list(range(len(OZELLIKLER))))
    print("\nAğaç:")
    yazdir_agac(agac)

    hatalar = sum(1 for x, y in VERI if tahmin(agac, x) != y)
    print(f"\nEğitim hatası: {hatalar}/{len(VERI)}")

    # Birkaç tahmin demosu
    demo = ("gunesli", "serin", "normal", "zayif")
    print(f"Demo {demo} → {tahmin(agac, demo)}")


if __name__ == "__main__":
    main()
