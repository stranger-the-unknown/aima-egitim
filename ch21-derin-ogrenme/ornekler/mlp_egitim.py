#!/usr/bin/env python3
"""Küçük bir çok katmanlı ağı numpy ile eğitmek (kitaptaki 21.4–21.5).

* XOR: doğrusal model öğrenemez; tek gizli katmanlı ağ öğrenir.
* Mini toplu SGD ve momentum; ağırlık bozunumu (λ Σ W², kitap: λ ≈ 10⁻⁴ yaygın) ve dropout
  (gizli birimlerde tutma olasılığı p = 0.5; test zamanında dropout yok).
* Toplu normalleştirme: ẑ = γ (z − μ) / √(ε + σ²) + β.
* Derin ağlarda kaybolan gradyan: Derin sigmoid ağında ilk katmanın gradyanı çok küçük; artık bağlantılar
  bunu önler.

Çalıştırma:
    python mlp_egitim.py
"""
from __future__ import annotations

import numpy as np


class MLP:
    """Gizli katmanları ReLU (ya da sigmoid), çıktısı softmax olan tam bağlı ağ."""

    def __init__(self, boyutlar, aktivasyon: str = "relu", tohum: int = 0):
        rng = np.random.default_rng(tohum)
        self.W = [rng.normal(0, np.sqrt(2 / a), (a, b)) for a, b in zip(boyutlar[:-1], boyutlar[1:])]
        self.b = [np.zeros(b) for b in boyutlar[1:]]
        self.akt = aktivasyon
        self.hiz = [np.zeros_like(w) for w in self.W] + [np.zeros_like(b) for b in self.b]
        self.rng = rng

    def _g(self, z):
        return np.maximum(0, z) if self.akt == "relu" else 1 / (1 + np.exp(-z))

    def _g_turev(self, z, a):
        return (z > 0).astype(float) if self.akt == "relu" else a * (1 - a)

    def ileri(self, X, dropout: float = 1.0):
        """dropout: gizli birimlerin tutulma olasılığı (eğitimde < 1, ters ölçeklemeyle)."""
        a, onbellek = X, []
        for i, (W, b) in enumerate(zip(self.W, self.b)):
            z = a @ W + b
            if i < len(self.W) - 1:
                h = self._g(z)
                maske = (self.rng.random(h.shape) < dropout) / dropout if dropout < 1 else np.ones_like(h)
                onbellek.append((a, z, h, maske))
                a = h * maske
            else:
                onbellek.append((a, z, None, None))
                e = np.exp(z - z.max(axis=1, keepdims=True))
                a = e / e.sum(axis=1, keepdims=True)
        return a, onbellek

    def adim(self, X, y, alfa: float = 0.1, momentum: float = 0.0, lam: float = 0.0, dropout: float = 1.0) -> float:
        P, onbellek = self.ileri(X, dropout)
        N = len(X)
        kayip = -np.mean(np.log(P[np.arange(N), y] + 1e-12))
        delta = P.copy()
        delta[np.arange(N), y] -= 1
        delta /= N                                         # softmax + çapraz entropi: ∂L/∂z = P − Y
        gW, gb = [None] * len(self.W), [None] * len(self.b)
        for i in reversed(range(len(self.W))):
            a, z, h, maske = onbellek[i]
            gW[i] = a.T @ delta + 2 * lam * self.W[i]
            gb[i] = delta.sum(axis=0)
            if i > 0:
                a_onceki, z_onceki, h_onceki, m_onceki = onbellek[i - 1]
                delta = (delta @ self.W[i].T) * m_onceki * self._g_turev(z_onceki, h_onceki)
        for j, g in enumerate(gW + gb):
            self.hiz[j] = momentum * self.hiz[j] - alfa * g
        for i in range(len(self.W)):
            self.W[i] += self.hiz[i]
            self.b[i] += self.hiz[len(self.W) + i]
        return float(kayip)

    def egit(self, X, y, tur: int = 300, toplu: int = 32, **kw) -> list[float]:
        kayiplar = []
        for _ in range(tur):
            sira = self.rng.permutation(len(X))
            for s in range(0, len(X), toplu):
                parca = sira[s:s + toplu]
                k = self.adim(X[parca], y[parca], **kw)
            kayiplar.append(k)
        return kayiplar

    def dogruluk(self, X, y) -> float:
        return float(np.mean(self.ileri(X)[0].argmax(axis=1) == y))


