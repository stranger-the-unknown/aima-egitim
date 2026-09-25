#!/usr/bin/env python3
"""Koşullu dağılımları verimli temsil etmek (kitaptaki 13.2.2 ve 13.2.3).

1. Gürültülü-VEYA: Fever ← Cold, Flu, Malaria. Engelleme olasılıkları
   q_cold = 0.6, q_flu = 0.2, q_malaria = 0.1. Tam tablo 2³ = 8 satır, ama yalnızca 3 sayı yeter:
       P(¬fever | nedenler) = Π_{doğru nedenler} q_j
   Kitaptaki tablo: fff 0.0, fft 0.9, ftf 0.8, ftt 0.98, tff 0.4, tft 0.94, ttf 0.88, ttt 0.988

2. Sürekli ebeveyn, ayrık çocuk: Buys ← Cost. Eşik maliyet ~ N(μ = 6.0, σ = 1.0).
       probit:  P(buys | c) = Φ((−c + μ) / σ)
       expit :  P(buys | c) = 1 / (1 + exp(−(4/√(2π)) (−c + μ) / σ))   (eğimler ortalamada eşit)
   İki eğri benzer, ama expit'in kuyrukları çok daha kalındır.

Çalıştırma:
    python yerel_dagilimlar.py
"""
from __future__ import annotations

import math

from bayes_agi import gurultulu_or

Q_ATES = {"Cold": 0.6, "Flu": 0.2, "Malaria": 0.1}
MU, SIGMA = 6.0, 1.0


def probit(c: float, mu: float = MU, sigma: float = SIGMA) -> float:
    return 0.5 * (1 + math.erf((-c + mu) / (sigma * math.sqrt(2))))


def expit(c: float, mu: float = MU, sigma: float = SIGMA) -> float:
    return 1 / (1 + math.exp(-(4 / math.sqrt(2 * math.pi)) * (-c + mu) / sigma))


def main() -> None:
    print("=== Gürültülü-VEYA: P(Fever | Cold, Flu, Malaria) ===")
    cpt = gurultulu_or(Q_ATES)
    print("  Cold  Flu   Malaria  P(fever)  P(¬fever)")
    for anahtar in sorted(cpt, key=lambda k: tuple(int(v) for v in k)):
        tf = "  ".join(f"{'t' if v else 'f':<4}" for v in anahtar)
        print(f"  {tf}     {cpt[anahtar]:.3f}     {1 - cpt[anahtar]:.3f}")
    for k in (3, 10, 20):
        print(f"  {k} neden: tam CPT {2 ** k:>9,} satır, gürültülü-VEYA {k} parametre")
    print("  Varsayımlar: (1) listelenen nedenler dışında neden yok (gerekirse 'sızıntı' düğümü eklenir),")
    print("  (2) her nedenin etkiyi engelleyen mekanizması diğerlerinden bağımsız.")

    print("\n=== Sürekli ebeveyn: P(buys | Cost = c), μ = 6, σ = 1 ===")
    print("   c    probit   expit")
    for c in (3, 4, 5, 6, 7, 8, 9, 10):
        print(f"  {c:>2}   {probit(c):.4f}   {expit(c):.4f}")
    print("  Ortalamada ikisi de 0.5 ve aynı eğimde. c = 10'da probit ≈ 3e-5, expit ≈ 3e-3:")
    print("  expit'in kuyrukları çok daha uzun.")


if __name__ == "__main__":
    main()
