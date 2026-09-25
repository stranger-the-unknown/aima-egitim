#!/usr/bin/env python3
"""Sürekli uzayda yerel arama: üç havalimanını nereye kurmalı?

Kitaptaki örneğin Türkiye uyarlaması: 20 il merkezinin her birinin **en yakın**
havalimanına uzaklığının karesi toplamını en aza indirecek şekilde 3 havalimanı
yerleştir. Durum uzayı 6 boyutludur: (x1, y1, x2, y2, x3, y3).

    f(x) = Σ_i Σ_{c ∈ C_i} (x_i − x_c)² + (y_i − y_c)²      C_i: i. havalimanına en yakın iller

Üç yöntem karşılaştırılıyor:
  1. Deneysel gradyan: f'yi küçük δ adımlarıyla ölçüp yokuş aşağı git (türev bilmeden).
  2. Gradyan inişi: ∂f/∂x_i = 2 Σ_{c∈C_i} (x_i − x_c) formülüyle x ← x − α∇f.
  3. Newton adımı: Bu f için Hessian 2|C_i|·I olduğundan Newton adımı havalimanını
     doğrudan kümesinin **ağırlık merkezine** taşır. (Bu, k-ortalamalar algoritmasıdır!)

Gradyan yalnızca **yerel olarak** doğrudur: Bir havalimanı çok hareket ederse
C_i kümeleri değişir. Bu yüzden farklı başlangıçlar farklı yerel minimumlara gider.

Çalıştırma:
    python havalimani_gradyan.py
"""
from __future__ import annotations

import math
import random

# Yaklaşık enlem, boylam (derece)
ILLER = {
    "İstanbul": (41.01, 28.98), "Ankara": (39.93, 32.86), "İzmir": (38.42, 27.14),
    "Bursa": (40.19, 29.06), "Antalya": (36.90, 30.70), "Adana": (37.00, 35.32),
    "Konya": (37.87, 32.48), "Gaziantep": (37.07, 37.38), "Şanlıurfa": (37.16, 38.79),
    "Diyarbakır": (37.91, 40.24), "Kayseri": (38.73, 35.48), "Samsun": (41.29, 36.33),
    "Trabzon": (41.00, 39.72), "Erzurum": (39.90, 41.27), "Van": (38.49, 43.38),
    "Eskişehir": (39.78, 30.52), "Malatya": (38.35, 38.31), "Denizli": (37.78, 29.09),
    "Edirne": (41.68, 26.56), "Sivas": (39.75, 37.02),
}

# Enlem/boylamı kabaca km'ye çevir (eşdikdörtgen izdüşüm, 39° enlem civarı)
KM_DERECE = 111.0
COS39 = math.cos(math.radians(39))
NOKTALAR = {ad: (boy * KM_DERECE * COS39, enl * KM_DERECE) for ad, (enl, boy) in ILLER.items()}
P = list(NOKTALAR.values())

Konum = list[tuple[float, float]]


def kumeler(havalimanlari: Konum) -> list[list[int]]:
    """Her ilin en yakın havalimanını bul: C_i kümeleri (il indeksleri)."""
    C: list[list[int]] = [[] for _ in havalimanlari]
    for j, (x, y) in enumerate(P):
        i = min(range(len(havalimanlari)),
                key=lambda k: (havalimanlari[k][0] - x) ** 2 + (havalimanlari[k][1] - y) ** 2)
        C[i].append(j)
    return C


def f(havalimanlari: Konum) -> float:
    """Amaç fonksiyonu (km²)."""
    return sum(
        min((hx - x) ** 2 + (hy - y) ** 2 for hx, hy in havalimanlari)
        for x, y in P
    )


def gradyan(havalimanlari: Konum) -> Konum:
    """Yerel olarak doğru analitik gradyan: 2 Σ (x_i − x_c)."""
    C = kumeler(havalimanlari)
    return [
        (2 * sum(hx - P[j][0] for j in C[i]), 2 * sum(hy - P[j][1] for j in C[i]))
        for i, (hx, hy) in enumerate(havalimanlari)
    ]


