#!/usr/bin/env python3
"""Şanslı oyunlar: beklenti-minimaks (expectiminimax).

Tavla gibi zar içeren oyunlarda ağaçta MAX ve MIN düğümlerinin yanında
**şans düğümleri** de vardır. Şans düğümünün değeri, çocuklarının olasılıkla
ağırlıklı ortalamasıdır:

    EM(s) = FAYDA(s)                         s terminal ise
          = max_a EM(SONUÇ(s, a))            sıra MAX'ta ise
          = min_a EM(SONUÇ(s, a))            sıra MIN'de ise
          = Σ_r P(r) · EM(SONUÇ(s, r))       şans düğümüyse (r: zar sonucu)

Kitaptaki önemli gözlem: Yaprak değerlerinin **sırasını koruyan** bir dönüşüm
bile en iyi hamleyi değiştirebilir. [1, 2, 3, 4] değerleriyle a1, [1, 20, 30, 400]
ile a2 en iyidir. Bu yüzden şanslı oyunlarda değerlendirme fonksiyonu, kazanma
olasılığının (ya da beklenen faydanın) **pozitif doğrusal** bir dönüşümü olmalıdır.

Çalıştırma:
    python beklenti_minimax.py
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Max:
    cocuklar: dict  # hamle adı → düğüm


@dataclass
class Min:
    cocuklar: list


@dataclass
class Sans:
    dallar: list  # (olasılık, düğüm)


def em(d) -> float:
    if isinstance(d, (int, float)):
        return d
    if isinstance(d, Max):
        return max(em(c) for c in d.cocuklar.values())
    if isinstance(d, Min):
        return min(em(c) for c in d.cocuklar)
    return sum(p * em(c) for p, c in d.dallar)


def en_iyi_hamle(d: Max) -> tuple[str, dict]:
    degerler = {a: em(c) for a, c in d.cocuklar.items()}
    return max(degerler, key=degerler.get), degerler


def ornek_agac(v1: float, v2: float, v3: float, v4: float) -> Max:
    """MAX iki hamle arasında seçer; her hamleden sonra 0,9 / 0,1 olasılıklı bir zar atılır,
    ardından MIN oynar. v1 < v2 < v3 < v4 yaprak değerleri."""
    return Max({
        "a1": Sans([(0.9, Min([v2, v2])), (0.1, Min([v3, v3]))]),
        "a2": Sans([(0.9, Min([v1, v1])), (0.1, Min([v4, v4]))]),
    })


def karmasiklik(b: int, n: int, m: int) -> tuple[int, int]:
    """m hamle derinliğinde: şanssız minimaks ~ b^m, beklenti-minimaks ~ (b·n)^m yaprak."""
    return b ** m, (b * n) ** m


def main() -> None:
    print("=== Sırayı koruyan dönüşüm en iyi hamleyi değiştirir ===")
    for degerler in [(1, 2, 3, 4), (1, 20, 30, 400)]:
        hamle, d = en_iyi_hamle(ornek_agac(*degerler))
        ayrinti = ", ".join(f"{a}: {v:g}" for a, v in d.items())
        print(f"  yapraklar {list(degerler)} → {ayrinti}  ⇒ en iyi: {hamle}")
    print("  a1 = 0,9·v2 + 0,1·v3,  a2 = 0,9·v1 + 0,1·v4. Büyük v4, a2'yi 'kurtarır'.")
    print("  Şanssız minimakste yalnızca SIRA önemlidir; şans düğümü ise ortalama aldığı için"
          "\n  değerlerin BÜYÜKLÜĞÜ de önemlidir.")

    print("\n=== Karmaşıklık: şans düğümleri ağacı ne kadar büyütür? ===")
    print("  Tavla: yaklaşık b = 20 hamle, n = 21 farklı zar sonucu")
    print(f"  {'derinlik':>9}{'minimaks b^m':>16}{'beklenti-minimaks (bn)^m':>28}")
    for m in (1, 2, 3, 4):
        a, b = karmasiklik(20, 21, m)
        print(f"  {m:>9}{a:>16,}{b:>28,}")
    print("  Zar yüzünden alfa-beta tarzı budama zorlaşır. Bu yüzden tavla programları sığ"
          "\n  arama + çok iyi (öğrenilmiş) bir değerlendirme fonksiyonu kullanır.")


if __name__ == "__main__":
    main()
