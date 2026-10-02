#!/usr/bin/env python3
"""N-vezir üzerinde tepe tırmanma: kitaptaki deneyi yeniden üretmek.

Durum: her sütunda bir vezir; tahta[c] = c. sütundaki vezirin satırı.
h = birbirini tehdit eden vezir çifti sayısı (0 = çözüm). Amaç h'yi küçültmek.

Algoritma: **en dik tırmanış** (steepest ascent). 8 × 7 = 56 komşunun hepsine bakılır;
en iyisine gidilir (eşitlik varsa rastgele biri). İyileşme yoksa durulur.
İsteğe bağlı **yana hamle**: En iyi komşu eşit değerdeyse, art arda en fazla
`yana_sinir` kez yine de hareket edilir (düzlükten çıkmayı ummak için).

Kitaptaki sonuçlar (8-vezir, rastgele başlangıç):
    yana hamle yok     → %14 başarı; başarıda ~4, takılmada ~3 adım
    100 yana hamleye kadar → %94 başarı; başarıda ~21, takılmada ~64 adım
Rastgele yeniden başlatma: beklenen deneme sayısı 1/p (yana hamle yoksa ~7).

Çalıştırma:
    python tepe_tirmanma_n_queens.py                    # tek koşu
    python tepe_tirmanma_n_queens.py --yeniden-baslat 30
    python tepe_tirmanma_n_queens.py --deney 1000       # kitaptaki istatistikler
"""
from __future__ import annotations

import argparse
import random
from dataclasses import dataclass


def saldiri_sayisi(tahta: list[int]) -> int:
    """Aynı satırda veya aynı çaprazda olan vezir çiftlerini say."""
    n = len(tahta)
    return sum(
        1
        for c1 in range(n)
        for c2 in range(c1 + 1, n)
        if tahta[c1] == tahta[c2] or abs(tahta[c1] - tahta[c2]) == c2 - c1
    )


def rastgele_tahta(n: int, rng: random.Random) -> list[int]:
    return [rng.randrange(n) for _ in range(n)]


def komsu_degerleri(tahta: list[int]) -> dict[tuple[int, int], int]:
    """Her (sütun, yeni satır) hamlesi için komşunun h değeri.

    Verimli hesap: Bir veziri taşımak yalnızca o vezirin yaptığı saldırıları
    değiştirir. h_yeni = h − çatışma(c, eski satır) + çatışma(c, yeni satır).
    """
    n = len(tahta)
    h = saldiri_sayisi(tahta)
    sonuc = {}
    for c in range(n):
        def catisma(satir: int) -> int:
            return sum(
                1 for c2 in range(n)
                if c2 != c and (tahta[c2] == satir or abs(tahta[c2] - satir) == abs(c2 - c))
            )
        eski = catisma(tahta[c])
        for satir in range(n):
            if satir != tahta[c]:
                sonuc[(c, satir)] = h - eski + catisma(satir)
    return sonuc


@dataclass
class Kosu:
    tahta: list[int]
    h: int
    adim: int

    @property
    def basarili(self) -> bool:
        return self.h == 0


def tepe_tirmanma(n: int, rng: random.Random, yana_sinir: int = 0, max_adim: int = 1000) -> Kosu:
    """En dik tırmanış (h'yi en çok azaltan komşu), isteğe bağlı yana hamle."""
    tahta = rastgele_tahta(n, rng)
    h = saldiri_sayisi(tahta)
    yana = 0
    for adim in range(max_adim):
        if h == 0:
            return Kosu(tahta, 0, adim)
        degerler = komsu_degerleri(tahta)
        en_iyi = min(degerler.values())
        if en_iyi > h or (en_iyi == h and yana >= yana_sinir):
            return Kosu(tahta, h, adim)  # yerel minimum ya da düzlük
        yana = yana + 1 if en_iyi == h else 0
        c, satir = rng.choice([k for k, v in degerler.items() if v == en_iyi])
        tahta = tahta.copy()
        tahta[c] = satir
        h = en_iyi
    return Kosu(tahta, h, max_adim)


