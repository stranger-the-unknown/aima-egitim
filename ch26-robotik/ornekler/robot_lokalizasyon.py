#!/usr/bin/env python3
"""Robot algısı: hareket ve algılayıcı modelleri, Monte Carlo lokalizasyonu, genişletilmiş Kalman süzgeci
(kitaptaki 26.4).

* Kinematik hareket modeli: X̂ₜ₊₁ = Xₜ + (vΔt cos θ, vΔt sin θ, ωΔt); gürültü N(X̂, Σx).
* İşaret noktası (landmark) modeli: uzaklık ve yön açısı, N(ẑ, Σz).
* Uzaklık taraması modeli: M ışın, bağımsız Gauss hata, P(z | x) = α Π exp(−(zⱼ − ẑⱼ)²/2σ²).
* Monte Carlo lokalizasyonu (Şekil 26.6): parçacıkları hareket modelinden örnekle, ışın izleme (ray cast)
  ile beklenen uzaklıkları hesapla, ağırlıklandır, ağırlıkla yeniden örnekle.
  Simetrik bir koridorda inanç iki tepeli olur; ayırt edici bir oda görülünce tek tepeye iner (Şekil 26.7).
* Genişletilmiş Kalman süzgeci: f ve h birinci derece Taylor açılımıyla doğrusallaştırılır. Robot ilerledikçe
  belirsizlik büyür; konumu bilinen bir işaret noktası görülünce küçülür (Şekil 26.9).

Çalıştırma:
    python robot_lokalizasyon.py
"""
from __future__ import annotations

import numpy as np

# Harita: 20 × 2 m koridor, kuzey duvarında x = 16–18 arasında 2 m derin bir girinti (bizim tasarımımız).
KOSELER = [(0, 0), (20, 0), (20, 2), (18, 2), (18, 4), (16, 4), (16, 2), (0, 2)]
DUVARLAR = np.array([(KOSELER[i], KOSELER[(i + 1) % len(KOSELER)]) for i in range(len(KOSELER))], dtype=float)
ISINLAR = np.radians(np.arange(0, 360, 45))          # robota göre 8 ışın
EN_UZAK = 25.0


