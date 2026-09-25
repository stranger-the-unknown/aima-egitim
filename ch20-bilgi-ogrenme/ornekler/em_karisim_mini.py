#!/usr/bin/env python3
"""Klasik iki madeni para EM demosu (eğitici, minik).

Gizli: her atış dizisinin hangi paradan geldiği.
E: sorumluluklar; M: θ güncelle.

Özgün eğitim. numpy OK. Kitap metni yok.

https://aima.cs.berkeley.edu/ · https://github.com/aimacode
"""
from __future__ import annotations

from typing import List, Tuple

import numpy as np


def bernoulli_olabilirlik(yazi: int, n: int, theta: float, eps: float = 1e-12) -> float:
    t = float(np.clip(theta, eps, 1.0 - eps))
    return (t**yazi) * ((1.0 - t) ** (n - yazi))


def em_iki_para(
    diziler: List[Tuple[int, int]],
    theta_a: float = 0.6,
    theta_b: float = 0.5,
    pi_a: float = 0.5,
    iterasyon: int = 8,
) -> None:
    print("=== EM — iki madeni para (klasik mini) ===\n")
    print(f"Başlangıç: θ_A={theta_a:.3f}, θ_B={theta_b:.3f}, π_A={pi_a:.3f}\n")

    for it in range(1, iterasyon + 1):
        sorumluluk_a: List[float] = []
        for yazi, n in diziler:
            like_a = bernoulli_olabilirlik(yazi, n, theta_a)
            like_b = bernoulli_olabilirlik(yazi, n, theta_b)
            numar = pi_a * like_a
            denom = numar + (1.0 - pi_a) * like_b
            r = numar / denom if denom > 0 else 0.5
            sorumluluk_a.append(r)

        ra = np.array(sorumluluk_a)
        yazilar = np.array([d[0] for d in diziler], dtype=float)
        nler = np.array([d[1] for d in diziler], dtype=float)

        ea_yazi = float(np.sum(ra * yazilar))
        ea_n = float(np.sum(ra * nler))
        eb_yazi = float(np.sum((1.0 - ra) * yazilar))
        eb_n = float(np.sum((1.0 - ra) * nler))

        theta_a = ea_yazi / ea_n if ea_n > 0 else theta_a
        theta_b = eb_yazi / eb_n if eb_n > 0 else theta_b
        pi_a = float(np.mean(ra))

        print(f"İterasyon {it}:")
        print(f"  sorumluluklar A: {np.round(ra, 3).tolist()}")
        print(f"  θ_A={theta_a:.4f}, θ_B={theta_b:.4f}, π_A={pi_a:.4f}")

    print("\nNot: E = yumuşak etiket; M = ağırlıklı frekans (MLE). Yerel en iyiye gidebilir.")


def main() -> None:
    rng = np.random.default_rng(0)
    gercek = []
    diziler: List[Tuple[int, int]] = []
    for _ in range(12):
        hangi = "A" if rng.random() < 0.5 else "B"
        theta = 0.8 if hangi == "A" else 0.3
        yazi = int(rng.binomial(5, theta))
        diziler.append((yazi, 5))
        gercek.append(hangi)
    print(f"(Gizli gerçek etiketler, sadece kontrol: {gercek})")
    print(f"Gözlenen (yazı, n): {diziler}\n")
    em_iki_para(diziler, theta_a=0.6, theta_b=0.5, pi_a=0.5, iterasyon=8)


if __name__ == "__main__":
    main()
