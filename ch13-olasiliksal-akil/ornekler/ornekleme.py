#!/usr/bin/env python3
"""Yaklaşık çıkarım: kitabın yağmurlama (sprinkler) ağında örnekleme yöntemleri.

    Cloudy → Sprinkler, Cloudy → Rain, (Sprinkler, Rain) → WetGrass
    P(C) = 0.5;  P(S | C) = 0.1 / 0.5;  P(R | C) = 0.8 / 0.2
    P(W | S, R): tt 0.99, tf 0.90, ft 0.90, ff 0.00

Kitaptaki değerler (testlerle doğrulanır):
  * S_PS(true, false, true, true) = 0.5 × 0.9 × 0.8 × 0.9 = 0.324
  * P(Rain | Sprinkler = true) = ⟨0.3, 0.7⟩ (ret örneklemesi buna yakınsar)
  * Olabilirlik ağırlıklandırmada [true, false, true, true] örneğinin ağırlığı 0.5 × 0.9 = 0.45

Çalıştırma:
    python ornekleme.py
"""
from __future__ import annotations

import random

from bayes_agi import BayesAgi

T, F = True, False


def yagmurlama_agi() -> BayesAgi:
    ag = BayesAgi()
    ag.ekle("Cloudy", [], {(): 0.5})
    ag.ekle("Sprinkler", ["Cloudy"], {(T,): 0.1, (F,): 0.5})
    ag.ekle("Rain", ["Cloudy"], {(T,): 0.8, (F,): 0.2})
    ag.ekle("WetGrass", ["Sprinkler", "Rain"], {(T, T): 0.99, (T, F): 0.90, (F, T): 0.90, (F, F): 0.00})
    return ag


def main() -> None:
    ag = yagmurlama_agi()
    rng = random.Random(42)

    print("=== Doğrudan (önsel) örnekleme ===")
    olay = {"Cloudy": T, "Sprinkler": F, "Rain": T, "WetGrass": T}
    print(f"  S_PS(true, false, true, true) = {ag.ortak(olay):.3f}  (kitap: 0.324)")
    N = 10000
    say = sum(ag.onsel_ornek(rng) == olay for _ in range(N))
    print(f"  {N} örnekte bu olayın oranı: {say / N:.3f}")

    print("\n=== Ret örneklemesi: P(Rain | Sprinkler = true), kesin ⟨0.3, 0.7⟩ ===")
    for N in (100, 1000, 10000, 100000):
        tahmin, kabul = ag.ret_ornekleme("Rain", {"Sprinkler": T}, N, rng)
        print(f"  N = {N:>6}: kabul edilen {kabul:>5} ({100 * kabul / N:4.1f}%), P̂(rain) = {tahmin[T]:.3f}")
    print("  Kanıt olasılığı P(Sprinkler) = 0.3: örneklerin ~%70'i boşa gider.")
    nadir = {"Sprinkler": T, "Rain": T, "WetGrass": F}
    p_nadir = sum(ag.ortak({**nadir, "Cloudy": c}) for c in (T, F))
    _, kabul = ag.ret_ornekleme("Cloudy", nadir, 10000, rng)
    print(f"  Kanıt ne kadar nadirse kayıp o kadar büyük: P(s, r, ¬w) = {p_nadir:.4f};"
          f" 10000 örnekten yalnızca {kabul} tanesi kabul edildi.")

    print("\n=== Olabilirlik ağırlıklandırma: P(Rain | Cloudy = true, WetGrass = true) ===")
    kesin = ag.numaralandirma("Rain", {"Cloudy": T, "WetGrass": T})[T]
    print(f"  Kesin değer: {kesin:.4f}")
    for N in (100, 1000, 10000):
        tahmin = ag.olabilirlik_agirliklandirma("Rain", {"Cloudy": T, "WetGrass": T}, N, rng)
        print(f"  N = {N:>5}: P̂(rain) = {tahmin[T]:.4f}")
    print("  Kanıt değişkenleri örneklenmez; örnek, kanıtın olabilirliğiyle ağırlıklandırılır."
          "\n  Örn. Sprinkler = false, Rain = true çıkarsa ağırlık = P(c) × P(w | ¬s, r) = 0.5 × 0.9 = 0.45.")

    print("\n=== Gibbs örneklemesi: P(Rain | Sprinkler = true, WetGrass = true) ===")
    kesin = ag.numaralandirma("Rain", {"Sprinkler": T, "WetGrass": T})[T]
    print(f"  Kesin değer: {kesin:.4f}")
    for N in (1000, 10000, 100000):
        tahmin = ag.gibbs("Rain", {"Sprinkler": T, "WetGrass": T}, N, rng, isinma=100)
        print(f"  N = {N:>6}: P̂(rain) = {tahmin[T]:.4f}")
    durum = {"Cloudy": T, "Sprinkler": T, "Rain": F, "WetGrass": T}
    print(f"  Cloudy'nin Markov örtüsü {sorted(ag.markov_ortusu('Cloudy'))}: "
          f"P(cloudy | s, ¬r) = {ag.markov_ortusu_dagilimi('Cloudy', durum):.4f}")
    print("  Her adımda bir değişken, Markov örtüsü verildiğinde yeniden örneklenir.")


if __name__ == "__main__":
    main()
