#!/usr/bin/env python3
"""Alıştırma 6 çözümü: GA'da mutasyon, seçim ve elitizmin etkisi."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ornekler"))

from genetik_8vezir import EN_IYI, genetik_algoritma, uygunluk  # noqa: E402

TOHUM = 10
NESIL = 500


def olc(mutasyon: float, secim: str, elit: int = 2) -> tuple[int, float]:
    basari = []
    for t in range(TOHUM):
        birey, nesil, _ = genetik_algoritma(100, mutasyon, NESIL, secim, elit, t)
        if uygunluk(birey) == EN_IYI:
            basari.append(nesil)
    ort = sum(basari) / len(basari) if basari else float("nan")
    return len(basari), ort


def main() -> None:
    print(f"Her ayar için {TOHUM} tohum, en fazla {NESIL} nesil, popülasyon 100\n")
    print(f"{'seçim':<10}{'mutasyon':>9}{'elit':>6}{'başarı':>9}{'ort. nesil':>12}")
    for secim in ("orantili", "turnuva"):
        for mut in (0.0, 0.1, 0.6):
            b, ort = olc(mut, secim)
            print(f"{secim:<10}{mut:>9}{2:>6}{b:>6}/{TOHUM}{ort:>12.0f}")
    b, ort = olc(0.6, "orantili", elit=0)
    print(f"{'orantili':<10}{0.6:>9}{0:>6}{b:>6}/{TOHUM}{ort:>12.0f}")


if __name__ == "__main__":
    main()
