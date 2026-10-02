#!/usr/bin/env python3
"""Parçacık filtresi (kitaptaki 14.5.3), şemsiye dünyası üzerinde.

Her adımda:
  1. Her parçacığı geçiş modeliyle ileri taşı:        x' ~ P(X_{t+1} | x)
  2. Her parçacığı gözlemin olabilirliğiyle ağırlıkla:  w = P(e_{t+1} | x')
  3. Ağırlıklara göre N parçacığı yeniden örnekle (ağırlıklar yeniden 1 olur)
Parçacıkların oranı, filtrelenmiş dağılımın tahminidir: N(x | e_{1:t}) / N ≈ P(x | e_{1:t}).

Yeniden örnekleme olmadan (SIS, ardışık önem örneklemesi) ağırlıklar birkaç parçacıkta toplanır
ve tahmin zamanla bozulur. Yeniden örnekleme, parçacıkları olası bölgelerde tutar.

Çalıştırma:
    python parcacik_filtresi.py
"""
from __future__ import annotations

import random

from zamansal import semsiye_hmm

P_GECIS = {True: 0.7, False: 0.3}     # P(R_{t+1} = yağmur | R_t)
P_SEMSIYE = {True: 0.9, False: 0.2}   # P(U_t = var | R_t)


def parcacik_filtresi(gozlemler, N: int, rng: random.Random, yeniden_ornekle: bool = True):
    """Her adım için P̂(yağmur | e_{1:t}) listesi."""
    parcaciklar = [rng.random() < 0.5 for _ in range(N)]
    agirliklar = [1.0] * N
    tahminler = []
    for u in gozlemler:
        parcaciklar = [rng.random() < P_GECIS[x] for x in parcaciklar]
        w = [(P_SEMSIYE[x] if u else 1 - P_SEMSIYE[x]) for x in parcaciklar]
        agirliklar = [a * b for a, b in zip(agirliklar, w)] if not yeniden_ornekle else w
        toplam = sum(agirliklar)
        tahminler.append(sum(a for a, x in zip(agirliklar, parcaciklar) if x) / toplam)
        if yeniden_ornekle:
            parcaciklar = rng.choices(parcaciklar, weights=agirliklar, k=N)
            agirliklar = [1.0] * N
        else:
            agirliklar = [a / toplam for a in agirliklar]
    return tahminler


def gozlem_uret(adim: int, rng: random.Random) -> list[bool]:
    r = rng.random() < 0.5
    sonuc = []
    for _ in range(adim):
        r = rng.random() < P_GECIS[r]
        sonuc.append(rng.random() < P_SEMSIYE[r])
    return sonuc


def ortalama_hata(N: int, adim: int, kosu: int, yeniden_ornekle: bool, tohum: int = 0) -> float:
    rng = random.Random(tohum)
    h = semsiye_hmm()
    toplam = 0.0
    for _ in range(kosu):
        g = gozlem_uret(adim, rng)
        kesin = [f[0] for f in h.filtrele(g)]
        pf = parcacik_filtresi(g, N, rng, yeniden_ornekle)
        toplam += sum(abs(a - b) for a, b in zip(kesin, pf)) / adim
    return toplam / kosu


def main() -> None:
    rng = random.Random(1)
    h = semsiye_hmm()
    gunler = [True, True, False, True, True]
    kesin = [f[0] for f in h.filtrele(gunler)]
    print("=== Şemsiye dünyası, [u, u, ¬u, u, u] ===")
    print("   N        " + "  ".join(f"gün {t + 1}" for t in range(5)))
    print("  kesin     " + "  ".join(f"{p:.3f}" for p in kesin))
    for N in (10, 100, 1000, 10000):
        pf = parcacik_filtresi(gunler, N, rng)
        print(f"  {N:<8}  " + "  ".join(f"{p:.3f}" for p in pf))

    print("\n=== Uzun dizilerde ortalama mutlak hata (100 adım, 20 koşu) ===")
    for N in (10, 100, 1000):
        pf = ortalama_hata(N, 100, 20, True)
        sis = ortalama_hata(N, 100, 20, False)
        print(f"  N = {N:<5}: yeniden örneklemeli PF {pf:.3f}    SIS (yeniden örneklemesiz) {sis:.3f}")
    print("  Yeniden örnekleme olmadan ağırlıklar birkaç parçacıkta toplanır; hata büyür.")


if __name__ == "__main__":
    main()
