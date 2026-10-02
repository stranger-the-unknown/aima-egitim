#!/usr/bin/env python3
"""Bölüm 19 alıştırmaları: kodlu çözümler (A3–A6, A8–A10).

Çalıştırma (bölüm klasöründen):
    python cozumler/alistirma_kod.py
"""
from __future__ import annotations

import math
import random
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "ornekler"))

import dogrusal_modeller as dm  # noqa: E402
import karar_agaci as ka  # noqa: E402
import parametrik_olmayan as po  # noqa: E402
import topluluk as tp  # noqa: E402


# --- A3: Patrons olmadan -----------------------------------------------------------
def a3() -> dict:
    nitelikler = [a for a in ka.SIRA if a != "Pat"]
    agac = ka.agac_ogren(ka.RESTORAN, nitelikler)
    return {"kök": agac[0], "düğüm": ka.dugum_sayisi(agac), "ağaç": agac,
            "Patrons'lı düğüm": ka.dugum_sayisi(ka.agac_ogren(ka.RESTORAN, ka.SIRA))}


# --- A4: χ² anlamlılığı (genel serbestlik derecesi) -----------------------------------------
def ki_kare_kuyruk(x: float, sd: int) -> float:
    """P(χ²_sd ≥ x) = 1 − P(sd/2, x/2); düzenlileştirilmiş alt eksik gama serisi."""
    a, z = sd / 2, x / 2
    if z <= 0:
        return 1.0
    terim = toplam = 1 / a
    n = 1
    while terim > 1e-15 * toplam:
        terim *= z / (a + n)
        toplam += terim
        n += 1
    return 1 - math.exp(-z + a * math.log(z) - math.lgamma(a)) * toplam


def a4() -> dict:
    sonuc = {}
    for a in ka.SIRA:
        d = ka.sapma(a, ka.RESTORAN)
        sd = len([v for v in ka.NITELIKLER[a] if any(x[a] == v for x, _ in ka.RESTORAN)]) - 1
        sonuc[a] = (d, sd, ki_kare_kuyruk(d, sd))
    return sonuc


# --- A5: kazanç oranı -------------------------------------------------------------------------
def a5() -> dict:
    """Her örneğe benzersiz bir 'Kimlik' niteliği ekle. Kazanç en büyük, ama bölünme bilgisi de çok büyük."""
    ornekler = [({**x, "Kimlik": f"k{j}"}, y) for j, (x, y) in enumerate(ka.RESTORAN)]
    ka.NITELIKLER["Kimlik"] = [f"k{j}" for j in range(len(ornekler))]
    try:
        sonuc = {}
        for a in ("Kimlik", "Pat", "Type", "Hun"):
            g = ka.kazanc(a, ornekler)
            oranlar = [sum(x[a] == v for x, _ in ornekler) / len(ornekler) for v in ka.NITELIKLER[a]]
            bolunme = ka.entropi([p for p in oranlar if p > 0])
            sonuc[a] = (g, bolunme, g / bolunme if bolunme else 0.0)
    finally:
        del ka.NITELIKLER["Kimlik"]
    return sonuc


# --- A6: gürültüde χ² budama ---------------------------------------------------------------------
def buda(agac, ornekler, alfa: float = 0.05):
    """Yalnızca yaprak çocukları olan test düğümlerini, Δ anlamlı değilse çoğunluk yaprağıyla değiştir."""
    if isinstance(agac, bool):
        return agac
    A, dallar = agac
    dallar = {v: buda(alt, [(x, y) for x, y in ornekler if x[A] == v], alfa) for v, alt in dallar.items()}
    if all(isinstance(alt, bool) for alt in dallar.values()) and ornekler:
        sd = max(len({x[A] for x, _ in ornekler}) - 1, 1)
        p = sum(y for _, y in ornekler)
        if 0 < p < len(ornekler) and ki_kare_kuyruk(ka.sapma(A, ornekler), sd) > alfa:
            return ka.cogunluk(ornekler)
        if p in (0, len(ornekler)):
            return ka.cogunluk(ornekler)
    return (A, dallar)


def a6(N: int = 200, gurultu: float = 0.2, deneme: int = 10) -> dict:
    sonuc = {"budamasız": [0.0, 0.0, 0.0], "budanmış": [0.0, 0.0, 0.0]}     # eğitim, test, düğüm
    for d in range(deneme):
        rng = random.Random(100 + d)
        egitim = [ka.rastgele_ornek(rng) for _ in range(N)]
        egitim = [(x, (not y) if rng.random() < gurultu else y) for x, y in egitim]
        test = [ka.rastgele_ornek(rng) for _ in range(500)]
        tam = ka.agac_ogren(egitim, ka.SIRA)
        for ad, agac in (("budamasız", tam), ("budanmış", buda(tam, egitim))):
            sonuc[ad][0] += np.mean([ka.siniflandir(agac, x) == y for x, y in egitim]) / deneme
            sonuc[ad][1] += np.mean([ka.siniflandir(agac, x) == y for x, y in test]) / deneme
            sonuc[ad][2] += ka.dugum_sayisi(agac) / deneme
    return sonuc


