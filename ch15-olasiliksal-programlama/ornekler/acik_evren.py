#!/usr/bin/env python3
"""Açık evren olasılık modeli (OUPM, kitaptaki 15.2): nesne sayısı da belirsiz.

Kitaptaki sayı ifadeleri:
    #Customer             ~ UniformInt(1, 3)
    #Book                 ~ UniformInt(2, 4)
    #LoginID(Owner = c)   ~ if Honest(c) then Exactly(1) else UniformInt(2, 5)
Dürüst olmayan bir müşteri birden çok kimlik açabilir (sybil saldırısı). Owner bir "köken
fonksiyonu"dur: Her giriş kimliği, onu üreten müşteriyi bilir.

Bu betik:
  1. Modelden olası dünyalar örnekler (üretimsel program).
  2. Kesin çıkarım: Sistemde 4 giriş kimliği görüldüyse kaç müşteri vardır? Sahtekâr var mı?
  3. Poisson dağılımı: ortalama λ, standart sapma √λ.

Çalıştırma:
    python acik_evren.py
"""
from __future__ import annotations

import itertools
import math
import random
from fractions import Fraction

P_HONEST = Fraction(99, 100)


def dunya_ornekle(rng: random.Random) -> dict:
    n_musteri = rng.randint(1, 3)
    n_kitap = rng.randint(2, 4)
    musteriler = []
    for c in range(1, n_musteri + 1):
        durust = rng.random() < float(P_HONEST)
        n_login = 1 if durust else rng.randint(2, 5)
        musteriler.append({"ad": f"Customer{c}", "durust": durust,
                           "loginler": [f"Login(Owner=Customer{c}, {i})" for i in range(1, n_login + 1)]})
    return {"#Customer": n_musteri, "#Book": n_kitap, "musteriler": musteriler}


def login_sayisi_sonsali(gozlenen: int) -> dict:
    """P(#Customer = n, dürüst olmayan sayısı = d | toplam giriş kimliği = gozlenen), kesin kesirlerle."""
    ortak: dict = {}
    for n in (1, 2, 3):
        for durustluk in itertools.product((True, False), repeat=n):
            p_d = math.prod(P_HONEST if h else 1 - P_HONEST for h in durustluk)
            sahte = durustluk.count(False)
            # sahte müşterilerin login sayıları UniformInt(2, 5)
            yollar = sum(1 for sayilar in itertools.product(range(2, 6), repeat=sahte)
                         if (n - sahte) + sum(sayilar) == gozlenen)
            p = Fraction(1, 3) * p_d * Fraction(yollar, 4 ** sahte)
            if p:
                ortak[(n, sahte)] = ortak.get((n, sahte), 0) + p
    z = sum(ortak.values())
    return {k: v / z for k, v in ortak.items()}


def poisson(k: int, lam: float) -> float:
    return math.exp(-lam) * lam ** k / math.factorial(k)


def main() -> None:
    rng = random.Random(5)
    print("=== Üretimsel programdan üç olası dünya ===")
    for _ in range(3):
        d = dunya_ornekle(rng)
        print(f"  #Customer = {d['#Customer']}, #Book = {d['#Book']}")
        for m in d["musteriler"]:
            print(f"    {m['ad']:<10} dürüst={m['durust']!s:<5} {len(m['loginler'])} kimlik")

    for gozlenen in (3, 4):
        print(f"\n=== {gozlenen} giriş kimliği görüldü: kaç müşteri var? ===")
        s = login_sayisi_sonsali(gozlenen)
        for n in (1, 2, 3):
            print(f"  P(#Customer = {n}) = {float(sum(v for (m, _), v in s.items() if m == n)):.3f}")
        print(f"  P(en az bir sahtekâr) = {float(sum(v for (_, d), v in s.items() if d > 0)):.3f}")
    print("  3 kimlik: En olası açıklama üç dürüst müşteri. 4 kimlik: En fazla 3 müşteri olabildiği için")
    print("  en az biri kesinlikle birden çok kimlik açmış: Kimlik sayısı ile kişi sayısı aynı şey değildir.")

    print("\n=== Poisson(λ): ortalama λ, standart sapma √λ ===")
    for lam in (3, 100, 1_000_000):
        print(f"  λ = {lam:>9,}: std = {math.sqrt(lam):>8,.1f}  (göreli {100 / math.sqrt(lam):.2f}%)")
    print(f"  Poisson(3): P(0) = {poisson(0, 3):.3f}, P(3) = {poisson(3, 3):.3f}, P(10) = {poisson(10, 3):.5f}")
    print("  Büyük λ'da göreli belirsizlik çok küçük: 'bir milyon civarı' gibi kaba bilgiler için")
    print("  kitap büyüklük mertebesi dağılımlarını önerir.")


if __name__ == "__main__":
    main()
