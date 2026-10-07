#!/usr/bin/env python3
"""Bölüm 23 alıştırmaları: kodlu çözümler (A3, A5, A7, A8, A9).

Çalıştırma (bölüm klasöründen):
    python cozumler/alistirma_kod.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "ornekler"))

import anlambilim as an  # noqa: E402
import ayristirma as ay  # noqa: E402
import dil_modelleri as dm  # noqa: E402


# --- A3: şaşkınlık ------------------------------------------------------------------
def a3() -> dict:
    test = "ayşe okulda kitap okudu .".split()
    sonuc = {}
    for ad, modeller, agirlik in (
        ("1-gram (Laplace)", [dm.NGram(1, dm.DERLEM, 1)], [1.0]),
        ("2-gram (Laplace)", [dm.NGram(2, dm.DERLEM, 1)], [1.0]),
        ("3-gram (Laplace)", [dm.NGram(3, dm.DERLEM, 1)], [1.0]),
        ("ara değerleme 0.6/0.3/0.1", [dm.NGram(3, dm.DERLEM), dm.NGram(2, dm.DERLEM), dm.NGram(1, dm.DERLEM, 1)], [0.6, 0.3, 0.1]),
    ):
        sonuc[ad] = dm.sasikinlik(dm.ara_degerleme(modeller, agirlik), test)
    return sonuc


# --- A5: CYK tablosu ---------------------------------------------------------------------
def a5() -> dict:
    s = "the wumpus is dead".split()
    P = ay.cyk(s)
    return {(i, j): {X: round(v[0], 8) for X, v in P[(i, j)].items()} for (i, j) in sorted(P) if P[(i, j)]}


# --- A7: edat öbeği bağlanması ---------------------------------------------------------------
def a7() -> dict:
    """'i feel the wumpus near 1 3' için iki ağacın olasılığı (kural olasılıklarıyla elle)."""
    np_i = 0.25 * 0.10
    vp_feel = 0.40 * 0.10
    np_wumpus = 0.25 * 0.40 * 0.15
    pp = 1.0 * 0.10 * (0.05 * 0.20 * 0.20)
    vp_baglama = 0.10 * (0.35 * vp_feel * np_wumpus) * pp
    np_baglama = 0.35 * vp_feel * (0.10 * np_wumpus * pp)
    return {"VP'ye bağlı": 0.90 * np_i * vp_baglama, "NP'ye bağlı": 0.90 * np_i * np_baglama,
            "CYK'nin bulduğu": ay.ayristir("i feel the wumpus near 1 3")[1]}


# --- A8: ağaç bankası ------------------------------------------------------------------------
def a8() -> dict:
    return ay.agac_bankasindan_pcfg(ay.AGAC_BANKASI)


# --- A9: anlamsal dilbilgisi ---------------------------------------------------------------------
def a9() -> dict:
    return {e: an.yorumla(e)[0] for e in ("2 × (3 + 4) - 5", "100 ÷ (2 + 3) ÷ 4", "((7))")}


def main() -> None:
    print("=== A3: şaşkınlık, 'ayşe okulda kitap okudu .' ===")
    for ad, v in a3().items():
        print(f"  {ad:<28} {v:.2f}")

    print("\n=== A5: 'the wumpus is dead' CYK tablosu (i, j): kategoriler ===")
    for hucre, kat in a5().items():
        print(f"  {hucre}: {kat}")

    print("\n=== A7: edat öbeği bağlanması ===")
    for k, v in a7().items():
        print(f"  {k}: {v:.3e}")

    print("\n=== A8: ağaç bankasından PCFG ===")
    for (X, sag), p in sorted(a8().items()):
        print(f"  {X} → {' '.join(sag):<18} [{p:.2f}]")

    print("\n=== A9: aritmetik dilbilgisi ===")
    for e, v in a9().items():
        print(f"  {e} = {v}")


if __name__ == "__main__":
    main()