def bos_alanda(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    koridor = (x > 0) & (x < 20) & (y > 0) & (y < 2)
    girinti = (x > 16) & (x < 18) & (y >= 2) & (y < 4)
    return koridor | girinti


def hareket(X: np.ndarray, v: float, w: float, dt: float = 1.0) -> np.ndarray:
    """Deterministik kinematik model; X: (..., 3) = (x, y, θ)."""
    x, y, t = X[..., 0], X[..., 1], X[..., 2]
    return np.stack([x + v * dt * np.cos(t), y + v * dt * np.sin(t), t + w * dt], axis=-1)


def hareket_ornekle(X: np.ndarray, v: float, w: float, rng, sigma=(0.05, 0.05, 0.03), dt: float = 1.0):
    return hareket(X, v, w, dt) + rng.normal(0, sigma, X.shape)


def isin_izle(X: np.ndarray, duvarlar: np.ndarray = DUVARLAR, isinlar: np.ndarray = ISINLAR) -> np.ndarray:
    """Her poz ve her ışın için en yakın duvara uzaklık. X: (N, 3) → (N, M)."""
    p = X[:, None, None, :2]
    aci = X[:, 2:3] + isinlar[None, :]
    d = np.stack([np.cos(aci), np.sin(aci)], axis=-1)[:, :, None, :]
    a = duvarlar[None, None, :, 0, :]
    e = duvarlar[None, None, :, 1, :] - duvarlar[None, None, :, 0, :]
    capraz = lambda u, v: u[..., 0] * v[..., 1] - u[..., 1] * v[..., 0]  # noqa: E731
    payda = capraz(d, e)
    with np.errstate(divide="ignore", invalid="ignore"):
        t = capraz(a - p, e) / payda
        s = capraz(a - p, d) / payda
    gecerli = (np.abs(payda) > 1e-12) & (t > 1e-9) & (s >= 0) & (s <= 1)
    return np.where(gecerli, t, EN_UZAK).min(axis=2)


def tarama_olabilirligi(z: np.ndarray, beklenen: np.ndarray, sigma: float) -> np.ndarray:
    """log P(z | x) = −Σ (zⱼ − ẑⱼ)² / 2σ² (sabit hariç)."""
    return -((z[None, :] - beklenen) ** 2).sum(axis=1) / (2 * sigma ** 2)


def mcl_adimi(S: np.ndarray, v: float, w: float, z: np.ndarray, rng, sigma_z: float = 0.3) -> np.ndarray:
    """Şekil 26.6'daki güncelleme döngüsü."""
    S2 = hareket_ornekle(S, v, w, rng)
    logW = tarama_olabilirligi(z, isin_izle(S2), sigma_z)
    logW[~bos_alanda(S2[:, 0], S2[:, 1])] = -np.inf          # duvarın içine düşen parçacık olamaz
    W = np.exp(logW - logW.max())
    return S2[rng.choice(len(S2), size=len(S2), p=W / W.sum())]


def baslangic_parcaciklari(N: int, rng, koridor_yonu: bool = True) -> np.ndarray:
    """P(X₀): konum boş alanda düzgün (reddetme örneklemesi).
    koridor_yonu=True: Robot koridora paralel durduğunu bilir ama doğuya mı batıya mı baktığını bilmez
    (bizim varsayımımız: θ ∈ {0, π} ± 0.1). False: θ tamamen düzgün; aynı başarı için çok daha çok parçacık gerekir."""
    parca = []
    while sum(len(p) for p in parca) < N:
        x, y = rng.uniform(0, 20, 4 * N), rng.uniform(0, 4, 4 * N)
        ic = bos_alanda(x, y)
        if koridor_yonu:
            t = rng.choice([0.0, np.pi], ic.sum()) + rng.normal(0, 0.1, ic.sum())
        else:
            t = rng.uniform(-np.pi, np.pi, ic.sum())
        parca.append(np.stack([x[ic], y[ic], t], axis=1))
    return np.concatenate(parca)[:N]


def yakindaki_oran(S: np.ndarray, poz, yaricap: float = 1.0) -> float:
    """Parçacıkların ne kadarı pozun yaricap içinde ve yönü ±0.5 rad içinde?"""
    dxy = np.hypot(S[:, 0] - poz[0], S[:, 1] - poz[1])
    dt = np.abs((S[:, 2] - poz[2] + np.pi) % (2 * np.pi) - np.pi)
    return float(((dxy < yaricap) & (dt < 0.5)).mean())


def mcl_deneyi(N: int = 5000, adim: int = 10, tohum: int = 0, koridor_yonu: bool = True) -> list[tuple]:
    """Robot (6, 1)'den doğuya 1 m/adım ilerler. Her adımda (robotun x'i, gerçeğe yakın oran, ayna pozuna yakın oran)."""
    rng = np.random.default_rng(tohum)
    S = baslangic_parcaciklari(N, rng, koridor_yonu)
    gercek = np.array([6.0, 1.0, 0.0])
    sonuc = []
    for k in range(adim + 1):
        v = 0.0 if k == 0 else 1.0
        if k > 0:
            gercek = hareket(gercek, v, 0.0)
        z = isin_izle(gercek[None, :])[0] + rng.normal(0, 0.05, len(ISINLAR))
        S = mcl_adimi(S, v, 0.0, z, rng)
        ayna = (20 - gercek[0], 2 - gercek[1], gercek[2] + np.pi)
        sonuc.append((float(gercek[0]), yakindaki_oran(S, gercek), yakindaki_oran(S, ayna)))
    return sonuc


# --- Genişletilmiş Kalman süzgeci ---------------------------------------------------------------------
def isaret_olcumu(x: np.ndarray, isaret) -> np.ndarray:
    """ẑ = h(x) = (uzaklık, yön açısı)."""
    dx, dy = isaret[0] - x[0], isaret[1] - x[1]
    return np.array([np.hypot(dx, dy), np.arctan2(dy, dx) - x[2]])


def ekf_adimi(mu, Sigma, v, w, z, isaret, Sx, Sz, dt: float = 1.0):
    """Tahmin: μ̄ = f(μ, a), Σ̄ = F Σ Fᵀ + Σx.  Düzeltme (z varsa): K = Σ̄ Hᵀ (H Σ̄ Hᵀ + Σz)⁻¹."""
    t = mu[2]
    F = np.array([[1, 0, -v * dt * np.sin(t)], [0, 1, v * dt * np.cos(t)], [0, 0, 1]])
    mu = hareket(mu, v, w, dt)
    Sigma = F @ Sigma @ F.T + Sx
    if z is not None:
        dx, dy = isaret[0] - mu[0], isaret[1] - mu[1]
        q = dx ** 2 + dy ** 2
        H = np.array([[-dx / np.sqrt(q), -dy / np.sqrt(q), 0], [dy / q, -dx / q, -1]])
        K = Sigma @ H.T @ np.linalg.inv(H @ Sigma @ H.T + Sz)
        yenilik = z - isaret_olcumu(mu, isaret)
        yenilik[1] = (yenilik[1] + np.pi) % (2 * np.pi) - np.pi
        mu = mu + K @ yenilik
        Sigma = (np.eye(3) - K @ H) @ Sigma
    return mu, Sigma


def ekf_deneyi(adim: int = 12, gorus: float = 3.0, tohum: int = 0) -> list[tuple]:
    """Düz çizgide ilerleyen robot; (6, 2)'deki işaret yalnızca 'gorus' metreden yakınken görülür.
    Her adımda (x, işaret görüldü mü, konumun standart sapmaları kökü √(σx² + σy²))."""
    rng = np.random.default_rng(tohum)
    isaret = (6.0, 2.0)
    Sx, Sz = np.diag([0.1, 0.1, 0.01]) ** 2 * 4, np.diag([0.1, 0.05]) ** 2
    gercek = np.array([0.0, 0.0, 0.0])
    mu, Sigma = gercek.copy(), np.diag([0.01, 0.01, 0.001])
    sonuc = []
    for _ in range(adim):
        gercek = hareket(gercek, 1.0, 0.0) + rng.normal(0, [0.2, 0.2, 0.02])
        z = None
        if np.hypot(*(np.array(isaret) - gercek[:2])) < gorus:
            z = isaret_olcumu(gercek, isaret) + rng.normal(0, [0.1, 0.05])
        mu, Sigma = ekf_adimi(mu, Sigma, 1.0, 0.0, z, isaret, Sx, Sz)
        sonuc.append((round(float(gercek[0]), 1), z is not None, float(np.sqrt(Sigma[0, 0] + Sigma[1, 1]))))
    return sonuc


def dogrusallastirma(mu: float = 1.0, sigma: float = 0.5, n: int = 200_000, tohum: int = 0) -> dict:
    """Şekil 26.8: f(x) = x + sin(2x). Taylor: ortalama f(μ), varyans F²σ²; Monte Carlo ile karşılaştır."""
    f = lambda x: x + np.sin(2 * x)  # noqa: E731
    F = 1 + 2 * np.cos(2 * mu)
    x = np.random.default_rng(tohum).normal(mu, sigma, n)
    return {"Taylor ortalama": float(f(mu)), "gerçek ortalama": float(f(x).mean()),
            "Taylor std": float(abs(F) * sigma), "gerçek std": float(f(x).std())}


def main() -> None:
    print("=== Hareket ve algılayıcı modelleri ===")
    X = np.array([2.0, 1.0, np.radians(30)])
    print(f"  (2, 1, 30°) + v = 1, ω = 0.2, Δt = 1 → {np.round(hareket(X, 1.0, 0.2), 3)}")
    z = isaret_olcumu(np.array([0.0, 0.0, 0.0]), (3.0, 4.0))
    print(f"  (0, 0, 0°)'dan (3, 4)'teki işaret: uzaklık {z[0]:.1f}, yön {np.degrees(z[1]):.1f}°")
    print(f"  (6, 1, 0°)'dan 8 ışınlık tarama: {np.round(isin_izle(np.array([[6.0, 1.0, 0.0]]))[0], 2)}")

    print("\n=== Monte Carlo lokalizasyonu (5000 parçacık, simetrik koridor + girinti) ===")
    for k, (x, g, a) in enumerate(mcl_deneyi()):
        print(f"  adım {k:>2}: robot x = {x:4.1f}   gerçeğe yakın %{100 * g:5.1f}   ayna pozuna yakın %{100 * a:5.1f}")
    print("  Koridor 180° dönmeye göre simetrik: Girinti görülene dek inanç iki tepeli, sonra tek tepeli.")
    print("  (Yeniden örnekleme rastgele olduğu için bazı tohumlarda tepelerden biri erken kaybolabilir: A3.)")

    print("\n=== Genişletilmiş Kalman süzgeci: (6, 2)'de bir işaret noktası ===")
    for x, gordu, s in ekf_deneyi():
        print(f"  x ≈ {x:5.1f}  işaret {'görüldü ' if gordu else 'yok     '}  konum belirsizliği {s:.3f}")

    print("\n=== Doğrusallaştırma (f(x) = x + sin 2x, μ = 1, σ = 0.5) ===")
    for k, v in dogrusallastirma().items():
        print(f"  {k:<16}: {v:.3f}")


if __name__ == "__main__":
    main()
