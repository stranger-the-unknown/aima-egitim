#!/usr/bin/env python3
"""Haydut (bandit) problemleri (kitaptaki 17.3).

1. Deterministik iki kollu haydut, γ = 0.5 (kitap):
     M  = 0, 2, 0, 7.2, 0, 0, ...     U(M)  = 1.9
     M1 = 1, 1, 1, ...                U(M1) = 2.0
     S  = M'yi 4 kez çek, sonra M1    U(S)  = 2.025  (en iyisi)
   Gittins indeksi λ = max_T E[Σ_{t<T} γ^t R_t] / E[Σ_{t<T} γ^t] = 1.0133 (T = 4).
   Yeniden başlatma MDP'si M^s: değer 2.0266, λ = 2.0266 (1 − γ) = 1.0133.
2. Bernoulli haydudu: durum (başarı, başarısızlık) sayıları (1, 1)'den başlar; sonraki çekiş
   s/(s+f) olasılıkla 1 verir. γ = 0.9, s + f ≤ 100'de kesilmiş MDP (kitap):
     Gittins(3, 2) = 0.7057 > Gittins(7, 4) = 0.6922, oysa tahminler 0.6 < 0.6364 → keşif bonusu.
3. Yaklaşık politikalar: UCB ve Thompson örneklemesi; pişmanlık O(log N) büyür.

Çalıştırma:
    python haydut.py
"""
from __future__ import annotations

import math

import numpy as np

M_DIZI = [0, 2, 0, 7.2]          # sonrası hep 0


def indirimli_toplam(odul: list[float], gama: float) -> float:
    return sum(gama ** t * r for t, r in enumerate(odul))


def deterministik_gittins(odul: list[float], gama: float, uzunluk: int = 50) -> tuple[float, list]:
    """Deterministik ödül dizisi için Gittins indeksi ve her T için (pay, payda, oran)."""
    dizi = list(odul) + [0.0] * (uzunluk - len(odul))
    tablo, pay, payda = [], 0.0, 0.0
    for T in range(1, uzunluk + 1):
        pay += gama ** (T - 1) * dizi[T - 1]
        payda += gama ** (T - 1)
        tablo.append((T, pay, payda, pay / payda))
    return max(t[3] for t in tablo), tablo


def yeniden_baslatma_degeri(odul: list[float], gama: float, eps: float = 1e-12) -> float:
    """Yeniden başlatma MDP'si M^s: her durumda 'devam et' ya da 'başa dön ve oradan devam et'.
    Durum t = 0..len(odul); t = len(odul) sonsuza dek 0 veren emici durum."""
    n = len(odul)
    V = np.zeros(n + 1)
    while True:
        devam = np.array([odul[t] + gama * V[t + 1] for t in range(n)] + [gama * V[n]])
        V2 = np.maximum(devam, devam[0])          # başa dönmek, başlangıçta devam etmekle aynıdır
        if np.max(np.abs(V2 - V)) < eps:
            return float(V2[0])
        V = V2


def bernoulli_gittins(s: int, f: int, gama: float = 0.9, ufuk: int = 100, tol: float = 1e-7) -> float:
    """Kalibrasyonla: λ'yı ikili aramayla, (s, f) durumunda 'çek' ile 'λ'yı sonsuza dek al'
    eşit olacak biçimde bul. s + f = ufuk'ta öğrenme durur: değer max(p, λ)/(1 − γ)."""
    def cekmeye_deger_mi(lam: float) -> bool:
        dur = lam / (1 - gama)
        # V[k] : toplam n = s' + f' sayısı sabitken, s' = k olan durumların değeri
        n = ufuk
        k = np.arange(1, n)                              # s' = 1..n−1, f' = n − s'
        V = np.maximum(k / n, lam) / (1 - gama)
        V = np.concatenate(([0.0], V, [0.0]))           # kenarlar kullanılmaz
        for n in range(ufuk - 1, s + f - 1, -1):
            k = np.arange(1, n)
            p = k / n
            cek = p * (1 + gama * V[k + 1]) + (1 - p) * gama * V[k]
            Vn = np.maximum(cek, dur)
            V = np.concatenate(([0.0], Vn, [0.0]))
            if n == s + f:
                return cek[s - 1] >= dur
        raise ValueError("s + f ufuktan küçük olmalı")

    alt, ust = 0.0, 1.0
    while ust - alt > tol:
        orta = (alt + ust) / 2
        alt, ust = (orta, ust) if cekmeye_deger_mi(orta) else (alt, orta)
    return (alt + ust) / 2


