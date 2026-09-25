#!/usr/bin/env python3
"""Minik Türkçe derlemden bigram dil modeli.

Add-one (Laplace) yumuşatma; cümle log-skoru ve kısa üretim.

Özgün eğitim. Kitap metni yok. numpy OK (rastgele üretim).
https://aima.cs.berkeley.edu/ · https://github.com/aimacode
"""
from __future__ import annotations

from collections import Counter, defaultdict
from typing import Dict, List, Tuple

import numpy as np

# Özgün minik derlem (kitap metni değil)
DERLEM = [
    "bugün hava çok güzel",
    "bugün hava biraz soğuk",
    "yarın hava güzel olacak",
    "kitap okumak çok güzel",
    "kitap okumak faydalı",
    "çay içmek güzel",
    "sıcak çay içmek istiyorum",
    "güzel bir film izledim",
    "film çok güzeldi",
    "yarın kitap okuyacağım",
]


def tokenize(cumle: str) -> List[str]:
    return cumle.lower().split()


def egit(cumleler: List[str]) -> Tuple[Counter, Dict[str, Counter], List[str]]:
    unigram: Counter = Counter()
    bigram: Dict[str, Counter] = defaultdict(Counter)
    for c in cumleler:
        tok = ["<s>"] + tokenize(c) + ["</s>"]
        for w in tok:
            unigram[w] += 1
        for i in range(len(tok) - 1):
            bigram[tok[i]][tok[i + 1]] += 1
    sozluk = sorted(unigram.keys())
    return unigram, bigram, sozluk


def P_bigram(
    w: str, onceki: str, unigram: Counter, bigram: Dict[str, Counter], V: int
) -> float:
    """Add-one: (c(w'|w)+1) / (c(w)+V)."""
    return (bigram[onceki][w] + 1) / (unigram[onceki] + V)


def log_skor(cumle: str, unigram: Counter, bigram: Dict[str, Counter], sozluk: List[str]) -> float:
    V = len(sozluk)
    tok = ["<s>"] + tokenize(cumle) + ["</s>"]
    toplam = 0.0
    for i in range(len(tok) - 1):
        p = P_bigram(tok[i + 1], tok[i], unigram, bigram, V)
        toplam += float(np.log(p))
    return toplam


def uret(
    unigram: Counter,
    bigram: Dict[str, Counter],
    sozluk: List[str],
    max_len: int = 8,
    seed: int = 0,
) -> str:
    rng = np.random.default_rng(seed)
    V = len(sozluk)
    onceki = "<s>"
    out: List[str] = []
    for _ in range(max_len):
        adaylar = [w for w in sozluk if w not in ("<s>",)]
        probs = np.array([P_bigram(w, onceki, unigram, bigram, V) for w in adaylar])
        probs = probs / probs.sum()
        nxt = adaylar[int(rng.choice(len(adaylar), p=probs))]
        if nxt == "</s>":
            break
        out.append(nxt)
        onceki = nxt
    return " ".join(out)


def main() -> None:
    unigram, bigram, sozluk = egit(DERLEM)
    print(f"Derlem: {len(DERLEM)} cümle, sözlük boyu V={len(sozluk)}")
    print("\n=== Örnek bigram sayımları (<s> sonrası) ===")
    for w, c in bigram["<s>"].most_common(5):
        print(f"  P(·|<s>) aday: {w}  sayım={c}")

    print("\n=== Cümle log-skorları (yüksek = daha uyumlu) ===")
    for s in ["bugün hava güzel", "çay içmek güzel", "uzaylı pizza dans"]:
        print(f"  {log_skor(s, unigram, bigram, sozluk):8.3f}  |  {s}")

    print("\n=== Örnek üretim ===")
    for i in range(3):
        print(f"  [{i}] {uret(unigram, bigram, sozluk, seed=i)}")


if __name__ == "__main__":
    main()
