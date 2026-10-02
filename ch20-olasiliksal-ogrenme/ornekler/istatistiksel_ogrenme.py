#!/usr/bin/env python3
"""İstatistiksel öğrenme: Bayesçi, MAP ve en büyük olabilirlik (kitaptaki 20.1–20.2.5).

Kitaptaki şeker torbaları: h1 %100 kirazlı, h2 %75, h3 %50, h4 %25, h5 %0 kirazlı (gerisi limonlu).
Önsel ⟨0.1, 0.2, 0.4, 0.2, 0.1⟩. Torba gerçekte h5 ve art arda limonlu şeker çıkıyor.
  * 1 limondan sonra h3 hâlâ en olası; 2'den sonra h4; 3 ve fazlasından sonra h5.
  * P(sonraki limon): başta 0.5, 1 limondan sonra 0.65, 3 limondan sonra ≈ 0.8 (MAP: 1.0).
En büyük olabilirlik: c kiraz, ℓ limon → θ = c / N. Ambalaj ağı: θ₁ = r_c / c, θ₂ = r_ℓ / ℓ.
Bayesçi parametre öğrenme: Beta(a, b) önseli; kiraz görünce a, limon görünce b bir artar (sanal sayımlar).
Ortalama a/(a+b); Beta(1, 1) düzgün dağılımdır.

Çalıştırma:
    python istatistiksel_ogrenme.py
"""
from __future__ import annotations

import math
from fractions import Fraction

TORBALAR = {"h1": Fraction(1), "h2": Fraction(3, 4), "h3": Fraction(1, 2), "h4": Fraction(1, 4), "h5": Fraction(0)}
ONSEL = {"h1": Fraction(1, 10), "h2": Fraction(2, 10), "h3": Fraction(4, 10), "h4": Fraction(2, 10), "h5": Fraction(1, 10)}


def olabilirlik(h: str, veri: list[str]) -> Fraction:
    """P(d | h) = Π P(d_j | h): örnekler i.i.d."""
    kiraz = TORBALAR[h]
    p = Fraction(1)
    for d in veri:
        p *= kiraz if d == "kiraz" else 1 - kiraz
    return p


def sonsal(veri: list[str], onsel=ONSEL) -> dict:
    """P(h | d) = α P(d | h) P(h)  (20.1)."""
    ham = {h: olabilirlik(h, veri) * onsel[h] for h in TORBALAR}
    z = sum(ham.values())
    return {h: v / z for h, v in ham.items()}


def bayes_tahmini(veri: list[str], onsel=ONSEL) -> Fraction:
    """P(sonraki limon | d) = Σ P(limon | h) P(h | d)  (20.2)."""
    return sum((1 - TORBALAR[h]) * p for h, p in sonsal(veri, onsel).items())


def map_hipotezi(veri: list[str], onsel=ONSEL) -> str:
    s = sonsal(veri, onsel)
    return max(s, key=lambda h: (s[h], h))


def ml_hipotezi(veri: list[str]) -> str:
    return max(TORBALAR, key=lambda h: (olabilirlik(h, veri), h))


def mdl_bitleri(h: str, veri: list[str], onsel=ONSEL) -> float:
    """−log₂ P(d | h) − log₂ P(h): veriyi ve hipotezi kodlamanın bit sayısı (MAP = en az bit)."""
    l = olabilirlik(h, veri)
    return (math.inf if l == 0 else -math.log2(l)) - math.log2(onsel[h])


# --- En büyük olabilirlik --------------------------------------------------------------
def ml_theta(c: int, l: int) -> float:
    return c / (c + l)


def log_olabilirlik(theta: float, c: int, l: int) -> float:
    return c * math.log(theta) + l * math.log(1 - theta)


def ambalaj_ml(sayimlar: dict) -> dict:
    """sayimlar[(tat, ambalaj)]. θ = P(kiraz), θ₁ = P(kırmızı | kiraz), θ₂ = P(kırmızı | limon)."""
    c = sayimlar[("kiraz", "kırmızı")] + sayimlar[("kiraz", "yeşil")]
    l = sayimlar[("limon", "kırmızı")] + sayimlar[("limon", "yeşil")]
    return {"θ": c / (c + l), "θ1": sayimlar[("kiraz", "kırmızı")] / c, "θ2": sayimlar[("limon", "kırmızı")] / l}


def laplace(sayi: int, toplam: int, deger_sayisi: int = 2) -> float:
    """Sayımları 0 yerine 1'den başlatmak: sıfır olasılık sorununu önler."""
    return (sayi + 1) / (toplam + deger_sayisi)


# --- Bayesçi parametre öğrenme: Beta ---------------------------------------------------------
def beta_guncelle(a: float, b: float, veri: list[str]) -> tuple[float, float]:
    for d in veri:
        if d == "kiraz":
            a += 1
        else:
            b += 1
    return a, b


def beta_ortalama(a: float, b: float) -> float:
    return a / (a + b)


def beta_varyans(a: float, b: float) -> float:
    return a * b / ((a + b) ** 2 * (a + b + 1))


def main() -> None:
    print("=== Şeker torbaları: art arda limonlu şekerler (kitaptaki Şekil 20.1) ===")
    print("   N   " + "  ".join(f"P({h}|d)" for h in TORBALAR) + "   P(limon)  MAP  ML")
    for N in range(0, 11):
        veri = ["limon"] * N
        s = sonsal(veri)
        print(f"  {N:>2}   " + "  ".join(f"{float(s[h]):7.4f}" for h in TORBALAR)
              + f"   {float(bayes_tahmini(veri)):7.4f}   {map_hipotezi(veri)}   {ml_hipotezi(veri) if N else '-'}")
    print("  3 limondan sonra MAP öğrenen 'sonraki kesin limon' (1.0) der; Bayesçi tahmin ≈ 0.8.")
    veri = ["limon"] * 3
    print("  MDL bakışı (3 limon): " + ", ".join(f"{h}: {mdl_bitleri(h, veri):.2f} bit" for h in TORBALAR))

    print("\n=== En büyük olabilirlik ===")
    print(f"  7 kiraz, 3 limon: θ_ML = {ml_theta(7, 3):.2f};  L(0.7) = {log_olabilirlik(0.7, 7, 3):.3f} > "
          f"L(0.5) = {log_olabilirlik(0.5, 7, 3):.3f}")
    print(f"  1 kiraz, 0 limon: θ_ML = {ml_theta(1, 0):.2f} (aşırı emin);  Laplace: {laplace(1, 1):.2f}")
    sayim = {("kiraz", "kırmızı"): 30, ("kiraz", "yeşil"): 10, ("limon", "kırmızı"): 6, ("limon", "yeşil"): 54}
    print(f"  Ambalaj ağı, sayımlar {sayim}:")
    print(f"    {ambalaj_ml(sayim)}  (her parametre kendi sayımlarından: olabilirlik ayrışır)")

    print("\n=== Bayesçi parametre öğrenme: Beta önseli ===")
    a, b = 1, 1
    for parca in (["kiraz"] * 2, ["kiraz"] * 3 + ["limon"], ["kiraz"] * 24 + ["limon"] * 8):
        a, b = beta_guncelle(a, b, parca)
        print(f"  Beta({a}, {b}): ortalama {beta_ortalama(a, b):.3f}, std {beta_varyans(a, b) ** 0.5:.3f}")
    print("  Kitaptaki dizi: Beta(3,1), Beta(6,2), Beta(30,10). Oran %75'te sabit, dağılım 0.75 çevresinde daralıyor.")


if __name__ == "__main__":
    main()
