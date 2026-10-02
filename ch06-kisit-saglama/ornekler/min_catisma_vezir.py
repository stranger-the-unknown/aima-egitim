#!/usr/bin/env python3
"""Min-çatışma yerel araması ile çok büyük N-vezir problemleri.

MIN-CONFLICTS: (1) her sütuna açgözlü bir başlangıç satırı ver, (2) çatışan vezirlerden
rastgele birini seç, (3) onu kendi sütununda en az çatışan satıra taşı. Tekrarla.

Kitaptaki gözlem: Açgözlü başlangıçla adım sayısı n'den neredeyse **bağımsızdır**;
bir milyon vezir bile ortalama ~50 adımda çözülür. Buradaki uygulama numpy ile
çatışma sayılarını satır ve çapraz sayaçlarıyla O(1)'de günceller.

Çalıştırma:
    python min_catisma_vezir.py
    python min_catisma_vezir.py --n 20000
"""
from __future__ import annotations

import argparse
import time

import numpy as np


def min_catisma(n: int, tohum: int = 0, max_adim: int = 10_000, acgozlu: bool = True,
                gurultu: float = 0.05):
    """Döner: (tahta dizisi, onarım adımı sayısı) ya da (None, max_adim).

    `gurultu` olasılığıyla vezir en az çatışan satır yerine rastgele bir satıra konur.
    Bu olmadan küçük tahtalarda algoritma bir yerel minimumda sonsuza kadar dönebilir:
    her çatışan vezirin en iyi satırı zaten bulunduğu satırdır.
    """
    rng = np.random.default_rng(tohum)
    satir = np.zeros(n, dtype=np.int64)          # satırdaki vezir sayısı
    capraz1 = np.zeros(2 * n, dtype=np.int64)    # r + c
    capraz2 = np.zeros(2 * n, dtype=np.int64)    # r − c + n
    tahta = np.empty(n, dtype=np.int64)
    satirlar = np.arange(n)

    def yerlestir(c: int, r: int, d: int) -> None:
        satir[r] += d
        capraz1[r + c] += d
        capraz2[r - c + n] += d

    # 1. Başlangıç
    for c in range(n):
        if acgozlu:
            catisma = satir + capraz1[satirlar + c] + capraz2[satirlar - c + n]
            en_az = catisma.min()
            r = int(rng.choice(np.flatnonzero(catisma == en_az)))
        else:
            r = int(rng.integers(n))
        tahta[c] = r
        yerlestir(c, r, +1)

    # 2. Onarım döngüsü
    sutunlar = np.arange(n)
    for adim in range(max_adim):
        # Her vezirin kendisi hariç çatışma sayısı
        catisma = satir[tahta] + capraz1[tahta + sutunlar] + capraz2[tahta - sutunlar + n] - 3
        catisanlar = np.flatnonzero(catisma > 0)
        if catisanlar.size == 0:
            return tahta, adim
        c = int(rng.choice(catisanlar))
        yerlestir(c, int(tahta[c]), -1)
        if rng.random() < gurultu:
            r = int(rng.integers(n))
        else:
            aday = satir + capraz1[satirlar + c] + capraz2[satirlar - c + n]
            en_az = aday.min()
            r = int(rng.choice(np.flatnonzero(aday == en_az)))
        tahta[c] = r
        yerlestir(c, r, +1)
    return None, max_adim


def dogru_mu(tahta) -> bool:
    n = len(tahta)
    t = [int(x) for x in tahta]
    return (len(set(t)) == n and len({t[c] + c for c in range(n)}) == n
            and len({t[c] - c for c in range(n)}) == n)


def main() -> None:
    ap = argparse.ArgumentParser(description="Min-çatışma ile N-vezir")
    ap.add_argument("--n", type=int, default=None, help="tek bir n dene")
    args = ap.parse_args()
    boyutlar = [args.n] if args.n else [8, 100, 1_000, 5_000]

    print(f"{'n':>8}{'açgözlü başlangıç: adım':>26}{'rastgele başlangıç: adım':>27}{'süre (sn)':>11}")
    for n in boyutlar:
        t0 = time.perf_counter()
        adimlar = []
        for tohum in range(5):
            tahta, adim = min_catisma(n, tohum)
            assert tahta is not None and dogru_mu(tahta)
            adimlar.append(adim)
        rast = [min_catisma(n, tohum, acgozlu=False)[1] for tohum in range(3)] if n <= 1000 else None
        sure = time.perf_counter() - t0
        rast_metin = f"{sum(rast) / len(rast):,.0f}" if rast else "—"
        print(f"{n:>8,}{sum(adimlar) / len(adimlar):>26,.1f}{rast_metin:>27}{sure:>11.1f}")
    print("\nAçgözlü başlangıçla onarım adımı sayısı n büyüse de küçük kalır (kitap: bir milyon"
          "\nvezirde ortalama ~50). Zamanın çoğu başlangıcı kurmaya gider. Rastgele başlangıçta ise"
          "\nçatışma sayısı n ile orantılı olduğu için adım sayısı da n ile birlikte büyür.")


if __name__ == "__main__":
    main()
