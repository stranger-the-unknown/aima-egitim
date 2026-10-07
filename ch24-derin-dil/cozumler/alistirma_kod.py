#!/usr/bin/env python3
"""Bölüm 24 alıştırmaları: kodlu çözümler (A3, A5, A6, A8, A9).

Çalıştırma (bölüm klasöründen):
    python cozumler/alistirma_kod.py
"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "ornekler"))

import dikkat as dk  # noqa: E402
import gomme as gm  # noqa: E402
import kod_cozme as kc  # noqa: E402


# --- A3: pencere boyutu ---------------------------------------------------------------
def a3() -> dict:
    sonuc = {}
    for pencere in (1, 2, 4):
        sozcukler, M = gm.birlikte_gecme(gm.DERLEM, pencere)
        V = gm.ppmi_svd(M)
        sonuc[pencere] = [w for w, _ in gm.en_yakinlar("kedi", sozcukler, V)]
    return sonuc


# --- A5: dikkati elle -------------------------------------------------------------------
def a5() -> dict:
    kaynak = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
    h = np.array([2.0, 0.0])
    a, c = dk.diziden_diziye_dikkat(h, kaynak)
    return {"puanlar": kaynak @ h, "olasılıklar": a, "bağlam": c}


# --- A6: konum kodlaması ------------------------------------------------------------------
def a6(n: int = 50, d: int = 32) -> dict:
    P = dk.konum_kodlamasi(n, d)
    return {k: float(P[10] @ P[10 + k]) for k in (0, 1, 2, 5, 20)} | {"aynı uzaklık, farklı yer": float(P[30] @ P[35])}


# --- A8: ışın genişliği ----------------------------------------------------------------------
def a8() -> dict:
    return {b: kc.isin_aramasi(b) for b in (1, 2, 3)}


# --- A9: maskeli dil modeli fikri -------------------------------------------------------------
def a9(cumle: str = "kedi [MASK] içti") -> dict:
    """Boşluğu yalnız soldaki sözcükle mi, hem sol hem sağ bağlamla mı tahmin etmek daha iyi?"""
    d = gm.DERLEM
    sol, sag = cumle.split()[0], cumle.split()[2]
    yalniz_sol = Counter(d[i + 1] for i in range(len(d) - 1) if d[i] == sol)
    iki_yon = Counter(d[i + 1] for i in range(len(d) - 2) if d[i] == sol and d[i + 2] == sag)
    return {"yalnız sol bağlam": yalniz_sol.most_common(3), "sol + sağ bağlam": iki_yon.most_common(3)}


def main() -> None:
    print("=== A3: pencere boyutu ve 'kedi'nin komşuları ===")
    for p, k in a3().items():
        print(f"  pencere {p}: {k}")

    print("\n=== A5: dikkati elle ===")
    for k, v in a5().items():
        print(f"  {k}: {np.round(v, 3)}")

    print("\n=== A6: konum kodlamalarının iç çarpımı (10. konumla) ===")
    for k, v in a6().items():
        print(f"  {'uzaklık ' + str(k) if isinstance(k, int) else k}: {v:.3f}")

    print("\n=== A8: ışın genişliği ===")
    for b, (s, p) in a8().items():
        print(f"  b = {b}: {' '.join(s)}  (log P {p:.3f})")

    print("\n=== A9: 'kedi [MASK] içti' ===")
    for k, v in a9().items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
