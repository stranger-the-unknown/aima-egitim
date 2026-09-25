#!/usr/bin/env python3
"""Bilgi değeri (VOI) — minik sayısal demo.

Senaryo (özgün): İki eylem — ameliyat / ilaç.
Gizli durum: hastalık ağır (A) veya hafif (H).
İsteğe bağlı ucuz test: durumu büyük olasılıkla doğru söyler.

VOI ≈ (test sonrası beklenen MEU) − (testsiz MEU)
(maliyet ayrı düşülür.)

Resmi referans: https://aima.cs.berkeley.edu/ · https://github.com/aimacode
"""
from __future__ import annotations

import numpy as np

# Önsel
P_AGIR = 0.4
P_HAFIF = 1.0 - P_AGIR

# Fayda: U[eylem][durum]  durum sırası: ağır, hafif
U = {
    "ameliyat": np.array([80.0, 40.0]),  # ağırda iyi; hafifte aşırı
    "ilac": np.array([30.0, 90.0]),      # ağırda zayıf; hafifte iyi
}

EYLEMLER = list(U.keys())
DURUMLAR = ("agir", "hafif")


def eu_oncu(p_agir: float) -> tuple[str, float]:
    """Verilen P(ağır) ile MEU eylem ve değeri."""
    p = np.array([p_agir, 1.0 - p_agir])
    best_a, best_v = EYLEMLER[0], -1e9
    for a in EYLEMLER:
        v = float(np.dot(p, U[a]))
        if v > best_v:
            best_a, best_v = a, v
    return best_a, best_v


def test_sonrasi(test_sonucu: str, dogruluk: float = 0.85) -> tuple[float, float]:
    """Basit simetrik test: P(T=d | D=d)=dogruluk.
    Bayes ile P(ağır | test) güncelle, MEU döndür.
    """
    if test_sonucu == "agir":
        like_agir = dogruluk
        like_hafif = 1.0 - dogruluk
    else:
        like_agir = 1.0 - dogruluk
        like_hafif = dogruluk

    pay = like_agir * P_AGIR
    payda = pay + like_hafif * P_HAFIF
    p_agir_son = pay / payda
    _, meu = eu_oncu(p_agir_son)
    return p_agir_son, meu


def main() -> None:
    print("Bilgi değeri (VOI) mini demo\n")

    a0, meu0 = eu_oncu(P_AGIR)
    print(f"Testsiz: P(ağır)={P_AGIR:.2f} → MEU eylem={a0}, EU={meu0:.2f}")

    dogruluk = 0.85
    p_t_agir = dogruluk * P_AGIR + (1 - dogruluk) * P_HAFIF
    p_t_hafif = 1.0 - p_t_agir

    p_son_a, meu_a = test_sonrasi("agir", dogruluk)
    p_son_h, meu_h = test_sonrasi("hafif", dogruluk)

    print(f"\nTest doğruluğu = {dogruluk:.0%}")
    print(f"  T=ağır  → P(ağır|T)={p_son_a:.3f}, MEU={meu_a:.2f}")
    print(f"  T=hafif → P(ağır|T)={p_son_h:.3f}, MEU={meu_h:.2f}")

    meu_testli = p_t_agir * meu_a + p_t_hafif * meu_h
    voi = meu_testli - meu0
    maliyet = 5.0

    print(f"\nTest sonrası beklenen MEU = {meu_testli:.2f}")
    print(f"VOI (maliyet öncesi)      = {voi:.2f}")
    print(f"Test maliyeti             = {maliyet:.2f}")
    print(f"Net değer                 = {voi - maliyet:.2f}")
    print(f"→ Testi {'al' if voi > maliyet else 'alma'} (eğitim kararı)")
    print("\nBitti. Kaynak: aima.cs.berkeley.edu · aimacode")


if __name__ == "__main__":
    main()
