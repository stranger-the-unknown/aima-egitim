#!/usr/bin/env python3
"""Topluluk öğrenmesi ve çevrimiçi öğrenme (kitaptaki 19.8).

Kitaptaki değerler (testlerle doğrulanır):
  * Bağımsız 5 sınıflandırıcı, her biri %75 doğru: çoğunluk oyu %89 doğru; 17 sınıflandırıcıyla %99.
  * AdaBoost karar kütükleriyle (K = 5) restoran verisinde tek kütükten çok daha iyi; K arttıkça eğitim
    hatası sıfıra iner, test doğruluğu bundan sonra da bir süre artabilir.
  * Rastgele ağırlıklı çoğunluk: M < (M* ln(1/β) + ln K) / (1 − β). K = 10 uzman için
    β = 1/2 → 1.39 M* + 4.6;  β = 3/4 → 1.15 M* + 9.2.

Çalıştırma:
    python topluluk.py
"""
from __future__ import annotations

import math
import random

import numpy as np

import karar_agaci as ka


def cogunluk_dogrulugu(K: int, p: float) -> float:
    """K bağımsız sınıflandırıcıdan en az ⌈(K+1)/2⌉'sinin doğru olma olasılığı (K tek)."""
    return sum(math.comb(K, i) * p ** i * (1 - p) ** (K - i) for i in range((K + 1) // 2, K + 1))


# --- Karar kütükleri ve AdaBoost -----------------------------------------------------------
def kutuk_ogren(ornekler, agirlik):
    """Tek testli ağaç: her (nitelik, değer) için 'değer ise s, değilse ¬s' kuralları arasında ağırlıklı
    hatası en küçük olanı seç. (nitelik, değer, eşitse verilecek sınıf)."""
    en = None
    for a, degerler in ka.NITELIKLER.items():
        for v in degerler:
            for s in (True, False):
                h = sum(w for (x, y), w in zip(ornekler, agirlik) if ((x[a] == v) == s) != y)
                if en is None or h < en[0]:
                    en = (h, (a, v, s))
    return en[1]


def kutuk(h, x) -> bool:
    a, v, s = h
    return (x[a] == v) == s


def adaboost(ornekler, K: int):
    """Kitaptaki ADABOOST (Şekil 19.25): hatalı örneklerin ağırlığı error/(1 − error) ile çarpılmayan
    (doğru olanlar çarpılan) ve normalleştirilen sürüm; hipotez ağırlığı ½ log((1 − error)/error)."""
    N = len(ornekler)
    w = np.full(N, 1 / N)
    hipotezler, z = [], []
    for _ in range(K):
        h = kutuk_ogren(ornekler, w)
        dogru = np.array([kutuk(h, x) == y for x, y in ornekler])
        hata = float(w[~dogru].sum())
        if hata > 0.5:
            break
        hata = min(max(hata, 1e-10), 1 - 1e-10)
        w[dogru] *= hata / (1 - hata)
        w /= w.sum()
        hipotezler.append(h)
        z.append(0.5 * math.log((1 - hata) / hata))
    return hipotezler, z


def agirlikli_cogunluk(hipotezler, z, x) -> bool:
    return sum(zi * (1 if kutuk(h, x) else -1) for h, zi in zip(hipotezler, z)) >= 0


def ogrenme_karsilastirmasi(N: int = 100, deneme: int = 10, Klar=(1, 5, 20, 50), tohum: int = 0) -> dict:
    """Gerçek ağaçtan üretilen N eğitim + 500 test örneğiyle tek kütük ve AdaBoost doğrulukları."""
    rng = random.Random(tohum)
    sonuc = {K: {"eğitim": 0.0, "test": 0.0} for K in Klar}
    for _ in range(deneme):
        egitim = [ka.rastgele_ornek(rng) for _ in range(N)]
        test = [ka.rastgele_ornek(rng) for _ in range(500)]
        for K in Klar:
            H, z = adaboost(egitim, K)
            sonuc[K]["eğitim"] += np.mean([agirlikli_cogunluk(H, z, x) == y for x, y in egitim]) / deneme
            sonuc[K]["test"] += np.mean([agirlikli_cogunluk(H, z, x) == y for x, y in test]) / deneme
    return sonuc


# --- Torbalama ------------------------------------------------------------------------------
def torbalama(ornekler, K: int, rng: random.Random):
    """K bootstrap örneklemiyle K karar ağacı."""
    return [ka.agac_ogren([rng.choice(ornekler) for _ in ornekler], ka.SIRA) for _ in range(K)]


def torba_tahmin(agaclar, x) -> bool:
    return sum(ka.siniflandir(a, x) for a in agaclar) * 2 >= len(agaclar)


def torbalama_karsilastirmasi(N: int, gurultu: float, deneme: int = 10, K: int = 25) -> tuple[float, float]:
    tek = tor = 0.0
    for d in range(deneme):
        rng = random.Random(d)
        egitim = [ka.rastgele_ornek(rng) for _ in range(N)]
        egitim = [(x, (not y) if rng.random() < gurultu else y) for x, y in egitim]
        test = [ka.rastgele_ornek(rng) for _ in range(400)]
        agac, torba = ka.agac_ogren(egitim, ka.SIRA), torbalama(egitim, K, rng)
        tek += np.mean([ka.siniflandir(agac, x) == y for x, y in test]) / deneme
        tor += np.mean([torba_tahmin(torba, x) == y for x, y in test]) / deneme
    return float(tek), float(tor)


# --- Rastgele ağırlıklı çoğunluk ---------------------------------------------------------------
def rwm_siniri(M_yildiz: float, K: int, beta: float) -> tuple[float, float]:
    """(M*'ın katsayısı, sabit terim)."""
    return math.log(1 / beta) / (1 - beta), math.log(K) / (1 - beta)


def rwm_benzetim(K: int = 10, T: int = 1000, beta: float = 0.5, tohum: int = 0) -> dict:
    """Uzmanların doğruluğu 0.55–0.9; en iyi uzman zamanla değişir (ilk yarıda 0, sonra 9 en iyi)."""
    rng = random.Random(tohum)
    w = [1.0] * K
    hatalar, uzman_hata = 0.0, [0] * K
    for t in range(T):
        dogruluk = [0.6] * K
        dogruluk[0 if t < T // 2 else 9] = 0.9
        y = rng.random() < 0.5
        tahmin = [y if rng.random() < dogruluk[k] else not y for k in range(K)]
        toplam = sum(w)
        hatalar += sum(w[k] for k in range(K) if tahmin[k] != y) / toplam    # beklenen hata
        for k in range(K):
            if tahmin[k] != y:
                uzman_hata[k] += 1
                w[k] *= beta
        s = sum(w)
        w = [x / s for x in w]
    M_yildiz = min(uzman_hata)
    a, b = rwm_siniri(M_yildiz, K, beta)
    return {"M": hatalar, "M*": M_yildiz, "sınır": a * M_yildiz + b}


def main() -> None:
    print("=== Bağımsız sınıflandırıcıların çoğunluk oyu (her biri %75 doğru) ===")
    for K in (1, 5, 11, 17, 21):
        print(f"  K = {K:>2}: %{100 * cogunluk_dogrulugu(K, 0.75):.1f}")
    print("  (Gerçekte sınıflandırıcılar aynı veriyi paylaşır, bağımsız değildir; kazanç daha küçüktür.)")

    print("\n=== AdaBoost, karar kütükleri, restoran verisi (100 eğitim örneği, 10 deneme) ===")
    for K, d in ogrenme_karsilastirmasi().items():
        print(f"  K = {K:>2}: eğitim {d['eğitim']:.3f}, test {d['test']:.3f}")
    H, z = adaboost(ka.RESTORAN, 5)
    print(f"  12 örnekte K = 5 kütük: {[(a, v, s) for a, v, s in H]}")

    print("\n=== Torbalama (bootstrap ile 25 ağaç, 60 eğitim örneği, 10 deneme) ===")
    for gurultu in (0.0, 0.15):
        tek, tor = torbalama_karsilastirmasi(60, gurultu)
        print(f"  etiket gürültüsü %{100 * gurultu:.0f}: tek ağaç {tek:.3f}, torba {tor:.3f}")
    print("  Torbalama varyansı azaltır: Gürültü ağaçları kararsızlaştırınca fark büyür.")

    print("\n=== Rastgele ağırlıklı çoğunluk (K = 10 uzman) ===")
    for beta in (0.5, 0.75):
        a, b = rwm_siniri(0, 10, beta)
        print(f"  β = {beta}: M < {a:.2f} M* + {b:.1f}")
    for beta in (0.5, 0.75):
        s = rwm_benzetim(beta=beta)
        print(f"  benzetim β = {beta}: beklenen hata {s['M']:.1f}, en iyi uzman {s['M*']}, sınır {s['sınır']:.1f}")


if __name__ == "__main__":
    main()
