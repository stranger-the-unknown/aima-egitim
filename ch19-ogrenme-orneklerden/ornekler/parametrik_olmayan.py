#!/usr/bin/env python3
"""Parametrik olmayan modeller (kitaptaki 19.7).

* k en yakın komşu: k = 1 aşırı uydurur, k = 5 daha düzgündür; birimler değişince komşular değişir,
  bu yüzden her boyut normalleştirilir.
* k-d ağacı: her düzeyde bir boyutta ortancaya göre böl; en yakın komşuyu kaba kuvvetle aynı bulur.
* Parametrik olmayan regresyon: k-NN ortalaması ve yerel ağırlıklı regresyon (dörtlü çekirdek).
* Destek vektör makinesi: en büyük marjlı ayırıcı (burada menteşe kaybıyla alt gradyan, Pegasos tarzı).
* Çekirdek hilesi (kitap, 19.12): F(x) = (x₁², x₂², √2 x₁x₂) için F(x)·F(z) = (x·z)². Çember içi/dışı
  veri girdi uzayında doğrusal ayrılamaz, F uzayında ayrılır.

Çalıştırma:
    python parametrik_olmayan.py
"""
from __future__ import annotations

import math

import numpy as np


# --- k-NN ----------------------------------------------------------------------------
def knn_siniflandir(X, y, sorgu, k: int) -> int:
    d = np.linalg.norm(X - sorgu, axis=1)
    komsular = y[np.argsort(d, kind="stable")[:k]]
    return int(np.round(komsular.mean()))          # çoğunluk oyu (ikili sınıf, k tek)


def birini_disarida_birak(X, y, k: int) -> float:
    """LOOCV doğruluğu."""
    dogru = 0
    for j in range(len(X)):
        maske = np.arange(len(X)) != j
        dogru += knn_siniflandir(X[maske], y[maske], X[j], k) == y[j]
    return dogru / len(X)


def gurultulu_veri(n: int = 120, gurultu: float = 0.12, tohum: int = 2):
    """x2 = 1.7 x1 − 4.9 sınırı; etiketlerin bir kısmı çevrilmiş."""
    rng = np.random.default_rng(tohum)
    X = np.column_stack([rng.uniform(4.5, 7.0, n), rng.uniform(2.5, 7.5, n)])
    y = (-4.9 + 1.7 * X[:, 0] - X[:, 1] > 0).astype(int)
    cevir = rng.random(n) < gurultu
    y[cevir] = 1 - y[cevir]
    return X, y


def normallestir(X):
    return (X - X.mean(axis=0)) / X.std(axis=0)


# --- k-d ağacı -------------------------------------------------------------------------
def kd_kur(noktalar: np.ndarray, indeksler=None, derinlik: int = 0):
    if indeksler is None:
        indeksler = np.arange(len(noktalar))
    if len(indeksler) <= 2:
        return ("yaprak", indeksler)
    boyut = derinlik % noktalar.shape[1]
    sirali = indeksler[np.argsort(noktalar[indeksler, boyut], kind="stable")]
    orta = len(sirali) // 2
    esik = noktalar[sirali[orta], boyut]
    return ("düğüm", boyut, esik, kd_kur(noktalar, sirali[:orta], derinlik + 1),
            kd_kur(noktalar, sirali[orta:], derinlik + 1))


def kd_en_yakin(agac, noktalar, q, en=(math.inf, -1), sayac=None):
    """(uzaklık, indeks). Öbür dala yalnızca sorgunun bölme düzlemine uzaklığı en iyi uzaklıktan küçükse inilir."""
    if sayac is not None:
        sayac[0] += 1
    if agac[0] == "yaprak":
        for i in agac[1]:
            d = float(np.linalg.norm(noktalar[i] - q))
            if d < en[0]:
                en = (d, int(i))
        return en
    _, boyut, esik, sol, sag = agac
    yakin, uzak = (sol, sag) if q[boyut] < esik else (sag, sol)
    en = kd_en_yakin(yakin, noktalar, q, en, sayac)
    if abs(q[boyut] - esik) < en[0]:
        en = kd_en_yakin(uzak, noktalar, q, en, sayac)
    return en


# --- Parametrik olmayan regresyon --------------------------------------------------------
def knn_regresyon(x, y, xq, k: int = 3) -> float:
    return float(y[np.argsort(np.abs(x - xq), kind="stable")[:k]].mean())


def yerel_agirlikli(x, y, xq, genislik: float = 3.0) -> float:
    """Dörtlü (quadratic) çekirdekle ağırlıklı doğrusal regresyon."""
    u = np.abs(x - xq) / genislik
    w = np.where(u < 1, 1 - u ** 2, 0.0)
    A = np.column_stack([np.ones_like(x), x]) * np.sqrt(w)[:, None]
    b = y * np.sqrt(w)
    katsayi, *_ = np.linalg.lstsq(A, b, rcond=None)
    return float(katsayi[0] + katsayi[1] * xq)


# --- SVM ve çekirdek hilesi -----------------------------------------------------------------
def svm_egit(X, y, lam: float = 0.01, adim: int = 30_000, tohum: int = 0):
    """Menteşe kaybı + (λ/2)‖w‖²; y ∈ {−1, +1}. Pegasos: η_t = 1/(λ t)."""
    rng = np.random.default_rng(tohum)
    w, b = np.zeros(X.shape[1]), 0.0
    for t in range(1, adim + 1):
        j = rng.integers(len(X))
        eta = 1 / (lam * t)
        if y[j] * (X[j] @ w + b) < 1:
            w = (1 - eta * lam) * w + eta * y[j] * X[j]
            b += eta * y[j] * 0.1
        else:
            w = (1 - eta * lam) * w
    return w, b


