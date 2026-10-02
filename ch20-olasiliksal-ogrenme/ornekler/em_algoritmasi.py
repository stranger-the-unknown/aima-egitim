#!/usr/bin/env python3
"""Gizli değişkenlerle öğrenme: EM algoritması (kitaptaki 20.3).

1. Karışmış iki şeker torbası (Şekil 20.14(a)): Torba gizli; her şekerin tadı (kiraz/limon), ambalajı
   (kırmızı/yeşil) ve deliği (var/yok) gözlenir. Torba verildiğinde nitelikler bağımsız (naif Bayes).
   Kitaptaki 1000 şekerlik sayımlar ve başlangıç değerleri (θ = 0.6, θ_F1 = θ_W1 = θ_H1 = 0.6,
   θ_F2 = θ_W2 = θ_H2 = 0.4) ile ilk yinelemeden sonra (testlerle doğrulanır):
       θ = 0.6124, θF1 = 0.6684, θW1 = 0.6483, θH1 = 0.6558, θF2 = 0.3887, θW2 = 0.3817, θH2 = 0.3827
   Log olabilirlik ≈ −2044'ten ≈ −2021'e çıkar; 10. yinelemede gerçek modelinkini (−1982.214) geçer.
2. Gauss karışımı (20.3.1): E adımı sorumluluklar p_ij, M adımı ağırlıklı ortalama, kovaryans, ağırlık.
3. Gizli değişkenin faydası (Şekil 20.11): Kalp hastalığı ağı 78 parametre; gizli düğüm çıkarılırsa 708.

Çalıştırma:
    python em_algoritmasi.py
"""
from __future__ import annotations

import itertools
import math

import numpy as np

# (tat kiraz mı, ambalaj kırmızı mı, delik var mı) → sayı  (kitaptaki tablo)
SAYIMLAR = {
    (1, 1, 1): 273, (1, 1, 0): 93, (1, 0, 1): 104, (1, 0, 0): 90,
    (0, 1, 1): 79, (0, 1, 0): 100, (0, 0, 1): 94, (0, 0, 0): 167,
}
GERCEK = {"θ": 0.5, "F1": 0.8, "W1": 0.8, "H1": 0.8, "F2": 0.3, "W2": 0.3, "H2": 0.3}
BASLANGIC = {"θ": 0.6, "F1": 0.6, "W1": 0.6, "H1": 0.6, "F2": 0.4, "W2": 0.4, "H2": 0.4}


def _p(deger: int, theta: float) -> float:
    return theta if deger else 1 - theta


def torba_olasiliklari(t: dict, seker: tuple) -> tuple[float, float]:
    """(P(şeker, Bag = 1), P(şeker, Bag = 2))."""
    f, w, h = seker
    b1 = t["θ"] * _p(f, t["F1"]) * _p(w, t["W1"]) * _p(h, t["H1"])
    b2 = (1 - t["θ"]) * _p(f, t["F2"]) * _p(w, t["W2"]) * _p(h, t["H2"])
    return b1, b2


def log_olabilirlik(t: dict, sayimlar=SAYIMLAR) -> float:
    return sum(n * math.log(sum(torba_olasiliklari(t, s))) for s, n in sayimlar.items())


def em_adimi(t: dict, sayimlar=SAYIMLAR) -> dict:
    """E: her şeker türü için P(Bag = 1 | şeker); M: beklenen sayımları normalleştir."""
    N = sum(sayimlar.values())
    n1 = 0.0
    beklenen = {"F1": 0.0, "W1": 0.0, "H1": 0.0, "F2": 0.0, "W2": 0.0, "H2": 0.0}
    for (f, w, h), n in sayimlar.items():
        b1, b2 = torba_olasiliklari(t, (f, w, h))
        r1 = b1 / (b1 + b2)
        n1 += n * r1
        for ad, deger in (("F", f), ("W", w), ("H", h)):
            beklenen[ad + "1"] += n * r1 * deger
            beklenen[ad + "2"] += n * (1 - r1) * deger
    n2 = N - n1
    yeni = {"θ": n1 / N}
    for ad in ("F", "W", "H"):
        yeni[ad + "1"] = beklenen[ad + "1"] / n1
        yeni[ad + "2"] = beklenen[ad + "2"] / n2
    return yeni


