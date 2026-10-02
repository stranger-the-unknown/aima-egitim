#!/usr/bin/env python3
"""Sürekli modeller: Gauss için en büyük olabilirlik, Bayesçi doğrusal regresyon,
parametrik olmayan yoğunluk kestirimi (kitaptaki 20.2.4, 20.2.6, 20.2.8).

* Gauss: μ_ML = örnek ortalaması, σ_ML = √(Σ(x − μ)²/N)  (20.4; N'ye bölünür, N − 1'e değil).
* Doğrusal–Gauss modelde (y = θ₁x + θ₂ + Gauss gürültü) θ'lar için en büyük olabilirlik = en küçük kareler.
* Bayesçi doğrusal regresyon (orijinden geçen doğru, y = θx + gürültü, σ bilinen):
      θ_N = (σ² θ₀ + σ₀² Σ xᵢyᵢ) / (σ² + σ₀² Σ xᵢ²),   σ_N² = σ² σ₀² / (σ² + σ₀² Σ xᵢ²).
  Veri orijine yakın toplanırsa σ_N² ≈ σ₀² (eğim az kısıtlanır); geniş yayılırsa σ_N² ≈ σ²/Σxᵢ².
* Yoğunluk kestirimi: k-NN (k = 3 çok sivri, 40 çok düz, 10 iyi) ve çekirdek (Gauss, genişlik w).

Çalıştırma:
    python surekli_modeller.py
"""
from __future__ import annotations

import math

import numpy as np


def gauss_ml(x) -> tuple[float, float]:
    mu = float(np.mean(x))
    return mu, float(np.sqrt(np.mean((x - mu) ** 2)))


def gauss_log_olabilirlik(x, mu: float, sigma: float) -> float:
    return float(np.sum(-0.5 * np.log(2 * np.pi) - np.log(sigma) - (x - mu) ** 2 / (2 * sigma ** 2)))


def dogrusal_gauss_ml(x, y) -> tuple[float, float, float]:
    """θ₁, θ₂ en küçük karelerden; σ artıkların ML standart sapması."""
    A = np.column_stack([x, np.ones_like(x)])
    (t1, t2), *_ = np.linalg.lstsq(A, y, rcond=None)
    return float(t1), float(t2), float(np.sqrt(np.mean((y - (t1 * x + t2)) ** 2)))


def bayes_regresyon(x, y, sigma: float, theta0: float = 0.0, sigma0: float = 10.0) -> tuple[float, float]:
    """Kitaptaki kapalı biçim: (θ_N, σ_N²)."""
    sxy, sxx = float(np.sum(x * y)), float(np.sum(x * x))
    payda = sigma ** 2 + sigma0 ** 2 * sxx
    return (sigma ** 2 * theta0 + sigma0 ** 2 * sxy) / payda, sigma ** 2 * sigma0 ** 2 / payda


def bayes_regresyon_sayisal(x, y, sigma: float, theta0: float = 0.0, sigma0: float = 10.0, n: int = 200_001):
    """Aynı sonsalı ızgarada hesapla (önsel × olabilirlik, normalleştir)."""
    t = np.linspace(-20, 20, n)
    log = -0.5 * ((t - theta0) / sigma0) ** 2 - 0.5 * np.sum((y[None, :] - t[:, None] * x[None, :]) ** 2, axis=1) / sigma ** 2
    p = np.exp(log - log.max())
    p /= np.trapezoid(p, t) if hasattr(np, "trapezoid") else np.trapz(p, t)
    integ = np.trapezoid if hasattr(np, "trapezoid") else np.trapz
    ort = integ(t * p, t)
    return float(ort), float(integ((t - ort) ** 2 * p, t))


def tahmin_varyansi(x_yeni: float, sigma: float, sigmaN2: float) -> float:
    """y_yeni = θ x_yeni + gürültü: Var = x_yeni² σ_N² + σ². Veriden uzaklaştıkça büyür."""
    return x_yeni ** 2 * sigmaN2 + sigma ** 2


# --- Yoğunluk kestirimi --------------------------------------------------------------------
def gercek_yogunluk(X):
    """İki boyutlu iki bileşenli Gauss karışımı."""
    def g(X, mu, s):
        return np.exp(-np.sum((X - mu) ** 2, axis=1) / (2 * s ** 2)) / (2 * math.pi * s ** 2)
    return 0.6 * g(X, np.array([0.3, 0.6]), 0.1) + 0.4 * g(X, np.array([0.7, 0.3]), 0.08)