def gradyan_inisi(baslangic: Konum, alfa: float = 0.01, adim: int = 300) -> tuple[Konum, list[float]]:
    x = list(baslangic)
    gecmis = [f(x)]
    for _ in range(adim):
        g = gradyan(x)
        x = [(hx - alfa * gx, hy - alfa * gy) for (hx, hy), (gx, gy) in zip(x, g)]
        gecmis.append(f(x))
    return x, gecmis


def deneysel_gradyan(baslangic: Konum, delta: float = 20.0, adim: int = 400) -> tuple[Konum, list[float]]:
    """Türev kullanmadan: 12 komşudan (her koordinat ±δ) en iyisine git; iyileşme yoksa δ'yı yarıla."""
    x = list(baslangic)
    fx = f(x)
    gecmis = [fx]
    for _ in range(adim):
        en_iyi, f_en_iyi = None, fx
        for i in range(len(x)):
            for dx, dy in ((delta, 0), (-delta, 0), (0, delta), (0, -delta)):
                aday = list(x)
                aday[i] = (x[i][0] + dx, x[i][1] + dy)
                fa = f(aday)
                if fa < f_en_iyi:
                    en_iyi, f_en_iyi = aday, fa
        if en_iyi is None:
            delta /= 2
            if delta < 0.5:
                break
        else:
            x, fx = en_iyi, f_en_iyi
        gecmis.append(fx)
    return x, gecmis


def newton(baslangic: Konum, adim: int = 20) -> tuple[Konum, list[float]]:
    """Newton–Raphson: x ← x − H⁻¹∇f. Burada H = 2|C_i|·I, adım = kümenin ağırlık merkezi."""
    x = list(baslangic)
    gecmis = [f(x)]
    for _ in range(adim):
        C = kumeler(x)
        yeni = [
            (sum(P[j][0] for j in C[i]) / len(C[i]), sum(P[j][1] for j in C[i]) / len(C[i]))
            if C[i] else x[i]
            for i in range(len(x))
        ]
        if yeni == x:
            break
        x = yeni
        gecmis.append(f(x))
    return x, gecmis


def en_yakin_il(konum: tuple[float, float]) -> str:
    return min(NOKTALAR, key=lambda ad: math.dist(NOKTALAR[ad], konum))


def rastgele_baslangic(rng: random.Random, k: int = 3) -> Konum:
    xs = [p[0] for p in P]
    ys = [p[1] for p in P]
    return [(rng.uniform(min(xs), max(xs)), rng.uniform(min(ys), max(ys))) for _ in range(k)]


def ozet(ad: str, x: Konum, gecmis: list[float]) -> None:
    C = kumeler(x)
    print(f"{ad:<20} f = {gecmis[-1] / 1000:>8,.0f} bin km²   ({len(gecmis) - 1} adım)")
    for i, h in enumerate(x):
        iller = ", ".join(sorted(list(NOKTALAR)[j] for j in C[i]))
        print(f"    ✈ {en_yakin_il(h):<11} yakını → {iller}")


def main() -> None:
    rng = random.Random(4)
    bas = rastgele_baslangic(rng)
    print(f"Başlangıç: f = {f(bas) / 1000:,.0f} bin km²\n")
    ozet("Deneysel gradyan", *deneysel_gradyan(bas))
    ozet("Gradyan inişi", *gradyan_inisi(bas))
    ozet("Newton (k-ortalama)", *newton(bas))

    print("\nFarklı rastgele başlangıçlar (Newton ile): yerel minimumlar")
    sonuclar = set()
    for tohum in range(12):
        x, g = newton(rastgele_baslangic(random.Random(tohum)))
        sonuclar.add((round(g[-1] / 1000), tuple(sorted(en_yakin_il(h) for h in x))))
    for deger, yerler in sorted(sonuclar):
        print(f"    f = {deger:>6,} bin km²   havalimanları: {', '.join(yerler)}")
    print("\nDers: Gradyan yöntemleri hızlı ama yereldir. En iyi sonucu bulmak için"
          "\nrastgele yeniden başlatma burada da işe yarar.")


if __name__ == "__main__":
    main()
