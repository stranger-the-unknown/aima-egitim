#!/usr/bin/env python3
"""Basit üretimsel model — saf Python.

Senaryo (özgün): İki tür zar kutusu
  - Adil zar: 1..6 eşit
  - Hileli zar: 6 gelme olasılığı yüksek

Üretim:
  1) kutu ~ {adil, hileli} önsel
  2) zar atışı ~ kutuya göre
  3) kanıt: örneğin "6 geldi" → P(hileli | 6) naif sayımla

Resmi referans: https://aima.cs.berkeley.edu/ · https://github.com/aimacode
"""
from __future__ import annotations

import random
from collections import Counter
from typing import Dict, List, Tuple

random.seed(42)

# Önsel: kutunun hileli olma olasılığı
P_HILELI = 0.3

# Hileli zarda P(yüz)
# Adil: her yüz 1/6
HILELI_P = {1: 0.05, 2: 0.05, 3: 0.05, 4: 0.05, 5: 0.10, 6: 0.70}


def ornekle_kutu() -> str:
    return "hileli" if random.random() < P_HILELI else "adil"


def ornekle_zar(kutu: str) -> int:
    if kutu == "adil":
        return random.randint(1, 6)
    r = random.random()
    akum = 0.0
    for yuz, p in HILELI_P.items():
        akum += p
        if r <= akum:
            return yuz
    return 6


def uret_dunya() -> Tuple[str, int]:
    """Tek bir dünya: (kutu, zar_sonucu)."""
    k = ornekle_kutu()
    z = ornekle_zar(k)
    return k, z


def naif_kosullandir(n: int, kanit_yuz: int) -> Dict[str, float]:
    """n örnek üret; zar==kanit olanlarda kutu frekansı."""
    sayac: Counter[str] = Counter()
    kabul = 0
    for _ in range(n):
        kutu, yuz = uret_dunya()
        if yuz == kanit_yuz:
            sayac[kutu] += 1
            kabul += 1
    if kabul == 0:
        raise RuntimeError("kanıta uyan örnek yok — n artırın")
    return {k: sayac[k] / kabul for k in ("adil", "hileli")}


def analitik_bayes(kanit_yuz: int = 6) -> float:
    """P(hileli | yüz) — kontrol için basit Bayes."""
    p_h = P_HILELI
    p_a = 1.0 - P_HILELI
    p_y_h = HILELI_P[kanit_yuz]
    p_y_a = 1.0 / 6.0
    return (p_y_h * p_h) / (p_y_h * p_h + p_y_a * p_a)


def main() -> None:
    print("Üretimsel model — adil / hileli zar (özgün eğitim)\n")
    print(f"P(hileli) önsel = {P_HILELI}")
    print(f"Hileli P(6) = {HILELI_P[6]}, adil P(6) = {1/6:.4f}")
    print()

    print("Örnek dünyalar (ilk 8):")
    for i in range(8):
        k, z = uret_dunya()
        print(f"  {i+1}. kutu={k:7} zar={z}")
    print()

    n = 20000
    kanit = 6
    dist = naif_kosullandir(n, kanit)
    exact = analitik_bayes(kanit)
    print(f"Kanıt: zar={kanit}  (n={n} örnekten naif koşullandırma)")
    print(f"  P(adil   | zar=6) ≈ {dist.get('adil', 0):.4f}")
    print(f"  P(hileli | zar=6) ≈ {dist.get('hileli', 0):.4f}")
    print(f"  Analitik P(hileli | zar=6) = {exact:.4f}")
    print()
    print("Fikir: program prior'dan örnekler → gözlem üretir → kanıta göre frekans = sonsal tahmini.")


if __name__ == "__main__":
    main()
