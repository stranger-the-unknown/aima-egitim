#!/usr/bin/env python3
"""Rastgele 3-SAT'ta faz geçişi: DPLL ve WalkSAT.

n sembollü, m tümceli rastgele 3-CNF cümleleri üret. m/n oranı küçükken cümleler
neredeyse hep karşılanabilir (az kısıt), büyükken neredeyse hiç karşılanamaz.
Geçiş, m/n ≈ 4,3 civarında keskin biçimde olur ve **en zor** problemler de oradadır.
Kitap bu deneyi n = 50 ile gösterir; burada hızlı çalışsın diye n = 30 kullanıyoruz
(geçiş, küçük n'de biraz daha yumuşaktır).

Çalıştırma:
    python sat_faz_gecisi.py
    python sat_faz_gecisi.py --n 30 --ornek 40
"""
from __future__ import annotations

import argparse
import random
import statistics

from onerme import dpll, rastgele_3cnf, walksat


def deney(n: int, oranlar, ornek: int, tohum: int = 0):
    rng = random.Random(tohum)
    satirlar = []
    for oran in oranlar:
        m = round(oran * n)
        karsilanan = 0
        dpll_cagri, walk_cevirme = [], []
        for _ in range(ornek):
            tumceler = rastgele_3cnf(n, m, rng)
            ist: dict = {}
            model = dpll(tumceler, ist=ist)
            dpll_cagri.append(ist["cagri"])
            if model is not None:
                karsilanan += 1
                _, cevirme = walksat(tumceler, max_cevirme=20_000, rng=rng)
                walk_cevirme.append(cevirme)
        satirlar.append((oran, karsilanan / ornek, statistics.median(dpll_cagri),
                         statistics.median(walk_cevirme) if walk_cevirme else None))
    return satirlar


def main() -> None:
    ap = argparse.ArgumentParser(description="Rastgele 3-SAT faz geçişi")
    ap.add_argument("--n", type=int, default=30)
    ap.add_argument("--ornek", type=int, default=30)
    args = ap.parse_args()
    oranlar = [1, 2, 3, 3.5, 4, 4.3, 4.6, 5, 6, 7, 8]
    print(f"n = {args.n} sembol, her oran için {args.ornek} rastgele cümle\n")
    print(f"{'m/n':>5}{'P(karşılanabilir)':>19}  {'DPLL çağrı (medyan)':>20}  {'WalkSAT çevirme':>16}  grafik")
    for oran, p, d, w in deney(args.n, oranlar, args.ornek):
        cubuk = "█" * round(p * 20)
        w_metin = f"{w:,.0f}" if w is not None else "—"
        print(f"{oran:>5}{p:>19.2f}  {d:>20,.0f}  {w_metin:>16}  {cubuk}")
    print("\n• Karşılanabilirlik olasılığı 4–5 arasında hızla 1'den 0'a düşer."
          "\n• DPLL'in işi de geçiş bölgesinde en yüksektir: Ne çözümü kolayca bulur ne de"
          "\n  çelişkiyi kolayca kanıtlar. Az kısıtlı cümleler kolayca karşılanır, çok kısıtlı"
          "\n  cümleler hızla çelişkiye düşer."
          "\n• WalkSAT yalnızca karşılanabilir cümlelerde çalışır: Çözüm yoksa bunu kanıtlayamaz.")


if __name__ == "__main__":
    main()
