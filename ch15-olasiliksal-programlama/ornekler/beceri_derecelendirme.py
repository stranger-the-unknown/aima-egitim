#!/usr/bin/env python3
"""Oyuncu becerisini derecelendirme (kitaptaki 15.1.2), olabilirlik ağırlıklandırmayla.

RPM:
    Skill(i)          ~ N(μ, σ²)
    Performance(i, g) ~ N(Skill(i), β²)
    Win(i, j, g)      = Performance(i, g) > Performance(j, g)
Performanslar gözlenmez; onlar üzerinden integral alınınca:
    P(i, j'yi yener | beceriler) = Φ((Skill(i) − Skill(j)) / (β √2))
Sayılar (μ = 25, σ = 25/3, β = 25/6) TrueSkill'in yaygın varsayılanlarıdır; kitap sayı vermez.

Çıkarım: Becerileri önselden örnekle, her örneği gözlenen sonuçların olasılığıyla ağırlıklandır.

Çalıştırma:
    python beceri_derecelendirme.py
"""
from __future__ import annotations

import math

import numpy as np

MU, SIGMA, BETA = 25.0, 25 / 3, 25 / 6
OYUNCULAR = ["Ayşe", "Burak", "Ceren", "Deniz"]
# (kazanan, kaybeden)
MACLAR = [("Ayşe", "Burak"), ("Burak", "Ceren"), ("Ceren", "Deniz"), ("Ayşe", "Ceren"),
          ("Deniz", "Burak"), ("Ayşe", "Deniz")]


def phi(x):
    """Standart normal birikimli dağılım (numpy dizileri için)."""
    return 0.5 * (1 + np.vectorize(math.erf)(x / math.sqrt(2)))


def sonsal_beceri(maclar=MACLAR, oyuncular=OYUNCULAR, N: int = 200_000, tohum: int = 0):
    rng = np.random.default_rng(tohum)
    idx = {o: i for i, o in enumerate(oyuncular)}
    beceri = rng.normal(MU, SIGMA, size=(N, len(oyuncular)))
    logw = np.zeros(N)
    for kazanan, kaybeden in maclar:
        fark = beceri[:, idx[kazanan]] - beceri[:, idx[kaybeden]]
        logw += np.log(np.clip(phi(fark / (BETA * math.sqrt(2))), 1e-300, None))
    w = np.exp(logw - logw.max())
    w /= w.sum()
    ort = w @ beceri
    std = np.sqrt(w @ (beceri - ort) ** 2)
    etkin = 1 / np.sum(w ** 2)
    return {o: (ort[i], std[i]) for o, i in idx.items()}, beceri, w, etkin


def kazanma_olasiligi(beceri, w, i: int, j: int) -> float:
    return float(w @ phi((beceri[:, i] - beceri[:, j]) / (BETA * math.sqrt(2))))


def main() -> None:
    print("Maçlar: " + ", ".join(f"{a} > {b}" for a, b in MACLAR))
    sonuc, beceri, w, etkin = sonsal_beceri()
    print(f"\n=== Sonsal beceri (önsel N({MU:.0f}, {SIGMA:.2f}²)), etkin örnek sayısı ≈ {etkin:,.0f} ===")
    for o, (m, s) in sorted(sonuc.items(), key=lambda x: -x[1][0]):
        print(f"  {o:<6} ortalama {m:5.2f}   std {s:4.2f}")
    print("  Burak, Ceren ve Deniz birbirini döngüsel yendi (B > C > D > B) ve üçü de Ayşe'ye kaybetti:")
    print("  Model üçünü eşit görür. Belirsizlik (std) önseldeki 8.33'ten düştü, ama 6 maç az.")

    print("\n=== Yeni bir maçın tahmini ===")
    for a, b in (("Ayşe", "Deniz"), ("Burak", "Deniz"), ("Ceren", "Burak")):
        p = kazanma_olasiligi(beceri, w, OYUNCULAR.index(a), OYUNCULAR.index(b))
        print(f"  P({a} > {b}) = {p:.3f}")


if __name__ == "__main__":
    main()