def rastgele_yeniden_baslat(n: int, rng: random.Random, yana_sinir: int = 0,
                            en_fazla: int = 1000) -> tuple[Kosu, int, int]:
    """Başarılı olana kadar yeniden başlat. Döner: (son koşu, deneme sayısı, toplam adım)."""
    toplam = 0
    for deneme in range(1, en_fazla + 1):
        k = tepe_tirmanma(n, rng, yana_sinir)
        toplam += k.adim
        if k.basarili:
            return k, deneme, toplam
    return k, en_fazla, toplam


def deney(tekrar: int, yana_sinir: int, tohum: int = 0, n: int = 8) -> dict[str, float]:
    """Kitaptaki istatistikleri hesapla: başarı oranı ve ortalama adım sayıları."""
    rng = random.Random(tohum)
    kosular = [tepe_tirmanma(n, rng, yana_sinir) for _ in range(tekrar)]
    basari = [k for k in kosular if k.basarili]
    takilma = [k for k in kosular if not k.basarili]
    ort = lambda ks: sum(k.adim for k in ks) / len(ks) if ks else float("nan")  # noqa: E731
    return {
        "oran": len(basari) / tekrar,
        "adim_basari": ort(basari),
        "adim_takilma": ort(takilma),
    }


def tahta_yazdir(tahta: list[int]) -> None:
    n = len(tahta)
    for r in range(n):
        print("  " + " ".join("♛" if tahta[c] == r else "·" for c in range(n)))


def main() -> None:
    ap = argparse.ArgumentParser(description="N-vezir tepe tırmanma (Bölüm 4)")
    ap.add_argument("-n", type=int, default=8)
    ap.add_argument("--yeniden-baslat", type=int, default=0, metavar="K",
                    help="başarılı olana kadar en fazla K deneme")
    ap.add_argument("--yana", type=int, default=0, help="izin verilen art arda yana hamle (kitap: 100)")
    ap.add_argument("--tohum", type=int, default=1)
    ap.add_argument("--deney", type=int, default=0, metavar="T",
                    help="T rastgele başlangıçla kitaptaki istatistikleri hesapla")
    args = ap.parse_args()
    rng = random.Random(args.tohum)

    if args.deney:
        print(f"8-vezir, {args.deney} rastgele başlangıç (kitap değerleri parantez içinde)\n")
        print(f"{'yana hamle':<12}{'başarı':>10}{'adım (başarı)':>16}{'adım (takılma)':>17}")
        for yana, kitap in [(0, "(%14, ~4, ~3)"), (100, "(%94, ~21, ~64)")]:
            d = deney(args.deney, yana, args.tohum)
            print(f"{yana:<12}{d['oran']:>9.0%}{d['adim_basari']:>16.1f}{d['adim_takilma']:>17.1f}   {kitap}")
        p = deney(args.deney, 0, args.tohum)["oran"]
        print(f"\nYeniden başlatmayla beklenen deneme sayısı ≈ 1/p = 1/{p:.2f} ≈ {1 / p:.1f} (kitap: ~7)")
        return

    print(f"=== {args.n}-vezir tepe tırmanma (yana hamle sınırı: {args.yana}) ===\n")
    if args.yeniden_baslat:
        k, deneme, toplam = rastgele_yeniden_baslat(args.n, rng, args.yana, args.yeniden_baslat)
        print(f"Yeniden başlatma: {deneme}. denemede {'başarılı' if k.basarili else 'başarısız'}, "
              f"toplam {toplam} adım")
    else:
        k = tepe_tirmanma(args.n, rng, args.yana)
        print(f"Tek koşu: {k.adim} adım, son h = {k.h}")
    print()
    tahta_yazdir(k.tahta)
    print(f"\nh = {k.h} → " + ("çözüm bulundu!" if k.basarili else
                               "yerel minimum/düzlük. --yeniden-baslat veya --yana 100 dene."))


if __name__ == "__main__":
    main()
