#!/usr/bin/env python3
"""Simüle tavlama demosu — küçük TSP (gezgin satıcı). Bölüm 4."""
from __future__ import annotations

import argparse
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


def tur_maliyeti(tur: List[int]) -> float:
    m = 0.0
    for i in range(len(tur)):
        m += mesafe(SEHIRLER[tur[i]], SEHIRLER[tur[(i + 1) % len(tur)]])
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
) -> Tuple[List[int], float, List[float]]:
    n = len(SEHIRLER)
    mevcut = list(range(n))
    random.shuffle(mevcut)
    maliyet = tur_maliyeti(mevcut)
    en_iyi, en_iyi_m = list(mevcut), maliyet
    t = baslangic_t
    gecmis = [maliyet]

    for _ in range(max_iter):
        if t < min_t:
            break
        aday = iki_opt_komsu(mevcut)
        m_aday = tur_maliyeti(aday)
        delta = m_aday - maliyet
        if delta < 0 or random.random() < math.exp(-delta / t):
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
    print(
        "\nSoğuma: T ← T * {:.4f}. Yüksek T'de kötü adımlar da kabul edilir; "
        "T düşünce arama yerelleşir.".format(args.soguma)
    )


if __name__ == "__main__":
    main()
