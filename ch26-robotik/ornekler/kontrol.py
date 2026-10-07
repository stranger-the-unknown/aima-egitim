#!/usr/bin/env python3
"""Yörünge izleme denetimi ve en iyi denetim (kitaptaki 26.5.3, 26.5.4).

Model: tek eklem, sürtünmesiz çift integratör q̈ = u + d (kütle 1; d sistematik dış kuvvet, ör. eğimli yol).
* P denetçisi: u = K_P (ξ − q). Sürtünme yokken bir yay yasasıdır: sonsuza dek salınır (K_P küçültmek de çözmez).
* PD denetçisi: u = K_P (ξ − q) + K_D (ξ̇ − q̇). Türev terimi sönümler (kitaptaki K_P = 0.3, K_D = 0.8).
* PID: + K_I ∫ (ξ − q). Sistematik bir kuvvet varken PD'nin bıraktığı kalıcı hatayı giderir.
* LQR: ẋ = Ax + Bu, maliyet ∫ xᵀQx + uᵀRu. En iyi politika doğrusal, u = −Kx; K Riccati denkleminden.
  Çift integratörde Q = diag(1, 0), R = 1 için sürekli zamanda K = [1, √2]: en iyi denetçi bir PD denetçisidir.

Çalıştırma:
    python kontrol.py
"""
from __future__ import annotations

import numpy as np


def benzet(KP: float, KD: float = 0.0, KI: float = 0.0, hedef: float = 1.0, d: float = 0.0,
           sure: float = 60.0, dt: float = 0.01) -> tuple[np.ndarray, np.ndarray]:
    """q(0) = 0, q̇(0) = 0'dan sabit ξ = hedef'e. (zamanlar, q dizisi)."""
    n = int(sure / dt)
    q, v, integral = 0.0, 0.0, 0.0
    Q = np.empty(n)
    for i in range(n):
        hata = hedef - q
        integral += hata * dt
        u = KP * hata + KD * (0.0 - v) + KI * integral
        v += (u + d) * dt                     # yarı örtük Euler: önce hız, sonra konum
        q += v * dt
        Q[i] = q
    return np.arange(1, n + 1) * dt, Q


def ozet(t: np.ndarray, Q: np.ndarray, hedef: float = 1.0) -> dict:
    son = Q[t > t[-1] - 10]
    return {"aşım": float(Q.max() - hedef), "son 10 s salınım": float(son.max() - son.min()),
            "son hata": float(hedef - Q[-1])}


def lqr_ayrik(A: np.ndarray, B: np.ndarray, Q: np.ndarray, R: np.ndarray, yineleme: int = 20000) -> np.ndarray:
    """Ayrık zamanlı cebirsel Riccati denklemini yineleyerek çöz; K döndür (u = −Kx)."""
    P = Q.copy()
    for _ in range(yineleme):
        K = np.linalg.solve(R + B.T @ P @ B, B.T @ P @ A)
        P_yeni = Q + A.T @ P @ (A - B @ K)
        if np.allclose(P_yeni, P, atol=1e-12):
            break
        P = P_yeni
    return np.linalg.solve(R + B.T @ P @ B, B.T @ P @ A)


def cift_integrator(dt: float):
    return np.array([[1.0, dt], [0.0, 1.0]]), np.array([[0.5 * dt * dt], [dt]])


def lqr_benzet(K: np.ndarray, x0=(1.0, 0.0), dt: float = 0.01, sure: float = 20.0) -> np.ndarray:
    A, B = cift_integrator(dt)
    x = np.array(x0, dtype=float)
    yol = []
    for _ in range(int(sure / dt)):
        x = A @ x + (B @ (-K @ x)).ravel()
        yol.append(x.copy())
    return np.array(yol)


def main() -> None:
    print("=== Denetçiler: q = 0'dan ξ = 1'e (sürtünmesiz çift integratör) ===")
    for ad, kw in (("P, K_P = 1.0", dict(KP=1.0)), ("P, K_P = 0.1", dict(KP=0.1)),
                   ("PD, K_P = 0.3, K_D = 0.8", dict(KP=0.3, KD=0.8))):
        o = ozet(*benzet(**kw))
        print(f"  {ad:<26}: aşım {o['aşım']:5.2f}, son 10 s'de q'nun en büyük − en küçük farkı "
              f"{o['son 10 s salınım']:5.2f}")
    print("  P denetçisi kararlı ama kesin kararlı değil: hata sınırlı kalır ama sıfıra inmez.")

    print("\n=== Sistematik dış kuvvet d = −0.05 (eğimli yol) ===")
    for ad, kw in (("PD, K_P = 0.3, K_D = 0.8", dict(KP=0.3, KD=0.8)),
                   ("PID, + K_I = 0.05", dict(KP=0.3, KD=0.8, KI=0.05))):
        o = ozet(*benzet(d=-0.05, sure=200, **kw))
        print(f"  {ad:<26}: son hata {o['son hata']:6.3f}")
    print(f"  PD'nin kalıcı hatası beklenen d / K_P = {0.05 / 0.3:.3f}; integral terimi bunu sıfırlar.")

    print("\n=== LQR: çift integratör, Q = diag(1, 0), R = 1 ===")
    for dt in (0.1, 0.01):
        A, B = cift_integrator(dt)
        K = lqr_ayrik(A, B, np.diag([1.0, 0.0]), np.array([[1.0]]))
        print(f"  Δt = {dt}: K = {np.round(K.ravel(), 3)}  (sürekli zaman: [1, √2 = 1.414])")
    K = lqr_ayrik(*cift_integrator(0.01), np.diag([1.0, 0.0]), np.array([[1.0]]))
    yol = lqr_benzet(K)
    print(f"  x₀ = (1, 0)'dan 20 s sonra: konum {yol[-1, 0]:.4f}, en büyük aşım {-yol[:, 0].min():.3f}")
    print("  u = −Kx = −K_P q − K_D q̇: LQR'nin bulduğu en iyi politika, K_P = 1, K_D ≈ 1.41 olan bir PD denetçisidir.")


if __name__ == "__main__":
    main()
