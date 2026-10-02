#!/usr/bin/env python3
"""Minimax ve alfa-beta: kitaptaki iki katlı oyun ağacı ve hamle sıralamasının etkisi.

Bölüm 1 — Kitaptaki ağaç (MAX kökü A; MIN düğümleri B, C, D):
    B: 3 12 8     C: 2 4 6     D: 14 5 2
    Minimax değerleri: B = 3, C = 2, D = 2, A = 3 → MAX a1'i (B'yi) seçer.
    Alfa-beta: C'nin ilk yaprağı 2 görülünce C ≤ 2 < α = 3 olur ve C'nin 4 ile 6
    yaprakları hiç değerlendirilmez (budanır).

Bölüm 2 — Hamle sıralaması. Rastgele ağaçlarda alfa-betanın değerlendirdiği
    yaprak sayısı: en iyi sıralamada kesin olarak b^⌈d/2⌉ + b^⌊d/2⌋ − 1
    (Knuth–Moore), rastgele sıralamada kabaca b^(3d/4), en kötü sıralamada b^d.

Çalıştırma:
    python oyun_agaci.py
"""
from __future__ import annotations

import math
import random
from typing import Union

Agac = Union[int, list]  # yaprak: sayı; iç düğüm: çocuk listesi

KITAP_AGACI: Agac = [[3, 12, 8], [2, 4, 6], [14, 5, 2]]
ETIKET = {0: "B", 1: "C", 2: "D"}


def minimax(dugum: Agac, max_sirasi: bool = True) -> int:
    if isinstance(dugum, int):
        return dugum
    degerler = [minimax(c, not max_sirasi) for c in dugum]
    return max(degerler) if max_sirasi else min(degerler)


def alfa_beta(dugum: Agac, max_sirasi: bool = True, alfa: float = -math.inf,
              beta: float = math.inf, iz: list | None = None, yol: str = "A") -> float:
    """Değerlendirilen yaprakları `iz` listesine (yol, değer) olarak ekler."""
    if isinstance(dugum, int):
        if iz is not None:
            iz.append((yol, dugum))
        return dugum
    if max_sirasi:
        v = -math.inf
        for i, c in enumerate(dugum):
            v = max(v, alfa_beta(c, False, alfa, beta, iz, yol + str(i + 1)))
            if v >= beta:
                return v          # MIN atası bu dala zaten izin vermez
            alfa = max(alfa, v)
        return v
    v = math.inf
    for i, c in enumerate(dugum):
        v = min(v, alfa_beta(c, True, alfa, beta, iz, yol + str(i + 1)))
        if v <= alfa:
            return v              # MAX atasının elinde daha iyisi var
        beta = min(beta, v)
    return v


def yaprak_say(dugum: Agac) -> int:
    return 1 if isinstance(dugum, int) else sum(yaprak_say(c) for c in dugum)


def rastgele_agac(b: int, d: int, rng: random.Random) -> Agac:
    if d == 0:
        return rng.randint(0, 1000)
    return [rastgele_agac(b, d - 1, rng) for _ in range(b)]


def sirala(dugum: Agac, max_sirasi: bool = True, en_iyi_once: bool = True) -> Agac:
    """Çocukları gerçek minimax değerlerine göre sırala (en iyi ya da en kötü önce)."""
    if isinstance(dugum, int):
        return dugum
    cocuklar = [sirala(c, not max_sirasi, en_iyi_once) for c in dugum]
    ters = max_sirasi == en_iyi_once
    return sorted(cocuklar, key=lambda c: minimax(c, not max_sirasi), reverse=ters)


def degerlendirilen(agac: Agac) -> int:
    iz: list = []
    alfa_beta(agac, iz=iz)
    return len(iz)


def main() -> None:
    print("=== Bölüm 1: kitaptaki iki katlı ağaç ===")
    for i, c in enumerate(KITAP_AGACI):
        print(f"  {ETIKET[i]} (MIN): yapraklar {c} → minimax {minimax(c, False)}")
    print(f"  A (MAX): minimax {minimax(KITAP_AGACI)} → en iyi hamle a1 (B)\n")

    iz: list = []
    alfa_beta(KITAP_AGACI, iz=iz)
    gorulen = {y for y, _ in iz}
    print("Alfa-beta değerlendirme sırası:")
    for y, v in iz:
        print(f"  {ETIKET[int(y[1]) - 1]}{y[2]} = {v}")
    budanan = [f"{ETIKET[i]}{j + 1}={v}" for i, c in enumerate(KITAP_AGACI)
               for j, v in enumerate(c) if f"A{i + 1}{j + 1}" not in gorulen]
    print(f"Budanan yapraklar: {', '.join(budanan)}  (9 yapraktan {len(iz)} tanesine bakıldı)")

    d_ters = [[3, 12, 8], [2, 4, 6], [2, 5, 14]]
    iz2: list = []
    alfa_beta(d_ters, iz=iz2)
    print(f"D'nin yaprakları 2, 5, 14 sırasında olsaydı: yalnızca {len(iz2)} yaprak değerlendirilirdi"
          " (D'nin ilk yaprağı 2 ≤ α = 3).")

    print("\n=== Bölüm 2: hamle sıralamasının etkisi (rastgele ağaçlar, 20'şer örnek) ===")
    print(f"{'b':>3}{'d':>3}{'minimax b^d':>13}{'en kötü':>10}{'rastgele':>10}{'en iyi':>9}"
          f"{'Knuth–Moore':>13}{'b^(3d/4)':>10}")
    rng = random.Random(0)
    for b, d in [(3, 4), (4, 4), (4, 6), (5, 6)]:
        kotu = rast = iyi = 0
        for _ in range(20):
            t = rastgele_agac(b, d, rng)
            kotu += degerlendirilen(sirala(t, en_iyi_once=False))
            rast += degerlendirilen(t)
            iyi += degerlendirilen(sirala(t, en_iyi_once=True))
        km = b ** math.ceil(d / 2) + b ** (d // 2) - 1
        print(f"{b:>3}{d:>3}{b ** d:>13,}{kotu / 20:>10,.0f}{rast / 20:>10,.0f}{iyi / 20:>9,.0f}"
              f"{km:>13,}{b ** (3 * d / 4):>10,.0f}")
    print("\nEn iyi sıralamada alfa-beta, aynı sürede yaklaşık iki kat derine inebilir"
          "\n(etkin dallanma faktörü b yerine √b). Pratikte önce 'iyi görünen' hamleleri"
          "\ndenemek (ör. taş alan hamleler, önceki aramanın en iyi hamlesi) bu ideale yaklaştırır.")


if __name__ == "__main__":
    main()
