#!/usr/bin/env python3
"""Doğrusal regresyon ve sınıflandırma (kitaptaki 19.6).

Kitabın veri kümeleri (Berkeley ev fiyatları, deprem/patlama sismik verisi) depoda yok; aynı yapıda
sentetik veri üretilir. Gösterilenler:
  * Tek değişkenli regresyon: kapalı biçim (19.3) ve toplu / stokastik gradyan inişi aynı yere varır.
  * Çok değişkenli regresyon: normal denklemler w* = (XᵀX)⁻¹Xᵀy (19.7).
  * L1 ve L2 düzenlileştirme: L1 seyrek (sıfır ağırlıklı) model verir.
  * Sert eşikli doğrusal sınıflandırıcı: algılayıcı öğrenme kuralı; doğrusal ayrılabilir veride yakınsar.
  * Lojistik regresyon: yumuşak eşik, gradyan inişi.
Kitaptaki sayısal örnek: Karar sınırı x2 = 1.7 x1 − 4.9, ağırlıklar ⟨−4.9, 1.7, −1⟩.

Çalıştırma:
    python dogrusal_modeller.py
"""
from __future__ import annotations

import numpy as np


# --- Regresyon -------------------------------------------------------------------
def ev_verisi(n: int = 60, tohum: int = 0):
    """Kitaptaki doğruya (y = 0.232 x + 246, x: ft², y: bin $) benzer sentetik ev verisi."""
    rng = np.random.default_rng(tohum)
    x = rng.uniform(500, 3500, n)
    y = 0.232 * x + 246 + rng.normal(0, 60, n)
    return x, y


def kapali_bicim(x, y) -> tuple[float, float]:
    """(19.3): w1 = (N Σxy − Σx Σy) / (N Σx² − (Σx)²);  w0 = (Σy − w1 Σx) / N."""
    N = len(x)
    w1 = (N * np.sum(x * y) - np.sum(x) * np.sum(y)) / (N * np.sum(x * x) - np.sum(x) ** 2)
    w0 = (np.sum(y) - w1 * np.sum(x)) / N
    return float(w0), float(w1)


def gradyan_inisi(x, y, alfa: float = 0.1, adim: int = 5000, toplu: bool = True, tohum: int = 0):
    """w0 ← w0 + α Σ(y − h(x));  w1 ← w1 + α Σ(y − h(x)) x.  Girdi ölçeklenir (ortalama 0, sapma 1);
    öğrenilen ağırlıklar özgün ölçeğe geri çevrilir."""
    rng = np.random.default_rng(tohum)
    mx, sx, my, sy = x.mean(), x.std(), y.mean(), y.std()
    xs, ys = (x - mx) / sx, (y - my) / sy
    w0 = w1 = 0.0
    for t in range(adim):
        if toplu:
            hata = ys - (w1 * xs + w0)
            w0 += alfa * hata.mean()
            w1 += alfa * (hata * xs).mean()
        else:
            j = rng.integers(len(xs))
            a = alfa / (1 + t / 500)            # azalan öğrenme hızı
            h = ys[j] - (w1 * xs[j] + w0)
            w0 += a * h
            w1 += a * h * xs[j]
    W1 = w1 * sy / sx
    return float(my + sy * w0 - W1 * mx), float(W1)


def normal_denklemler(X, y):
    X1 = np.column_stack([np.ones(len(X)), X])
    return np.linalg.solve(X1.T @ X1, X1.T @ y)


def duzenlilestirilmis(X, y, lam: float, q: int, adim: int = 20_000, alfa: float = 0.01):
    """Kayıp = ortalama kare hata + λ Σ|w_i|^q (kesişim düzenlileştirilmez). L1 için alt gradyan +
    yakınsal (soft-threshold) adım, L2 için düz gradyan."""
    X1 = np.column_stack([np.ones(len(X)), X])
    w = np.zeros(X1.shape[1])
    for _ in range(adim):
        g = 2 * X1.T @ (X1 @ w - y) / len(y)
        if q == 2:
            g[1:] += 2 * lam * w[1:]
            w -= alfa * g
        else:
            w -= alfa * g
            w[1:] = np.sign(w[1:]) * np.maximum(np.abs(w[1:]) - alfa * lam, 0.0)
    return w


# --- Sınıflandırma -------------------------------------------------------------------
def sismik_veri(n: int = 63, tohum: int = 1):
    """Kitaptaki sınıra (x2 = 1.7 x1 − 4.9) göre doğrusal ayrılabilir sentetik veri.
    1 = patlama (sınırın altı/sağı), 0 = deprem."""
    rng = np.random.default_rng(tohum)
    X, y = [], []
    while len(X) < n:
        x1, x2 = rng.uniform(4.5, 7.0), rng.uniform(2.5, 7.5)
        z = -4.9 + 1.7 * x1 - x2
        if abs(z) > 0.15:                        # sınırın hemen yanını boş bırak: ayrılabilir
            X.append((x1, x2))
            y.append(1 if z > 0 else 0)
    return np.array(X), np.array(y)