# --- A8: λ ile seyreklik --------------------------------------------------------------------------
def a8() -> dict:
    rng = np.random.default_rng(3)
    X = rng.normal(size=(80, 8))
    gercek = np.array([0.5, 3.0, -2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    y = gercek[0] + X @ gercek[1:] + rng.normal(0, 0.5, 80)
    sonuc = {}
    for lam in (0.0, 0.05, 0.3, 1.0, 3.0):
        w1 = dm.duzenlilestirilmis(X, y, lam, 1, adim=8000)
        w2 = dm.duzenlilestirilmis(X, y, lam, 2, adim=8000)
        sonuc[lam] = (int(np.sum(np.abs(w1[1:]) < 1e-9)), int(np.sum(np.abs(w2[1:]) < 1e-9)),
                      np.round(w1[1:3], 2).tolist(), np.round(w2[1:3], 2).tolist())
    return sonuc


# --- A9: merkezi kaymış çember ------------------------------------------------------------------------
def a9(tohum: int = 7) -> dict:
    rng = np.random.default_rng(tohum)
    X = rng.uniform(-2, 3, (300, 2))
    r = np.linalg.norm(X - np.array([1.0, 0.5]), axis=1)
    X = X[np.abs(r - 1.2) > 0.1]
    y = np.where(np.linalg.norm(X - np.array([1.0, 0.5]), axis=1) < 1.2, 1, -1)
    ozellikler = {
        "girdi (x₁, x₂)": X,
        "kitaptaki F (x₁², x₂², √2x₁x₂)": po.F(X),
        "(x₁, x₂, x₁² + x₂²)": np.column_stack([X, (X ** 2).sum(axis=1)]),
    }
    return {ad: po.algilayici_ayirir_mi(Z, y, en_cok_tur=300) for ad, Z in ozellikler.items()}


# --- A10: β seçimi ------------------------------------------------------------------------------------
def a10(M_yildiz: float = 250, K: int = 10) -> dict:
    betalar = np.linspace(0.05, 0.99, 95)
    sinirlar = [sum(tp.rwm_siniri(M_yildiz, K, b) * np.array([M_yildiz, 1])) for b in betalar]
    i = int(np.argmin(sinirlar))
    return {"en iyi β": float(betalar[i]), "sınır": float(sinirlar[i]),
            "β = 0.5": float(sum(tp.rwm_siniri(M_yildiz, K, 0.5) * np.array([M_yildiz, 1])))}


def main() -> None:
    print("=== A3: Patrons olmadan öğrenilen ağaç ===")
    s = a3()
    print(f"  kök {s['kök']}, {s['düğüm']} düğüm (Patrons'la {s["Patrons'lı düğüm"]})")
    print(ka.agac_yaz(s["ağaç"], "    "))

    print("\n=== A4: kökte χ² anlamlılığı ===")
    for a, (d, sd, p) in sorted(a4().items(), key=lambda t: t[1][2]):
        print(f"  {a:<5}: Δ = {d:5.2f}, sd = {sd}, p = {p:.3f}{'  ← %5 düzeyinde anlamlı' if p < 0.05 else ''}")

    print("\n=== A5: kazanç oranı ===")
    for a, (g, b, o) in a5().items():
        print(f"  {a:<6}: kazanç {g:.3f}, bölünme bilgisi {b:.3f}, oran {o:.3f}")

    print("\n=== A6: %20 etiket gürültüsünde χ² budama (200 örnek, 10 deneme) ===")
    for ad, (e, t, n) in a6().items():
        print(f"  {ad:<10}: eğitim {e:.3f}, test {t:.3f}, ortalama {n:.0f} düğüm")

    print("\n=== A8: λ ile sıfır ağırlık sayısı (7 ilgisiz nitelikten) ===")
    for lam, (z1, z2, w1, w2) in a8().items():
        print(f"  λ = {lam:<4}: L1 {z1} sıfır, ilgili ağırlıklar {w1};  L2 {z2} sıfır, {w2}")

    print("\n=== A9: merkezi (1, 0.5) olan çember ===")
    for ad, ayrilir in a9().items():
        print(f"  {ad:<34}: doğrusal ayrılabilir mi? {ayrilir}")

    print("\n=== A10: rastgele ağırlıklı çoğunlukta β seçimi (M* = 250, K = 10) ===")
    s = a10()
    print(f"  en iyi β ≈ {s['en iyi β']:.2f}, sınır {s['sınır']:.1f};  β = 0.5 ile sınır {s['β = 0.5']:.1f}")


if __name__ == "__main__":
    main()
