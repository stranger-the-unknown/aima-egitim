#!/usr/bin/env python3
"""Gözetim, güvenlik ve mahremiyet (kitaptaki 27.3.2).

* Kimliksizleştirme ve yeniden tanımlama: Ad ve numara silinse de doğum tarihi + cinsiyet + posta kodu
  çoğu kişiyi tek başına tanımlar (Sweeney 2000: ABD nüfusunun %87'si). Burada yapay bir nüfusla benzetiyoruz.
* k-anonimlik: Her kayıt, yarı-tanımlayıcılar bakımından en az k − 1 başka kayıttan ayırt edilemez.
  Alanları genelleştirerek (doğum tarihi → yıl → on yıl) k büyütülür.
* Fark saldırısı: "30–40 yaş" ve "30–41 yaş" ortalamaları tek bir kişinin maaşını ele verir (kitaptaki örnek).
* ε-diferansiyel mahremiyet: |log P(Q(D) = y) − log P(Q(D + r) = y)| ≤ ε. Sayım sorgusuna Laplace(1/ε) gürültüsü
  eklemek bunu sağlar (Laplace mekanizması; standart yöntem, kitap mekanizmayı adlandırmaz).
* Federe öğrenme ve güvenli toplama: Kullanıcılar parametrelerine toplamı sıfır olan maskeler ekler; sunucu
  yalnızca toplamı (ortalamayı) doğru öğrenir.

Çalıştırma:
    python mahremiyet.py
"""
from __future__ import annotations

from collections import Counter

import numpy as np


# --- Yeniden tanımlama ve k-anonimlik -------------------------------------------------------------
def yapay_nufus(n: int = 10_000, posta_kodu: int = 1, yil: int = 80, tohum: int = 0) -> np.ndarray:
    """Sütunlar: doğum günü (0 … 365·yil − 1), cinsiyet (0/1), posta kodu. Düzgün dağılım (varsayım)."""
    rng = np.random.default_rng(tohum)
    return np.stack([rng.integers(0, 365 * yil, n), rng.integers(0, 2, n), rng.integers(0, posta_kodu, n)], axis=1)


def tekil_oran(tablo: np.ndarray) -> float:
    """Yarı-tanımlayıcılarıyla tek başına olan kayıtların oranı."""
    sayim = Counter(map(tuple, tablo))
    return float(np.mean([sayim[tuple(r)] == 1 for r in tablo]))


def k_degeri(tablo: np.ndarray) -> int:
    """Tablonun k-anonimlik düzeyi: en küçük eşdeğerlik sınıfının boyu."""
    return min(Counter(map(tuple, tablo)).values())


def genellestir(tablo: np.ndarray, gun_kovasi: int) -> np.ndarray:
    """Doğum gününü gun_kovasi günlük aralıklara indir (365 → yıl, 3650 → on yıl)."""
    T = tablo.copy()
    T[:, 0] //= gun_kovasi
    return T


# --- Fark saldırısı --------------------------------------------------------------------------------
def fark_saldirisi(ort1: float, n1: int, ort2: float, n2: int) -> float:
    """İki toplu yanıttan, ikinci kümede fazladan bulunan tek kişinin değeri."""
    return ort2 * n2 - ort1 * n1


# --- Diferansiyel mahremiyet ----------------------------------------------------------------------
def laplace_sayim(gercek: int, eps: float, rng) -> float:
    """Duyarlılığı 1 olan sayım sorgusu için Laplace mekanizması."""
    return gercek + rng.laplace(0.0, 1.0 / eps)


def log_yogunluk_farki(eps: float, ys=np.linspace(-20, 20, 2001)) -> float:
    """D'de sayım c, D + r'de c + 1. En büyük |log p(y | c) − log p(y | c + 1)|."""
    logp = lambda y, c: np.log(eps / 2) - eps * np.abs(y - c)  # noqa: E731
    return float(np.max(np.abs(logp(ys, 0) - logp(ys, 1))))


def sayim_fark_saldirisi(eps: float, deneme: int = 20_000, tohum: int = 0) -> float:
    """Saldırgan, 41 yaşındaki kişinin hasta olup olmadığını iki gürültülü sayımın farkından tahmin eder.
    Kişi yarı yarıya hasta (önsel 0.5). Doğru tahmin oranı (0.5 = hiçbir şey öğrenemedi)."""
    rng = np.random.default_rng(tohum)
    hasta = rng.integers(0, 2, deneme)
    taban = 12
    s1 = taban + rng.laplace(0, 1 / eps, deneme)
    s2 = taban + hasta + rng.laplace(0, 1 / eps, deneme)
    return float(np.mean((s2 - s1 > 0.5) == (hasta == 1)))


