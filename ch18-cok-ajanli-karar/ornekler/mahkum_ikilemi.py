#!/usr/bin/env python3
"""Mahkûm ikilemi — ödeme matrisi, en iyi yanıt, saf Nash.

Özgün eğitim örneği (kitap metni yok). numpy ile matris.

https://aima.cs.berkeley.edu/ · https://github.com/aimacode
"""
from __future__ import annotations

from typing import List, Tuple

import numpy as np

# Strateji adları (Türkçe)
STRATEJILER = ["isbirligi", "ihanet"]

# Ödemeler: satır = oyuncu A, sütun = oyuncu B
# klasik: işbirliği/işbirliği (3,3); ihanet/işbirliği (5,0); ...
U_A = np.array([
    [3, 0],  # A işbirliği: B işbirliği / B ihanet
    [5, 1],  # A ihanet
], dtype=float)

U_B = np.array([
    [3, 5],  # B'nin ödemesi (simetrik ikilem)
    [0, 1],
], dtype=float)


def en_iyi_yanit_satir(u_satir: np.ndarray, sutun: int) -> List[int]:
    """Sabit sütun stratejisine karşı satır oyuncusunun en iyi yanıt(lar)ı."""
    sutun_odeme = u_satir[:, sutun]
    en = sutun_odeme.max()
    return [i for i, v in enumerate(sutun_odeme) if v == en]


def en_iyi_yanit_sutun(u_sutun: np.ndarray, satir: int) -> List[int]:
    satir_odeme = u_sutun[satir, :]
    en = satir_odeme.max()
    return [j for j, v in enumerate(satir_odeme) if v == en]


def saf_nash(u_a: np.ndarray, u_b: np.ndarray) -> List[Tuple[int, int]]:
    n, m = u_a.shape
    denge: List[Tuple[int, int]] = []
    for i in range(n):
        for j in range(m):
            if i in en_iyi_yanit_satir(u_a, j) and j in en_iyi_yanit_sutun(u_b, i):
                denge.append((i, j))
    return denge


def baskin_strateji(u: np.ndarray, oyuncu: str) -> None:
    """Sıkı baskın strateji var mı? (satır oyuncusu için u satır ödemesi)."""
    n, m = u.shape
    print(f"\n--- Baskın strateji kontrolü ({oyuncu}) ---")
    for i in range(n):
        digerleri = [k for k in range(n) if k != i]
        # i, her sütunda diğer tüm satırlardan >= ve en az birinde > mı?
        zayif = all(all(u[i, j] >= u[k, j] for k in digerleri) for j in range(m))
        siki = zayif and any(
            any(u[i, j] > u[k, j] for k in digerleri) for j in range(m)
        )
        if siki:
            print(f"  Sıkı baskın: {STRATEJILER[i]}")
        elif zayif:
            print(f"  Zayıf baskın: {STRATEJILER[i]}")


def main() -> None:
    print("=== Mahkûm İkilemi (özgün eğitim) ===\n")
    print("Ödeme matrisi (u_A, u_B):")
    for i, sa in enumerate(STRATEJILER):
        hucreler = []
        for j, sb in enumerate(STRATEJILER):
            hucreler.append(f"({U_A[i, j]:g},{U_B[i, j]:g})")
        print(f"  A={sa:10s} | " + "  ".join(hucreler))
    print("                 B=" + "          ".join(STRATEJILER))

    baskin_strateji(U_A, "A (satır)")
    # B için sütun oyuncusu: baskınlığı satır gibi görmek için U_B.T
    baskin_strateji(U_B.T, "B (sütun, transpoz bakış)")

    print("\n--- En iyi yanıtlar ---")
    for j, sb in enumerate(STRATEJILER):
        br = en_iyi_yanit_satir(U_A, j)
        print(f"  B={sb} iken A en iyi yanıt: {[STRATEJILER[i] for i in br]}")
    for i, sa in enumerate(STRATEJILER):
        br = en_iyi_yanit_sutun(U_B, i)
        print(f"  A={sa} iken B en iyi yanıt: {[STRATEJILER[j] for j in br]}")

    denge = saf_nash(U_A, U_B)
    print("\n--- Saf Nash ---")
    if not denge:
        print("  (yok)")
    for i, j in denge:
        print(
            f"  ({STRATEJILER[i]}, {STRATEJILER[j]}) "
            f"→ ödemeler ({U_A[i, j]:g}, {U_B[i, j]:g})"
        )

    # Pareto notu
    print("\nNot: (isbirligi, isbirligi) ödemeleri Nash'ten yüksek olabilir;")
    print("      bireysel teşvik yine de ihanete iter (ikilem).")


if __name__ == "__main__":
    main()
