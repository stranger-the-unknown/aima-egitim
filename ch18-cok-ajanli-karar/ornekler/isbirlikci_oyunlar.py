#!/usr/bin/env python3
"""İşbirlikçi oyun kuramı (kitaptaki 18.3).

Oyun G = (N, ν): oyuncular ve her koalisyonun elde edebileceği değer ν(C).
Kitaptaki örnekler (testlerle doğrulanır):
  * N = {1, 2, 3} için 7 koalisyon ve 5 koalisyon yapısı; N = {1, 2, 3, 4} için 15 yapı.
  * ν({1}) = 4, ν({2, 3}) = 10 → olası sonuç ({{1}, {2, 3}}, (4, 5, 5)).
  * Çekirdeği boş, süperadditif bir oyun: ν(C) = 1 eğer |C| ≥ 2, değilse 0.
  * ν({1}) = ν({2}) = 5, ν({1, 2}) = 20: (6, 14) çekirdekte ama "adil" görünmüyor; Shapley (10, 10).
  * MC-ağı kuralları {({1,2}, 5), ({2}, 2), ({3}, 4)}: ν({1}) = 0, ν({3}) = 4, ν({1,3}) = 4,
    ν({2,3}) = 6, ν({1,2,3}) = 11. Shapley değeri kural başına simetriden: (2.5, 4.5, 4).
  * Koalisyon yapısı grafının ilk iki düzeyini aramak, en iyinin en az 1/n'ini garanti eder.

Çalıştırma:
    python isbirlikci_oyunlar.py
"""
from __future__ import annotations

import itertools
import math
from fractions import Fraction

import numpy as np

import oyun_kurami as ok


def koalisyonlar(N) -> list[frozenset]:
    N = list(N)
    return [frozenset(c) for r in range(1, len(N) + 1) for c in itertools.combinations(N, r)]


def koalisyon_yapilari(N) -> list[list[frozenset]]:
    """N'nin bütün bölüntüleri (koalisyon yapıları)."""
    N = list(N)
    if not N:
        return [[]]
    ilk, kalan = N[0], N[1:]
    yapilar = []
    for yapi in koalisyon_yapilari(kalan):
        for i in range(len(yapi)):                          # ilk'i var olan bir koalisyona ekle
            yapilar.append(yapi[:i] + [yapi[i] | {ilk}] + yapi[i + 1:])
        yapilar.append(yapi + [frozenset({ilk})])          # ya da tek başına
    return yapilar


def superadditif_mi(N, nu) -> bool:
    K = koalisyonlar(N)
    return all(nu(C | D) >= nu(C) + nu(D) for C in K for D in K if not C & D)


def cekirdekte_mi(N, nu, x: dict) -> bool:
    """x bir paylaşım (Σ x = ν(N), bireysel rasyonel) ve hiçbir koalisyon itiraz etmiyor mu?"""
    if sum(x.values()) != nu(frozenset(N)):
        return False
    return all(sum(x[i] for i in C) >= nu(C) for C in koalisyonlar(N))


def cekirdek_bos_mu(N, nu) -> bool:
    """Çekirdek boş değil ⇔ min Σ x_i (her C için x(C) ≥ ν(C) kısıtıyla) ≤ ν(N).
    Bu LP'nin ikilisi: max Σ_C ν(C) y_C, her i için Σ_{C∋i} y_C ≤ 1, y ≥ 0.
    z_C = ν(C) y_C değişkeniyle amaç Σ z_C olur ve oyun_kurami'ndaki simpleksle çözülür."""
    N = list(N)
    K = [C for C in koalisyonlar(N) if nu(C) > 0]
    if not K:
        return False
    B = np.array([[(1.0 / nu(C)) if i in C else 0.0 for C in K] for i in N])
    _, _, amac = ok.simpleks(B)
    return amac > nu(frozenset(N)) + 1e-9


def shapley(N, nu) -> dict:
    """φ_i = (1/n!) Σ_p mc_i(p_i): bütün sıralamalarda i'nin öncekilere kattığı değerin ortalaması."""
    N = list(N)
    phi = {i: Fraction(0) for i in N}
    for sira in itertools.permutations(N):
        onceki = frozenset()
        for i in sira:
            phi[i] += Fraction(nu(onceki | {i}) - nu(onceki))
            onceki = onceki | {i}
    return {i: v / math.factorial(len(N)) for i, v in phi.items()}


