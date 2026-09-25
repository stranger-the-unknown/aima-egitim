#!/usr/bin/env python3
"""2×2 Stag Hunt (geyik avı / koordinasyon) — saf Nash arama.

Özgün eğitim. İkinci oyun olarak kısa Tavuk (Chicken) özeti de basılır.

https://aima.cs.berkeley.edu/ · https://github.com/aimacode
"""
from __future__ import annotations

from typing import List, Sequence, Tuple

import numpy as np

Strateji = str


def en_iyi_yanit_satir(u: np.ndarray, j: int) -> List[int]:
    col = u[:, j]
    m = col.max()
    return [i for i, v in enumerate(col) if np.isclose(v, m)]


def en_iyi_yanit_sutun(u: np.ndarray, i: int) -> List[int]:
    row = u[i, :]
    m = row.max()
    return [j for j, v in enumerate(row) if np.isclose(v, m)]


def saf_nash(u_a: np.ndarray, u_b: np.ndarray) -> List[Tuple[int, int]]:
    n, m = u_a.shape
    out: List[Tuple[int, int]] = []
    for i in range(n):
        for j in range(m):
            if i in en_iyi_yanit_satir(u_a, j) and j in en_iyi_yanit_sutun(u_b, i):
                out.append((i, j))
    return out


def yazdir_oyun(
    ad: str,
    stratejiler: Sequence[Strateji],
    u_a: np.ndarray,
    u_b: np.ndarray,
) -> None:
    print(f"\n=== {ad} ===")
    print("Ödemeler (u_A, u_B):")
    for i, sa in enumerate(stratejiler):
        h = [f"({u_a[i, j]:g},{u_b[i, j]:g})" for j in range(len(stratejiler))]
        print(f"  {sa:8s} | " + "  ".join(h))
    denge = saf_nash(u_a, u_b)
    print("Saf Nash:")
    for i, j in denge:
        print(
            f"  ({stratejiler[i]}, {stratejiler[j]}) "
            f"→ ({u_a[i, j]:g}, {u_b[i, j]:g})"
        )
    if len(denge) > 1:
        print("  → Birden fazla saf denge: koordinasyon / risk-getiri gerilimi.")


def main() -> None:
    print("2×2 oyunlarda saf Nash (özgün eğitim)\n")

    # Stag Hunt: Geyik (riskli işbirliği) vs Tavşan (güvenli)
    sh = ["geyik", "tavsan"]
    # (2,2) birlikte geyik; (1,1) ikisi tavşan; çaprazda geyikçi 0, tavşan 1
    u_a = np.array([[2.0, 0.0], [1.0, 1.0]])
    u_b = np.array([[2.0, 1.0], [0.0, 1.0]])
    yazdir_oyun("Stag Hunt (Geyik Avı)", sh, u_a, u_b)

    # Chicken: düz / saptır — çarpışma çok kötü
    ch = ["duz", "saptir"]
    # (duz,duz)=(-5,-5); (duz,saptir)=(2,-1); (saptir,duz)=(-1,2); (saptir,saptir)=(0,0)
    u_a2 = np.array([[-5.0, 2.0], [-1.0, 0.0]])
    u_b2 = np.array([[-5.0, -1.0], [2.0, 0.0]])
    yazdir_oyun("Tavuk (Chicken)", ch, u_a2, u_b2)

    print("\nNot: Saf Nash yoksa karma denge gündeme gelir (ileri konu).")


if __name__ == "__main__":
    main()