def esik(z):
    return (np.asarray(z) >= 0).astype(int)


def algilayici(X, y, alfa: float = 0.1, en_cok: int = 100_000, tohum: int = 0):
    """Algılayıcı öğrenme kuralı: w ← w + α (y − h_w(x)) x. (ağırlıklar, adım sayısı)."""
    rng = np.random.default_rng(tohum)
    X1 = np.column_stack([np.ones(len(X)), X])
    w = np.zeros(X1.shape[1])
    for t in range(1, en_cok + 1):
        j = rng.integers(len(X1))
        w += alfa * (y[j] - esik(X1[j] @ w)) * X1[j]
        if t % len(X1) == 0 and np.all(esik(X1 @ w) == y):
            return w, t
    return w, en_cok


def lojistik(z):
    return 1 / (1 + np.exp(-z))


def lojistik_regresyon(X, y, alfa: float = 0.5, adim: int = 20_000):
    """w ← w + α (y − h_w(x)) h_w(x) (1 − h_w(x)) x  (toplu, ortalama)."""
    X1 = np.column_stack([np.ones(len(X)), X])
    mu, sd = X1[:, 1:].mean(axis=0), X1[:, 1:].std(axis=0)
    X1[:, 1:] = (X1[:, 1:] - mu) / sd
    w = np.zeros(X1.shape[1])
    for _ in range(adim):
        h = lojistik(X1 @ w)
        w += alfa * ((y - h) * h * (1 - h)) @ X1 / len(y)
    return w, (mu, sd)


def main() -> None:
    print("=== Tek değişkenli doğrusal regresyon (sentetik ev verisi; kitap: y = 0.232 x + 246) ===")
    x, y = ev_verisi()
    print(f"  kapalı biçim      : w0 = {kapali_bicim(x, y)[0]:7.2f}, w1 = {kapali_bicim(x, y)[1]:.4f}")
    w0, w1 = gradyan_inisi(x, y)
    print(f"  toplu gradyan     : w0 = {w0:7.2f}, w1 = {w1:.4f}")
    w0, w1 = gradyan_inisi(x, y, alfa=0.05, adim=40_000, toplu=False)
    print(f"  stokastik gradyan : w0 = {w0:7.2f}, w1 = {w1:.4f}  (azalan öğrenme hızıyla yaklaşık)")

    print("\n=== Çok değişkenli regresyon ve düzenlileştirme ===")
    rng = np.random.default_rng(3)
    X = rng.normal(size=(80, 8))
    gercek = np.array([0.5, 3.0, -2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])    # yalnızca 2 ilgili nitelik
    yv = gercek[0] + X @ gercek[1:] + rng.normal(0, 0.5, 80)
    np.set_printoptions(precision=2, suppress=True)
    print(f"  gerçek ağırlıklar : {gercek}")
    print(f"  normal denklemler : {normal_denklemler(X, yv)}")
    w1_ = duzenlilestirilmis(X, yv, 0.3, 1)
    w2_ = duzenlilestirilmis(X, yv, 0.3, 2)
    print(f"  L1 (λ = 0.3)      : {w1_}   sıfır ağırlık: {int(np.sum(np.abs(w1_[1:]) < 1e-9))}")
    print(f"  L2 (λ = 0.3)      : {w2_}   sıfır ağırlık: {int(np.sum(np.abs(w2_[1:]) < 1e-9))}")
    print("  L1 ilgisiz niteliklerin çoğunu tam sıfıra indirir (seyrek model); L2 yalnızca küçültür.")

    print("\n=== Algılayıcı (doğrusal ayrılabilir veri, 63 örnek) ===")
    Xs, ys = sismik_veri()
    w, adim = algilayici(Xs, ys)
    print(f"  kitaptaki sınır ⟨−4.9, 1.7, −1⟩ bütün örnekleri ayırıyor mu? "
          f"{np.all(esik(np.column_stack([np.ones(len(Xs)), Xs]) @ np.array([-4.9, 1.7, -1])) == ys)}")
    print(f"  algılayıcı {adim} adımda yakınsadı; w = {w}")

    print("\n=== Lojistik regresyon ===")
    w, (mu, sd) = lojistik_regresyon(Xs, ys)
    olas = lojistik(np.column_stack([np.ones(len(Xs)), (Xs - mu) / sd]) @ w)
    print(f"  eğitim doğruluğu {np.mean((olas >= 0.5) == ys):.3f}; ilk 5 örnek için P(patlama) {np.round(olas[:5], 3)}"
          f", gerçek {ys[:5]}")
    print("  Çıktı bir olasılıktır; sınırın yakınındaki örnekler 0.5'e yakın değer alır.")


if __name__ == "__main__":
    main()
