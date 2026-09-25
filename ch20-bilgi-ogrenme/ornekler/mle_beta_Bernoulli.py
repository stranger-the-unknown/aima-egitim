#!/usr/bin/env python3
"""Bernoulli MLE ve Beta-önsel MAP sezgisi.

Özgün eğitim demosu. numpy OK. Kitap metni yok.

https://aima.cs.berkeley.edu/ · https://github.com/aimacode
"""
from __future__ import annotations

import numpy as np


def mle_bernoulli(k: int, n: int) -> float:
    """N denemede k başarı → θ_MLE = k/N."""
    if n <= 0:
        raise ValueError("n > 0 olmalı")
    return k / n


def map_beta_bernoulli(k: int, n: int, alpha: float = 2.0, beta: float = 2.0) -> float:
    """Beta(α,β) önseli ile MAP (mod). α,β > 1 varsayımı."""
    return (k + alpha - 1.0) / (n + alpha + beta - 2.0)


def kategorik_mle(sayimlar: np.ndarray) -> np.ndarray:
    """Zar / kategorik: θ_i = n_i / Σ n_j."""
    sayimlar = np.asarray(sayimlar, dtype=float)
    toplam = sayimlar.sum()
    if toplam <= 0:
        raise ValueError("toplam sayım > 0 olmalı")
    return sayimlar / toplam


def main() -> None:
    print("=== Bernoulli MLE / Beta-MAP ===\n")
    k, n = 28, 40
    theta_mle = mle_bernoulli(k, n)
    print(f"Veri: {k} yazı / {n} atış")
    print(f"θ_MLE = {theta_mle:.4f}")

    for a, b in [(1.0, 1.0), (2.0, 2.0), (10.0, 10.0)]:
        if a <= 1 or b <= 1:
            theta_map = theta_mle
            etiket = "düzgün (≈MLE)"
        else:
            theta_map = map_beta_bernoulli(k, n, a, b)
            etiket = f"Beta({a:g},{b:g})"
        print(f"θ_MAP [{etiket}] = {theta_map:.4f}")

    print("\n--- Kategorik (zar) MLE ---")
    sayim = np.array([3, 7, 2, 5, 4, 9])
    theta = kategorik_mle(sayim)
    print(f"Sayımlar: {sayim.tolist()} (toplam {int(sayim.sum())})")
    print(f"θ_MLE   : {np.round(theta, 4).tolist()}")
    print(f"Σθ      : {theta.sum():.6f}  (1 olmalı)")
    print("\nNot: Az veride MAP / önsel aşırı 0-1 tahmini yumuşatır.")


if __name__ == "__main__":
    main()