def mc_agi(kurallar):
    """Marjinal katkı ağı: ν(C) = Σ {x | (C_i, x) kural ve C_i ⊆ C}."""
    return lambda C: sum(x for Ci, x in kurallar if set(Ci) <= set(C))


def mc_agi_shapley(N, kurallar) -> dict:
    """Her kural kendi başına simetrik bir oyundur: kuraldaki her oyuncu x/|C_i| alır (polinom zaman)."""
    phi = {i: Fraction(0) for i in N}
    for Ci, x in kurallar:
        for i in Ci:
            phi[i] += Fraction(x, len(Ci))
    return phi


def sosyal_refah(yapi, nu) -> float:
    return sum(nu(C) for C in yapi)


def ilk_iki_duzey(N, nu):
    """Koalisyon yapısı grafının 1. ve 2. düzeyleri (en çok iki koalisyonlu yapılar) içinde en iyisi."""
    yapilar = [y for y in koalisyon_yapilari(N) if len(y) <= 2]
    return max(yapilar, key=lambda y: sosyal_refah(y, nu))


def yaz(phi: dict) -> str:
    return "{" + ", ".join(f"{i}: {v}" for i, v in phi.items()) + "}"


def main() -> None:
    N3, N4 = [1, 2, 3], [1, 2, 3, 4]
    print("=== Koalisyonlar ve koalisyon yapıları ===")
    print(f"  N = {{1,2,3}}: {len(koalisyonlar(N3))} koalisyon, {len(koalisyon_yapilari(N3))} yapı")
    for y in koalisyon_yapilari(N3):
        print("    " + str([set(C) for C in y]))
    print(f"  N = {{1,2,3,4}}: {len(koalisyon_yapilari(N4))} yapı;  n = 10 için {len(koalisyon_yapilari(range(10)))}")

    print("\n=== Çekirdek ===")
    bos = lambda C: 1 if len(C) >= 2 else 0
    print(f"  ν(C) = 1 (|C| ≥ 2): süperadditif mi? {superadditif_mi(N3, bos)}, çekirdek boş mu? {cekirdek_bos_mu(N3, bos)}")
    iki = lambda C: {1: 5, 2: 20}[len(C)] if C else 0
    print(f"  ν({{1}}) = ν({{2}}) = 5, ν({{1,2}}) = 20: (6, 14) çekirdekte mi? {cekirdekte_mi([1, 2], iki, {1: 6, 2: 14})};"
          f" çekirdek boş mu? {cekirdek_bos_mu([1, 2], iki)}")
    print(f"  Shapley değeri: {yaz(shapley([1, 2], iki))}  (artığı eşit böler)")

    print("\n=== Marjinal katkı ağı ===")
    kurallar = [({1, 2}, 5), ({2}, 2), ({3}, 4)]
    nu = mc_agi(kurallar)
    for C in ({1}, {3}, {1, 3}, {2, 3}, {1, 2, 3}):
        print(f"  ν({C}) = {nu(C)}")
    print(f"  Shapley (bütün sıralamalar): {yaz(shapley(N3, nu))}")
    print(f"  Shapley (kural başına):      {yaz(mc_agi_shapley(N3, kurallar))}")

    print("\n=== En iyi koalisyon yapısı ve ilk iki düzey ===")
    tekil = lambda C: 1 if len(C) == 1 else 0           # yalnız çalışmak kazandırır: en kötü durum örneği
    en_iyi = max(koalisyon_yapilari(N4), key=lambda y: sosyal_refah(y, tekil))
    ilk = ilk_iki_duzey(N4, tekil)
    print(f"  ν(C) = 1 yalnızca tekli koalisyonlar için: en iyi {[set(C) for C in en_iyi]} → {sosyal_refah(en_iyi, tekil)};"
          f" ilk iki düzeyin en iyisi {sosyal_refah(ilk, tekil)}")
    print("  Garanti: İlk iki düzeyin en iyisi ≥ (1/n) × en iyi; burada 1 = 4/4, yani sınır sıkı.")


if __name__ == "__main__":
    main()
