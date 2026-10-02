#!/usr/bin/env python3
"""Model seçimi, kayıp fonksiyonları ve öğrenme kuramı (kitaptaki 19.4–19.5, 19.7.1).

* Polinom derecesi seçimi: eğitim hatası dereceyle hep azalır; doğrulama hatası U biçimlidir.
  k katlı çapraz doğrulama (kitaptaki MODEL-SELECTION / CROSS-VALIDATION).
* Kayıp fonksiyonları: L1, L2, L0/1; spam örneği: L(spam, spam değil) = 1, L(spam değil, spam) = 10.
* PAC öğrenme: N ≥ (1/ε)(ln(1/δ) + ln |H|)  (19.1). Bütün Boolean fonksiyonlarında |H| = 2^(2^n).
* k-DL: |Conj(n, k)| = Σ_{i≤k} C(2n, i).
* Boyutların laneti (kitap): k = 10, N = 10⁶ için komşuluğun kenarı ℓ = (k/N)^(1/n):
  n = 2 → 0.003, n = 3 → 0.02, n = 17 → ~0.5, n = 200 → 0.94. Dış %1'lik kabuktaki noktalar:
  1 boyutta %2, 200 boyutta %98'den fazla.

Çalıştırma:
    python model_secimi.py
"""
from __future__ import annotations

import math

import numpy as np


def polinom_veri(n: int = 30, tohum: int = 0):
    rng = np.random.default_rng(tohum)
    x = np.sort(rng.uniform(-1, 1, n))
    y = np.sin(2.5 * x) + 0.3 * x ** 2 + rng.normal(0, 0.2, n)
    return x, y


def polinom_ogren(x, y, derece: int):
    return np.polyfit(x, y, derece)


def hata(w, x, y) -> float:
    return float(np.mean((np.polyval(w, x) - y) ** 2))


def capraz_dogrulama(x, y, derece: int, k: int = 5) -> float:
    """CROSS-VALIDATION: veriyi k parçaya böl; her turda bir parça doğrulama, gerisi eğitim."""
    N = len(x)
    sira = np.arange(N)
    hatalar = []
    for i in range(k):
        dog = sira[i * N // k:(i + 1) * N // k]
        egit = np.setdiff1d(sira, dog)
        w = polinom_ogren(x[egit], y[egit], derece)
        hatalar.append(hata(w, x[dog], y[dog]))
    return float(np.mean(hatalar))


def model_secimi(x, y, dereceler=range(0, 13), k: int = 5, tohum: int = 1):
    """MODEL-SELECTION: veriyi karıştır, her derece için çapraz doğrulama hatasını hesapla, en iyisini seç."""
    rng = np.random.default_rng(tohum)
    p = rng.permutation(len(x))
    x, y = x[p], y[p]
    tablo = {d: (hata(polinom_ogren(x, y, d), x, y), capraz_dogrulama(x, y, d, k)) for d in dereceler}
    en_iyi = min(tablo, key=lambda d: tablo[d][1])
    return en_iyi, tablo


# --- Kayıp fonksiyonları ---------------------------------------------------------------
def L1(y, yh):
    return abs(y - yh)


def L2(y, yh):
    return (y - yh) ** 2


def L01(y, yh):
    return 0 if y == yh else 1


SPAM_KAYBI = {("spam", "spam değil"): 1, ("spam değil", "spam"): 10}   # (gerçek, tahmin)


def beklenen_kayip(tahminler, gercekler, kayip=SPAM_KAYBI) -> float:
    return sum(kayip.get((g, t), 0) for g, t in zip(gercekler, tahminler)) / len(gercekler)


# --- PAC öğrenme --------------------------------------------------------------------------
def pac_ornek_sayisi(eps: float, delta: float, ln_H: float) -> int:
    return math.ceil((math.log(1 / delta) + ln_H) / eps)


def baglac_sayisi(n: int, k: int) -> int:
    """En çok k literalli bağlaçların sayısı (n Boolean nitelik, 2n literal)."""
    return sum(math.comb(2 * n, i) for i in range(k + 1))


def kdl_ln_H(n: int, k: int) -> float:
    """ln |k-DL(n)| ≤ ln(3^c · c!), c = |Conj(n, k)|."""
    c = baglac_sayisi(n, k)
    return c * math.log(3) + math.lgamma(c + 1)


# --- Boyutların laneti -----------------------------------------------------------------------
def komsuluk_kenari(n: int, k: int = 10, N: int = 1_000_000) -> float:
    return (k / N) ** (1 / n)


def dis_kabuk_orani(n: int, kalinlik: float = 0.01) -> float:
    """Birim küpte her kenardan 'kalinlik' kadar içerideki kabukta kalan hacim oranı."""
    return 1 - (1 - 2 * kalinlik) ** n


def main() -> None:
    print("=== Polinom derecesi seçimi (30 örnek, 5 katlı çapraz doğrulama) ===")
    x, y = polinom_veri()
    en_iyi, tablo = model_secimi(x, y)
    print("  derece   eğitim hatası   doğrulama hatası")
    for d, (e, v) in tablo.items():
        print(f"  {d:>6}   {e:13.4f}   {v:16.4f}{'   ← seçilir' if d == en_iyi else ''}")
    print("  Eğitim hatası dereceyle azalır; doğrulama hatası U biçiminde: az ve aşırı uydurma.")

    print("\n=== Kayıp fonksiyonları ===")
    print(f"  y = 137.036, ŷ = 137.035999: L1 = {L1(137.036, 137.035999):.6f}, L2 = {L2(137.036, 137.035999):.2e}")
    g = ["spam"] * 90 + ["spam değil"] * 10
    a = ["spam değil"] * 1 + ["spam"] * 89 + ["spam değil"] * 10        # 1 spam kaçırıldı
    b = ["spam"] * 90 + ["spam"] * 1 + ["spam değil"] * 9               # 1 önemli posta spam sanıldı
    print(f"  İki sınıflandırıcı birer hata yapıyor. Spam'ı kaçıran: ortalama kayıp {beklenen_kayip(a, g):.2f};"
          f" önemli postayı spam sanan: {beklenen_kayip(b, g):.2f}")

    print("\n=== PAC öğrenme: N ≥ (1/ε)(ln(1/δ) + ln|H|), ε = 0.1, δ = 0.05 ===")
    for n in (5, 10, 20):
        tum = pac_ornek_sayisi(0.1, 0.05, (2 ** n) * math.log(2))
        kdl = pac_ornek_sayisi(0.1, 0.05, kdl_ln_H(n, 2))
        print(f"  n = {n:>2}: bütün Boolean fonksiyonları {tum:>10,} örnek (olası girdi {2 ** n:,});"
              f"  2-DL {kdl:>8,} örnek")
    print("  Bütün fonksiyonlar için gereken örnek 2^n gibi büyür (olası girdi sayısını aşar); k-DL için n'de polinomdur.")
    print("  (Küçük n'de 2-DL sınırı daha büyük çıkıyor: |k-DL| ≤ 3^c c! üst sınırı gevşektir.)")

    print("\n=== Boyutların laneti (k = 10, N = 1 000 000) ===")
    for n in (1, 2, 3, 10, 17, 100, 200):
        print(f"  n = {n:>3}: komşuluk kenarı ℓ = {komsuluk_kenari(n):.3f}, dış %1 kabuktaki noktalar %{100 * dis_kabuk_orani(n):.1f}")


if __name__ == "__main__":
    main()
