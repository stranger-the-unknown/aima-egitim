#!/usr/bin/env python3
"""Bölüm 15 alıştırmaları: kodlu çözümler (A5, A6, A7, A9, A10).

Çalıştırma (bölüm klasöründen):
    python cozumler/alistirma_kod.py
"""
from __future__ import annotations

import itertools
import math
import random
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "ornekler"))

import acik_evren as ae  # noqa: E402
import beceri_derecelendirme as bd  # noqa: E402
import metin_okuma as mo  # noqa: E402
import rpm_oneriler as rpm  # noqa: E402


# --- A5: tek bir puanın etkisi ------------------------------------------------
def a5() -> dict:
    tek = rpm.sonsal({("C1", "B1"): 5}, ["B1"])
    iki = rpm.sonsal({("C1", "B1"): 5, ("C1", "B2"): 5}, ["B1", "B2"])
    return {"E[Q(B1)] | C1:5": rpm.ortalama(tek["kalite"]["B1"]),
            "P(Honest(C1)) | C1:5": tek["durust"]["C1"],
            "E[Q(B1)] | C1:5,5": rpm.ortalama(iki["kalite"]["B1"]),
            "P(Honest(C1)) | C1:5,5": iki["durust"]["C1"]}


# --- A6: şans oyunu mu, beceri oyunu mu? -------------------------------------
def a6() -> dict:
    maclar = [("Ayşe", "Burak")] * 10
    sonuc = {}
    for beta in (25 / 6, 25.0):
        eski, bd.BETA = bd.BETA, beta
        try:
            s, _, _, _ = bd.sonsal_beceri(maclar, ["Ayşe", "Burak"], N=100_000)
        finally:
            bd.BETA = eski
        sonuc[round(beta, 2)] = {o: round(float(m), 1) for o, (m, _) in s.items()}
    return sonuc


# --- A7: 5 giriş kimliği -------------------------------------------------------
def a7() -> dict:
    s = ae.login_sayisi_sonsali(5)
    return {n: float(sum(v for (m, _), v in s.items() if m == n)) for n in (1, 2, 3)}


# --- A9: veri ilişkilendirme ---------------------------------------------------
def a9(T: int = 6, tohum: int = 6, konumlar=(0.0, 1.5), sigma: float = 1.0, tau: float = 10.0) -> dict:
    """İki durağan hedef (1B), her adımda iki etiketsiz gözlem. Hipotez: her adımda gözlemler
    yer değiştirdi mi? Hedef konumlarının önseli N(0, τ²); konum üzerinden integral alınır."""
    rng = np.random.default_rng(tohum)
    gercek_takas = rng.integers(0, 2, size=T)
    gercek_takas[0] = 0
    gozlem = []
    for t in range(T):
        z = [konumlar[0] + rng.normal(0, sigma), konumlar[1] + rng.normal(0, sigma)]
        gozlem.append(z[::-1] if gercek_takas[t] else z)

    def log_marjinal(z: np.ndarray) -> float:
        n = len(z)
        cov = sigma ** 2 * np.eye(n) + tau ** 2 * np.ones((n, n))
        _, logdet = np.linalg.slogdet(cov)
        return float(-0.5 * (z @ np.linalg.solve(cov, z) + logdet + n * math.log(2 * math.pi)))

    hipotezler = [(0,) + h for h in itertools.product((0, 1), repeat=T - 1)]
    logp = []
    for h in hipotezler:
        a = np.array([gozlem[t][h[t]] for t in range(T)])
        b = np.array([gozlem[t][1 - h[t]] for t in range(T)])
        logp.append(log_marjinal(a) + log_marjinal(b))
    logp = np.array(logp)
    p = np.exp(logp - logp.max())
    p /= p.sum()
    sira = np.argsort(-p)

    # en yakın komşu: ilk gözlemlerle başla, her adımda ortalamalara en yakın eşleşmeyi seç
    ort = [gozlem[0][0], gozlem[0][1]]
    say = [1, 1]
    nn = [0]
    for t in range(1, T):
        z0, z1 = gozlem[t]
        duz = abs(z0 - ort[0]) + abs(z1 - ort[1])
        ters = abs(z1 - ort[0]) + abs(z0 - ort[1])
        s = 0 if duz <= ters else 1
        nn.append(s)
        a, b = (z0, z1) if s == 0 else (z1, z0)
        ort = [(ort[0] * say[0] + a) / (say[0] + 1), (ort[1] * say[1] + b) / (say[1] + 1)]
        say = [say[0] + 1, say[1] + 1]
    return {"hipotez sayısı": len(hipotezler), "gerçek": tuple(int(x) for x in gercek_takas),
            "en olası 3": [(hipotezler[i], round(float(p[i]), 3)) for i in sira[:3]],
            "P(gerçek)": float(p[hipotezler.index(tuple(int(x) for x in gercek_takas))]),
            "en yakın komşu": tuple(nn)}


# --- A10: harf harf en olası (ileri–geri) vs Viterbi ---------------------------
def _logsumexp(xs):
    m = max(xs)
    return m + math.log(sum(math.exp(x - m) for x in xs))


def ileri_geri_oku(goruntuler, p: float, model=None) -> str:
    baslangic, gecis = model or mo.ikili_model()
    H = mo.HARFLER
    obs = [{h: mo.log_olabilirlik(g, h, p) for h in H} for g in goruntuler]
    f = [{h: math.log(baslangic[h]) + obs[0][h] for h in H}]
    for t in range(1, len(goruntuler)):
        f.append({b: obs[t][b] + _logsumexp([f[-1][a] + math.log(gecis[a][b]) for a in H]) for b in H})
    b = [{h: 0.0 for h in H}]
    for t in range(len(goruntuler) - 1, 0, -1):
        b.insert(0, {a: _logsumexp([math.log(gecis[a][c]) + obs[t][c] + b[0][c] for c in H]) for a in H})
    return "".join(max(H, key=lambda h: f[t][h] + b[t][h]) for t in range(len(goruntuler)))


def a10(p: float = 0.2, deneme: int = 15, tohum: int = 1) -> dict:
    rng = random.Random(tohum)
    model = mo.ikili_model()
    harf_v = harf_ig = kelime_v = kelime_ig = toplam = 0
    for _ in range(deneme):
        for k in mo.TEST:
            g = mo.ciz(k, p, rng)
            v, ig = mo.markov_oku(g, p, model), ileri_geri_oku(g, p, model)
            harf_v += sum(a == b for a, b in zip(v, k))
            harf_ig += sum(a == b for a, b in zip(ig, k))
            kelime_v += v == k
            kelime_ig += ig == k
            toplam += len(k)
    n = deneme * len(mo.TEST)
    return {"Viterbi harf": harf_v / toplam, "ileri–geri harf": harf_ig / toplam,
            "Viterbi kelime": kelime_v / n, "ileri–geri kelime": kelime_ig / n}


def main() -> None:
    print("A5:", {k: round(v, 3) for k, v in a5().items()})
    print("A6 (β → sonsal ortalamalar):", a6())
    print("A7: P(#Customer | 5 kimlik):", {k: round(v, 3) for k, v in a7().items()})
    r = a9()
    print("A9:", r)
    print("A10:", {k: f"{v:.1%}" for k, v in a10().items()})


if __name__ == "__main__":
    main()