def em(t: dict = BASLANGIC, yineleme: int = 10, sayimlar=SAYIMLAR) -> list[tuple[dict, float]]:
    gecmis = [(dict(t), log_olabilirlik(t, sayimlar))]
    for _ in range(yineleme):
        t = em_adimi(t, sayimlar)
        gecmis.append((t, log_olabilirlik(t, sayimlar)))
    return gecmis


def iki_nitelik_em(t: dict, yineleme: int = 500) -> tuple[dict, float]:
    """Delik niteliği atılınca (yalnızca tat ve ambalaj) aynı EM."""
    sayim = {}
    for (f, w, h), n in SAYIMLAR.items():
        sayim[(f, w)] = sayim.get((f, w), 0) + n

    def ortak(t, f, w):
        return (t["θ"] * _p(f, t["F1"]) * _p(w, t["W1"]), (1 - t["θ"]) * _p(f, t["F2"]) * _p(w, t["W2"]))

    N = sum(sayim.values())
    for _ in range(yineleme):
        n1 = f1 = w1 = f2 = w2 = 0.0
        for (f, w), n in sayim.items():
            b1, b2 = ortak(t, f, w)
            r = b1 / (b1 + b2)
            n1 += n * r
            f1, w1 = f1 + n * r * f, w1 + n * r * w
            f2, w2 = f2 + n * (1 - r) * f, w2 + n * (1 - r) * w
        t = {"θ": n1 / N, "F1": f1 / n1, "W1": w1 / n1, "F2": f2 / (N - n1), "W2": w2 / (N - n1)}
    L = sum(n * math.log(sum(ortak(t, f, w))) for (f, w), n in sayim.items())
    return t, L


# --- Gauss karışımı ------------------------------------------------------------------------
def gauss(x, mu, Sigma):
    d = x.shape[1]
    fark = x - mu
    ters = np.linalg.inv(Sigma)
    us = -0.5 * np.einsum("ij,jk,ik->i", fark, ters, fark)
    return np.exp(us) / math.sqrt((2 * math.pi) ** d * np.linalg.det(Sigma))


def gauss_karisimi_em(X, k: int, yineleme: int = 50, tohum: int = 0):
    """(ağırlıklar, ortalamalar, kovaryanslar, log olabilirlik geçmişi)."""
    rng = np.random.default_rng(tohum)
    N, d = X.shape
    w = np.full(k, 1 / k)
    mu = X[rng.choice(N, k, replace=False)]
    Sigma = np.array([np.cov(X.T) for _ in range(k)])
    gecmis = []
    for _ in range(yineleme):
        yog = np.column_stack([w[i] * gauss(X, mu[i], Sigma[i]) for i in range(k)])
        gecmis.append(float(np.log(yog.sum(axis=1)).sum()))
        p = yog / yog.sum(axis=1, keepdims=True)                 # E: sorumluluklar p_ij
        n = p.sum(axis=0)                                        # M
        mu = (p.T @ X) / n[:, None]
        Sigma = np.array([((p[:, i, None] * (X - mu[i])).T @ (X - mu[i])) / n[i] + 1e-6 * np.eye(d) for i in range(k)])
        w = n / N
    return w, mu, Sigma, gecmis


