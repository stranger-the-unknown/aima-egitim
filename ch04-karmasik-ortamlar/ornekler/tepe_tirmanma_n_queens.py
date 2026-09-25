#!/usr/bin/env python3
"""N-vezir tepe tırmanma — Bölüm 4. Saldırı metriği + isteğe bağlı rastgele yeniden başlatma."""
from __future__ import annotations

import argparse
import random
from typing import List, Tuple


def saldiri_sayisi(tahta: List[int]) -> int:
    """tahta[c] = satır (0..N-1). Aynı satır veya çaprazdaki vezir çiftlerini say."""
    n = len(tahta)
    saldiri = 0
    for c1 in range(n):
        for c2 in range(c1 + 1, n):
            r1, r2 = tahta[c1], tahta[c2]
            if r1 == r2 or abs(r1 - r2) == abs(c1 - c2):
                saldiri += 1
    return saldiri


def rastgele_tahta(n: int) -> List[int]:
    return [random.randrange(n) for _ in range(n)]


def en_iyi_komsu(tahta: List[int]) -> Tuple[List[int], int]:
    """Tek bir veziri başka satıra taşıyarak en az saldırılı komşuyu bul."""
    n = len(tahta)
    en_iyi = list(tahta)
    en_iyi_saldiri = saldiri_sayisi(tahta)
    for sutun in range(n):
        eski = tahta[sutun]
        for satir in range(n):
            if satir == eski:
                continue
            aday = list(tahta)
            aday[sutun] = satir
            s = saldiri_sayisi(aday)
            if s < en_iyi_saldiri:
                en_iyi_saldiri = s
                en_iyi = aday
    return en_iyi, en_iyi_saldiri


def tepe_tirmanma(n: int, max_adim: int = 200) -> Tuple[List[int], int, int]:
    """Tek koşu. Döner: (tahta, saldiri, adim_sayisi)."""
    tahta = rastgele_tahta(n)
    mevcut = saldiri_sayisi(tahta)
    for adim in range(max_adim):
        if mevcut == 0:
            return tahta, 0, adim
        komsu, ks = en_iyi_komsu(tahta)
        if ks >= mevcut:
            return tahta, mevcut, adim  # yerel tepe / plato
        tahta, mevcut = komsu, ks
    return tahta, mevcut, max_adim


def rastgele_yeniden_baslat(
    n: int, deneme: int, max_adim: int = 200
) -> Tuple[List[int], int, int, int]:
    """En iyi sonucu sakla. Döner: (tahta, saldiri, basarili_deneme_no, toplam_adim)."""
    en_iyi_t: List[int] = []
    en_iyi_s = n * n
    toplam_adim = 0
    basarili = -1
    for i in range(1, deneme + 1):
        t, s, a = tepe_tirmanma(n, max_adim)
        toplam_adim += a
        if s < en_iyi_s:
            en_iyi_s, en_iyi_t = s, t
            if s == 0:
                basarili = i
                break
    return en_iyi_t, en_iyi_s, basarili if basarili > 0 else deneme, toplam_adim


def tahta_yazdir(tahta: List[int]) -> None:
    n = len(tahta)
    for r in range(n):
        satir = ""
        for c in range(n):
            satir += "♛ " if tahta[c] == r else ". "
        print(satir)


def main() -> None:
    p = argparse.ArgumentParser(description="N-vezir tepe tırmanma (Bölüm 4)")
    p.add_argument("-n", type=int, default=8, help="Tahta boyutu (varsayılan 8)")
    p.add_argument(
        "--yeniden-baslat",
        type=int,
        default=0,
        metavar="K",
        help="K rastgele yeniden başlatma (0 = tek koşu)",
    )
    p.add_argument("--tohum", type=int, default=None, help="Rastgele tohum")
    p.add_argument("--max-adim", type=int, default=200)
    args = p.parse_args()

    if args.tohum is not None:
        random.seed(args.tohum)

    print(f"=== N-vezir tepe tırmanma (N={args.n}) ===\n")

    if args.yeniden_baslat <= 0:
        tahta, saldiri, adim = tepe_tirmanma(args.n, args.max_adim)
        print(f"Tek koşu — adım: {adim}, saldırı: {saldiri}")
    else:
        tahta, saldiri, deneme, toplam = rastgele_yeniden_baslat(
            args.n, args.yeniden_baslat, args.max_adim
        )
        print(
            f"Yeniden başlatma — deneme: {deneme}/{args.yeniden_baslat}, "
            f"toplam adım≈{toplam}, saldırı: {saldiri}"
        )

    print("\nTahta:")
    tahta_yazdir(tahta)
    print(f"\nSaldırı metriği: {saldiri}", end="")
    if saldiri == 0:
        print(" → çözüm bulundu!")
    else:
        print(" → yerel tepe (tam çözüm değil). --yeniden-baslat deneyin.")


if __name__ == "__main__":
    main()
