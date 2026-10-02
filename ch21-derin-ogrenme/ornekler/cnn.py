#!/usr/bin/env python3
"""Evrişimli ağlar (kitaptaki 21.3).

* 1 boyutlu evrişim (21.8): zᵢ = Σⱼ kⱼ x_{j+i−(l+1)/2}. Kitaptaki Şekil 21.4: x = ⟨5, 6, 6, 2, 5, 6, 5⟩,
  çekirdek ⟨+1, −1, +1⟩ (koyu noktayı bulur), adım s = 2 → ⟨5, 9, 4⟩. Aynı işlem bir matris çarpımıdır (21.9).
* Alıcı alan: Adım 1, çekirdek l iken k. gizli katmandaki bir birimin alıcı alanı k(l − 1) + 1 piksel.
* Havuzlama: ortalama havuzlama (çekirdeği 1/l olan evrişim) ve en büyük havuzlama ("bu bölgede özellik var mı?").
* Parametre paylaşımı: Evrişim katmanı tam bağlı katmandan çok daha az parametre ister.
* Artık bağlantı: z⁽ⁱ⁾ = g(z⁽ⁱ⁻¹⁾ + f(z⁽ⁱ⁻¹⁾)); ağırlıklar sıfırsa katman girdiyi aynen geçirir (ReLU ile).

Çalıştırma:
    python cnn.py
"""
from __future__ import annotations

import numpy as np


def evrisim_1b(x, k, adim: int = 1, dolgu: int = 0):
    """Kitaptaki tanım (çekirdek ters çevrilmez: sinyal işlemedeki çapraz ilinti)."""
    x = np.pad(np.asarray(x, float), dolgu)
    l = len(k)
    return np.array([np.dot(k, x[i:i + l]) for i in range(0, len(x) - l + 1, adim)])


def evrisim_matrisi(n: int, k, adim: int) -> np.ndarray:
    l = len(k)
    satirlar = []
    for i in range(0, n - l + 1, adim):
        satir = np.zeros(n)
        satir[i:i + l] = k
        satirlar.append(satir)
    return np.array(satirlar)


def alici_alan(katman: int, l: int = 3, adim: int = 1) -> int:
    """Adım 1 iken: k(l − 1) + 1. Genel adımda her katmanda alan (l − 1) × (önceki adımların çarpımı) büyür."""
    alan, carpim = 1, 1
    for _ in range(katman):
        alan += (l - 1) * carpim
        carpim *= adim
    return alan


def havuzla(x, l: int = 2, tur: str = "max"):
    x = np.asarray(x, float)
    parcalar = x[: len(x) // l * l].reshape(-1, l)
    return parcalar.max(axis=1) if tur == "max" else parcalar.mean(axis=1)


def evrisim_2b(goruntu, cekirdek):
    H, W = goruntu.shape
    h, w = cekirdek.shape
    return np.array([[np.sum(goruntu[i:i + h, j:j + w] * cekirdek) for j in range(W - w + 1)] for i in range(H - h + 1)])


def parametre_karsilastirmasi(boyut: int = 256, kanal: int = 3, cekirdek: int = 5, d: int = 32) -> tuple[int, int]:
    """boyut × boyut × kanal görüntüden aynı boyutta d kanallı bir katmana: tam bağlı ve evrişimli."""
    tam = (boyut * boyut * kanal) * (boyut * boyut * d)
    evr = cekirdek * cekirdek * kanal * d + d
    return tam, evr


def artik_katman(z, W, b):
    """ReLU artık katmanı: g(z + f(z)), f(z) = W relu(z) + b."""
    return np.maximum(0, z + W @ np.maximum(0, z) + b)


def main() -> None:
    print("=== Şekil 21.4: 1 boyutlu evrişim ===")
    x, k = [5, 6, 6, 2, 5, 6, 5], [1, -1, 1]
    z = evrisim_1b(x, k, adim=2)
    M = evrisim_matrisi(len(x), k, 2)
    print(f"  x = {x}, k = {k}, adım 2 → {z.astype(int).tolist()}   (kitap: 5, 9, 4)")
    print(f"  Matris biçimi (21.9):\n{M.astype(int)}\n  M x = {(M @ x).astype(int).tolist()}")
    print(f"  Adım 1 ve dolgu 1 ile çıktı girdiyle aynı boyda: {evrisim_1b(x, k, 1, 1).astype(int).tolist()}")

    print("\n=== Alıcı alan (çekirdek 3) ===")
    for n in (1, 2, 3, 5, 10):
        print(f"  {n:>2}. gizli katman: adım 1 → {alici_alan(n)} piksel, adım 2 → {alici_alan(n, adim=2)} piksel")

    print("\n=== Havuzlama ===")
    y = [1, 3, 2, 8, 0, 0, 5, 4]
    print(f"  {y}: en büyük {havuzla(y).tolist()}, ortalama {havuzla(y, tur='ort').tolist()}")

    print("\n=== 2 boyutlu evrişim: dikey kenar bulucu ===")
    goruntu = np.zeros((6, 6))
    goruntu[:, 3:] = 1
    sobel = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    print(evrisim_2b(goruntu, sobel).astype(int))

    print("\n=== Parametre paylaşımı (256 × 256 × 3 görüntü, 32 kanal, 5 × 5 çekirdek) ===")
    tam, evr = parametre_karsilastirmasi()
    print(f"  tam bağlı: {tam:,} ağırlık;  evrişim: {evr:,} ağırlık")

    print("\n=== Artık katman ===")
    zi = np.array([0.5, 1.2, 0.0, 2.0])
    print(f"  Ağırlıklar sıfırken artık katman girdiyi geçirir: {artik_katman(zi, np.zeros((4, 4)), np.zeros(4)).tolist()}")


if __name__ == "__main__":
    main()
