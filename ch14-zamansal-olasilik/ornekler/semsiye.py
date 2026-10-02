#!/usr/bin/env python3
"""Şemsiye dünyası: filtreleme, tahmin, yumuşatma, en olası dizi, olabilirlik.

Güvenlik görevlisi yeraltında çalışıyor; dışarıyı göremiyor. Her sabah müdürün şemsiyeyle
gelip gelmediğini görüyor ve yağmur yağıp yağmadığını tahmin etmeye çalışıyor.
    P(R_t | R_{t-1}) = 0.7, P(R_t | ¬R_{t-1}) = 0.3
    P(U_t | R_t)     = 0.9, P(U_t | ¬R_t)     = 0.2,   P(R_0) = ⟨0.5, 0.5⟩

Kitaptaki değerler (testlerle doğrulanır):
    P(R_1 | u_1) ≈ ⟨0.818, 0.182⟩,  P(R_2 | u_1) ≈ ⟨0.627, 0.373⟩,  P(R_2 | u_1, u_2) ≈ ⟨0.883, 0.117⟩
    b_{2:2} = ⟨0.69, 0.41⟩,  P(R_1 | u_1, u_2) ≈ ⟨0.883, 0.117⟩  (yumuşatma, filtrelemeden yüksek)
    Viterbi, [u, u, ¬u, u, u] için: yağmur, yağmur, kuru, yağmur, yağmur
    Tahmin uzadıkça dağılım durağan ⟨0.5, 0.5⟩'e yakınsar.

Çalıştırma:
    python semsiye.py
"""
from __future__ import annotations

from zamansal import semsiye_hmm

GUNLER = [True, True, False, True, True]


def main() -> None:
    h = semsiye_hmm()

    print("=== Filtreleme: 1. ve 2. günde şemsiye ===")
    f1 = h.filtrele([True])[0]
    tahmin2 = h.tahmin_adimi(f1)
    f2 = h.filtrele([True, True])[1]
    print(f"  P(R1 | u1)      = ⟨{f1[0]:.3f}, {f1[1]:.3f}⟩")
    print(f"  P(R2 | u1)      = ⟨{tahmin2[0]:.3f}, {tahmin2[1]:.3f}⟩   (tahmin adımı)")
    print(f"  P(R2 | u1, u2)  = ⟨{f2[0]:.3f}, {f2[1]:.3f}⟩")

    print("\n=== Tahmin: 2. günden sonrası, yeni gözlem yok ===")
    for k, p in enumerate(h.ileriye_tahmin(f2, 8), start=3):
        print(f"  P(R{k} | u1, u2) = {p[0]:.4f}")
    print(f"  Durağan dağılım: {[round(x, 3) for x in h.duragan_dagilim()]} (karışma süresinden sonra tahmin bilgisizleşir)")

    print("\n=== Yumuşatma: 1. gün, iki gözlemle ===")
    b = h.geri_mesajlari([True, True])[0]
    s = h.ileri_geri([True, True])[0]
    print(f"  Geri mesaj b_2:2 = ⟨{b[0]:.2f}, {b[1]:.2f}⟩")
    print(f"  P(R1 | u1, u2) = α⟨0.818, 0.182⟩ × ⟨0.69, 0.41⟩ = ⟨{s[0]:.3f}, {s[1]:.3f}⟩")
    print("  2. gündeki şemsiye, 1. günde yağmur yağdığını daha olası kılar (0.818 → 0.883).")

    print("\n=== Beş günlük dizi: [u, u, ¬u, u, u] ===")
    filtre = h.filtrele(GUNLER)
    yumusak = h.ileri_geri(GUNLER)
    yol, mesajlar = h.viterbi(GUNLER)
    print("  gün  şemsiye  filtre  yumuşatma  Viterbi mesajı m1:t (yağmur, kuru)  en olası dizi")
    for t in range(len(GUNLER)):
        print(f"   {t + 1}   {'var ' if GUNLER[t] else 'yok '}     {filtre[t][0]:.3f}    {yumusak[t][0]:.3f}"
              f"      ⟨{mesajlar[t][0]:.4f}, {mesajlar[t][1]:.4f}⟩               {yol[t]}")
    print(f"  P(e_1:5) = {h.olabilirlik(GUNLER):.5f}")
    print("  Yumuşatma geleceği de kullanır: 3. günde yağmur olasılığı artar (0.19 → 0.31), çünkü 4. ve 5.")
    print("  günler yağmurlu. 2. günde azalır (0.88 → 0.82), çünkü ertesi gün kuru görünüyor.")


if __name__ == "__main__":
    main()
