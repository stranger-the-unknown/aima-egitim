#!/usr/bin/env python3
"""Alıştırma 10 çözümü: Dört-Bir-Arada'da değerlendirme özniteliklerinin önemi."""
from __future__ import annotations

import sys
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ornekler"))

from dortlu_ab import BOS, O, PENCERELER, SATIR, X, Arama, Tahta, degerlendir  # noqa: E402


def yalniz_merkez(t: Tahta, oyuncu: str) -> int:
    rakip = O if oyuncu == X else X
    merkez = [t.h[r][3] for r in range(SATIR)]
    return merkez.count(oyuncu) - merkez.count(rakip)


def yalniz_tehdit(t: Tahta, oyuncu: str) -> int:
    rakip = O if oyuncu == X else X
    puan = 0
    for p in PENCERELER:
        d = [t.h[r][c] for r, c in p]
        if d.count(BOS) == 1:
            puan += (d.count(oyuncu) == 3) - (d.count(rakip) == 3)
    return puan


FONKSIYONLAR = {"özgün": degerlendir, "merkez": yalniz_merkez, "tehdit": yalniz_tehdit}


def mac(f_x, f_o, derinlik: int = 3) -> str:
    t, sira = Tahta(), X
    ajanlar = {X: Arama(degerlendirme=f_x), O: Arama(degerlendirme=f_o)}
    while t.kazanan() is None and t.gecerli():
        t = t.oyna(ajanlar[sira].en_iyi_hamle(t, sira, derinlik), sira)
        sira = O if sira == X else X
    return t.kazanan() or "berabere"


def main() -> None:
    print("Derinlik 3, her ikili için 6 oyun (başlayan dönüşümlü). Deterministik ajanlar olduğu için"
          "\naynı başlangıçla aynı oyun tekrarlanır; bu yüzden 6 oyun = 3 + 3 tekrar.\n")
    puan = {ad: 0.0 for ad in FONKSIYONLAR}
    for a, b in combinations(FONKSIYONLAR, 2):
        sonuc = {a: 0, b: 0, "berabere": 0}
        for i in range(6):
            x, o = (a, b) if i % 2 == 0 else (b, a)
            k = mac(FONKSIYONLAR[x], FONKSIYONLAR[o])
            if k == X:
                sonuc[x] += 1
            elif k == O:
                sonuc[o] += 1
            else:
                sonuc["berabere"] += 1
        puan[a] += sonuc[a] + sonuc["berabere"] / 2
        puan[b] += sonuc[b] + sonuc["berabere"] / 2
        print(f"  {a:>7} — {b:<7}: {sonuc[a]} – {sonuc[b]}  (berabere {sonuc['berabere']})")
    print("\nToplam puan: " + ", ".join(f"{ad} {p:g}" for ad, p in sorted(puan.items(), key=lambda x: -x[1])))


if __name__ == "__main__":
    main()
