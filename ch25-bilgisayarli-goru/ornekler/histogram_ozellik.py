#!/usr/bin/env python3
"""Histogram özelliği ile toy sınıflandırma / uzaklık.

Sentetik gri ve renk yamaları; L1 uzaklığı ile en yakın prototip.
Özgün eğitim. Kitap metni yok. numpy OK.
https://aima.cs.berkeley.edu/ · https://github.com/aimacode
"""
from __future__ import annotations

from typing import Dict, List, Tuple

import numpy as np

RNG = np.random.default_rng(42)
BINS = 8


def gri_histogram(img: np.ndarray, bins: int = BINS) -> np.ndarray:
    """img ∈ [0,1]; normalize frekans vektörü."""
    h, _ = np.histogram(img.ravel(), bins=bins, range=(0.0, 1.0))
    h = h.astype(float)
    s = h.sum()
    return h / s if s > 0 else h


def renk_histogram(rgb: np.ndarray, bins: int = 4) -> np.ndarray:
    """H×W×3, değerler [0,1]; kanal başına histogram birleştir."""
    parcalar = []
    for c in range(3):
        h, _ = np.histogram(rgb[:, :, c].ravel(), bins=bins, range=(0.0, 1.0))
        parcalar.append(h.astype(float))
    v = np.concatenate(parcalar)
    s = v.sum()
    return v / s if s > 0 else v


def l1(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.sum(np.abs(a - b)))


def yama_acik(n: int = 16) -> np.ndarray:
    return np.clip(RNG.normal(0.85, 0.05, size=(n, n)), 0, 1)


def yama_koyu(n: int = 16) -> np.ndarray:
    return np.clip(RNG.normal(0.15, 0.05, size=(n, n)), 0, 1)


def yama_kirmizi(n: int = 16) -> np.ndarray:
    rgb = np.zeros((n, n, 3), dtype=float)
    rgb[:, :, 0] = np.clip(RNG.normal(0.85, 0.05, size=(n, n)), 0, 1)
    rgb[:, :, 1] = np.clip(RNG.normal(0.15, 0.05, size=(n, n)), 0, 1)
    rgb[:, :, 2] = np.clip(RNG.normal(0.15, 0.05, size=(n, n)), 0, 1)
    return rgb


def yama_yesilimsi(n: int = 16) -> np.ndarray:
    rgb = np.zeros((n, n, 3), dtype=float)
    rgb[:, :, 0] = np.clip(RNG.normal(0.15, 0.05, size=(n, n)), 0, 1)
    rgb[:, :, 1] = np.clip(RNG.normal(0.75, 0.05, size=(n, n)), 0, 1)
    rgb[:, :, 2] = np.clip(RNG.normal(0.20, 0.05, size=(n, n)), 0, 1)
    return rgb


def en_yakin(ozellik: np.ndarray, prototipler: Dict[str, np.ndarray]) -> Tuple[str, float]:
    best_et, best_d = "", float("inf")
    for et, p in prototipler.items():
        d = l1(ozellik, p)
        if d < best_d:
            best_d, best_et = d, et
    return best_et, best_d


def main() -> None:
    print("=== Gri histogram: açık vs koyu ===")
    proto_gri = {
        "acik": gri_histogram(yama_acik()),
        "koyu": gri_histogram(yama_koyu()),
    }
    testler_gri: List[Tuple[str, np.ndarray]] = [
        ("acik?", yama_acik()),
        ("koyu?", yama_koyu()),
        ("acik-gürültü", np.clip(yama_acik() - 0.05, 0, 1)),
    ]
    for ad, img in testler_gri:
        tah, d = en_yakin(gri_histogram(img), proto_gri)
        print(f"  {ad:14s} → {tah}  (L1={d:.3f})")

    print("\n=== Renk histogramı: kırmızımsı vs yeşilimsi ===")
    proto_renk = {
        "kirmizi": renk_histogram(yama_kirmizi()),
        "yesil": renk_histogram(yama_yesilimsi()),
    }
    testler_renk = [
        ("kirmizi?", yama_kirmizi()),
        ("yesil?", yama_yesilimsi()),
    ]
    for ad, img in testler_renk:
        tah, d = en_yakin(renk_histogram(img), proto_renk)
        print(f"  {ad:14s} → {tah}  (L1={d:.3f})")

    bozuk = np.clip(yama_acik() * 0.2, 0, 1)
    tah, d = en_yakin(gri_histogram(bozuk), proto_gri)
    print(f"\nBozulmuş 'açık'*0.2 → {tah} (L1={d:.3f})  # beklenen: koyu'ya kayma")


if __name__ == "__main__":
    main()
