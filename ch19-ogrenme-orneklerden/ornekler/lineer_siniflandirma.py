#!/usr/bin/env python3
"""2B sentetik veri üzerinde sıfırdan perceptron.

Özgün eğitim. numpy OK. Doğrusal ayrılabilir iki Gaussian küme.

https://aima.cs.berkeley.edu/ · https://github.com/aimacode
"""
from __future__ import annotations

from typing import Tuple

import numpy as np


def veri_uret(
    n: int = 80, seed: int = 0
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    # sınıf 0: merkez (-1,-1), sınıf 1: merkez (1,1)
    x0 = rng.normal(loc=(-1.0, -1.0), scale=0.45, size=(n // 2, 2))
    x1 = rng.normal(loc=(1.0, 1.0), scale=0.45, size=(n // 2, 2))
    X = np.vstack([x0, x1])
    y = np.array([-1] * (n // 2) + [1] * (n // 2))
    # karıştır
    perm = rng.permutation(n)
    X, y = X[perm], y[perm]
    # %75 train
    k = int(0.75 * n)
    return X[:k], y[:k], X[k:], y[k:]


def perceptron(
    X: np.ndarray, y: np.ndarray, epoch: int = 20, eta: float = 0.1, seed: int = 0
) -> Tuple[np.ndarray, float]:
    rng = np.random.default_rng(seed)
    w = rng.normal(scale=0.01, size=X.shape[1])
    b = 0.0
    for _ in range(epoch):
        for xi, yi in zip(X, y):
            skor = float(np.dot(w, xi) + b)
            if yi * skor <= 0:
                w = w + eta * yi * xi
                b = b + eta * yi
    return w, b


def dogruluk(X: np.ndarray, y: np.ndarray, w: np.ndarray, b: float) -> float:
    pred = np.where(X @ w + b > 0, 1, -1)
    return float(np.mean(pred == y))


def main() -> None:
    print("=== Perceptron — 2B doğrusal sınıflandırma ===\n")
    Xtr, ytr, Xte, yte = veri_uret(n=80, seed=42)
    w, b = perceptron(Xtr, ytr, epoch=25, eta=0.1, seed=1)
    acc_tr = dogruluk(Xtr, ytr, w, b)
    acc_te = dogruluk(Xte, yte, w, b)
    print(f"Eğitim örnekleri: {len(ytr)}, test: {len(yte)}")
    print(f"Öğrenilen w = {np.round(w, 3)}, b = {b:.3f}")
    print(f"Eğitim doğruluğu: {acc_tr:.3f}")
    print(f"Test doğruluğu:   {acc_te:.3f}")
    # karar sınırı özeti: w·x + b = 0
    if abs(w[1]) > 1e-9:
        print(f"Karar doğrusu (kabaca): x2 = {(-w[0]/w[1]):.3f} * x1 + {(-b/w[1]):.3f}")
    print("\nNot: Doğrusal ayrılabilir kümelerde perceptron ayracı bulur.")


if __name__ == "__main__":
    main()