def ornekle(N: int, rng):
    bilesen = rng.random(N) < 0.6
    return np.where(bilesen[:, None], rng.normal([0.3, 0.6], 0.1, (N, 2)), rng.normal([0.7, 0.3], 0.08, (N, 2)))


def knn_yogunluk(veri, sorgu, k: int):
    """P(x) ≈ (k/N) / V, V: k. komşuya kadar olan dairenin alanı."""
    d = np.sort(np.linalg.norm(veri[None, :, :] - sorgu[:, None, :], axis=2), axis=1)[:, k - 1]
    return (k / len(veri)) / (math.pi * d ** 2)


def cekirdek_yogunluk(veri, sorgu, w: float):
    d2 = np.sum((veri[None, :, :] - sorgu[:, None, :]) ** 2, axis=2)
    return np.mean(np.exp(-d2 / (2 * w ** 2)), axis=1) / (2 * math.pi * w ** 2)


def ortalama_mutlak_hata(tahmin, gercek) -> float:
    return float(np.mean(np.abs(tahmin - gercek)))


def main() -> None:
    rng = np.random.default_rng(0)
    print("=== Gauss için en büyük olabilirlik ===")
    x = rng.normal(5.0, 2.0, 200)
    mu, s = gauss_ml(x)
    print(f"  gerçek μ = 5, σ = 2;  ML: μ = {mu:.3f}, σ = {s:.3f}  (N − 1'li sapma {np.std(x, ddof=1):.3f})")
    print(f"  L(ML) = {gauss_log_olabilirlik(x, mu, s):.2f} ≥ L(5, 2) = {gauss_log_olabilirlik(x, 5, 2):.2f}")

    print("\n=== Doğrusal–Gauss model = en küçük kareler ===")
    xs = rng.uniform(0, 1, 50)
    ys = 0.7 * xs + 0.2 + rng.normal(0, 0.1, 50)
    t1, t2, sg = dogrusal_gauss_ml(xs, ys)
    print(f"  gerçek θ₁ = 0.7, θ₂ = 0.2, σ = 0.1;  ML: θ₁ = {t1:.3f}, θ₂ = {t2:.3f}, σ = {sg:.3f};"
          f"  np.polyfit aynı mı? {np.allclose(np.polyfit(xs, ys, 1), [t1, t2])}")

    print("\n=== Bayesçi doğrusal regresyon (y = θx + gürültü, σ = 1, önsel N(0, 10²)) ===")
    for ad, xv in (("orijine yakın x ∈ [−0.1, 0.1]", rng.uniform(-0.1, 0.1, 20)), ("geniş x ∈ [−3, 3]", rng.uniform(-3, 3, 20))):
        yv = 1.5 * xv + rng.normal(0, 1, len(xv))
        tN, vN = bayes_regresyon(xv, yv, 1.0)
        tS, vS = bayes_regresyon_sayisal(xv, yv, 1.0)
        print(f"  {ad}: θ_N = {tN:.3f}, σ_N = {math.sqrt(vN):.3f}  (sayısal: {tS:.3f}, {math.sqrt(vS):.3f})")
        print(f"      x = 0.5'te tahmin std {math.sqrt(tahmin_varyansi(0.5, 1, vN)):.3f}, x = 10'da {math.sqrt(tahmin_varyansi(10, 1, vN)):.3f}")

    print("\n=== Parametrik olmayan yoğunluk kestirimi (128 örnek) ===")
    veri = ornekle(128, rng)
    izgara = np.array([[a, b] for a in np.linspace(0.05, 0.95, 19) for b in np.linspace(0.05, 0.95, 19)])
    gercek = gercek_yogunluk(izgara)
    for k in (3, 10, 40):
        print(f"  k-NN, k = {k:>2}: ortalama mutlak hata {ortalama_mutlak_hata(knn_yogunluk(veri, izgara, k), gercek):.3f}")
    for w in (0.02, 0.07, 0.20):
        print(f"  çekirdek, w = {w:.2f}: ortalama mutlak hata {ortalama_mutlak_hata(cekirdek_yogunluk(veri, izgara, w), gercek):.3f}")
    print("  Çok küçük k / w: sivri ve gürültülü; çok büyük: aşırı düz. Arada bir değer en iyisi.")


if __name__ == "__main__":
    main()
