#!/usr/bin/env python3
"""XOR üzerinde sıfırdan minik MLP (2 → 2 → 1), saf numpy.

Birkaç yüz epoch; kayıp yazdırılır. torch yok.

Özgün eğitim. Kitap metni yok.
https://aima.cs.berkeley.edu/ · https://github.com/aimacode
"""
from __future__ import annotations

from typing import Tuple

import numpy as np


def sigmoid(z: np.ndarray) -> np.ndarray:
    z = np.clip(z, -50, 50)
    return 1.0 / (1.0 + np.exp(-z))


def sigmoid_turev_a(a: np.ndarray) -> np.ndarray:
    """σ'(z) = a(1-a) — a = σ(z) biliniyorsa."""
    return a * (1.0 - a)


def egit(
    X: np.ndarray,
    y: np.ndarray,
    epoch: int = 4000,
    eta: float = 0.5,
    seed: int = 1,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, list]:
    """
    X: (4, 2), y: (4, 1)
    Gizli: 2 birim, çıkış: 1 birim. Sigmoid + MSE.
    """
    rng = np.random.default_rng(seed)
    W1 = rng.normal(scale=0.5, size=(2, 2))
    b1 = np.zeros(2)
    W2 = rng.normal(scale=0.5, size=(2, 1))
    b2 = np.zeros(1)
    kayip_gecmisi: list = []

    for ep in range(1, epoch + 1):
        z1 = X @ W1 + b1
        a1 = sigmoid(z1)
        z2 = a1 @ W2 + b2
        a2 = sigmoid(z2)

        err = a2 - y
        loss = float(np.mean(err**2))
        kayip_gecmisi.append(loss)

        n = X.shape[0]
        da2 = (2.0 / n) * err
        dz2 = da2 * sigmoid_turev_a(a2)
        dW2 = a1.T @ dz2
        db2 = dz2.sum(axis=0)

        da1 = dz2 @ W2.T
        dz1 = da1 * sigmoid_turev_a(a1)
        dW1 = X.T @ dz1
        db1 = dz1.sum(axis=0)

        W2 -= eta * dW2
        b2 -= eta * db2
        W1 -= eta * dW1
        b1 -= eta * db1

        if ep == 1 or ep % 500 == 0 or ep == epoch:
            print(f"epoch {ep:5d}  MSE={loss:.6f}")

    return W1, b1, W2, b2, kayip_gecmisi


def tahmin(
    X: np.ndarray, W1: np.ndarray, b1: np.ndarray, W2: np.ndarray, b2: np.ndarray
) -> np.ndarray:
    a1 = sigmoid(X @ W1 + b1)
    return sigmoid(a1 @ W2 + b2)


def main() -> None:
    print("=== Minik MLP — XOR (saf numpy) ===\n")
    X = np.array([[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]])
    y = np.array([[0.0], [1.0], [1.0], [0.0]])

    W1, b1, W2, b2, hist = egit(X, y, epoch=4000, eta=0.8, seed=42)
    pred = tahmin(X, W1, b1, W2, b2)

    print("\nGirdi → hedef → tahmin (sürekli) → yuvarlak")
    for xi, yi, pi in zip(X, y, pred):
        print(
            f"  {xi.astype(int).tolist()} → {int(yi[0])} → {pi[0]:.3f} → {int(pi[0] >= 0.5)}"
        )
    print(f"\nİlk MSE={hist[0]:.4f}, son MSE={hist[-1]:.4f}")
    print("Not: Gizli katman + sigmoid XOR’u doğrusal olmayan sınırla çözer.")


if __name__ == "__main__":
    main()
