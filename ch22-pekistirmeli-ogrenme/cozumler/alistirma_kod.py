#!/usr/bin/env python3
"""Bölüm 22 alıştırmaları: kodlu çözümler (A2, A3, A6, A8, A9).

Çalıştırma (bölüm klasöründen):
    python cozumler/alistirma_kod.py
"""
from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "ornekler"))

import aktif_ogrenme as ao  # noqa: E402
import pasif_ogrenme as po  # noqa: E402
import yaklasik_ve_politika as yp  # noqa: E402


# --- A2: üç denemeden doğrudan kestirim ----------------------------------------------
def a2() -> dict:
    ajan = po.DogrudanKestirim()
    for d in po.KITAP_DENEMELERI:
        ajan.ogren(d)
    return {s: (ajan.U(s), ajan.sayi[s]) for s in sorted(ajan.sayi)}


# --- A3: üç denemeden ADP modeli ---------------------------------------------------------
def a3() -> dict:
    adp = po.PasifADP()
    for d in po.KITAP_DENEMELERI:
        adp.ogren(d)
    sonuc = {}
    for (s, a), n in sorted(adp.N_sa.items()):
        sonuc[(s, a)] = {s2: k / n for s2, k in sorted(((s2, k) for (s2, s_, a_), k in adp.N_s2_sa.items()
                                                         if s_ == s and a_ == a))}
    return sonuc


# --- A6: Nₑ'nin etkisi ---------------------------------------------------------------------
def a6(tohumlar=(0, 1, 2)) -> dict:
    import statistics
    sonuc = {}
    for ne in (1, 5, 20):
        k = [ao.egit(ao.ADPAjani(N_e=ne), 100, tohum=t, kontrol=(20, 100)) for t in tohumlar]
        sonuc[ne] = {n: statistics.median(x[n] for x in k) for n in (20, 100)}
    return sonuc


# --- A8: hedefe uzaklık özelliği ---------------------------------------------------------------
def a8() -> dict:
    durumlar = yp.DURUMLAR
    sonuc = {}
    for ad, f in (("(1, x, y)", lambda s: [1, s[0], s[1]]),
                  ("(1, x, y, hedefe uzaklık)", lambda s: [1, s[0], s[1], abs(4 - s[0]) + abs(3 - s[1])]),
                  ("(1, x, y, uzaklık, −1'e komşu mu)", lambda s: [1, s[0], s[1], abs(4 - s[0]) + abs(3 - s[1]),
                                                                    1.0 if s in ((4, 1), (3, 2)) else 0.0])):
        A = np.array([f(s) for s in durumlar], float)
        b = np.array([po.GERCEK_U[s] for s in durumlar])
        th = np.linalg.lstsq(A, b, rcond=None)[0]
        sonuc[ad] = float(np.sqrt(np.mean((A @ th - b) ** 2)))
    return sonuc


# --- A9: REINFORCE'ta öğrenme hızı ----------------------------------------------------------------
def a9() -> dict:
    return {alfa: yp.reinforce(bolum=1500, alfa=alfa, kontrol=(300, 1500)) for alfa in (0.01, 0.05, 0.2)}


def main() -> None:
    print("=== A2: üç denemeden doğrudan fayda kestirimi ===")
    for s, (u, n) in a2().items():
        print(f"  {s}: {u:.3f} ({n} örnek), gerçek {po.GERCEK_U[s]:.3f}")

    print("\n=== A3: üç denemeden öğrenilen geçiş modeli ===")
    for (s, a), dag in a3().items():
        print(f"  {s} {a:<6}: " + ", ".join(f"{s2} {p:.2f}" for s2, p in dag.items()))

    print("\n=== A6: keşifçi ADP'de Nₑ ===")
    for ne, k in a6().items():
        print(f"  Nₑ = {ne:>2}: 20 denemede kayıp {k[20]:.3f}, 100 denemede {k[100]:.3f}")

    print("\n=== A8: özellik eklemek ===")
    for ad, h in a8().items():
        print(f"  {ad:<34}: RMS hata {h:.3f}")

    print("\n=== A9: REINFORCE öğrenme hızı ===")
    for alfa, k in a9().items():
        print(f"  α = {alfa}: 300 bölümde kayıp {k[300]:.3f}, 1500 bölümde {k[1500]:.3f}")


if __name__ == "__main__":
    main()