def ay_verisi(N: int, gurultu: float, tohum: int):
    """İç içe geçmiş iki yarım ay."""
    rng = np.random.default_rng(tohum)
    t = rng.uniform(0, np.pi, N)
    y = rng.integers(0, 2, N)
    X = np.where(y[:, None] == 0, np.column_stack([np.cos(t), np.sin(t)]), np.column_stack([1 - np.cos(t), 0.5 - np.sin(t)]))
    return X + rng.normal(0, gurultu, X.shape), y


def duzenlilestirme_karsilastirmasi(N: int = 30, gurultu: float = 0.35, tur: int = 800, tohumlar=(0, 1, 2)) -> dict:
    Xt, yt = ay_verisi(2000, gurultu, 2)
    sonuc = {}
    for ad, kw in (("düzenlileştirme yok", {}), ("ağırlık bozunumu λ = 1e-2", {"lam": 1e-2}),
                   ("dropout p = 0.5", {"dropout": 0.5})):
        e = t = 0.0
        for s in tohumlar:
            Xe, ye = ay_verisi(N, gurultu, 10 + s)
            m = MLP([2, 64, 64, 2], tohum=s)
            m.egit(Xe, ye, tur=tur, toplu=10, **{"alfa": 0.1, **kw})
            e += m.dogruluk(Xe, ye) / len(tohumlar)
            t += m.dogruluk(Xt, yt) / len(tohumlar)
        sonuc[ad] = (e, t)
    return sonuc


def toplu_normallestir(Z, gamma=1.0, beta=0.0, eps=1e-5):
    return gamma * (Z - Z.mean(axis=0)) / np.sqrt(eps + Z.var(axis=0)) + beta


def ilk_katman_gradyani(derinlik: int, artik: bool, genislik: int = 16, tohum: int = 0) -> float:
    """Derin, sigmoid aktivasyonlu ağda kaybın ilk katmanın girdisine göre gradyanının normu."""
    rng = np.random.default_rng(tohum)
    W = [rng.normal(0, 1 / np.sqrt(genislik), (genislik, genislik)) for _ in range(derinlik)]
    x = rng.normal(size=genislik)
    a, turevler = x, []
    for Wi in W:
        h = 1 / (1 + np.exp(-(a @ Wi)))
        turevler.append(h * (1 - h))
        a = a + h if artik else h
    g = np.ones(genislik)                                  # ∂L/∂(son çıktı) = 1
    for Wi, d in zip(reversed(W), reversed(turevler)):
        g_ic = (g * d) @ Wi.T
        g = g + g_ic if artik else g_ic
    return float(np.linalg.norm(g))


def main() -> None:
    print("=== XOR ===")
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], float)
    y = np.array([0, 1, 1, 0])
    dogrusal = MLP([2, 2], tohum=1)
    dogrusal.egit(X, y, tur=2000, toplu=4, alfa=0.5)
    ag = MLP([2, 8, 2], tohum=1)
    ag.egit(X, y, tur=2000, toplu=4, alfa=0.5)
    print(f"  gizli katmansız (doğrusal) doğruluk {dogrusal.dogruluk(X, y):.2f};  8 gizli birimli ağ {ag.dogruluk(X, y):.2f}")

    print("\n=== İki yarım ay: 30 gürültülü eğitim örneği, büyük ağ (2-64-64-2), 3 tohumun ortalaması ===")
    for ad, (e, t) in duzenlilestirme_karsilastirmasi().items():
        print(f"  {ad:<26}: eğitim {e:.3f}, test {t:.3f}")
    print("  Bu küçük problemde düzenlileştirmenin test kazancı küçüktür (~1 puan) ve tohumdan tohuma değişir;")
    print("  düzenlileştirmenin asıl yararı büyük ağlarda ve az veride ortaya çıkar.")

    print("\n=== Toplu normalleştirme ===")
    Z = np.random.default_rng(0).normal(5, 3, (64, 3))
    Zn = toplu_normallestir(Z)
    print(f"  önce: ortalama {np.round(Z.mean(axis=0), 2)}, std {np.round(Z.std(axis=0), 2)};"
          f"  sonra: ortalama {np.round(Zn.mean(axis=0), 2)}, std {np.round(Zn.std(axis=0), 2)}")

    print("\n=== Derin sigmoid ağında ilk katmanın gradyanı ===")
    for d in (2, 10, 30, 60):
        print(f"  {d:>2} katman: düz {ilk_katman_gradyani(d, False):.2e}, artık bağlantılı {ilk_katman_gradyani(d, True):.2e}")


if __name__ == "__main__":
    main()
