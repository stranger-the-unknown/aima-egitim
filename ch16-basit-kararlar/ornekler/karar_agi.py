#!/usr/bin/env python3
"""Çok nitelikli fayda ve karar ağları: havalimanı yeri seçimi (kitaptaki 16.4–16.5).

1. Baskınlık
   * Katı baskınlık: Bir seçenek bütün niteliklerde daha iyiyse diğeri elenir.
   * Stokastik baskınlık (kitaptaki sayılar): S1'in maliyeti U[2.8, 4.8] milyar $, S2'nin
     U[3.0, 5.2] milyar $. Tutumluluk = −maliyet. S1'in birikimli dağılımı hep S2'ninkinin
     "iyi" tarafında olduğu için S1, S2'yi stokastik olarak baskılar — fayda fonksiyonunu
     bilmeden karar verilebilir.
2. Karar ağı (sayılar bizim varsayımımız; yapı kitaptaki gibi):
   Karar: Yer ∈ {S1, S2, S3}. Şans düğümleri: HavaTrafiği, Dava, İnşaat.
   Sonuç nitelikleri: Güvenlik (beklenen ölüm), Sessizlik (etkilenen kişi), Tutumluluk (maliyet).
   Karşılıklı tercih bağımsızlığı varsayımıyla toplamsal değer: U = −(w_ö ölüm + w_g gürültü + w_m maliyet).
   Değerlendirme: Her karar değeri için EU = Σ P(şans | karar) U(sonuçlar); en büyüğünü seç.

Çalıştırma:
    python karar_agi.py
"""
from __future__ import annotations

import itertools

import numpy as np


# --- Stokastik baskınlık --------------------------------------------------------
def birikimli_tekduze(a: float, b: float, x):
    return np.clip((np.asarray(x) - a) / (b - a), 0.0, 1.0)


def stokastik_baskin_mi(maliyet1: tuple, maliyet2: tuple, n: int = 2001) -> bool:
    """Maliyette küçük iyi: A1, A2'yi baskılar ⇔ her c için P(maliyet1 ≤ c) ≥ P(maliyet2 ≤ c)."""
    x = np.linspace(min(maliyet1[0], maliyet2[0]), max(maliyet1[1], maliyet2[1]), n)
    return bool(np.all(birikimli_tekduze(*maliyet1, x) >= birikimli_tekduze(*maliyet2, x) - 1e-12))


def katı_baskin_mi(a: dict, b: dict) -> bool:
    """Nitelikler 'büyük iyi' olacak biçimde verilmeli."""
    return all(a[k] >= b[k] for k in a) and any(a[k] > b[k] for k in a)


# --- Karar ağı --------------------------------------------------------------------
YERLER = ["S1", "S2", "S3"]
P_TRAFIK_YOGUN = 0.4
P_DAVA = {"S1": 0.3, "S2": 0.1, "S3": 0.5}
P_INSAAT_PAHALI = {"S1": 0.5, "S2": 0.3, "S3": 0.2}
TEMEL = {  # (ölüm/yıl, gürültüden etkilenen bin kişi, maliyet milyar $)
    "S1": (0.5, 40, 3.8),
    "S2": (0.8, 15, 4.1),
    "S3": (0.3, 70, 3.5),
}
AGIRLIK = {"olum": 5.0, "gurultu": 0.05, "maliyet": 1.0}   # hepsi "milyar $ eşdeğeri" cinsinden


def sonuclar(yer: str, trafik_yogun: bool, dava: bool, pahali: bool) -> tuple[float, float, float]:
    olum, gurultu, maliyet = TEMEL[yer]
    if trafik_yogun:
        olum *= 1.5
        gurultu *= 1.3
    if dava:
        maliyet += 0.6
    if pahali:
        maliyet += 0.8
    return olum, gurultu, maliyet


def fayda(olum: float, gurultu: float, maliyet: float, w=AGIRLIK) -> float:
    return -(w["olum"] * olum + w["gurultu"] * gurultu + w["maliyet"] * maliyet)


def beklenen_fayda(yer: str, w=AGIRLIK, trafik_bilgisi: bool | None = None) -> float:
    toplam = 0.0
    for t, d, p in itertools.product((True, False), repeat=3):
        if trafik_bilgisi is not None and t != trafik_bilgisi:
            continue
        p_t = 1.0 if trafik_bilgisi is not None else (P_TRAFIK_YOGUN if t else 1 - P_TRAFIK_YOGUN)
        olasilik = p_t * (P_DAVA[yer] if d else 1 - P_DAVA[yer]) * (P_INSAAT_PAHALI[yer] if p else 1 - P_INSAAT_PAHALI[yer])
        toplam += olasilik * fayda(*sonuclar(yer, t, d, p), w)
    return toplam


def en_iyi_yer(w=AGIRLIK) -> tuple[str, dict]:
    eu = {y: beklenen_fayda(y, w) for y in YERLER}
    return max(eu, key=eu.get), eu


def main() -> None:
    print("=== Stokastik baskınlık (kitaptaki maliyetler) ===")
    print(f"  S1 ~ U[2.8, 4.8], S2 ~ U[3.0, 5.2]: S1 baskın mı? {stokastik_baskin_mi((2.8, 4.8), (3.0, 5.2))}")
    print(f"  S1 kesin 3.8, S2 ~ U[3.0, 5.2]:     S1 baskın mı? {stokastik_baskin_mi((3.8, 3.8 + 1e-9), (3.0, 5.2))}")
    print("  Kesin 3.8 bilinse karar vermek zorlaşır: S2 bazen daha ucuz olabilir; paranın faydasını")
    print("  bilmeden seçilemez (beklenen maliyetler 3.8 ve 4.1 olsa da).")
    print(f"  Katı baskınlık örneği: {katı_baskin_mi({'güvenlik': 2, 'sessizlik': 3, 'tutumluluk': -3}, {'güvenlik': 1, 'sessizlik': 3, 'tutumluluk': -4})}")

    print("\n=== Karar ağı: havalimanı yeri ===")
    en_iyi, eu = en_iyi_yer()
    for y in YERLER:
        print(f"  EU({y}) = {eu[y]:7.3f}{'   ← seçilir' if y == en_iyi else ''}")
    for ad, w in (("güvenliğe çok önem ver (w_ölüm = 20)", {**AGIRLIK, "olum": 20.0}),
                  ("gürültüye çok önem ver (w_gürültü = 0.2)", {**AGIRLIK, "gurultu": 0.2})):
        e, _ = en_iyi_yer(w)
        print(f"  {ad}: en iyi yer {e}")
    print("  Fayda fonksiyonu (ağırlıklar) değişince en iyi karar değişir: tercihler kararın parçasıdır.")

    print("\n=== Eylem–fayda tablosu (Q-fonksiyonu) biçimi ===")
    print("  Sonuç düğümleri atılıp fayda doğrudan şans düğümlerine ve karara bağlanabilir:")
    for t in (True, False):
        satir = ", ".join(f"{y}: {beklenen_fayda(y, trafik_bilgisi=t):6.2f}" for y in YERLER)
        print(f"  HavaTrafiği = {'yoğun ' if t else 'normal'} → {satir}")


if __name__ == "__main__":
    main()
