#!/usr/bin/env python3
"""Değer yinelemesi ve yakınsaması (kitaptaki 17.2.1).

* Bellman güncellemesi U_{i+1} = B U_i bir büzülmedir: ‖B U − B U′‖ ≤ γ ‖U − U′‖  (17.11).
* ε hatası için yeterli yineleme sayısı: N = ⌈log(2 R_max / (ε (1 − γ))) / log(1/γ)⌉.
* Durma koşulu: ‖U_{i+1} − U_i‖ < ε (1 − γ)/γ  ise  ‖U_{i+1} − U‖ < ε   (17.12).
* Politika kaybı: ‖U_i − U‖ < ε ise ‖U^{π_i} − U‖ < 2ε   (17.13).
Kitaptaki gözlem (4 × 3 dünya, γ = 0.9): Politika, faydalardaki en büyük hata hâlâ ~0.51 iken en iyi olur.
(Eski sürümdeki hata — uç durum ödülünün iki kez sayılması — bu sürümde yok: Uç durumların faydası 0'dır,
ödül yalnızca uç duruma giriş geçişinde verilir.)

Çalıştırma:
    python deger_yineleme.py
"""
from __future__ import annotations

import math
import random

import mdp


def yineleme_siniri(gama: float, eps: float, rmax: float = 1.0) -> int:
    return math.ceil(math.log(2 * rmax / (eps * (1 - gama))) / math.log(1 / gama))


def hata_ve_politika_kaybi(m: mdp.MDP, adim: int) -> list[tuple[int, float, float]]:
    """Her yinelemede (i, ‖U_i − U‖, ‖U^{π_i} − U‖)."""
    U_gercek, _ = mdp.deger_yineleme(m, eps=1e-12)
    U, satirlar = {s: 0.0 for s in m.durumlar}, []
    for i in range(1, adim + 1):
        U = m.bellman(U)
        pi = m.acgozlu(U)
        satirlar.append((i, mdp.en_cok_hata(U, U_gercek), mdp.en_cok_hata(mdp.politika_degerlendir(m, pi), U_gercek)))
    return satirlar


def buzulme_orani(m: mdp.MDP, deneme: int = 200, tohum: int = 0) -> float:
    """Rastgele fayda vektörleri için en büyük ‖BU − BU′‖ / ‖U − U′‖ oranı (≤ γ olmalı)."""
    rng = random.Random(tohum)
    en = 0.0
    for _ in range(deneme):
        U = {s: (0.0 if s in m.uclar else rng.uniform(-3, 3)) for s in m.durumlar}
        V = {s: (0.0 if s in m.uclar else rng.uniform(-3, 3)) for s in m.durumlar}
        en = max(en, mdp.en_cok_hata(m.bellman(U), m.bellman(V)) / mdp.en_cok_hata(U, V))
    return en


def main() -> None:
    m = mdp.dort_uc(gama=0.9)
    print("=== 4 × 3 dünya, γ = 0.9: fayda hatası ve politika kaybı (Şekil 17.8) ===")
    print("   i   ‖U_i − U‖   ‖U^π_i − U‖")
    for i, hata, kayip in hata_ve_politika_kaybi(m, 12):
        print(f"  {i:>2}   {hata:8.4f}    {kayip:8.4f}")
    print("  Politika 3. güncellemede en iyi oluyor; fayda hatası ise 4. güncellemede bile ~0.51.")

    U, i = mdp.deger_yineleme(m, eps=1e-4)
    print(f"\n  ε = 1e-4 durma koşuluyla {i} yinelemede durdu. Faydalar:")
    print(mdp.ciz(U))

    print("\n=== Büzülme ===")
    for g in (0.5, 0.9, 0.99):
        print(f"  γ = {g}: rastgele vektörlerde en büyük ‖BU − BU′‖/‖U − U′‖ = {buzulme_orani(mdp.dort_uc(gama=g)):.4f}")

    print("\n=== Kaç yineleme gerekir? N = ⌈log(2R_max/(ε(1−γ))) / log(1/γ)⌉, ε = c · R_max ===")
    print("   γ       c = 0.1   c = 0.01   c = 0.001")
    for g in (0.5, 0.9, 0.99, 0.999):
        print(f"  {g:<6}  " + "  ".join(f"{yineleme_siniri(g, c):>8}" for c in (0.1, 0.01, 0.001)))
    print("  N, ε'a az bağlı (üstel yakınsama) ama γ → 1 iken hızla büyür.")


if __name__ == "__main__":
    main()