# --- Yaklaşık politikalar ---------------------------------------------------------
def haydut_oyna(mu: list[float], politika: str, N: int, rng: np.random.Generator) -> float:
    """Bernoulli kolları; N çekiş sonunda pişmanlık = N μ* − toplam beklenen ödül."""
    k = len(mu)
    basari, sayi = np.zeros(k), np.zeros(k)
    pismanlik = 0.0
    for n in range(N):
        if politika == "açgözlü":
            kol = int(np.argmax((basari + 1) / (sayi + 2)))
        elif politika == "UCB":
            if n < k:
                kol = n
            else:
                g = math.sqrt(2 * math.log(1 + n * math.log(n) ** 2))   # kitaptaki g(N)
                kol = int(np.argmax(basari / sayi + g / np.sqrt(sayi)))
        elif politika == "Thompson":
            kol = int(np.argmax(rng.beta(basari + 1, sayi - basari + 1)))
        else:
            raise ValueError(politika)
        odul = rng.random() < mu[kol]
        basari[kol] += odul
        sayi[kol] += 1
        pismanlik += max(mu) - mu[kol]
    return pismanlik


def main() -> None:
    g = 0.5
    print("=== Deterministik haydut, γ = 0.5 (kitap) ===")
    print(f"  U(M)  = {indirimli_toplam(M_DIZI, g):.3f}")
    print(f"  U(M1) = {sum(g ** t for t in range(200)):.3f}")
    print(f"  U(S)  = {indirimli_toplam(M_DIZI, g) + sum(g ** t for t in range(4, 200)):.3f}   (4 çekişten sonra M1'e geç)")
    lam, tablo = deterministik_gittins(M_DIZI, g)
    print("   T   Σγ^t R_t   Σγ^t     oran")
    for T, pay, payda, oran in tablo[:6]:
        print(f"  {T:>2}   {pay:7.4f}   {payda:7.4f}   {oran:7.4f}")
    print(f"  Gittins indeksi = {lam:.4f}")
    v = yeniden_baslatma_degeri(M_DIZI, g)
    print(f"  Yeniden başlatma MDP'si: değer {v:.4f}, λ = değer × (1 − γ) = {v * (1 - g):.4f}")

    print("\n=== Bernoulli haydudu: Gittins indeksleri, γ = 0.9 (kitap: s + f ≤ 100) ===")
    for s, f in ((1, 1), (2, 1), (1, 2), (3, 2), (7, 4), (10, 10)):
        print(f"  (s, f) = ({s}, {f}): tahmin {s / (s + f):.4f}, Gittins {bernoulli_gittins(s, f):.4f}")
    print("  (3, 2)'nin indeksi (7, 4)'ünkinden büyük: az denenmiş kola keşif bonusu.")

    print("\n=== Yaklaşık politikalar: ortalama pişmanlık (μ = 0.3, 0.5, 0.6; 20 deneme) ===")
    mu = [0.3, 0.5, 0.6]
    for N in (100, 1000, 3000):
        satir = []
        for pol in ("açgözlü", "UCB", "Thompson"):
            rng = np.random.default_rng(17)
            satir.append(f"{pol} {np.mean([haydut_oyna(mu, pol, N, rng) for _ in range(20)]):6.1f}")
        print(f"  N = {N:>4}: " + ",  ".join(satir))
    print("  UCB ve Thompson'ın pişmanlığı log N gibi büyür; açgözlü bazen kötü kola takılır.")


if __name__ == "__main__":
    main()
