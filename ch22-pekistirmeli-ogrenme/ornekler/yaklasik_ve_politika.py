#!/usr/bin/env python3
"""Pekiştirmeli öğrenmede genelleme ve politika araması (kitaptaki 22.4–22.5).

* Doğrusal işlev yaklaşımı (22.9): Û_θ(x, y) = θ₀ + θ₁x + θ₂y. Kitap: θ = (0.5, 0.2, 0.1) → Û(1, 1) = 0.8.
  Delta kuralı (22.10): θᵢ ← θᵢ + α[u − Û_θ(s)] ∂Û/∂θᵢ. Örnekte u(1, 1) = 0.4 ise θ₀, θ₁, θ₂ hepsi 0.4α azalır;
  tek bir gözlem bütün durumların tahminini değiştirir (genelleme).
* 4 × 3 dünyada en iyi politikanın faydaları bu üç özellikle ne kadar iyi temsil edilir? En küçük kareler.
* TD ile işlev yaklaşımı: θᵢ ← θᵢ + α[R + γ Û(s′) − Û(s)] ∂Û(s)/∂θᵢ.
* Politika araması: Softmax politika π_θ(s, a) = e^{θ_{s,a}} / Σ e^{θ_{s,a′}}; politika değeri ρ(θ)'nın gradyanını
  denemelerden tahmin eden REINFORCE: θ ← θ + α G ∇ log π_θ(s, a).

Çalıştırma:
    python yaklasik_ve_politika.py
"""
from __future__ import annotations

import math
import random

import numpy as np

import pasif_ogrenme as po

DURUMLAR = [s for s in po.DUNYA.durumlar if s not in po.DUNYA.uclar]


def ozellik(s) -> np.ndarray:
    return np.array([1.0, s[0], s[1]])


def U_hat(theta, s) -> float:
    return float(theta @ ozellik(s))


def delta_kurali(theta, s, u, alfa: float):
    return theta + alfa * (u - U_hat(theta, s)) * ozellik(s)


def en_kucuk_kareler(U: dict, durumlar=DURUMLAR) -> np.ndarray:
    A = np.array([ozellik(s) for s in durumlar])
    b = np.array([U[s] for s in durumlar])
    return np.linalg.lstsq(A, b, rcond=None)[0]


def td_yaklasik(deneme_sayisi: int = 2000, alfa: float = 0.01, tohum: int = 0) -> np.ndarray:
    rng = random.Random(tohum)
    theta = np.zeros(3)
    for _ in range(deneme_sayisi):
        for s, _, r, s2 in po.deneme_uret(rng):
            sonraki = 0.0 if s2 in po.DUNYA.uclar else U_hat(theta, s2)
            theta += alfa * (r + sonraki - U_hat(theta, s)) * ozellik(s)
    return theta


# --- Politika araması: REINFORCE ----------------------------------------------------------
EYLEMLER = list(po.mdp.YONLER)


def softmax_politika(theta: dict, s) -> np.ndarray:
    z = np.array([theta[(s, a)] for a in EYLEMLER])
    e = np.exp(z - z.max())
    return e / e.sum()


def reinforce(bolum: int = 3000, alfa: float = 0.05, tohum: int = 0, kontrol=(0, 500, 1500, 3000)) -> dict:
    """Tablo biçimli softmax politika; her bölümün getirisi G_t ile θ ← θ + α G_t ∇ log π (temel çizgi: ortalama)."""
    rng = random.Random(tohum)
    nrng = np.random.default_rng(tohum)
    theta = {(s, a): 0.0 for s in DURUMLAR for a in EYLEMLER}
    ortalama, sonuc = 0.0, {}
    for b in range(bolum + 1):
        if b in kontrol:
            pi = {s: EYLEMLER[int(np.argmax(softmax_politika(theta, s)))] for s in DURUMLAR}
            sonuc[b] = po.GERCEK_U[(1, 1)] - _deger(pi)
        if b == bolum:
            break
        s, yol = (1, 1), []
        for _ in range(100):
            if s in po.DUNYA.uclar:
                break
            p = softmax_politika(theta, s)
            i = int(nrng.choice(4, p=p))
            sonuclar = po.DUNYA.gecis[(s, EYLEMLER[i])]
            s2 = rng.choices([x for _, x in sonuclar], weights=[q for q, _ in sonuclar])[0]
            yol.append((s, i, po.DUNYA.odul(s, EYLEMLER[i], s2)))
            s = s2
        G = 0.0
        for s, i, r in reversed(yol):
            G += r
            p = softmax_politika(theta, s)
            for j, a in enumerate(EYLEMLER):
                theta[(s, a)] += alfa * (G - ortalama) * ((1.0 if j == i else 0.0) - p[j])
        ortalama += 0.01 * (sum(r for _, _, r in yol) - ortalama)
    return sonuc


def _deger(pi) -> float:
    try:
        return po.mdp.politika_degerlendir(po.DUNYA, pi)[(1, 1)]
    except Exception:
        return -math.inf


def main() -> None:
    print("=== Doğrusal işlev yaklaşımı (kitap) ===")
    theta = np.array([0.5, 0.2, 0.1])
    print(f"  θ = {theta}: Û(1, 1) = {U_hat(theta, (1, 1)):.2f}")
    yeni = delta_kurali(theta, (1, 1), 0.4, alfa=0.1)
    print(f"  u(1,1) = 0.4, α = 0.1 → θ = {np.round(yeni, 3)} (hepsi 0.4α = 0.04 azaldı)")
    print(f"  Bu tek güncelleme Û(4, 3)'ü de değiştirdi: {U_hat(theta, (4, 3)):.2f} → {U_hat(yeni, (4, 3)):.2f}")

    print("\n=== Gerçek faydalar üç özellikle ne kadar iyi temsil edilir? ===")
    th = en_kucuk_kareler(po.GERCEK_U)
    print(f"  En küçük kareler θ = {np.round(th, 3)}")
    for s in ((1, 1), (3, 2), (4, 1), (3, 3)):
        print(f"    {s}: gerçek {po.GERCEK_U[s]:.3f}, Û {U_hat(th, s):.3f}")
    hata = np.sqrt(np.mean([(po.GERCEK_U[s] - U_hat(th, s)) ** 2 for s in DURUMLAR]))
    print(f"  RMS hata {hata:.3f}: Özellikler −1 durumunun yakınındaki düşüşü yakalayamaz (ör. (4,1)).")
    print(f"  TD + işlev yaklaşımı (2000 deneme): θ = {np.round(td_yaklasik(), 3)}")

    print("\n=== Politika araması: REINFORCE, tablo biçimli softmax politika ===")
    for b, kayip in reinforce().items():
        print(f"  {b:>4} bölüm: politika kaybı {kayip:.3f}")


if __name__ == "__main__":
    main()
