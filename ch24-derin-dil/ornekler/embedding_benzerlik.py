#!/usr/bin/env python3
"""Minik kelime gömüleri + kosinüs benzerliği (Türkçe sözcükler).

Elle seçilmiş 2B vektörler — eğitim yok; sezgi demosu.
İsteğe bağlı: rastgele başlangıç + birkaç skip-gram-toy adımı.

Özgün eğitim. Kitap metni yok. numpy OK; torch/tensorflow yok.
https://aima.cs.berkeley.edu/ · https://github.com/aimacode
"""
from __future__ import annotations

from typing import Dict, List, Tuple

import numpy as np

# Elle seçilmiş 2B gömüler (sezgi; gerçek Word2Vec değil)
ELLE_GOMU: Dict[str, np.ndarray] = {
    "kedi": np.array([0.90, 0.20]),
    "köpek": np.array([0.85, 0.25]),
    "kuzgun": np.array([0.70, 0.55]),
    "masa": np.array([-0.20, 0.90]),
    "sandalye": np.array([-0.15, 0.85]),
    "mutlu": np.array([0.40, -0.80]),
    "sevinçli": np.array([0.45, -0.75]),
    "üzgün": np.array([-0.50, -0.70]),
}


def kosinus(a: np.ndarray, b: np.ndarray) -> float:
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na < 1e-12 or nb < 1e-12:
        return 0.0
    return float(np.dot(a, b) / (na * nb))


def cift_skorlari(gomu: Dict[str, np.ndarray]) -> List[Tuple[str, str, float]]:
    kelimeler = list(gomu.keys())
    sonuclar: List[Tuple[str, str, float]] = []
    for i, w1 in enumerate(kelimeler):
        for w2 in kelimeler[i + 1 :]:
            sonuclar.append((w1, w2, kosinus(gomu[w1], gomu[w2])))
    sonuclar.sort(key=lambda t: t[2], reverse=True)
    return sonuclar


def skipgram_toy(
    sozluk: List[str],
    pencereler: List[Tuple[str, str]],
    dim: int = 2,
    adim: int = 80,
    lr: float = 0.08,
    seed: int = 0,
) -> Dict[str, np.ndarray]:
    """Çok kaba skip-gram-toy: hedef–bağlam nokta çarpımını yükselt.

    Gerçek negatif örnekleme / softmax yok; yalnızca eğitici gürültü.
    """
    rng = np.random.default_rng(seed)
    W = {w: rng.normal(0, 0.3, size=dim) for w in sozluk}
    for _ in range(adim):
        for hedef, baglam in pencereler:
            Wh, Wb = W[hedef], W[baglam]
            W[hedef] = Wh + lr * Wb
            W[baglam] = Wb + lr * Wh
        for w in W:
            n = np.linalg.norm(W[w])
            if n > 1e-9:
                W[w] = W[w] / n
    return W


def main() -> None:
    print("=== Elle gömü kosinüs (Türkçe) ===")
    skorlar = cift_skorlari(ELLE_GOMU)
    for w1, w2, s in skorlar[:6]:
        print(f"  {w1:10s} ~ {w2:10s}  cos={s:+.3f}")
    print("  …")
    for w1, w2, s in skorlar[-3:]:
        print(f"  {w1:10s} ~ {w2:10s}  cos={s:+.3f}")

    print("\nEn yüksek:", f"{skorlar[0][0]}–{skorlar[0][1]} ({skorlar[0][2]:+.3f})")
    print("En düşük :", f"{skorlar[-1][0]}–{skorlar[-1][1]} ({skorlar[-1][2]:+.3f})")

    sozluk = ["kedi", "köpek", "masa", "sandalye", "mutlu", "üzgün"]
    pencereler = [
        ("kedi", "köpek"),
        ("köpek", "kedi"),
        ("masa", "sandalye"),
        ("sandalye", "masa"),
        ("mutlu", "üzgün"),
        ("üzgün", "mutlu"),
    ]
    toy = skipgram_toy(sozluk, pencereler)
    print("\n=== Skip-gram-toy sonrası (normalize) ===")
    for w1, w2 in [("kedi", "köpek"), ("masa", "sandalye"), ("kedi", "masa")]:
        print(f"  {w1} ~ {w2}: cos={kosinus(toy[w1], toy[w2]):+.3f}")


if __name__ == "__main__":
    main()
