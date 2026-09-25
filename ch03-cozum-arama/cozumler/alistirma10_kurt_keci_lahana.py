#!/usr/bin/env python3
"""Alıştırma 10 çözümü: kurt, keçi, lahana problemi.

Durum: (çiftçi, kurt, keçi, lahana) — her biri 0 (başlangıç kıyısı) veya 1 (karşı kıyı).
2⁴ = 16 durum vardır; bunların 10'u "güvenli"dir (kimse kimseyi yemez).
"""
from __future__ import annotations

import sys
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ornekler"))

from arama import Problem, genislik_oncelikli, tekduze_maliyet  # noqa: E402

ADLAR = ("çiftçi", "kurt", "keçi", "lahana")


def guvenli(durum) -> bool:
    ciftci, kurt, keci, lahana = durum
    if kurt == keci != ciftci:
        return False  # kurt keçiyi yer
    if keci == lahana != ciftci:
        return False  # keçi lahanayı yer
    return True


class KurtKeciLahana(Problem):
    def __init__(self):
        super().__init__((0, 0, 0, 0), (1, 1, 1, 1))

    def eylemler(self, durum):
        ciftci = durum[0]
        # Çiftçi tek başına ya da kendi kıyısındaki bir şeyle karşıya geçer
        for yolcu in (None, 1, 2, 3):
            if yolcu is not None and durum[yolcu] != ciftci:
                continue
            yeni = self.sonuc(durum, yolcu)
            if guvenli(yeni):
                yield yolcu

    def sonuc(self, durum, yolcu):
        yeni = list(durum)
        yeni[0] = 1 - yeni[0]
        if yolcu is not None:
            yeni[yolcu] = 1 - yeni[yolcu]
        return tuple(yeni)


def anlat(durum) -> str:
    sol = [ADLAR[i] for i in range(4) if durum[i] == 0]
    sag = [ADLAR[i] for i in range(4) if durum[i] == 1]
    return f"{', '.join(sol) or '—':<30} ~~~  {', '.join(sag) or '—'}"


def main() -> None:
    tum = list(product((0, 1), repeat=4))
    print(f"Toplam durum: {len(tum)}, güvenli durum: {sum(map(guvenli, tum))}\n")

    p = KurtKeciLahana()
    s = genislik_oncelikli(p)
    print(f"BFS çözümü ({len(s.eylemler)} geçiş):")
    print(f"  0. {anlat(s.yol[0])}")
    for i, (eylem, durum) in enumerate(zip(s.eylemler, s.yol[1:]), 1):
        kim = "yalnız" if eylem is None else f"{ADLAR[eylem]} ile"
        print(f"  {i}. çiftçi {kim} geçer → {anlat(durum)}")

    u = tekduze_maliyet(p)
    print(f"\nUCS çözüm uzunluğu: {len(u.eylemler)} (BFS ile aynı: tüm geçişlerin maliyeti 1)")


if __name__ == "__main__":
    main()