def marj(X, y, w, b) -> float:
    """Ayırıcıdan en yakın örneğe uzaklığın iki katı (ayırıyorsa)."""
    uz = y * (X @ w + b) / np.linalg.norm(w)
    return float(2 * uz.min())


def F(X):
    X = np.atleast_2d(X)
    return np.column_stack([X[:, 0] ** 2, X[:, 1] ** 2, math.sqrt(2) * X[:, 0] * X[:, 1]])


def cember_verisi(n: int = 200, tohum: int = 4):
    rng = np.random.default_rng(tohum)
    X = rng.uniform(-1.5, 1.5, (n, 2))
    r = np.linalg.norm(X, axis=1)
    keep = np.abs(r - 1) > 0.1
    X = X[keep]
    return X, np.where(np.linalg.norm(X, axis=1) < 1, 1, -1)


def algilayici_ayirir_mi(X, y, en_cok_tur: int = 200) -> bool:
    """Algılayıcı birkaç yüz turda hatasız olursa doğrusal ayrılabilir kabul et."""
    X1 = np.column_stack([np.ones(len(X)), X])
    w = np.zeros(X1.shape[1])
    for _ in range(en_cok_tur):
        hata = 0
        for xj, yj in zip(X1, y):
            if yj * (xj @ w) <= 0:
                w += yj * xj
                hata += 1
        if hata == 0:
            return True
    return False


def main() -> None:
    print("=== k en yakın komşu (gürültülü veri, LOOCV doğruluğu) ===")
    X, y = gurultulu_veri()
    for k in (1, 3, 5, 9, 25):
        print(f"  k = {k:>2}: {birini_disarida_birak(X, y, k):.3f}")
    print("  k = 1 gürültüyü ezberler; orta k daha iyi genelleştirir; çok büyük k sınırı bulanıklaştırır.")
    Xm = X.copy()
    Xm[:, 1] *= 1000                                 # ikinci boyutun birimi değişti
    print(f"  Birim değişince (k = 5): {birini_disarida_birak(Xm, y, 5):.3f}; "
          f"normalleştirince: {birini_disarida_birak(normallestir(Xm), y, 5):.3f}")

    print("\n=== k-d ağacı ===")
    rng = np.random.default_rng(5)
    P = rng.random((2000, 3))
    agac = kd_kur(P)
    ayni, ziyaret = 0, []
    for _ in range(100):
        q = rng.random(3)
        sayac = [0]
        d, i = kd_en_yakin(agac, P, q, sayac=sayac)
        ayni += i == int(np.argmin(np.linalg.norm(P - q, axis=1)))
        ziyaret.append(sayac[0])
    print(f"  2000 nokta, 3 boyut: 100 sorgunun {ayni}'ünde kaba kuvvetle aynı komşu; "
          f"ortalama {np.mean(ziyaret):.0f} düğüm ziyareti")

    print("\n=== Parametrik olmayan regresyon ===")
    xr = np.arange(0, 15, 1.0)
    yr = np.array([1.0, 2.2, 2.9, 4.2, 3.6, 5.1, 6.0, 7.4, 6.9, 7.8, 9.1, 8.7, 10.2, 11.5, 11.0])
    for xq in (0.0, 6.5, 14.0):
        print(f"  x = {xq:>4}: 3-NN ortalaması {knn_regresyon(xr, yr, xq):.2f}, yerel ağırlıklı {yerel_agirlikli(xr, yr, xq):.2f}")
    print("  Uçlarda k-NN ortalaması içeri çekilir; yerel doğrusal regresyon eğilimi korur.")

    print("\n=== Destek vektör makinesi: en büyük marj ===")
    rng = np.random.default_rng(6)
    A = rng.normal([1, 1], 0.4, (40, 2))
    B = rng.normal([3, 3], 0.4, (40, 2))
    Xs = np.vstack([A, B])
    ys = np.array([-1] * 40 + [1] * 40)
    w, b = svm_egit(Xs, ys)
    X1 = np.column_stack([np.ones(len(Xs)), Xs])
    wp = np.zeros(3)
    for _ in range(100):
        for xj, yj in zip(X1, ys):
            if yj * (xj @ wp) <= 0:
                wp += yj * xj
    print(f"  SVM marjı {marj(Xs, ys, w, b):.3f};  algılayıcının bulduğu ayırıcının marjı {marj(Xs, ys, wp[1:], wp[0]):.3f}")
    destek = np.sum(ys * (Xs @ w + b) < 1.05)
    print(f"  Marjın üzerindeki ya da içindeki örnek (destek vektörü adayı): {destek} / {len(Xs)}")

    print("\n=== Çekirdek hilesi ===")
    x, z = np.array([0.8, -1.2]), np.array([1.5, 0.4])
    print(f"  F(x)·F(z) = {float(F(x)[0] @ F(z)[0]):.6f},  (x·z)² = {float(x @ z) ** 2:.6f}")
    Xc, yc = cember_verisi()
    print(f"  Çember verisi girdi uzayında doğrusal ayrılabilir mi? {algilayici_ayirir_mi(Xc, yc)};"
          f"  F uzayında? {algilayici_ayirir_mi(F(Xc), yc)}")


if __name__ == "__main__":
    main()
