#!/usr/bin/env python3
"""Bilinmeyen tercihler (kitaptaki 16.7).

1. Kendi tercihinden emin olmamak — durian dondurması: İki çeşit kaldı, ikisi de 2 $.
   Vanilya: 3 $ değerinde → net +1 $. Durian: %50 bayılırsın (+100 $ → net +98), %50 nefret edersin
   (−80 $ → net −82). EU(durian) = +8 > EU(vanilya) = +1. Belirsizlik fayda fonksiyonundan
   yeni bir rastgele değişkene (LikesDurian) taşınabilir.

2. İnsana saygı — kapatma düğmesi oyunu: Robbie, Harriet için otel ayarlayacak. Otelin Harriet'e
   değeri u ~ U[−40, 60] (ortalama +10).
       hemen yap: E[u] = +10      kendini kapat: 0
       bekle ve Harriet'e bırak: Harriet u < 0 ise kapatır  → E[max(u, 0)] = 0.4 × 0 + 0.6 × 30 = +18
   Beklemenin değeri = E[max(u, 0)] − max(E[u], 0) ≥ 0: Harriet'in kararının Robbie için bilgi değeri.
   Robbie Harriet'in ne isteyeceğinden emin olduğu anda (σ → 0) bu değer sıfıra iner.

Çalıştırma:
    python bilinmeyen_tercihler.py
"""
from __future__ import annotations

import math


def durian() -> dict:
    return {"vanilya": 1.0, "durian": 0.5 * 98 + 0.5 * (-82)}


def tekduze_oyun(a: float, b: float) -> dict:
    """u ~ U[a, b] için üç seçeneğin değeri (kesin formüller)."""
    ort = (a + b) / 2
    if b <= 0:
        bekle = 0.0
    elif a >= 0:
        bekle = ort
    else:
        bekle = (b / (b - a)) * (b / 2)   # P(u > 0) × E[u | u > 0]
    return {"hemen yap": ort, "kendini kapat": 0.0, "bekle": bekle}


def normal_oyun(mu: float, sigma: float) -> dict:
    """u ~ N(μ, σ²): E[max(u, 0)] = μ Φ(μ/σ) + σ φ(μ/σ)."""
    if sigma == 0:
        return {"hemen yap": mu, "kendini kapat": 0.0, "bekle": max(mu, 0.0)}
    z = mu / sigma
    phi = math.exp(-z * z / 2) / math.sqrt(2 * math.pi)
    Phi = 0.5 * (1 + math.erf(z / math.sqrt(2)))
    return {"hemen yap": mu, "kendini kapat": 0.0, "bekle": mu * Phi + sigma * phi}


def main() -> None:
    print("=== Durian mı, vanilya mı? ===")
    for k, v in durian().items():
        print(f"  EU({k}) = {v:+.0f} $")
    print("  Tercihinden emin olmasan bile beklenen faydası yüksek olan seçilir: durian.")
    print("  Yiyince LikesDurian öğrenilir; bu bilginin gelecekteki seçimler için de değeri var.")

    print("\n=== Kapatma düğmesi oyunu (kitap) ===")
    for a, b in ((-40, 60), (-60, 40)):
        d = tekduze_oyun(a, b)
        print(f"  u ~ U[{a}, {b}]: " + ", ".join(f"{k} {v:+.1f}" for k, v in d.items()))
    print("  İki durumda da beklemek en iyisi: Harriet'in kararı Robbie'ye bilgi verir.")

    print("\n=== Belirsizlik azalınca saygı gösterme isteği azalır (u ~ N(10, σ²)) ===")
    for sigma in (50, 20, 10, 5, 1, 0):
        d = normal_oyun(10, sigma)
        print(f"  σ = {sigma:>2}: hemen yap {d['hemen yap']:+.2f}, bekle {d['bekle']:+.2f},"
              f" beklemenin fazlası {d['bekle'] - max(d['hemen yap'], 0):.3f}")
    print("  Robbie Harriet'in tercihlerinden kesin emin olursa danışmanın hiçbir faydası kalmaz.")
    print("  Bu, tercihleri belirsiz tutmanın güvenli yapay zekâ için neden önemli olduğunu gösterir.")


if __name__ == "__main__":
    main()
