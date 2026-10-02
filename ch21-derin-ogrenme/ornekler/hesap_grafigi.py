#!/usr/bin/env python3
"""İleri beslemeli ağlar ve hesap grafikleri (kitaptaki 21.1–21.2).

* Aktivasyonlar: sigmoid, ReLU, softplus = log(1 + eˣ) (türevi sigmoid), tanh = 2σ(2x) − 1.
* Şekil 21.3(a): 2 girdi, 2 gizli birim (3, 4), 1 çıktı birimi (5).
      ŷ = g5(w05 + w35 g3(w03 + w13 x1 + w23 x2) + w45 g4(w04 + w14 x1 + w24 x2))      (21.2)
  Geri yayılım (21.4–21.5): ∂L/∂w35 = −2(y − ŷ) g5'(in5) a3,  ∂L/∂w13 = −2(y − ŷ) g5'(in5) w35 g3'(in3) x1.
  Sayısal gradyanla doğrulanır.
* Softmax (kitap): girdi ⟨5, 2, 0, −2⟩ → ⟨0.946, 0.047, 0.006, 0.001⟩. d = 2'de sigmoid'e indirgenir.
* Çapraz entropi H(P, Q) = H(P) + D_KL(P ‖ Q).
* Kaybolan gradyan: sigmoid'in türevi en çok 1/4; n katmandan geçen gradyan ≤ (w/4)ⁿ ile küçülür.

Çalıştırma:
    python hesap_grafigi.py
"""
from __future__ import annotations

import math

import numpy as np


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def relu(x):
    return np.maximum(0, x)


def softplus(x):
    return np.log1p(np.exp(x))


def softmax(z):
    z = np.asarray(z, dtype=float)
    e = np.exp(z - z.max())
    return e / e.sum()


def capraz_entropi(P, Q) -> float:
    """H(P, Q) = −Σ P log Q (kitap beklentiyi log Q ile yazar; burada alışılmış negatif işaretli biçim)."""
    P, Q = np.asarray(P, float), np.asarray(Q, float)
    return float(-np.sum(P * np.log(Q)))


def entropi(P) -> float:
    P = np.asarray(P, float)
    P = P[P > 0]
    return float(-np.sum(P * np.log(P)))


def kl(P, Q) -> float:
    P, Q = np.asarray(P, float), np.asarray(Q, float)
    m = P > 0
    return float(np.sum(P[m] * np.log(P[m] / Q[m])))


# --- Şekil 21.3'teki ağ ----------------------------------------------------------------
AGIRLIKLAR = {"w03": 0.1, "w13": 0.5, "w23": -0.3, "w04": -0.2, "w14": 0.8, "w24": 0.4,
              "w05": 0.05, "w35": 1.2, "w45": -0.7}          # örnek değerler (kitap sayı vermez)


def ileri(w: dict, x1: float, x2: float, g=sigmoid):
    in3 = w["w03"] + w["w13"] * x1 + w["w23"] * x2
    in4 = w["w04"] + w["w14"] * x1 + w["w24"] * x2
    a3, a4 = g(in3), g(in4)
    in5 = w["w05"] + w["w35"] * a3 + w["w45"] * a4
    return {"in3": in3, "in4": in4, "a3": a3, "a4": a4, "in5": in5, "y_hat": g(in5)}


def kayip(w, x1, x2, y) -> float:
    return float((y - ileri(w, x1, x2)["y_hat"]) ** 2)


def geri_yayilim(w: dict, x1: float, x2: float, y: float) -> dict:
    """Bütün ağırlıkların gradyanı; Δ5 = 2(ŷ − y) g5'(in5), Δ3 = Δ5 w35 g3'(in3) (sigmoid için g' = g(1 − g))."""
    a = ileri(w, x1, x2)
    d5 = 2 * (a["y_hat"] - y) * a["y_hat"] * (1 - a["y_hat"])
    d3 = d5 * w["w35"] * a["a3"] * (1 - a["a3"])
    d4 = d5 * w["w45"] * a["a4"] * (1 - a["a4"])
    return {"w05": d5, "w35": d5 * a["a3"], "w45": d5 * a["a4"],
            "w03": d3, "w13": d3 * x1, "w23": d3 * x2,
            "w04": d4, "w14": d4 * x1, "w24": d4 * x2}


def sayisal_gradyan(w: dict, x1, x2, y, h: float = 1e-6) -> dict:
    g = {}
    for k in w:
        art, eks = dict(w), dict(w)
        art[k] += h
        eks[k] -= h
        g[k] = (kayip(art, x1, x2, y) - kayip(eks, x1, x2, y)) / (2 * h)
    return g


def kaybolan_gradyan(derinlik: int, w: float = 1.0, tohum: int = 0) -> float:
    """Her katmanda tek sigmoid birim, ağırlık w: çıktıdan girdiye geri yayılan gradyanın büyüklüğü."""
    rng = np.random.default_rng(tohum)
    a, turev = rng.normal(), 1.0
    for _ in range(derinlik):
        a = sigmoid(w * a)
        turev *= w * a * (1 - a)
    return float(abs(turev))


def main() -> None:
    print("=== Aktivasyon fonksiyonları ===")
    x = np.array([-2.0, 0.0, 2.0])
    print(f"  x = {x}: sigmoid {np.round(sigmoid(x), 3)}, ReLU {relu(x)}, softplus {np.round(softplus(x), 3)}, tanh {np.round(np.tanh(x), 3)}")
    print(f"  tanh(x) = 2σ(2x) − 1? {np.allclose(np.tanh(x), 2 * sigmoid(2 * x) - 1)};  softplus'(x) = σ(x)? "
          f"{np.allclose((softplus(x + 1e-6) - softplus(x - 1e-6)) / 2e-6, sigmoid(x))}")

    print("\n=== Şekil 21.3: 2-2-1 ağ, ileri hesap ve geri yayılım ===")
    a = ileri(AGIRLIKLAR, 1.0, 0.5)
    print(f"  x = (1, 0.5): a3 = {a['a3']:.4f}, a4 = {a['a4']:.4f}, ŷ = {a['y_hat']:.4f}")
    g, s = geri_yayilim(AGIRLIKLAR, 1.0, 0.5, 1.0), sayisal_gradyan(AGIRLIKLAR, 1.0, 0.5, 1.0)
    for k in ("w35", "w13", "w24", "w05"):
        print(f"  ∂L/∂{k}: geri yayılım {g[k]:+.6f}, sayısal {s[k]:+.6f}")

    print("\n=== Softmax ve çapraz entropi ===")
    print(f"  softmax(⟨5, 2, 0, −2⟩) = {np.round(softmax([5, 2, 0, -2]), 3)}   (kitap: 0.946, 0.047, 0.006, 0.001)")
    print(f"  d = 2'de softmax(⟨z, 0⟩)₁ = σ(z)? {np.isclose(softmax([1.7, 0])[0], sigmoid(1.7))}")
    P, Q = [0.7, 0.2, 0.1], [0.5, 0.3, 0.2]
    print(f"  H(P, Q) = {capraz_entropi(P, Q):.4f} = H(P) + KL = {entropi(P):.4f} + {kl(P, Q):.4f};  H(P, P) = {capraz_entropi(P, P):.4f} ≠ 0")

    print("\n=== Kaybolan gradyan (her katmanda bir sigmoid, w = 1) ===")
    for n in (1, 5, 10, 20, 50):
        print(f"  {n:>2} katman: gradyan büyüklüğü {kaybolan_gradyan(n):.2e}   (üst sınır 0.25^n = {0.25 ** n:.2e})")


if __name__ == "__main__":
    main()
