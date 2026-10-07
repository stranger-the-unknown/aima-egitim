#!/usr/bin/env python3
"""Bölüm 28 alıştırmaları: kodlu çözümler (A2–A6).

Çalıştırma (bölüm klasöründen):
    python cozumler/alistirma_kod.py
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "ornekler"))

import hesaplama_sinirlari as hs  # noqa: E402


# --- A2: Borges ve bir insan hayatının planı -------------------------------------------------------
def a2() -> dict:
    yil_12 = 100_000 ** 12 / (1e51 * hs.YIL)
    return {"12 sözcük için gereken yıl": yil_12,
            "20 trilyon kas hareketlik plan, her adımda 2 seçenek: log10(plan sayısı)": 20e12 * math.log10(2)}


# --- A3: eğilimler ---------------------------------------------------------------------------------
def a3() -> dict:
    return {"6 yılda 3.5 ayda bir ikiye": 2 ** (72 / 3.5),
            "aynı hızla 10 yıl daha": 2 ** (120 / 3.5),
            "depolama: $0.02'den 10 yıl sonra (aynı yarılanmayla)": 0.02 / 2 ** (10 / hs.katlanma_suresi(5e7, 50))}


# --- A4: her an kesilebilirlik ve 1/√n -------------------------------------------------------------------
def a4(tohum_sayisi: int = 50) -> float:
    """Ortalama hatanın örnek sayısına göre log-log eğimi."""
    n = np.array([100, 1_000, 10_000, 100_000])
    hatalar = np.mean([[h for _, h in hs.anytime_tahmin(tuple(n), tohum=t)] for t in range(tohum_sayisi)], axis=0)
    return float(np.polyfit(np.log(n), np.log(hatalar), 1)[0])


# --- A5: miyop olmayan hesaplama değeri ---------------------------------------------------------------------
def k_adimli_deger(m: float, v: float, rakip: float, gurultu: float, k: int) -> float:
    """Aynı seçenek için k benzetim birden: sonsal ortalamanın değişim varyansı v² / (v + σ²/k)."""
    return hs.hesaplama_degeri(m, v, rakip, gurultu / k)


def ileri_bakan_karar(maliyet: float, gercek=(1.0, 1.3), gurultu: float = 1.0, en_cok: int = 500, tohum: int = 0,
                      ufuk: int = 20):
    """Bir sonraki benzetimi, 1..ufuk benzetimlik paketlerden en az birinin net değeri pozitifse yap."""
    rng = np.random.default_rng(tohum)
    m, v = [0.0, 0.0], [1.0, 1.0]
    for k in range(en_cok):
        en_iyi = max(((k_adimli_deger(m[i], v[i], m[1 - i], gurultu, j) - j * maliyet) / j, i)
                     for i in (0, 1) for j in range(1, ufuk + 1))
        if en_iyi[0] <= 0:
            return k, int(np.argmax(m)), k * maliyet
        i = en_iyi[1]
        x = gercek[i] + rng.normal(0, math.sqrt(gurultu))
        yeni_v = 1 / (1 / v[i] + 1 / gurultu)
        m[i] = yeni_v * (m[i] / v[i] + x / gurultu)
        v[i] = yeni_v
    return en_cok, int(np.argmax(m)), en_cok * maliyet


def a5(maliyet: float = 0.01, deneme: int = 200) -> dict:
    sonuc = {}
    for ad, f in (("miyop", hs.ustakil_karar), ("ileri bakan", ileri_bakan_karar)):
        r = [f(maliyet, tohum=t) for t in range(deneme)]
        sonuc[ad] = (round(float(np.mean([s[0] for s in r])), 1), round(float(np.mean([s[1] == 1 for s in r])), 2),
                     round(float(np.mean([(1.0, 1.3)[s[1]] - s[2] for s in r])), 3))
    return sonuc


# --- A6: sınırlı en iyilik ve dallanma -------------------------------------------------------------------------
def a6() -> dict:
    return {b: hs.en_iyi_derinlik(1e-4, dallanma=b) for b in (2, 3, 10)}


def main() -> None:
    print("=== A2 ===")
    for k, v in a2().items():
        print(f"  {k}: {v:.3g}")
    print("\n=== A3 ===")
    for k, v in a3().items():
        print(f"  {k}: {v:.3g}")
    print(f"\n=== A4: log(hata) – log(n) eğimi: {a4():.2f} (kuram: −0.5) ===")
    print("\n=== A5: benzetim maliyeti 0.01 → (ort. benzetim, doğru eylem oranı, net fayda) ===")
    for k, v in a5().items():
        print(f"  {k}: {v}")
    print("\n=== A6: dallanma → (en iyi derinlik, net değer) ===")
    for b, (d, net) in a6().items():
        print(f"  b = {b}: derinlik {d}, net {net:.3f}")


if __name__ == "__main__":
    main()
