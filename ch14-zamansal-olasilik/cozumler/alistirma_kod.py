#!/usr/bin/env python3
"""Bölüm 14 alıştırmaları: kodlu çözümler (A2, A4, A5, A6, A7, A8, A9, A10).

Çalıştırma (bölüm klasöründen):
    python cozumler/alistirma_kod.py
"""
from __future__ import annotations

import itertools
import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "ornekler"))

import kalman as km  # noqa: E402
import lokalizasyon as lk  # noqa: E402
from zamansal import HMM, semsiye_hmm  # noqa: E402


def semsiye_benzeri(kal: float, gec: float = None) -> HMM:
    """P(yağmur | dün yağmur) = kal, P(yağmur | dün kuru) = gec (verilmezse 1 − kal)."""
    gec = 1 - kal if gec is None else gec
    return HMM(["Yağmur", "Kuru"], [[kal, 1 - kal], [gec, 1 - gec]],
               lambda u: [0.9, 0.2] if u else [0.1, 0.8], [0.5, 0.5])


# --- A2 / A4 ----------------------------------------------------------------
def a2() -> float:
    return semsiye_hmm().filtrele([True, True, False])[2][0]


def a4() -> tuple[float, list]:
    h = semsiye_hmm()
    return h.ileri_geri([True, True, False])[1][0], h.geri_mesajlari([True, True, False])[1]


# --- A5: Viterbi yolu ≠ adım adım en olası durumlar --------------------------
def a5(uzunluk: int = 4):
    """Şemsiye dünyasında Viterbi yolunun, yumuşatılmış marjinallerin adım adım argmax'ından
    farklı olduğu en kısa gözlem dizisini bul."""
    h = semsiye_hmm()
    for n in range(1, uzunluk + 1):
        for dizi in itertools.product((True, False), repeat=n):
            yol, _ = h.viterbi(list(dizi))
            yumusak = h.ileri_geri(list(dizi))
            argmax = [h.durumlar[0] if s[0] > s[1] else h.durumlar[1] for s in yumusak]
            if yol != argmax:
                return list(dizi), yol, argmax, [round(s[0], 3) for s in yumusak]
    return None


# --- A6: durağan dağılım ve karışma süresi ----------------------------------
def karisma_adimi(h: HMM, baslangic, tol: float = 0.01) -> int:
    hedef = h.duragan_dagilim()
    f, t = baslangic, 0
    while abs(f[0] - hedef[0]) > tol:
        f = h.tahmin_adimi(f)
        t += 1
    return t


def a6() -> dict:
    return {ad: (round(h.duragan_dagilim()[0], 3), karisma_adimi(h, [1.0, 0.0]))
            for ad, h in (("0.7 / 0.3", semsiye_benzeri(0.7)), ("0.9 / 0.1", semsiye_benzeri(0.9)),
                          ("0.7 / 0.2", semsiye_benzeri(0.7, 0.2)))}


# --- A7: Kalman ikinci adım ---------------------------------------------------
def a7() -> tuple[float, float]:
    mu1, var1 = km.kalman_1b(0.0, 1.5 ** 2, 2.5, 4.0, 1.0)
    return km.kalman_1b(mu1, var1, 1.0, 4.0, 1.0)


# --- A8: simetrik koridor ---------------------------------------------------
KORIDOR = ["......."]


def a8(adim: int = 40, kosu: int = 20, tohum: int = 3) -> dict:
    rng = random.Random(tohum)
    h, kareler = lk.konum_hmm(0.0, KORIDOR)
    hata = 0.0
    son_inanc = None
    for _ in range(kosu):
        yol, gozlemler = lk.simule_et(0.0, adim, rng, KORIDOR)
        f = h.filtrele(gozlemler)[-1]
        hata += sum(p * lk.manhattan(k, yol[-1]) for p, k in zip(f, kareler))
        son_inanc = (yol[-1], [round(p, 2) for p in f])
    return {"ortalama hata": hata / kosu, "son koşu (gerçek, inanç)": son_inanc}


# --- A9: genel parçacık filtresi, konumlandırmada ---------------------------
def parcacik_hmm(h: HMM, gozlemler, N: int, rng: random.Random) -> list[list[float]]:
    parcaciklar = rng.choices(range(h.n), weights=h.onsel, k=N)
    sonuc = []
    for e in gozlemler:
        parcaciklar = [rng.choices(range(h.n), weights=h.T[i])[0] for i in parcaciklar]
        o = h.sensor(e)
        w = [o[i] for i in parcaciklar]
        if sum(w) == 0:
            w = [1.0] * N
        parcaciklar = rng.choices(parcaciklar, weights=w, k=N)
        dagilim = [0.0] * h.n
        for i in parcaciklar:
            dagilim[i] += 1 / N
        sonuc.append(dagilim)
    return sonuc


def a9(epsilon: float = 0.1, adim: int = 25, kosu: int = 10, tohum: int = 5) -> dict:
    rng = random.Random(tohum)
    h, kareler = lk.konum_hmm(epsilon)
    sonuc = {"kesin": 0.0, 20: 0.0, 100: 0.0, 1000: 0.0}
    for _ in range(kosu):
        yol, gozlemler = lk.simule_et(epsilon, adim, rng)
        f = h.filtrele(gozlemler)[-1]
        sonuc["kesin"] += sum(p * lk.manhattan(k, yol[-1]) for p, k in zip(f, kareler)) / kosu
        for N in (20, 100, 1000):
            g = parcacik_hmm(h, gozlemler, N, rng)[-1]
            sonuc[N] += sum(p * lk.manhattan(k, yol[-1]) for p, k in zip(g, kareler)) / kosu
    return sonuc


# --- A10: olabilirlikle model seçimi ----------------------------------------
def a10(gun: int = 500, tohum: int = 11) -> dict:
    rng = random.Random(tohum)
    r, gozlem = rng.random() < 0.5, []
    for _ in range(gun):                          # veri "kalıcı hava" modelinden
        r = rng.random() < (0.9 if r else 0.1)
        gozlem.append(rng.random() < (0.9 if r else 0.2))
    sonuc = {}
    for kal in (0.5, 0.7, 0.9, 0.95):
        sonuc[kal] = math.log(semsiye_benzeri(kal).olabilirlik(gozlem))
    return sonuc


def main() -> None:
    print(f"A2: P(R3 | u1, u2, ¬u3) = {a2():.4f}")
    p, b = a4()
    print(f"A4: b_3:3 = {[round(x, 2) for x in b]},  P(R2 | u1, u2, ¬u3) = {p:.4f}")
    print(f"A5: {a5()}")
    print("A6: (durağan P(yağmur), %1'e yakınsama adımı):", a6())
    mu2, var2 = a7()
    print(f"A7: μ2 = {mu2:.3f}, σ²2 = {var2:.3f}")
    print("A8:", a8())
    print("A9: beklenen konum hatası:", {k: round(v, 2) for k, v in a9().items()})
    for gun in (60, 500):
        print(f"A10 ({gun} gün): log P(e | model):", {k: round(v, 1) for k, v in a10(gun).items()})


if __name__ == "__main__":
    main()
