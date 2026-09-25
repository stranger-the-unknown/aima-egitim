#!/usr/bin/env python3
"""Bayes kuralı: tıbbi test ve yağmur–şemsiye güncellemesi.

Özgün eğitim örneği. Kitap metni kopyası değildir.
Sadece Python standart kütüphanesi (+ isteğe bağlı numpy yok).

Resmi referans: https://aima.cs.berkeley.edu/ · https://github.com/aimacode
"""
from __future__ import annotations


def bayes(oncel: float, olabilirlik: float, yanlis_poz: float) -> tuple[float, float, float]:
    """İki hipotezli boolean güncelleme.

    P(H|E) = P(E|H)P(H) / P(E)
    P(E) = P(E|H)P(H) + P(E|¬H)P(¬H)

    Returns: (sonsal, kanit_marjinal, pay)
    """
    pay = olabilirlik * oncel
    payda = pay + yanlis_poz * (1.0 - oncel)
    return pay / payda, payda, pay


def ornek_tibbi() -> None:
    print("=" * 60)
    print("Örnek 1 — Tıbbi test (nadir hastalık)")
    print("=" * 60)
    # Eğitim sayıların: nadir hastalık, iyi ama kusurlu test
    oncel = 0.001          # P(Hasta) = %0.1
    duyarlilik = 0.99      # P(Pozitif | Hasta)
    yanlis_poz = 0.05      # P(Pozitif | Sağlam)

    sonsal, p_e, pay = bayes(oncel, duyarlilik, yanlis_poz)

    print(f"  P(Hasta)              = {oncel:.4f}  (önsel)")
    print(f"  P(+ | Hasta)          = {duyarlilik:.2f}")
    print(f"  P(+ | Sağlam)         = {yanlis_poz:.2f}")
    print(f"  P(+) = P(+|H)P(H)+P(+|¬H)P(¬H)")
    print(f"       = {pay:.6f} + {yanlis_poz * (1 - oncel):.6f} = {p_e:.6f}")
    print(f"  P(Hasta | +)          = {sonsal:.4f}  ≈ %{100 * sonsal:.1f}")
    print()
    print("  Sezgi: hastalık nadir → çoğu pozitif aslında sağlıklı kişiden gelir.")
    print("  Test 'iyi' olsa bile sonsal %99 olmaz; önsel baskındır.")
    print()


def ornek_yagmur() -> None:
    print("=" * 60)
    print("Örnek 2 — Yağmur ve ıslak şemsiye")
    print("=" * 60)
    # H = Yağmur, E = Şemsiye ıslak görüldü (komşu şemsiyesi)
    oncel = 0.20           # P(Yağmur) sabah tahmini
    olasilik = 0.90        # P(Islak | Yağmur)
    yanlis = 0.15          # P(Islak | Yağmur yok) — sprinkler, dükkân vb.

    sonsal, p_e, pay = bayes(oncel, olasilik, yanlis)

    print(f"  P(Yağmur)             = {oncel:.2f}")
    print(f"  P(Islak | Yağmur)     = {olasilik:.2f}")
    print(f"  P(Islak | ¬Yağmur)    = {yanlis:.2f}")
    print(f"  P(Islak)              = {p_e:.4f}")
    print(f"  P(Yağmur | Islak)     = {sonsal:.4f}  ≈ %{100 * sonsal:.1f}")
    print()
    print("  Kanıt inancı %.0f%% → %.0f%% yükseltti." % (100 * oncel, 100 * sonsal))
    print()


def ornek_oransal() -> None:
    """Odds formu: sonsal_odds = likelihood_ratio * prior_odds."""
    print("=" * 60)
    print("Örnek 3 — Odds (oran) formu")
    print("=" * 60)
    oncel = 0.20
    lr = 0.90 / 0.15  # P(E|H) / P(E|¬H)
    prior_odds = oncel / (1 - oncel)
    post_odds = lr * prior_odds
    sonsal = post_odds / (1 + post_odds)
    print(f"  Önceki odds  P(H):P(¬H) = {prior_odds:.3f}")
    print(f"  Olabilirlik oranı       = {lr:.3f}")
    print(f"  Sonsal odds            = {post_odds:.3f}")
    print(f"  P(H|E)                  = {sonsal:.4f}")
    print()


def main() -> None:
    print("Bayes kuralı demoları (özgün Türkçe eğitim)\n")
    ornek_tibbi()
    ornek_yagmur()
    ornek_oransal()


if __name__ == "__main__":
    main()
