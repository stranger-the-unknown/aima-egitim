#!/usr/bin/env python3
"""İlişkisel olasılık modeli (RPM): kitaptaki kitap önerisi örneği (15.1).

Tipler: Müşteri, Kitap.  Fonksiyonlar ve bağımlılık ifadeleri:
    Honest(c)            ~ ⟨0.99, 0.01⟩
    Kindness(c)          ~ ⟨0.1, 0.1, 0.2, 0.3, 0.3⟩        (1..5)
    Quality(b)           ~ ⟨0.05, 0.2, 0.4, 0.2, 0.15⟩      (1..5)
    Recommendation(c, b) ~ if Honest(c) then HonestRecCPT(Kindness(c), Quality(b))
                           else ⟨0.4, 0.1, 0.0, 0.1, 0.4⟩   (bağlama özgü bağımsızlık)
Kitap HonestRecCPT'yi vermiyor. Bizim varsayımımız: dürüst müşteri, kitabın kalitesi çevresinde
puan verir; nazik müşteriler biraz daha cömerttir (ortalama = Quality + 0.5 × (Kindness − 3)).

Temellendirme (unrolling): C müşteri ve B kitap için 2C + B + BC düğümlü bir Bayes ağı.
Çıkarım: Kitap kaliteleri verildiğinde müşteriler birbirinden bağımsız olduğu için
    P(kanıt | Q) = Π_c Σ_{h,k} P(h) P(k) Π_b P(rec(c,b) | h, k, Q_b)
ile kesin hesap yapılır (yapıdaki tekrarı kullanmak, kitaptaki "yinelenen alt yapı" fikri).

Çalıştırma:
    python rpm_oneriler.py
"""
from __future__ import annotations

import itertools
import math

PUANLAR = [1, 2, 3, 4, 5]
P_HONEST = 0.99
P_KINDNESS = [0.1, 0.1, 0.2, 0.3, 0.3]
P_QUALITY = [0.05, 0.2, 0.4, 0.2, 0.15]
DURUST_OLMAYAN = [0.4, 0.1, 0.0, 0.1, 0.4]


def durust_oneri(kindness: int, quality: int, sigma: float = 0.6) -> list[float]:
    """Varsayımsal HonestRecCPT(Kindness, Quality)."""
    orta = quality + 0.5 * (kindness - 3)
    w = [math.exp(-(r - orta) ** 2 / (2 * sigma ** 2)) for r in PUANLAR]
    s = sum(w)
    return [x / s for x in w]


def p_oneri(r: int, honest: bool, kindness: int, quality: int) -> float:
    dagilim = durust_oneri(kindness, quality) if honest else DURUST_OLMAYAN
    return dagilim[r - 1]


def temellendir(musteriler: list[str], kitaplar: list[str]) -> list[tuple[str, list[str]]]:
    """Açılmış Bayes ağının düğümleri ve ebeveynleri."""
    dugumler = [(f"Quality({b})", []) for b in kitaplar]
    for c in musteriler:
        dugumler += [(f"Honest({c})", []), (f"Kindness({c})", [])]
        dugumler += [(f"Recommendation({c},{b})", [f"Honest({c})", f"Kindness({c})", f"Quality({b})"])
                     for b in kitaplar]
    return dugumler


def sonsal(kanit: dict[tuple[str, str], int], kitaplar: list[str]) -> dict:
    """Kesin çıkarım. Döner: her kitap için P(Quality), her müşteri için P(Honest)."""
    musteriler = sorted({c for c, _ in kanit})
    q_dagilim = {b: [0.0] * 5 for b in kitaplar}
    h_toplam = {c: 0.0 for c in musteriler}
    z = 0.0
    for Q in itertools.product(PUANLAR, repeat=len(kitaplar)):
        q = dict(zip(kitaplar, Q))
        p_q = math.prod(P_QUALITY[v - 1] for v in Q)
        musteri_olab, durust_olab = {}, {}
        for c in musteriler:
            toplam = durust = 0.0
            for h in (True, False):
                for k in PUANLAR:
                    p = (P_HONEST if h else 1 - P_HONEST) * P_KINDNESS[k - 1]
                    for (c2, b), r in kanit.items():
                        if c2 == c:
                            p *= p_oneri(r, h, k, q[b])
                    toplam += p
                    durust += p if h else 0.0
            musteri_olab[c], durust_olab[c] = toplam, durust
        agirlik = p_q * math.prod(musteri_olab.values())
        z += agirlik
        for b in kitaplar:
            q_dagilim[b][q[b] - 1] += agirlik
        for c in musteriler:
            h_toplam[c] += agirlik * durust_olab[c] / musteri_olab[c]
    return {"kalite": {b: [x / z for x in v] for b, v in q_dagilim.items()},
            "durust": {c: v / z for c, v in h_toplam.items()}}


def ortalama(dagilim: list[float]) -> float:
    return sum(p * r for p, r in zip(dagilim, PUANLAR))


def main() -> None:
    print("=== Temellendirme ===")
    for C, B in ((2, 2), (10, 5), (1000, 100)):
        dugum = 2 * C + B + B * C
        print(f"  {C} müşteri, {B} kitap: {dugum:,} düğüm, 2^{C}·5^{C + B + B * C} olası dünya")
    print("  2 müşteri, 2 kitap için düğümler:")
    for ad, ebeveyn in temellendir(["C1", "C2"], ["B1", "B2"]):
        print(f"    {ad:<22} ← {', '.join(ebeveyn) or '—'}")

    print(f"\n=== Önsel: E[Quality] = {ortalama(P_QUALITY):.2f} ===")
    kitaplar = ["B1", "B2"]
    kanit = {("C1", "B1"): 4, ("C2", "B1"): 5, ("C3", "B1"): 4,
             ("C1", "B2"): 2, ("C2", "B2"): 3, ("C3", "B2"): 2}
    s = sonsal(kanit, kitaplar)
    print("=== Üç dürüst görünen müşterinin puanları: B1 → 4, 5, 4;  B2 → 2, 3, 2 ===")
    for b in kitaplar:
        print(f"  P(Quality({b})) = {[round(p, 3) for p in s['kalite'][b]]},  E = {ortalama(s['kalite'][b]):.2f}")

    kanit2 = {**kanit, ("C4", "B1"): 1, ("C4", "B2"): 5}
    s2 = sonsal(kanit2, kitaplar)
    print("\n=== Dördüncü müşteri tam tersini söylüyor: B1 → 1, B2 → 5 ===")
    for b in kitaplar:
        print(f"  E[Quality({b})] = {ortalama(s2['kalite'][b]):.2f}")
    for c, p in s2["durust"].items():
        print(f"  P(Honest({c})) = {p:.3f}")
    print("  Uç ve diğerleriyle çelişen puanlar, C4'ün dürüst olmadığı olasılığını önseldeki 0.01'den")
    print("  çok yukarı taşır; model onun puanlarını büyük ölçüde görmezden gelir.")


if __name__ == "__main__":
    main()
