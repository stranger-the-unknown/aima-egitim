#!/usr/bin/env python3
"""Dinamik Bayes ağında algılayıcı arızaları (kitaptaki 14.5.1'deki pil ölçer fikri).

Robotun pil düzeyi Battery ∈ {0..5}; ölçer BMeter ∈ {0..5}. İki gözlem dizisi:
    geçici arıza : 5555555 00 5555555    (ölçer iki kez saçmalıyor)
    kalıcı arıza : 5555555 000000000     (ölçer bozuldu, hep 0 gösteriyor)

Üç algılayıcı modeli karşılaştırılır (sayılar bizim varsayımımız, fikir kitaptan):
  1. Yalnızca Gauss hatası: Tek bir 0 okuması "pil bitti" diye yorumlanır.
  2. Geçici arıza modeli: P(BMeter = 0 | Battery) ≥ 0.03 (ölçer ara sıra 0 gönderir).
     Kısa aksaklıklar atlatılır; ama uzun 0 dizisinde pilin bittiğine karar verilir (aşırı karamsarlık).
  3. Kalıcı arıza modeli: BMBroken durum değişkeni eklenir (her adım 0.001 olasılıkla bozulur,
     bir kez bozulunca bozuk kalır; bozukken ölçer hep 0 gösterir). İki durumu da doğru açıklar.

Pil dinamiği (varsayım): Her adım aynı kalma olasılığı 0.999; başka herhangi bir değere 0.0002.

Çalıştırma:
    python pil_sensoru.py
"""
from __future__ import annotations

import math

from zamansal import HMM

DUZEYLER = range(6)
GECICI = [5] * 7 + [0] * 2 + [5] * 7
KALICI = [5] * 7 + [0] * 9


def _gauss(m: int, b: int, sigma: float = 1.0) -> float:
    agirlik = [math.exp(-(x - b) ** 2 / (2 * sigma ** 2)) for x in DUZEYLER]
    return agirlik[m] / sum(agirlik)


def _pil_gecisi(b: int, b2: int) -> float:
    return 0.999 if b == b2 else 0.0002


def model(tur: str) -> HMM:
    """tur: 'gauss', 'gecici' ya da 'kalici'."""
    if tur == "kalici":
        durumlar = [(b, bozuk) for bozuk in (False, True) for b in DUZEYLER]
    else:
        durumlar = [(b, False) for b in DUZEYLER]
    T = []
    for b, bozuk in durumlar:
        satir = []
        for b2, bozuk2 in durumlar:
            p = _pil_gecisi(b, b2)
            if tur == "kalici":
                p *= (1.0 if bozuk2 else 0.0) if bozuk else (0.001 if bozuk2 else 0.999)
            satir.append(p)
        T.append(satir)

    def sensor(m):
        sonuc = []
        for b, bozuk in durumlar:
            if bozuk:
                sonuc.append(1.0 if m == 0 else 0.0)
            elif tur == "gauss":
                sonuc.append(_gauss(m, b))
            else:  # geçici arıza: %3 olasılıkla 0, yoksa Gauss hatalı ölçüm
                sonuc.append(0.03 * (m == 0) + 0.97 * _gauss(m, b))
        return sonuc

    onsel = [(1.0 / len(DUZEYLER)) if not bozuk else 0.0 for _, bozuk in durumlar]
    return HMM(durumlar, T, sensor, onsel)


def izle(tur: str, gozlemler) -> tuple[list[float], list[float]]:
    """Her adımda E(Battery | gözlemler) ve P(BMBroken | gözlemler)."""
    h = model(tur)
    beklenen, bozuk = [], []
    for f in h.filtrele(gozlemler):
        beklenen.append(sum(p * b for p, (b, _) in zip(f, h.durumlar)))
        bozuk.append(sum(p for p, (_, k) in zip(f, h.durumlar) if k))
    return beklenen, bozuk


def main() -> None:
    for ad, dizi in (("Geçici arıza", GECICI), ("Kalıcı arıza", KALICI)):
        print(f"=== {ad}: okumalar {''.join(map(str, dizi))} ===")
        print("  model      " + " ".join(f"{t + 1:>4}" for t in range(len(dizi))))
        for tur, etiket in (("gauss", "Gauss"), ("gecici", "geçici"), ("kalici", "kalıcı")):
            e, _ = izle(tur, dizi)
            print(f"  E(B) {etiket:<6}" + " ".join(f"{x:4.1f}" for x in e))
        _, bozuk = izle("kalici", dizi)
        print("  P(bozuk)   " + " ".join(f"{x:4.2f}" for x in bozuk))
        print()
    print("Gauss modeli tek bir 0'da pilin bittiğine inanır. Geçici arıza modeli kısa aksaklığı atlatır,")
    print("ama ölçer gerçekten bozulunca pilin bittiğine karar verir. Kalıcı arıza modeli bozulmayı")
    print("P(BMBroken) ile açıklar ve pil tahminini korur.")


if __name__ == "__main__":
    main()
