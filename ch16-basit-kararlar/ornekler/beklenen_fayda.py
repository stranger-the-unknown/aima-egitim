#!/usr/bin/env python3
"""Beklenen fayda (MEU) — piyango ve tıbbi tedavi örnekleri.

Özgün eğitim senaryoları; kitap metni yok.
numpy ile vektör hesap; çıktılar Türkçe.

Resmi referans: https://aima.cs.berkeley.edu/ · https://github.com/aimacode
"""
from __future__ import annotations

import numpy as np


def eu(olasiliklar: np.ndarray, faydalar: np.ndarray) -> float:
    """EU = Σ P(s) U(s)."""
    return float(np.dot(olasiliklar, faydalar))


def piyango_ornek() -> None:
    print("=== Piyango: iki bilet ===")
    u_a = eu(np.array([0.5, 0.5]), np.array([10.0, 0.0]))
    u_b = eu(np.array([1.0]), np.array([4.0]))
    print(f"  Bilet A EU = {u_a:.2f}")
    print(f"  Bilet B EU = {u_b:.2f}")
    print(f"  MEU seçimi: {'A' if u_a > u_b else 'B'}")
    print()


def tibbi_tedavi_ornek() -> None:
    print("=== Tıbbi karar: tedavi mi, bekle mi? ===")
    p_hasta = 0.3
    p_saglikli = 1.0 - p_hasta
    U = {
        "tedavi": np.array([70.0, 75.0]),
        "bekle": np.array([20.0, 95.0]),
    }
    sonuclar = []
    for eylem, faydalar in U.items():
        p = np.array([p_hasta, p_saglikli])
        deger = eu(p, faydalar)
        sonuclar.append((eylem, deger))
        print(f"  EU({eylem}) = {deger:.2f}")
    en_iyi = max(sonuclar, key=lambda t: t[1])
    print(f"  → MEU eylem: {en_iyi[0]} (EU={en_iyi[1]:.2f})")
    print()


def risk_kacinma_kisa() -> None:
    print("=== Risk kaçınma (kısa) ===")
    eu_riskli = 0.5 * np.sqrt(100) + 0.5 * np.sqrt(0)
    eu_kesin = np.sqrt(50)
    print(f"  Riskli kura EU (√para) = {eu_riskli:.2f}")
    print(f"  Kesin 50 TL faydası     = {eu_kesin:.2f}")
    print(f"  Risk kaçınan seçer: {'kesin' if eu_kesin > eu_riskli else 'riskli'}")
    print()


def main() -> None:
    print("Beklenen fayda / MEU demosu\n")
    piyango_ornek()
    tibbi_tedavi_ornek()
    risk_kacinma_kisa()
    print("Bitti. Kaynak: aima.cs.berkeley.edu · aimacode")


if __name__ == "__main__":
    main()
