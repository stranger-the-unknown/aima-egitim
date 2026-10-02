#!/usr/bin/env python3
"""Naif Bayes öğrenme; üretici ve ayırt edici modeller (kitaptaki 20.2.2–20.2.3).

* Naif Bayes: P(C | x₁..xₙ) = α P(C) Π P(xᵢ | C). n Boolean nitelikte 2n + 1 parametre, arama yok.
  Restoran probleminde (Bölüm 19) öğrenme eğrisi karar ağacınınkinden aşağıda kalır, çünkü gerçek
  hipotez bir karar ağacıdır ve naif Bayes onu tam temsil edemez (kitaptaki Şekil 20.3).
* Üretici (naif Bayes) ve ayırt edici (lojistik regresyon) modeller: Az veride üretici, çok veride
  ayırt edici model çoğu zaman daha iyidir (kitap: Ng ve Jordan, 2002).

Çalıştırma:
    python naif_bayes.py
"""
from __future__ import annotations

import math
import random
import sys
from collections import Counter
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "ch19-ogrenme-orneklerden" / "ornekler"))

import karar_agaci as ka  # noqa: E402  (Bölüm 19'un restoran verisi ve ağaç öğrenicisi)


def naif_bayes_ogren(ornekler, nitelikler: dict, m: float = 1.0):
    """En büyük olabilirlik + m-tahmini (Laplace, m = 1): sayımlar 0 yerine m'den başlar."""
    sinif = Counter(y for _, y in ornekler)
    onsel = {c: (sinif[c] + m) / (len(ornekler) + 2 * m) for c in (True, False)}
    kosullu = {}
    for a, degerler in nitelikler.items():
        for c in (True, False):
            sayim = Counter(x[a] for x, y in ornekler if y == c)
            for v in degerler:
                kosullu[(a, v, c)] = (sayim[v] + m) / (sinif[c] + m * len(degerler))
    return onsel, kosullu


def naif_bayes_sonsal(model, x: dict) -> float:
    """P(C = true | x)."""
    onsel, kosullu = model
    log = {c: math.log(onsel[c]) + sum(math.log(kosullu[(a, v, c)]) for a, v in x.items()) for c in (True, False)}
    m = max(log.values())
    p = {c: math.exp(l - m) for c, l in log.items()}
    return p[True] / (p[True] + p[False])


def ogrenme_egrileri(boyutlar=(5, 10, 20, 40, 80), deneme: int = 20, tohum: int = 0) -> dict:
    rng = random.Random(tohum)
    sonuc = {N: [0.0, 0.0] for N in boyutlar}
    for N in boyutlar:
        for _ in range(deneme):
            veri = [ka.rastgele_ornek(rng) for _ in range(100)]
            egitim, test = veri[:N], veri[N:]
            nb = naif_bayes_ogren(egitim, ka.NITELIKLER)
            agac = ka.agac_ogren(egitim, ka.SIRA)
            sonuc[N][0] += np.mean([(naif_bayes_sonsal(nb, x) >= 0.5) == y for x, y in test]) / deneme
            sonuc[N][1] += np.mean([ka.siniflandir(agac, x) == y for x, y in test]) / deneme
    return sonuc


# --- Üretici ve ayırt edici ------------------------------------------------------------------
def ikili_veri(N: int, rng: np.random.Generator, n: int = 15):
    """Gerçek model naif Bayes değil: nitelikler sınıf verildiğinde ilişkili (gizli ortak etken)."""
    y = rng.random(N) < 0.5
    z = rng.random(N) < 0.5                                     # nitelikleri birlikte etkileyen etken
    p = np.where(y[:, None], 0.6, 0.4) + np.where(z[:, None], 0.25, -0.25) * (np.arange(n) % 2 == 0)
    X = rng.random((N, n)) < np.clip(p, 0.05, 0.95)
    return X.astype(float), y


def lojistik_ogren(X, y, adim: int = 3000, alfa: float = 0.5, lam: float = 1e-3):
    X1 = np.column_stack([np.ones(len(X)), X])
    w = np.zeros(X1.shape[1])
    for _ in range(adim):
        h = 1 / (1 + np.exp(-X1 @ w))
        w += alfa * (X1.T @ (y - h) / len(y) - lam * w)
    return w


def ikili_naif_bayes(X, y):
    p1 = (X[y].sum(axis=0) + 1) / (y.sum() + 2)
    p0 = (X[~y].sum(axis=0) + 1) / ((~y).sum() + 2)
    onsel = (y.sum() + 1) / (len(y) + 2)
    return onsel, p1, p0


def ikili_naif_bayes_tahmin(model, X):
    onsel, p1, p0 = model
    l1 = math.log(onsel) + X @ np.log(p1) + (1 - X) @ np.log(1 - p1)
    l0 = math.log(1 - onsel) + X @ np.log(p0) + (1 - X) @ np.log(1 - p0)
    return l1 > l0


def uretici_ayirtedici(boyutlar=(10, 30, 100, 1000, 5000), deneme: int = 6, tohum: int = 3) -> dict:
    rng = np.random.default_rng(tohum)
    Xt, yt = ikili_veri(5000, rng)
    sonuc = {}
    for N in boyutlar:
        nb = lr = 0.0
        for _ in range(deneme):
            X, y = ikili_veri(N, rng)
            nb += np.mean(ikili_naif_bayes_tahmin(ikili_naif_bayes(X, y), Xt) == yt) / deneme
            w = lojistik_ogren(X, y)
            lr += np.mean(((np.column_stack([np.ones(len(Xt)), Xt]) @ w) > 0) == yt) / deneme
        sonuc[N] = (nb, lr)
    return sonuc


def main() -> None:
    print("=== Naif Bayes, restoran verisi (12 örnek) ===")
    model = naif_bayes_ogren(ka.RESTORAN, ka.NITELIKLER)
    dogru = sum((naif_bayes_sonsal(model, x) >= 0.5) == y for x, y in ka.RESTORAN)
    print(f"  Eğitim doğruluğu {dogru}/12. Boolean niteliklerde parametre sayısı 2n + 1 (n = 10 → 21).")
    for j in (0, 4, 8):
        x, y = ka.RESTORAN[j]
        print(f"  x{j + 1}: P(WillWait | x) = {naif_bayes_sonsal(model, x):.3f}  (gerçek {'Yes' if y else 'No'})")

    print("\n=== Öğrenme eğrileri (gerçek ağaçtan örnekler, 20 deneme) ===")
    print("   N   naif Bayes   karar ağacı")
    for N, (nb, ag) in ogrenme_egrileri().items():
        print(f"  {N:>3}   {nb:10.3f}   {ag:11.3f}")
    print("  Naif Bayes her boyutta ağacın altında kalır ve ~%87'de doyar: Gerçek fonksiyon bir karar ağacıdır,")
    print("  naif Bayes onu tam temsil edemez (kitaptaki Şekil 20.3).")

    print("\n=== Üretici (naif Bayes) ve ayırt edici (lojistik regresyon) ===")
    print("    N    naif Bayes   lojistik")
    for N, (nb, lr) in uretici_ayirtedici().items():
        print(f"  {N:>5}   {nb:10.3f}   {lr:8.3f}")
    print("  Az veride üretici model, çok veride (varsayımı yanlışsa) ayırt edici model önde.")


if __name__ == "__main__":
    main()
