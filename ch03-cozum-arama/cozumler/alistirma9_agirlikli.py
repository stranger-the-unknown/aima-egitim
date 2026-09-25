#!/usr/bin/env python3
"""Alıştırma 9 çözümü: ağırlıklı A* ile hız–kalite ödünleşimi (8-bulmaca, h2)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ornekler"))

from arama import agirlikli_a_yildiz  # noqa: E402
from sekiz_bulmaca import KITAP_BASLANGIC, SekizBulmaca  # noqa: E402

C_YILDIZ = 26  # kitap örneğinin optimal çözüm uzunluğu


def deney(agirliklar=(1.0, 1.5, 2.0, 5.0)):
    satirlar = []
    for W in agirliklar:
        s = agirlikli_a_yildiz(SekizBulmaca(KITAP_BASLANGIC), W=W)
        satirlar.append((W, len(s.eylemler), s.uretilen))
    return satirlar


def main() -> None:
    print(f"{'W':>5}{'çözüm':>8}{'üretilen':>11}{'W·C*':>7}{'sınır tutuyor mu?':>20}")
    for W, uzunluk, uretilen in deney():
        print(f"{W:>5}{uzunluk:>8}{uretilen:>11,}{W * C_YILDIZ:>7.0f}{str(uzunluk <= W * C_YILDIZ):>20}")
    print(
        "\nW büyüdükçe arama sezgisele daha çok güvenir ve genelde çok daha az düğüm üretir."
        "\nBedeli daha uzun çözümlerdir. Ama maliyet her zaman W·C* sınırının altında kalır."
        "\nW = 1 sıradan A*'tır (optimal). W → ∞ ise açgözlü aramaya yaklaşır."
    )


if __name__ == "__main__":
    main()
