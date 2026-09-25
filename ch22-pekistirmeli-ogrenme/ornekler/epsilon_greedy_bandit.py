#!/usr/bin/env python3
"""Çok kollu bandit — epsilon-açgözlü demo.

Her kol Bernoulli/Gaussian benzeri sabit ortalama ödül üretir.
ε-açgözlü ajan ortalama ödülü ve kol seçim sayılarını yazdırır.

Özgün eğitim. Kitap metni yok. numpy OK.
https://aima.cs.berkeley.edu/ · https://github.com/aimacode
"""
from __future__ import annotations

from typing import List

import numpy as np


def calistir(
    kollar_ortalama: List[float] | None = None,
    adim: int = 2000,
    epsilon: float = 0.1,
    seed: int = 42,
) -> None:
    if kollar_ortalama is None:
        kollar_ortalama = [0.1, 0.3, 0.8, 0.2, 0.5]
    k = len(kollar_ortalama)
    rng = np.random.default_rng(seed)

    Q = np.zeros(k)
    N = np.zeros(k, dtype=int)
    odul_toplam = 0.0
    pencere: List[float] = []

    print(f"Kollar (gerçek ort.): {kollar_ortalama}")
    print(f"ε = {epsilon}, adım = {adim}\n")

    for t in range(1, adim + 1):
        if rng.random() < epsilon:
            a = int(rng.integers(0, k))
        else:
            a = int(np.argmax(Q))
        # Gauss gürültülü ödül
        r = float(rng.normal(kollar_ortalama[a], 0.1))
        N[a] += 1
        Q[a] += (r - Q[a]) / N[a]
        odul_toplam += r
        pencere.append(r)

        if t % 500 == 0 or t == adim:
            son = pencere[-500:] if len(pencere) >= 500 else pencere
            print(
                f"t={t:4d}  ort.ödül(son~500)={np.mean(son):.3f}  "
                f"kümülatif ort.={odul_toplam / t:.3f}  "
                f"seçimler={N.tolist()}"
            )

    print("\n=== Tahmini Q ===")
    for i in range(k):
        print(f"  kol {i}: Q̂={Q[i]:.3f}  N={N[i]}  (gerçek μ={kollar_ortalama[i]})")
    print(f"En çok seçilen kol: {int(np.argmax(N))}  |  En yüksek Q̂: {int(np.argmax(Q))}")


def main() -> None:
    calistir()


if __name__ == "__main__":
    main()
