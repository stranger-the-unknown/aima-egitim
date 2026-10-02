#!/usr/bin/env python3
"""İyileştiricinin laneti (optimizer's curse, kitaptaki 16.3.3).

k seçeneğin hepsinin gerçek faydası 0, ama her birinin tahmini N(0, 1) hatası taşıyor.
En yüksek tahmini seçersek, seçtiğimizin tahmini ortalamada sıfırdan büyük çıkar ve gerçekleşen
değer bizi hayal kırıklığına uğratır. En büyük tahminin yoğunluğu: k f(x) F(x)^{k−1}.
Kitaptaki değerler: k = 3 için ortalama ~0.85 standart sapma; k = 30 için ~2 katı.

Çalıştırma:
    python iyimserlik_laneti.py
"""
from __future__ import annotations

import math

import numpy as np


def en_buyugun_ortalamasi(k: int, n: int = 20_001, sinir: float = 8.0) -> float:
    """E[max(X1..Xk)], Xi ~ N(0, 1): ∫ x k f(x) F(x)^{k−1} dx (sayısal integral)."""
    x = np.linspace(-sinir, sinir, n)
    f = np.exp(-x ** 2 / 2) / math.sqrt(2 * math.pi)
    F = 0.5 * (1 + np.vectorize(math.erf)(x / math.sqrt(2)))
    yogunluk = k * f * F ** (k - 1)
    return float(np.trapezoid(x * yogunluk, x) if hasattr(np, "trapezoid") else np.trapz(x * yogunluk, x))


def simule_et(k: int, deneme: int = 100_000, tohum: int = 0) -> float:
    rng = np.random.default_rng(tohum)
    return float(rng.normal(size=(deneme, k)).max(axis=1).mean())


def ilac_secimi(aday: int = 2000, hasta: int = 10, gercek: float = 0.7, tohum: int = 1):
    """Bütün ilaçların gerçek başarı oranı 0.7. 10 hastada denenen binlerce aday arasında en iyisi
    ne kadar iyi görünür?"""
    rng = np.random.default_rng(tohum)
    gozlenen = rng.binomial(hasta, gercek, size=aday) / hasta
    return float(gozlenen.max()), int((gozlenen == 1.0).sum())


def main() -> None:
    print("=== Seçilen seçeneğin tahmini ne kadar şişkin? (gerçek fayda 0, hata ~ N(0,1)) ===")
    print("   k    integral   simülasyon")
    for k in (1, 3, 10, 30, 100):
        print(f"  {k:>3}   {en_buyugun_ortalamasi(k):8.3f}   {simule_et(k):8.3f}")
    print("  k = 3: ortalama hayal kırıklığı ~0.85 standart sapma; k = 30: ~2 standart sapma (kitap).")

    print("\n=== İlaç denemesi ===")
    en_iyi, mukemmel = ilac_secimi()
    print(f"  Gerçek başarısı 0.7 olan 2000 aday ilaç, her biri 10 hastada denendi.")
    print(f"  En iyi görünen ilacın gözlenen başarısı: {en_iyi:.0%};  10'da 10 yapan aday: {mukemmel}")
    print("  Seçim sürecinin kendisi yanlılık yaratır. 1000 hastanın 800'ünü iyileştiren bir ilaç,")
    print("  binlerce aday arasından seçilmiş 10'da 9'luk bir ilaçtan muhtemelen daha iyidir (kitap).")
    print("  Çare: Tahminleri Bayesçi olarak önsele doğru 'büzmek' (shrinkage).")


if __name__ == "__main__":
    main()