def karisim_ornekle(N: int = 500, tohum: int = 1):
    rng = np.random.default_rng(tohum)
    agirlik = np.array([0.2, 0.3, 0.5])
    mu = np.array([[0.2, 0.7], [0.5, 0.25], [0.8, 0.65]])
    Sigma = np.array([[[0.005, 0.0], [0.0, 0.01]], [[0.01, 0.004], [0.004, 0.006]], [[0.008, -0.003], [-0.003, 0.01]]])
    bilesen = rng.choice(3, N, p=agirlik)
    X = np.array([rng.multivariate_normal(mu[c], Sigma[c]) for c in bilesen])
    return X, (agirlik, mu, Sigma)


# --- Gizli değişkenler parametre sayısını azaltır ------------------------------------------------
def parametre_sayisi(ebeveyn_sayilari: list[int], deger: int = 3) -> int:
    """Her düğüm 'deger' değerli; ebeveyni p olan düğümün bağımsız parametresi deger^p · (deger − 1)."""
    return sum(deger ** p * (deger - 1) for p in ebeveyn_sayilari)


def kalp_hastaligi() -> tuple[int, int]:
    gizli_ile = parametre_sayisi([0, 0, 0, 3, 1, 1, 1])          # 3 etken, Hastalık, 3 belirti
    gizlisiz = parametre_sayisi([0, 0, 0, 3, 4, 5])              # belirtiler etkenlere ve birbirine bağlı
    return gizli_ile, gizlisiz


def main() -> None:
    print("=== İki torba, gizli Bag değişkeni: EM ===")
    gecmis = em()
    adlar = ["θ", "F1", "W1", "H1", "F2", "W2", "H2"]
    print("  yineleme  " + "  ".join(f"{a:>6}" for a in adlar) + "   log olabilirlik")
    for i, (t, L) in enumerate(gecmis):
        print(f"  {i:>8}  " + "  ".join(f"{t[a]:6.4f}" for a in adlar) + f"   {L:10.3f}")
    print(f"  Gerçek modelin log olabilirliği: {log_olabilirlik(GERCEK):.3f}")
    print("  İlk adım olabilirliği ~e^23 ≈ 10^10 kat artırır; sonrası yavaşlar (EM'in tipik davranışı).")

    print("\n=== Tanımlanabilirlik ===")
    print("  Üç nitelik: 7 parametre, 2³ − 1 = 7 bağımsız sayım. İki nitelik (delik yok): 5 parametre, 3 sayım.")
    for bas in ({"θ": 0.6, "F1": 0.6, "W1": 0.6, "F2": 0.4, "W2": 0.4}, {"θ": 0.3, "F1": 0.9, "W1": 0.5, "F2": 0.4, "W2": 0.6}):
        t, L = iki_nitelik_em(bas)
        print(f"  başlangıç {bas} → " + ", ".join(f"{k} {v:.3f}" for k, v in t.items()) + f";  log olabilirlik {L:.3f}")
    print("  Farklı parametreler, aynı olabilirlik: İki nitelikli model tanımlanamaz. (Üç nitelikte bile torbaların")
    print("  adları yer değiştirebilir; hiç gözlenmeyen değişkenlerde bu kaçınılmazdır.)")

    print("\n=== Gauss karışımı, 3 bileşen, 500 nokta ===")
    X, (gw, gmu, _) = karisim_ornekle()
    w, mu, Sigma, L = gauss_karisimi_em(X, 3)
    sira = np.argsort(mu[:, 0])
    print(f"  gerçek ağırlıklar {gw},  öğrenilen {np.round(w[sira], 3)}")
    print(f"  gerçek ortalamalar {gmu.tolist()}")
    print(f"  öğrenilen          {np.round(mu[sira], 3).tolist()}")
    print(f"  log olabilirlik: başta {L[0]:.1f}, sonda {L[-1]:.1f}; hiç azaldı mı? {any(b < a - 1e-6 for a, b in zip(L, L[1:]))}")

    print("\n=== Gizli değişken: kalp hastalığı ağı (her değişken 3 değerli) ===")
    g, s = kalp_hastaligi()
    print(f"  Gizli HeartDisease ile {g} parametre; çıkarılınca {s} parametre.")


if __name__ == "__main__":
    main()