# --- Güvenli toplama ---------------------------------------------------------------------------------
def guvenli_toplama(degerler: np.ndarray, tohum: int = 0) -> tuple[np.ndarray, np.ndarray]:
    """Her (i, j) çifti ortak rastgele bir m_ij seçer; i +m_ij, j −m_ij ekler. Maskeler toplamı sıfır.
    (sunucunun gördüğü maskeli değerler, toplam)."""
    rng = np.random.default_rng(tohum)
    n = len(degerler)
    maskeli = degerler.astype(float).copy()
    for i in range(n):
        for j in range(i + 1, n):
            m = rng.normal(0, 1000, degerler.shape[1:])
            maskeli[i] += m
            maskeli[j] -= m
    return maskeli, maskeli.sum(axis=0)


def federe_sgd(kullanicilar: list[tuple[np.ndarray, np.ndarray]], tur: int = 200, adim: float = 0.1) -> np.ndarray:
    """Her turda her kullanıcı kendi verisinde gradyan hesaplar; sunucu örnek sayısıyla ağırlıklı ortalamayı alır.
    Ham veri hiç paylaşılmaz. Doğrusal regresyon y ≈ X w."""
    d = kullanicilar[0][0].shape[1]
    w = np.zeros(d)
    N = sum(len(y) for _, y in kullanicilar)
    for _ in range(tur):
        g = sum(X.T @ (X @ w - y) for X, y in kullanicilar) / N
        w -= adim * g
    return w


def main() -> None:
    print("=== Yeniden tanımlama: doğum tarihi + cinsiyet + posta kodu (yapay nüfus) ===")
    T = yapay_nufus()
    print(f"  Bir posta kodunda 10 000 kişi, 80 yıllık doğum tarihi aralığı: tek başına olanlar %{100 * tekil_oran(T):.0f}")
    for ad, kova in (("doğum yılı", 365), ("on yıl", 3650)):
        G = genellestir(T, kova)
        print(f"  Doğum tarihi → {ad:<10}: tek başına %{100 * tekil_oran(G):5.1f}, k = {k_degeri(G)}")

    print("\n=== Fark saldırısı (kitaptaki örnek) ===")
    m = fark_saldirisi(81_234, 12, 81_199, 13)
    print(f"  30–40 yaş: ort. $81 234 (12 kişi); 30–41 yaş: ort. $81 199 (13 kişi) → 41 yaşındakinin maaşı ${m:,.0f}".replace(",", " "))

    print("\n=== ε-diferansiyel mahremiyet: Laplace mekanizması ===")
    for eps in (0.1, 1.0, 5.0):
        print(f"  ε = {eps:>3}: en büyük |log p(y|D) − log p(y|D + r)| = {log_yogunluk_farki(eps):.3f}; "
              f"gürültü std {np.sqrt(2) / eps:5.2f}; fark saldırısının başarısı %{100 * sayim_fark_saldirisi(eps):.0f}")
    print("  Gürültüsüz sayımlarda saldırı %100 başarılı olurdu.")

    print("\n=== Güvenli toplama ve federe öğrenme ===")
    rng = np.random.default_rng(1)
    parametre = rng.normal(0, 1, (5, 3))
    maskeli, toplam = guvenli_toplama(parametre)
    print(f"  1. kullanıcının gerçek parametreleri {np.round(parametre[0], 2)}, sunucunun gördüğü {np.round(maskeli[0], 0)}")
    print(f"  Toplam doğru mu? {np.allclose(toplam, parametre.sum(axis=0))}")
    w_gercek = np.array([2.0, -1.0, 0.5])
    kullanicilar = []
    for k in range(5):
        X = rng.normal(0, 1, (20 + 10 * k, 3))
        kullanicilar.append((X, X @ w_gercek + rng.normal(0, 0.1, len(X))))
    w = federe_sgd(kullanicilar)
    Xh = np.concatenate([X for X, _ in kullanicilar])
    yh = np.concatenate([y for _, y in kullanicilar])
    w_merkez = np.linalg.lstsq(Xh, yh, rcond=None)[0]
    print(f"  Federe SGD: {np.round(w, 3)};  bütün veri bir yerde olsaydı: {np.round(w_merkez, 3)}")


if __name__ == "__main__":
    main()
