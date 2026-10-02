#!/usr/bin/env python3
"""Denetimsiz öğrenme: PCA ve doğrusal otokodlayıcı (kitaptaki 21.7.1).

* PCA: Verinin kovaryansının en büyük m özdeğerine karşılık gelen özvektörler (en çok varyansı tutan yönler).
* Doğrusal otokodlayıcı: kodlayıcı z = W x, kod çözücü x̂ = Wᵀ z (ağırlıklar ortak), kare hata ile eğitilir.
  Kitap: Bu otokodlayıcı PCA ile yakından ilişkilidir; öğrenilen alt uzay en büyük m özdeğerin
  özvektörlerinin gerdiği alt uzaydır. Kod, iki alt uzay arasındaki temel açıları ölçerek doğrular.
* Olasılıksal PCA (PPCA): z ~ N(0, I), x = W z + N(0, σ² I); veri üretmek kolaydır.

Çalıştırma:
    python otokodlayici.py
"""
from __future__ import annotations

import numpy as np


def ppca_ornekle(N: int, W, sigma: float, rng):
    z = rng.normal(size=(N, W.shape[1]))
    return z @ W.T + rng.normal(0, sigma, (N, W.shape[0]))


def pca(X, m: int):
    Xm = X - X.mean(axis=0)
    deger, vektor = np.linalg.eigh(np.cov(Xm.T))
    sira = np.argsort(deger)[::-1]
    return deger[sira], vektor[:, sira[:m]]


def dogrusal_otokodlayici(X, m: int, adim: int = 3000, tohum: int = 0):
    """Ortak ağırlıklı doğrusal otokodlayıcı: kayıp ‖x − WᵀW x‖². (W: m × n).
    Öğrenme hızı verinin ölçeğine göre seçilir (en büyük özdeğer büyükse küçük adım; yoksa ıraksar)."""
    rng = np.random.default_rng(tohum)
    Xm = X - X.mean(axis=0)
    alfa = 0.1 / np.linalg.eigvalsh(np.cov(Xm.T)).max()
    W = rng.normal(0, 0.1, (m, X.shape[1]))
    for _ in range(adim):
        Z = Xm @ W.T
        R = Z @ W - Xm                                    # yeniden kurma hatası
        g = 2 * (Z.T @ R + (R @ W.T).T @ Xm) / len(Xm)
        W -= alfa * g
    return W


def temel_acilar(A, B) -> np.ndarray:
    """Sütunları alt uzay geren iki matris arasındaki temel açılar (derece)."""
    Qa, _ = np.linalg.qr(A)
    Qb, _ = np.linalg.qr(B)
    s = np.clip(np.linalg.svd(Qa.T @ Qb, compute_uv=False), -1, 1)
    return np.degrees(np.arccos(s))


def yeniden_kurma_hatasi(X, taban) -> float:
    Xm = X - X.mean(axis=0)
    Q, _ = np.linalg.qr(taban)
    return float(np.mean(np.sum((Xm - Xm @ Q @ Q.T) ** 2, axis=1)))


def main() -> None:
    rng = np.random.default_rng(0)
    W_gercek = rng.normal(size=(10, 2)) * np.array([3.0, 1.5])
    X = ppca_ornekle(1000, W_gercek, 0.3, rng)
    print("=== PPCA'dan üretilmiş veri: 10 boyut, 2 gizli boyut, gürültü σ = 0.3 ===")
    deger, P = pca(X, 2)
    print("  kovaryans özdeğerleri: " + ", ".join(f"{d:.2f}" for d in deger))
    print("  İlk iki özdeğer büyük, gerisi gürültü düzeyinde (σ² = 0.09): veri gerçekten 2 boyutlu.")

    print("\n=== Doğrusal otokodlayıcı ve PCA ===")
    W = dogrusal_otokodlayici(X, 2)
    print(f"  otokodlayıcı alt uzayı ile PCA alt uzayı arasındaki temel açılar: {np.round(temel_acilar(W.T, P), 3)} derece")
    print(f"  PCA'nın gerdiği alt uzay ile gerçek W'nin gerdiği arasındaki açılar: {np.round(temel_acilar(P, W_gercek), 2)} derece")
    for ad, taban in (("PCA (2 bileşen)", P), ("otokodlayıcı", W.T), ("rastgele 2 boyut", rng.normal(size=(10, 2)))):
        print(f"  {ad:<17} yeniden kurma hatası {yeniden_kurma_hatasi(X, taban):.3f}")


if __name__ == "__main__":
    main()
