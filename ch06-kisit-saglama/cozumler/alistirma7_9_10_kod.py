#!/usr/bin/env python3
"""Alıştırma 7, 9 ve 10 çözümleri: kesme kümesi, min-çatışmada gürültü, değer simetrisi."""
from __future__ import annotations

import sys
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ornekler"))

import avustralya_csp as av  # noqa: E402
import harita_boyama_csp as tr  # noqa: E402
from kisit import CSP, geri_izleme, kesme_kumesi_coz  # noqa: E402
from min_catisma_vezir import min_catisma  # noqa: E402


def agac_mi(dugumler: set, komsular: dict) -> bool:
    """Kalan graf bir orman mı? (kenar sayısı = düğüm − bileşen)"""
    kenarlar = {frozenset((a, b)) for a in dugumler for b in komsular[a] if b in dugumler}
    gorulen, bilesen = set(), 0
    for d in dugumler:
        if d in gorulen:
            continue
        bilesen += 1
        yigin = [d]
        while yigin:
            x = yigin.pop()
            if x in gorulen:
                continue
            gorulen.add(x)
            yigin += [y for y in komsular[x] if y in dugumler]
    return len(kenarlar) == len(dugumler) - bilesen


def en_kucuk_kesme_kumesi(bolgeler: list, komsular: dict) -> list:
    for k in range(len(bolgeler) + 1):
        for aday in combinations(bolgeler, k):
            if agac_mi(set(bolgeler) - set(aday), komsular):
                return list(aday)
    return list(bolgeler)


def a7() -> None:
    print("=== A7: Türkiye haritasında döngü kesme kümesi ===")
    tek = [b for b in tr.BOLGELER if agac_mi(set(tr.BOLGELER) - {b}, tr.KOMSULUK)]
    print(f"  Tek başına ağaç bırakan bölge: {tek or 'yok'}")
    kesme = en_kucuk_kesme_kumesi(tr.BOLGELER, tr.KOMSULUK)
    print(f"  En küçük kesme kümesi: {kesme} (boyut {len(kesme)})")
    cozum = kesme_kumesi_coz(tr.turkiye(4), kesme)
    print(f"  4 renkle çözüm: {cozum}")
    print(f"  3 renkle: {kesme_kumesi_coz(tr.turkiye(3), kesme)}  (None = çözüm yok)")


def a9() -> None:
    print("\n=== A9: min-çatışmada gürültü (20 tohum, en fazla 10.000 adım) ===")
    print(f"  {'gürültü':>8}{'n':>7}{'başarı':>9}{'ort. adım':>12}")
    for g in (0.0, 0.05, 0.3):
        for n in (8, 1000):
            sonuc = [min_catisma(n, t, 10_000, gurultu=g) for t in range(20)]
            basari = [a for tahta, a in sonuc if tahta is not None]
            ort = sum(basari) / len(basari) if basari else float("nan")
            print(f"  {g:>8}{n:>7}{len(basari):>6}/20{ort:>12.1f}")


def a10() -> None:
    print("\n=== A10: değer simetrisi ===")
    sira = {r: i for i, r in enumerate(sorted(av.RENKLER))}  # alfabetik sıra

    def kisit(A, a, B, b):
        if a == b:
            return False
        if (A, B) == ("NT", "SA") or (A, B) == ("SA", "WA"):
            return sira[a] < sira[b]
        if (A, B) == ("SA", "NT") or (A, B) == ("WA", "SA"):
            return sira[a] > sira[b]
        return True

    normal = av.avustralya()
    kirik = CSP(av.BOLGELER, normal.alanlar, av.KOMSULAR, kisit)
    for ad, csp in (("simetri kırılmadan", normal), ("NT < SA < WA ile", kirik)):
        cozumler, ist = geri_izleme(csp, "mrv", "sirali", "ileri", tum_cozumler=True)
        print(f"  {ad:<20}: {len(cozumler):>2} çözüm, tümünü bulmak için {ist.atama} atama")


def main() -> None:
    a7()
    a9()
    a10()


if __name__ == "__main__":
    main()
