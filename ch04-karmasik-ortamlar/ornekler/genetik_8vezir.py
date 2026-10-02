#!/usr/bin/env python3
"""Genetik algoritma ile 8-vezir.

Birey: 8 haneli rakam dizisi, "24748552" gibi. i. hane, i. sütundaki vezirin
satırıdır (1–8). Uygunluk: birbirini tehdit **etmeyen** vezir çifti sayısı
(en fazla 8·7/2 = 28; 28 = çözüm).

Kitaptaki örnek popülasyonun uygunlukları (testlerle doğrulanır):
    24748552 → 24, 32752411 → 23, 24415124 → 20, 32543213 → 11
Seçilme olasılıkları uygunlukla orantılıdır: 24/78 ≈ %31, 23/78 ≈ %29, …
Örnek çaprazlama (kesim noktası 3): 327|52411 × 247|48552 → 32748552

Çalıştırma:
    python genetik_8vezir.py
    python genetik_8vezir.py --secim turnuva --tohum 3
"""
from __future__ import annotations

import argparse
import random

N = 8
EN_IYI = N * (N - 1) // 2  # 28

KITAP_POPULASYON = ["24748552", "32752411", "24415124", "32543213"]


def uygunluk(birey: str) -> int:
    """Birbirini tehdit etmeyen vezir çiftleri."""
    q = [int(c) for c in birey]
    saldiri = sum(
        1 for i in range(N) for j in range(i + 1, N)
        if q[i] == q[j] or abs(q[i] - q[j]) == j - i
    )
    return EN_IYI - saldiri


def caprazla(x: str, y: str, kesim: int) -> str:
    """Tek noktalı çaprazlama: x'in ilk `kesim` hanesi + y'nin geri kalanı."""
    return x[:kesim] + y[kesim:]


def mutasyon(birey: str, rng: random.Random) -> str:
    i = rng.randrange(N)
    return birey[:i] + str(rng.randint(1, N)) + birey[i + 1:]


def rastgele_birey(rng: random.Random) -> str:
    return "".join(str(rng.randint(1, N)) for _ in range(N))


def secim_orantili(pop: list[str], puan: list[int], rng: random.Random) -> tuple[str, str]:
    """Kitaptaki gibi: seçilme olasılığı uygunlukla orantılı (rulet tekerleği)."""
    return tuple(rng.choices(pop, weights=puan, k=2))


def secim_turnuva(pop: list[str], puan: list[int], rng: random.Random, k: int = 3) -> tuple[str, str]:
    """Rastgele k birey seç, en iyisini al (iki kez). Seçim baskısı daha güçlü."""
    return tuple(pop[max(rng.sample(range(len(pop)), k), key=puan.__getitem__)] for _ in range(2))


def genetik_algoritma(pop_boyu: int = 100, mutasyon_olasiligi: float = 0.6,
                      nesil_siniri: int = 1000, secim: str = "orantili",
                      elit: int = 2, tohum: int = 0) -> tuple[str, int, list[float]]:
    """Döner: (en iyi birey, bulunduğu nesil, nesil başına ortalama uygunluk)."""
    rng = random.Random(tohum)
    sec = secim_orantili if secim == "orantili" else secim_turnuva
    pop = [rastgele_birey(rng) for _ in range(pop_boyu)]
    gecmis = []
    for nesil in range(nesil_siniri):
        puan = [uygunluk(b) for b in pop]  # her nesilde bir kez hesapla
        gecmis.append(sum(puan) / pop_boyu)
        sirali = sorted(range(pop_boyu), key=puan.__getitem__, reverse=True)
        if puan[sirali[0]] == EN_IYI:
            return pop[sirali[0]], nesil, gecmis
        yeni = [pop[i] for i in sirali[:elit]]  # elitizm: en iyiler olduğu gibi aktarılır
        while len(yeni) < pop_boyu:
            x, y = sec(pop, puan, rng)
            cocuk = caprazla(x, y, rng.randint(1, N - 1))
            if rng.random() < mutasyon_olasiligi:
                cocuk = mutasyon(cocuk, rng)
            yeni.append(cocuk)
        pop = yeni
    en_iyi = max(pop, key=uygunluk)
    return en_iyi, nesil_siniri, gecmis


def tahta(birey: str) -> str:
    satirlar = []
    for r in range(N, 0, -1):
        satirlar.append("  " + " ".join("♛" if int(birey[c]) == r else "·" for c in range(N)))
    return "\n".join(satirlar)


def main() -> None:
    ap = argparse.ArgumentParser(description="Genetik algoritma ile 8-vezir")
    ap.add_argument("--pop", type=int, default=100)
    ap.add_argument("--mutasyon", type=float, default=0.6)
    ap.add_argument("--secim", choices=["orantili", "turnuva"], default="orantili")
    ap.add_argument("--tohum", type=int, default=1)
    args = ap.parse_args()

    print("Kitaptaki başlangıç popülasyonu:")
    toplam = sum(map(uygunluk, KITAP_POPULASYON))
    for b in KITAP_POPULASYON:
        print(f"  {b}  uygunluk = {uygunluk(b):2d}   seçilme olasılığı = {uygunluk(b) / toplam:.0%}")
    c = caprazla("32752411", "24748552", 3)
    print(f"\nÇaprazlama (kesim 3): 327|52411 × 247|48552 → {c}  (uygunluk {uygunluk(c)})\n")

    birey, nesil, gecmis = genetik_algoritma(args.pop, args.mutasyon, secim=args.secim, tohum=args.tohum)
    durum = "çözüm bulundu" if uygunluk(birey) == EN_IYI else "nesil sınırına ulaşıldı"
    print(f"GA ({args.secim} seçim, popülasyon {args.pop}, mutasyon {args.mutasyon}): "
          f"{nesil}. nesilde {durum}")
    adimlar = sorted({0, len(gecmis) // 4, len(gecmis) // 2, len(gecmis) - 1})
    print("  ortalama uygunluk: " + ", ".join(f"n{i}: {gecmis[i]:.1f}" for i in adimlar))
    print(f"\nEn iyi birey: {birey}  (uygunluk {uygunluk(birey)}/{EN_IYI})")
    print(tahta(birey))
    print("\nNotlar:"
          "\n • Orantılı seçimde uygunluklar birbirine yakın (ör. 20 ile 24) olduğu için seçim"
          "\n   baskısı zayıftır. --secim turnuva ile karşılaştır."
          "\n • GA stokastiktir: bazı tohumlarda nesil sınırı içinde çözüm bulamaz. Popülasyon"
          "\n   çeşitliliğini kaybedip 'erken yakınsama' yaşar; mutasyon bunu dengeler."
          "\n • 8-vezir için aslında tepe tırmanma + yeniden başlatma çok daha hızlıdır. GA'nın"
          "\n   gücü, iyi 'yapı taşlarının' çaprazlamayla birleşebildiği problemlerde ortaya çıkar.")


if __name__ == "__main__":
    main()
