#!/usr/bin/env python3
"""Simüle tavlama demosu — küçük TSP (gezgin satıcı). Bölüm 4."""
from __future__ import annotations

import argparse
import itertools
import math
import random
from typing import List, Tuple

# 8 şehir: düzlemde sabit noktalar (eğitim örneği)
SEHIRLER: List[Tuple[float, float]] = [
    (0, 0),
    (1, 3),
    (4, 3),
    (5, 1),
    (3, 0),
    (2, 2),
    (6, 4),
    (1, 1),
]


def mesafe(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def tur_maliyeti(tur: List[int], noktalar: List[Tuple[float, float]] = SEHIRLER) -> float:
    m = 0.0
    for i in range(len(tur)):
        m += mesafe(noktalar[tur[i]], noktalar[tur[(i + 1) % len(tur)]])
    return m


def iki_opt_komsu(tur: List[int]) -> List[int]:
    """Rastgele iki kesim noktası arasında segmenti ters çevir (2-opt komşu)."""
    n = len(tur)
    i, j = sorted(random.sample(range(n), 2))
    yeni = tur[:i] + list(reversed(tur[i : j + 1])) + tur[j + 1 :]
    return yeni


def simule_tavlama(
    baslangic_t: float = 10.0,
    soguma: float = 0.995,
    min_t: float = 1e-3,
    max_iter: int = 5000,
    noktalar: List[Tuple[float, float]] = SEHIRLER,
) -> Tuple[List[int], float, List[float]]:
    """baslangic_t = 0 verilirse yalnızca iyileşmeler kabul edilir: tepe tırmanma."""
    n = len(noktalar)
    mevcut = list(range(n))
    random.shuffle(mevcut)
    maliyet = tur_maliyeti(mevcut, noktalar)
    en_iyi, en_iyi_m = list(mevcut), maliyet
    t = baslangic_t
    gecmis = [maliyet]

    for _ in range(max_iter):
        if 0 < t < min_t:
            break
        aday = iki_opt_komsu(mevcut)
        m_aday = tur_maliyeti(aday, noktalar)
        delta = m_aday - maliyet
        if delta < 0 or (t > 0 and random.random() < math.exp(-delta / t)):
            mevcut, maliyet = aday, m_aday
            if maliyet < en_iyi_m:
                en_iyi, en_iyi_m = list(mevcut), maliyet
        t *= soguma
        gecmis.append(en_iyi_m)

    return en_iyi, en_iyi_m, gecmis


def main() -> None:
    p = argparse.ArgumentParser(description="TSP üzerinde simüle tavlama")
    p.add_argument("--tohum", type=int, default=42)
    p.add_argument("--baslangic-t", type=float, default=10.0)
    p.add_argument("--soguma", type=float, default=0.995)
    p.add_argument("--max-iter", type=int, default=5000)
    args = p.parse_args()
    random.seed(args.tohum)

    print("=== Simüle tavlama — küçük TSP (8 şehir) ===\n")
    rastgele = list(range(len(SEHIRLER)))
    random.shuffle(rastgele)
    print(f"Rastgele tur maliyeti: {tur_maliyeti(rastgele):.3f}")

    tur, maliyet, gecmis = simule_tavlama(
        baslangic_t=args.baslangic_t,
        soguma=args.soguma,
        max_iter=args.max_iter,
    )
    print(f"SA sonrası tur: {tur}")
    print(f"SA maliyeti:    {maliyet:.3f}")
    print(f"İterasyon:      {len(gecmis)}")
    print(f"İlk en-iyi → son: {gecmis[0]:.3f} → {gecmis[-1]:.3f}")
    en_iyi = min(tur_maliyeti([0] + list(p)) for p in itertools.permutations(range(1, len(SEHIRLER))))
    print(f"Kaba kuvvet optimumu ({math.factorial(len(SEHIRLER) - 1)} tur denendi): {en_iyi:.3f}")
    print(
        "\nSoğuma: T ← T * {:.4f}. Yüksek T'de kötü adımlar da kabul edilir; "
        "T düşünce arama yerelleşir.".format(args.soguma)
    )

    # Daha büyük bir örnekte tepe tırmanma (T = 0) ile karşılaştır
    rng = random.Random(7)
    buyuk = [(rng.uniform(0, 100), rng.uniform(0, 100)) for _ in range(30)]
    tt, sa = [], []
    for tohum in range(15):
        random.seed(tohum)
        tt.append(simule_tavlama(baslangic_t=0, max_iter=20000, noktalar=buyuk)[1])
        random.seed(tohum)
        sa.append(simule_tavlama(baslangic_t=30.0, soguma=0.9995, min_t=1e-3,
                                 max_iter=20000, noktalar=buyuk)[1])
    print("\n30 şehir, 15 farklı başlangıç, her biri en fazla 20.000 adım:")
    print(f"  tepe tırmanma (yalnızca iyileşme): ortalama {sum(tt) / len(tt):7.1f}   en iyi {min(tt):7.1f}")
    print(f"  simüle tavlama                   : ortalama {sum(sa) / len(sa):7.1f}   en iyi {min(sa):7.1f}")
    print("Tavlama başta kötüleştiren adımları da kabul ettiği için yerel minimumlardan kaçabilir.")


if __name__ == "__main__":
    main()
