#!/usr/bin/env python3
"""Sigmoid / ReLU / tanh değer karşılaştırması.

Tablo her zaman basılır. matplotlib varsa isteğe bağlı grafik kaydeder.

Özgün eğitim. Kitap metni yok.
https://aima.cs.berkeley.edu/ · https://github.com/aimacode
"""
from __future__ import annotations

from pathlib import Path

import numpy as np


def sigmoid(z: np.ndarray) -> np.ndarray:
    z = np.clip(z, -50, 50)
    return 1.0 / (1.0 + np.exp(-z))


def relu(z: np.ndarray) -> np.ndarray:
    return np.maximum(0.0, z)


def tanh(z: np.ndarray) -> np.ndarray:
    return np.tanh(z)


def main() -> None:
    print("=== Aktivasyon karşılaştırması ===\n")
    zs = np.array([-4.0, -2.0, -1.0, 0.0, 1.0, 2.0, 4.0])
    s = sigmoid(zs)
    r = relu(zs)
    t = tanh(zs)

    print(f"{'z':>6}  {'sigmoid':>10}  {'ReLU':>10}  {'tanh':>10}")
    print("-" * 42)
    for z, a, b, c in zip(zs, s, r, t):
        print(f"{z:6.1f}  {a:10.4f}  {b:10.4f}  {c:10.4f}")

    try:
        import matplotlib.pyplot as plt

        x = np.linspace(-5, 5, 201)
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.plot(x, sigmoid(x), label="sigmoid")
        ax.plot(x, relu(x), label="ReLU")
        ax.plot(x, tanh(x), label="tanh")
        ax.axhline(0, color="gray", lw=0.5)
        ax.axvline(0, color="gray", lw=0.5)
        ax.set_xlabel("z")
        ax.set_ylabel("σ(z)")
        ax.set_title("Aktivasyon fonksiyonları")
        ax.legend()
        ax.grid(True, alpha=0.3)
        out = Path(__file__).resolve().parent / "aktivasyon_plot.png"
        fig.tight_layout()
        fig.savefig(out, dpi=100)
        plt.close(fig)
        print(f"\nGrafik kaydedildi: {out.name}")
    except Exception as exc:
        print(f"\n(Grafik atlandı: {exc})")


if __name__ == "__main__":
    main()
