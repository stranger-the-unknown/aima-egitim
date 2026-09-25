#!/usr/bin/env python3
"""Minik 2D konvolüsyon: sentetik görüntü + kenar çekirdeği.

Sonucu yazdırır; isteğe bağlı PNG (matplotlib varsa).
Özgün eğitim. Kitap metni yok. numpy/matplotlib OK; torch yok.
https://aima.cs.berkeley.edu/ · https://github.com/aimacode
"""
from __future__ import annotations

from pathlib import Path

import numpy as np

# Dikey kenar (Sobel-x benzeri, 3×3)
KERNEL_DIKEY = np.array(
    [
        [-1.0, 0.0, 1.0],
        [-2.0, 0.0, 2.0],
        [-1.0, 0.0, 1.0],
    ]
)

# Yatay kenar (Sobel-y benzeri) — A1 için alternatif
KERNEL_YATAY = np.array(
    [
        [-1.0, -2.0, -1.0],
        [0.0, 0.0, 0.0],
        [1.0, 2.0, 1.0],
    ]
)


def konvolusyon2d(img: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    """Valid (kenarsız) 2D konvolüsyon — eğitici, yavaş ama net."""
    kh, kw = kernel.shape
    h, w = img.shape
    out_h, out_w = h - kh + 1, w - kw + 1
    out = np.zeros((out_h, out_w), dtype=float)
    for i in range(out_h):
        for j in range(out_w):
            pencere = img[i : i + kh, j : j + kw]
            out[i, j] = float(np.sum(pencere * kernel))
    return out


def sentetik_dikey_kenar(n: int = 5) -> np.ndarray:
    """Sol yarı düşük, sağ yarı yüksek — dikey geçiş."""
    img = np.zeros((n, n), dtype=float)
    img[:, n // 2 :] = 1.0
    return img


def main() -> None:
    img = sentetik_dikey_kenar(5)
    print("=== Girdi (5×5, dikey kenar) ===")
    print(np.round(img, 2))

    kenar = konvolusyon2d(img, KERNEL_DIKEY)
    print("\n=== Dikey kenar çekirdeği yanıtı ===")
    print(np.round(kenar, 2))
    print("mutlak max konum:", np.unravel_index(np.argmax(np.abs(kenar)), kenar.shape))

    yatay = konvolusyon2d(img, KERNEL_YATAY)
    print("\n=== Aynı girdi + yatay çekirdek (karşılaştırma) ===")
    print(np.round(yatay, 2))

    # İsteğe bağlı görsel
    out_path = Path(__file__).resolve().parent / "konvolusyon_sonuc.png"
    try:
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(1, 3, figsize=(8, 2.5))
        axes[0].imshow(img, cmap="gray", vmin=0, vmax=1)
        axes[0].set_title("girdi")
        axes[1].imshow(np.abs(kenar), cmap="magma")
        axes[1].set_title("|dikey|")
        axes[2].imshow(np.abs(yatay), cmap="magma")
        axes[2].set_title("|yatay|")
        for ax in axes:
            ax.axis("off")
        fig.tight_layout()
        fig.savefig(out_path, dpi=100)
        plt.close(fig)
        print(f"\nPNG kaydedildi: {out_path.name}")
    except Exception as exc:  # matplotlib yoksa sessizce geç
        print(f"\n(PNG atlandı: {exc})")


if __name__ == "__main__":
    main()
