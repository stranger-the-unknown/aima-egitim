#!/usr/bin/env python3
"""Minik BoW + naif Bayes tarzı duygu sınıflandırıcı.

Elle sayım; sklearn yok. Eğitim cümlelerinden P(w|sınıf) ve MAP etiket.

Özgün eğitim. Kitap metni yok.
https://aima.cs.berkeley.edu/ · https://github.com/aimacode
"""
from __future__ import annotations

import math
from collections import Counter, defaultdict
from typing import Dict, List, Tuple

# (metin, etiket) — özgün minik veri
EGITIM: List[Tuple[str, str]] = [
    ("film çok güzeldi harika oyunculuk", "pozitif"),
    ("muhteşem bir hikaye tavsiye ederim", "pozitif"),
    ("güzel atmosfer ve iyi tempo", "pozitif"),
    ("berbat senaryo zaman kaybı", "negatif"),
    ("çok kötü oyunculuk hayal kırıklığı", "negatif"),
    ("sıkıcı ve yavaş ilerliyor", "negatif"),
    ("konu ilginç ama final zayıf", "negatif"),
    ("keyifle izledim tekrar bakarım", "pozitif"),
]

TEST = [
    "güzel film tavsiye ederim",
    "berbat ve sıkıcı",
    "harika tempo iyi hikaye",
    "zaman kaybı kötü",
]


def tokenize(t: str) -> List[str]:
    return t.lower().split()


def egit(
    veriler: List[Tuple[str, str]],
) -> Tuple[Dict[str, float], Dict[str, Counter], Counter, int]:
    sinif_say: Counter = Counter()
    kelime_say: Dict[str, Counter] = defaultdict(Counter)
    for metin, y in veriler:
        sinif_say[y] += 1
        for w in tokenize(metin):
            kelime_say[y][w] += 1
    once = {c: sinif_say[c] / len(veriler) for c in sinif_say}
    V = len({w for c in kelime_say for w in kelime_say[c]})
    return once, kelime_say, sinif_say, V


def log_P_w_sinif(w: str, sinif: str, kelime_say: Dict[str, Counter], V: int) -> float:
    """Add-one: (count+1)/(toplam+V)."""
    toplam = sum(kelime_say[sinif].values())
    return math.log((kelime_say[sinif][w] + 1) / (toplam + V))


def tahmin(
    metin: str,
    once: Dict[str, float],
    kelime_say: Dict[str, Counter],
    V: int,
) -> Tuple[str, Dict[str, float]]:
    skorlar: Dict[str, float] = {}
    for c in once:
        s = math.log(once[c])
        for w in tokenize(metin):
            s += log_P_w_sinif(w, c, kelime_say, V)
        skorlar[c] = s
    etiket = max(skorlar, key=skorlar.get)
    return etiket, skorlar


def main() -> None:
    once, kelime_say, sinif_say, V = egit(EGITIM)
    print(f"Eğitim: {len(EGITIM)} örnek, V≈{V}, sınıflar={dict(sinif_say)}")
    print(f"Önceler: { {k: round(v, 3) for k, v in once.items()} }\n")
    print("=== Test ===")
    for t in TEST:
        y, skor = tahmin(t, once, kelime_say, V)
        skor_s = " ".join(f"{k}:{v:.2f}" for k, v in skor.items())
        print(f"  [{y:8s}]  {t}")
        print(f"           log-skor {skor_s}")


if __name__ == "__main__":
    main()
