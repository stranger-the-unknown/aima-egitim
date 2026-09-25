#!/usr/bin/env python3
"""Reddetme örneklemesi demosu — küçük sorgu.

Aynı adil/hileli zar modeli.
Algoritma:
  tekrar:
    dünya ~ prior (üretimsel)
    eğer kanıta UYMUYORSA reddet
    değilse sayaca ekle
  dönüş: kabul edilenlerde sorgu frekansı

Resmi referans: https://aima.cs.berkeley.edu/ · https://github.com/aimacode
"""
from __future__ import annotations

import random
from typing import Dict, Optional, Tuple

random.seed(7)

P_HILELI = 0.3
HILELI_P = {1: 0.05, 2: 0.05, 3: 0.05, 4: 0.05, 5: 0.10, 6: 0.70}


def sample_prior() -> Tuple[str, int]:
    kutu = "hileli" if random.random() < P_HILELI else "adil"
    if kutu == "adil":
        yuz = random.randint(1, 6)
    else:
        r = random.random()
        akum = 0.0
        yuz = 6
        for y, p in HILELI_P.items():
            akum += p
            if r <= akum:
                yuz = y
                break
    return kutu, yuz


def reddetme(
    n_deneme: int,
    kanit_yuz: int,
    sorgu_kutu: str = "hileli",
) -> Dict[str, float]:
    """Reddetme örneklemesi: P(kutu=sorgu | zar=kanit)."""
    kabul = 0
    sorgu_say = 0
    for _ in range(n_deneme):
        kutu, yuz = sample_prior()
        if yuz != kanit_yuz:
            continue  # reddet
        kabul += 1
        if kutu == sorgu_kutu:
            sorgu_say += 1
    oran_kabul = kabul / n_deneme if n_deneme else 0.0
    p_sorgu = sorgu_say / kabul if kabul else float("nan")
    return {
        "deneme": float(n_deneme),
        "kabul": float(kabul),
        "red_orani": 1.0 - oran_kabul,
        "p_sorgu": p_sorgu,
    }


def main() -> None:
    print("Reddetme örneklemesi — P(hileli | zar=6)\n")
    kanit = 6
    for n in (1000, 5000, 20000):
        r = reddetme(n, kanit)
        print(
            f"n={n:5d}  kabul={int(r['kabul']):5d}  "
            f"red_oranı={r['red_orani']:.3f}  "
            f"P(hileli|6)≈{r['p_sorgu']:.4f}"
        )

    # Nadir kanıt örneği: zar=1 (hilelide çok düşük)
    print()
    print("Nadir kanıt: zar=1 (hilelide P(1)=0.05) → çoğu örnek reddedilir:")
    r1 = reddetme(30000, 1)
    print(
        f"n=30000  kabul={int(r1['kabul'])}  red_oranı={r1['red_orani']:.3f}  "
        f"P(hileli|1)≈{r1['p_sorgu']:.4f}"
    )
    print()
    print("Ders: reddetme basit ama kanıt seyrekse verimsiz — çoğu örnek çöpe gider.")


if __name__ == "__main__":
    main()
