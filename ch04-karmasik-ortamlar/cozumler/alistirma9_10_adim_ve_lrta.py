#!/usr/bin/env python3
"""Alıştırma 9 ve 10 çözümleri: gradyan adım büyüklüğü ve LRTA* sezgiselleri."""
from __future__ import annotations

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ornekler"))

import havalimani_gradyan as hg  # noqa: E402
import lrta_yildiz as lr  # noqa: E402


def adim_deneyi() -> list[tuple[float, float]]:
    bas = hg.rastgele_baslangic(random.Random(4))
    sonuc = []
    for alfa in (0.001, 0.01, 0.03, 0.1, 0.2):
        _, gecmis = hg.gradyan_inisi(bas, alfa=alfa, adim=300)
        sonuc.append((alfa, gecmis[-1]))
    return sonuc


def lrta_deneyi(tekrar: int = 40) -> dict[str, list[int]]:
    sezgiseller = {
        "Manhattan": lr.h,
        "h = 0": lambda s: 0,
        "3 × Manhattan": lambda s: 3 * lr.h(s),
    }
    sonuc = {}
    for ad, f in sezgiseller.items():
        ajan = lr.LRTAAjani(f)
        sonuc[ad] = [lr.deneme(ajan) for _ in range(tekrar)]
    return sonuc


def optimale_oturma(uzunluklar: list[int], optimal: int) -> int | None:
    for i in range(len(uzunluklar)):
        if all(u == optimal for u in uzunluklar[i:]):
            return i + 1
    return None


def main() -> None:
    print("=== A9: Gradyan inişinde adım büyüklüğü (300 adım) ===")
    print(f"Newton ile bulunan yerel minimum: {hg.newton(hg.rastgele_baslangic(random.Random(4)))[1][-1] / 1000:,.0f} bin km²")
    for alfa, f in adim_deneyi():
        metin = "IRAKSADI (her adımda büyüyor)" if f > 1e7 else f"{f / 1000:,.0f} bin km²"
        print(f"  α = {alfa:<6} → f = {metin}")
    print("Kararlılık: Bir havalimanına n il düşüyorsa o yöndeki eğrilik 2n'dir. α < 1/n olmalı;"
          "\nα = 1/(2n) tam olarak Newton adımıdır. En kalabalık kümede n ≈ 11 → α ≲ 0,09."
          "\nα = 0,1 sınırda: ilk adımlarda aşırı sıçrıyor ve şans eseri daha iyi bir çukura (942)"
          "\ndüşüyor. Bu güvenilir bir strateji değil; α = 0,2 tamamen ıraksıyor.")

    print("\n=== A10: LRTA* ve sezgisel ===")
    opt = lr.optimal_uzunluk()
    for ad, u in lrta_deneyi().items():
        print(f"  {ad:<14} ilk 6 deneme: {u[:6]}  → {optimale_oturma(u, opt)}. denemeden itibaren hep {opt}")


if __name__ == "__main__":
    main()
