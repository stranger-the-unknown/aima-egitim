#!/usr/bin/env python3
"""Kalman filtresi (kitaptaki 14.4).

1. Tek boyutlu rastgele yürüyüş (kitaptaki örnek):
       P(x_{t+1} | x_t) = N(x_t, σx²),   P(z_t | x_t) = N(x_t, σz²)
       μ_{t+1}  = ((σt² + σx²) z_{t+1} + σz² μt) / (σt² + σx² + σz²)
       σ²_{t+1} = (σt² + σx²) σz² / (σt² + σx² + σz²)
   Kitaptaki şekil: μ0 = 0.0, σ0 = 1.5, σx = 2.0, σz = 1.0, z1 = 2.5
   → tahmin P(x1) = N(0, 6.25), güncelleme P(x1 | z1) = N(2.155, 0.862).
   Varyans güncellemesi gözlemden bağımsızdır ve hızla sabit bir değere yakınsar.

2. Genel durum (matrislerle): konum–hız izleme, sabit hız modeli.
       x_{t+1} = F x_t + gürültü(Σx),   z_t = H x_t + gürültü(Σz)
       K = (F Σ Fᵀ + Σx) Hᵀ (H (F Σ Fᵀ + Σx) Hᵀ + Σz)⁻¹
       μ ← F μ + K (z − H F μ),   Σ ← (I − K H)(F Σ Fᵀ + Σx)

Çalıştırma:
    python kalman.py
"""
from __future__ import annotations

import math

import numpy as np


def kalman_1b(mu: float, var: float, z: float, var_x: float, var_z: float) -> tuple[float, float]:
    """Tek boyutlu Kalman adımı: (μ_{t+1}, σ²_{t+1})."""
    tahmin_var = var + var_x
    yeni_mu = (tahmin_var * z + var_z * mu) / (tahmin_var + var_z)
    yeni_var = tahmin_var * var_z / (tahmin_var + var_z)
    return yeni_mu, yeni_var


def sabit_varyans(var_x: float, var_z: float) -> float:
    """σ² = (σ² + σx²) σz² / (σ² + σx² + σz²) denkleminin pozitif kökü."""
    # σ⁴ + σx² σ² − σx² σz² = 0
    return (-var_x + math.sqrt(var_x ** 2 + 4 * var_x * var_z)) / 2


def kalman_adimi(mu, Sigma, z, F, Sx, H, Sz):
    tahmin_mu = F @ mu
    tahmin_S = F @ Sigma @ F.T + Sx
    K = tahmin_S @ H.T @ np.linalg.inv(H @ tahmin_S @ H.T + Sz)
    yeni_mu = tahmin_mu + K @ (z - H @ tahmin_mu)
    yeni_S = (np.eye(len(mu)) - K @ H) @ tahmin_S
    return yeni_mu, yeni_S


def izleme(adim: int = 100, tohum: int = 0) -> dict:
    """Bir nesne sabit hızla (az gürültüyle) hareket ediyor; yalnızca konumu gürültülü ölçülüyor."""
    rng = np.random.default_rng(tohum)
    dt = 1.0
    F = np.array([[1, dt], [0, 1]])
    H = np.array([[1.0, 0.0]])
    Sx = np.diag([0.01, 0.01])
    Sz = np.array([[4.0]])                      # ölçüm gürültüsü: σ = 2
    x = np.array([0.0, 1.0])                    # gerçek: konum 0, hız 1
    mu, Sigma = np.array([0.0, 0.0]), np.diag([10.0, 10.0])
    ham_hata, filtre_hata, hizlar = [], [], []
    for _ in range(adim):
        x = F @ x + rng.multivariate_normal([0, 0], Sx)
        z = H @ x + rng.normal(0, 2.0, size=1)
        mu, Sigma = kalman_adimi(mu, Sigma, z, F, Sx, H, Sz)
        ham_hata.append(abs(z[0] - x[0]))
        filtre_hata.append(abs(mu[0] - x[0]))
        hizlar.append(mu[1])
    return {"ham": ham_hata, "filtre": filtre_hata, "hiz": hizlar, "gercek_hiz": x[1], "Sigma": Sigma}


def main() -> None:
    print("=== Tek boyutlu örnek (kitaptaki şekil) ===")
    mu0, var0, var_x, var_z, z1 = 0.0, 1.5 ** 2, 2.0 ** 2, 1.0 ** 2, 2.5
    print(f"  Önsel P(x0)          = N({mu0}, {var0})")
    print(f"  Tahmin P(x1)         = N({mu0}, {var0 + var_x})   (varyans büyür: belirsizlik artar)")
    mu1, var1 = kalman_1b(mu0, var0, z1, var_x, var_z)
    print(f"  Güncelleme P(x1|z1)  = N({mu1:.3f}, {var1:.3f})   (ortalama, gözleme doğru kayar; varyans küçülür)")
    print("  Yeni ortalama, tahmin ile gözlemin ağırlıklı ortalaması: güvenilir olanın ağırlığı büyük.")

    print("\n=== Varyansın yakınsaması (gözlemlerden bağımsız) ===")
    var = var0
    for t in range(1, 7):
        _, var = kalman_1b(0.0, var, 0.0, var_x, var_z)
        print(f"  σ²_{t} = {var:.4f}")
    print(f"  Sabit nokta: {sabit_varyans(var_x, var_z):.4f}  (σ⁴ + σx² σ² − σx² σz² = 0)")

    print("\n=== Genel durum: konum–hız izleme (yalnızca konum ölçülüyor, σz = 2) ===")
    r = izleme()
    for t in (1, 10, 30, 60, 100):
        print(f"  t={t:>3}: ham ölçüm hatası {r['ham'][t - 1]:5.2f}   filtre hatası {r['filtre'][t - 1]:5.2f}"
              f"   tahmin edilen hız {r['hiz'][t - 1]:5.2f}")
    print(f"  Ortalama hata: ham {np.mean(r['ham']):.2f}, filtre {np.mean(r['filtre']):.2f}")
    print(f"  Gerçek hız {r['gercek_hiz']:.2f}: Hız hiç ölçülmediği hâlde konum dizisinden çıkarıldı.")


if __name__ == "__main__":
    main()
