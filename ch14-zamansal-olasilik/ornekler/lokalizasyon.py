#!/usr/bin/env python3
"""HMM ile robot konumlandırma (kitaptaki 14.3.2'nin özgün bir labirentte uygulaması).

Robot, labirentin boş karelerinde rastgele dolaşıyor: Her adımda komşu boş karelerden birine
eşit olasılıkla geçer. Dört algılayıcısı (K, G, D, B) o yönde engel olup olmadığını söyler;
her bit bağımsız olarak ε olasılıkla yanlıştır:
    P(e_t | X_t = i) = (1 − ε)^(4 − d) · ε^d,   d = gerçek engel bitleriyle uyuşmayan bit sayısı
Başlangıçta konum bilinmiyor: P(X_0 = i) = 1/S.

Kitaptaki gözlemler burada da görülür: ε küçükken robot birkaç adımda yerini bulur; ε = 0.4
gibi çok gürültülü algılayıcılarda kaybolur. Viterbi yolu tüm geçmişi birlikte kestirir.

Çalıştırma:
    python lokalizasyon.py
"""
from __future__ import annotations

import random

from zamansal import HMM

LABIRENT = [
    "..#....#......#.",
    ".##.##...#.##...",
    "....#..#.#....#.",
    "#.#...#....#.#..",
]
YONLER = {"K": (-1, 0), "G": (1, 0), "D": (0, 1), "B": (0, -1)}  # kuzey, güney, doğu, batı


def bos_kareler(labirent=LABIRENT) -> list[tuple[int, int]]:
    return [(r, c) for r, satir in enumerate(labirent) for c, ch in enumerate(satir) if ch == "."]


def komsular(kare, bos: set) -> list[tuple[int, int]]:
    r, c = kare
    return [(r + dr, c + dc) for dr, dc in YONLER.values() if (r + dr, c + dc) in bos]


def engel_bitleri(kare, bos: set) -> tuple[bool, ...]:
    r, c = kare
    return tuple((r + dr, c + dc) not in bos for dr, dc in YONLER.values())


def konum_hmm(epsilon: float, labirent=LABIRENT) -> tuple[HMM, list]:
    kareler = bos_kareler(labirent)
    bos = set(kareler)
    idx = {k: i for i, k in enumerate(kareler)}
    S = len(kareler)
    T = [[0.0] * S for _ in range(S)]
    for k in kareler:
        kom = komsular(k, bos) or [k]
        for n in kom:
            T[idx[k]][idx[n]] = 1 / len(kom)
    bitler = [engel_bitleri(k, bos) for k in kareler]

    def sensor(e):
        sonuc = []
        for b in bitler:
            d = sum(x != y for x, y in zip(b, e))
            sonuc.append((1 - epsilon) ** (4 - d) * epsilon ** d)
        return sonuc

    return HMM(kareler, T, sensor, [1 / S] * S), kareler


def simule_et(epsilon: float, adim: int, rng: random.Random, labirent=LABIRENT):
    kareler = bos_kareler(labirent)
    bos = set(kareler)
    x = rng.choice(kareler)
    yol, gozlemler = [], []
    for _ in range(adim):
        x = rng.choice(komsular(x, bos) or [x])
        gercek = engel_bitleri(x, bos)
        gozlemler.append(tuple(b if rng.random() > epsilon else not b for b in gercek))
        yol.append(x)
    return yol, gozlemler


def manhattan(a, b) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def konum_hatasi(epsilon: float, adim: int, kosu: int, tohum: int = 1) -> tuple[list[float], float]:
    """Her adımda beklenen Manhattan hatası (inanca göre) ve son Viterbi yolunun ortalama hatası."""
    rng = random.Random(tohum)
    h, kareler = konum_hmm(epsilon)
    toplam = [0.0] * adim
    viterbi_toplam = 0.0
    for _ in range(kosu):
        yol, gozlemler = simule_et(epsilon, adim, rng)
        for t, f in enumerate(h.filtrele(gozlemler)):
            toplam[t] += sum(p * manhattan(k, yol[t]) for p, k in zip(f, kareler))
        v, _ = h.viterbi(gozlemler)
        viterbi_toplam += sum(manhattan(a, b) for a, b in zip(v, yol)) / adim
    return [x / kosu for x in toplam], viterbi_toplam / kosu


def main() -> None:
    kareler = bos_kareler()
    print(f"Labirent: {len(kareler)} boş kare")
    for satir in LABIRENT:
        print("   " + satir.replace(".", "·"))

    adim, kosu = 30, 20
    print(f"\n=== Beklenen konum hatası (Manhattan), {kosu} koşunun ortalaması ===")
    print("   ε     t=1    t=5    t=10   t=20   t=30   Viterbi yolu hatası")
    for eps in (0.0, 0.05, 0.1, 0.2, 0.4):
        hata, vit = konum_hatasi(eps, adim, kosu)
        print(f"  {eps:<4}  " + "  ".join(f"{hata[t - 1]:5.2f}" for t in (1, 5, 10, 20, 30)) + f"   {vit:5.2f}")
    print("  ε ≤ 0.1: birkaç adımda robot yerini bulur. ε = 0.2: yavaş ama yine de öğrenir.")
    print("  ε = 0.4: algılayıcı neredeyse yazı-tura kadar bilgisiz; robot kaybolur.")


if __name__ == "__main__":
    main()
