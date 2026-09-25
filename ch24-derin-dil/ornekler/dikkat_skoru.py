#!/usr/bin/env python3
"""Eğitici dikkat skoru: α = softmax(Q Kᵀ / √d).

Minik sayısal demo (2–3 konum). torch/tensorflow yok.
Özgün eğitim. Kitap metni yok.
https://aima.cs.berkeley.edu/ · https://github.com/aimacode
"""
from __future__ import annotations

import numpy as np


def softmax(x: np.ndarray, eksen: int = -1) -> np.ndarray:
    x = x - np.max(x, axis=eksen, keepdims=True)
    e = np.exp(x)
    return e / np.sum(e, axis=eksen, keepdims=True)


def dikkat(Q: np.ndarray, K: np.ndarray, V: np.ndarray, olcek: bool = True) -> tuple:
    """Döndür: skorlar, α, çıktı."""
    d = Q.shape[-1]
    skor = Q @ K.T
    if olcek:
        skor = skor / np.sqrt(d)
    alfa = softmax(skor, eksen=-1)
    cikti = alfa @ V
    return skor, alfa, cikti


def main() -> None:
    # 3 konum, d=2 — elle seçilmiş (eğitim değil)
    Q = np.array(
        [
            [1.0, 0.2],  # sorgu 0: "anahtar 0'a yakın"
            [0.1, 1.0],  # sorgu 1: "anahtar 1'e yakın"
            [0.5, 0.5],  # sorgu 2: dengeli
        ],
        dtype=float,
    )
    K = np.array(
        [
            [1.0, 0.0],
            [0.0, 1.0],
            [0.6, 0.6],
        ],
        dtype=float,
    )
    V = np.array(
        [
            [10.0, 0.0],
            [0.0, 20.0],
            [5.0, 5.0],
        ],
        dtype=float,
    )

    skor, alfa, cikti = dikkat(Q, K, V, olcek=True)

    print("=== Q (sorgular) ===")
    print(np.round(Q, 3))
    print("=== K (anahtarlar) ===")
    print(np.round(K, 3))
    print("=== ölçekli skorlar QKᵀ/√d ===")
    print(np.round(skor, 3))
    print("=== α = softmax(skor) — satır toplamı 1 olmalı ===")
    print(np.round(alfa, 3))
    print("satır toplamları:", np.round(alfa.sum(axis=1), 6))
    print("=== çıktı = α V ===")
    print(np.round(cikti, 3))

    for i in range(alfa.shape[0]):
        j = int(np.argmax(alfa[i]))
        print(f"sorgu {i} → en çok anahtar {j} (α={alfa[i, j]:.3f})")


if __name__ == "__main__":
    main()
