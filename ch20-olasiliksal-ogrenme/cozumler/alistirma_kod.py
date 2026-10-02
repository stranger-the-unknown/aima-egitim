#!/usr/bin/env python3
"""Bölüm 20 alıştırmaları: kodlu çözümler (A3, A5–A10).

Çalıştırma (bölüm klasöründen):
    python cozumler/alistirma_kod.py
"""
from __future__ import annotations

import math
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "ornekler"))

import em_algoritmasi as em  # noqa: E402
import istatistiksel_ogrenme as io  # noqa: E402
import surekli_modeller as sm  # noqa: E402


# --- A3: önselin etkisi -------------------------------------------------------------------
def a3(esik: float = 0.9) -> dict:
    duzgun = {h: Fraction(1, 5) for h in io.TORBALAR}
    sonuc = {}
    for ad, onsel in (("kitabın önseli", io.ONSEL), ("düzgün önsel", duzgun)):
        N = next(n for n in range(1, 50) if io.sonsal(["limon"] * n, onsel)["h5"] > esik)
        sonuc[ad] = (N, float(io.bayes_tahmini(["limon"], onsel)))
    return sonuc


# --- A5: naif Bayes'in aşırı güveni -----------------------------------------------------------
def a5(kopya_sayilari=(1, 2, 5, 10)) -> dict:
    """Tek bir ipucu: P(belirti | hasta) = 0.8, P(belirti | sağlıklı) = 0.3, P(hasta) = 0.2.
    Aynı belirti k kez (kopya nitelik) sayılırsa naif Bayes sonsalı ne olur?"""
    sonuc = {}
    for k in kopya_sayilari:
        h = 0.2 * 0.8 ** k
        s = 0.8 * 0.3 ** k
        sonuc[k] = h / (h + s)
    return sonuc


# --- A6: Bayesçi regresyonda veri arttıkça -----------------------------------------------------
def a6(tohum: int = 5) -> dict:
    rng = np.random.default_rng(tohum)
    x = rng.uniform(-2, 2, 200)
    y = 0.8 * x + rng.normal(0, 1, 200)
    return {N: sm.bayes_regresyon(x[:N], y[:N], 1.0) for N in (1, 5, 20, 200)}


# --- A7: EM'in ilk adımı ---------------------------------------------------------------------
def a7() -> dict:
    t = em.BASLANGIC
    b1, b2 = em.torba_olasiliklari(t, (1, 1, 1))
    katki = 273 / 1000 * b1 / (b1 + b2)
    return {"273 şekerin katkısı": katki, "θ(1)": em.em_adimi(t)["θ"]}


# --- A8: simetrik başlangıç -------------------------------------------------------------------
def a8() -> dict:
    sonuc = {}
    for ad, bas in (("simetrik (hepsi 0.5)", {k: 0.5 for k in em.BASLANGIC}),
                    ("kitabın başlangıcı", em.BASLANGIC),
                    ("ters başlangıç", {"θ": 0.4, "F1": 0.4, "W1": 0.4, "H1": 0.4, "F2": 0.6, "W2": 0.6, "H2": 0.6})):
        t, L = em.em(bas, 200)[-1]
        sonuc[ad] = ({k: round(v, 3) for k, v in t.items()}, round(L, 3))
    return sonuc


# --- A9: kaç bileşen? -----------------------------------------------------------------------------
def a9(tohum: int = 2) -> dict:
    X, _ = em.karisim_ornekle(800, tohum)
    egitim, test = X[:500], X[500:]
    sonuc = {}
    for k in (1, 2, 3, 4, 6):
        w, mu, Sigma, L = em.gauss_karisimi_em(egitim, k, yineleme=80)
        yog = np.column_stack([w[i] * em.gauss(test, mu[i], Sigma[i]) for i in range(k)]).sum(axis=1)
        sonuc[k] = (L[-1], float(np.log(yog).sum()))
    return sonuc


# --- A10: gizli değişken ve parametre sayısı ---------------------------------------------------------
def a10(belirti_sayilari=(3, 5, 8)) -> dict:
    """3 etken (3 değerli), 3 değerli gizli Hastalık, n belirti. Hastalık çıkarılınca her belirti
    3 etkene ve kendinden önceki bütün belirtilere bağlı olur."""
    sonuc = {}
    for n in belirti_sayilari:
        gizli = em.parametre_sayisi([0, 0, 0, 3] + [1] * n)
        gizlisiz = em.parametre_sayisi([0, 0, 0] + [3 + i for i in range(n)])
        sonuc[n] = (gizli, gizlisiz)
    return sonuc


def main() -> None:
    print("=== A3: önselin etkisi ===")
    for ad, (N, p) in a3().items():
        print(f"  {ad}: P(h5 | d) > 0.9 için {N} limon gerekir;  1 limondan sonra P(limon) = {p:.3f}")

    print("\n=== A5: aynı ipucunu k kez saymak ===")
    for k, p in a5().items():
        print(f"  k = {k:>2}: P(hasta | belirti) = {p:.4f}")

    print("\n=== A6: veri arttıkça Bayesçi eğim (gerçek θ = 0.8) ===")
    for N, (t, v) in a6().items():
        print(f"  N = {N:>3}: θ_N = {t:.3f}, σ_N = {math.sqrt(v):.3f}")

    print("\n=== A7: EM'in ilk adımı ===")
    for k, v in a7().items():
        print(f"  {k}: {v:.5f}")

    print("\n=== A8: başlangıç noktasının etkisi (200 yineleme) ===")
    for ad, (t, L) in a8().items():
        print(f"  {ad:<22}: {t}, L = {L}")

    print("\n=== A9: kaç Gauss bileşeni? (gerçek: 3) ===")
    for k, (Le, Lt) in a9().items():
        print(f"  k = {k}: eğitim log olabilirliği {Le:8.1f}, test {Lt:8.1f}")

    print("\n=== A10: gizli değişkenle ve gizli değişkensiz parametre sayısı ===")
    for n, (g, s) in a10().items():
        print(f"  {n} belirti: gizli değişkenle {g}, gizli değişkensiz {s:,}")


if __name__ == "__main__":
    main()
