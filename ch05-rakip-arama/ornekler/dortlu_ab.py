#!/usr/bin/env python3
"""Sezgisel alfa-beta: Dört-Bir-Arada (Connect Four, 6 × 7).

Oyun ağacı XOX'tan çok büyük (≈ 4,5 × 10¹² durum); sonuna kadar aranamaz.
Kitaptaki "sezgisel alfa-beta" bileşenleri:

  * KESME TESTİ     : belirli bir derinlikte dur.
  * DEĞERLENDİRME   : durumu sayıya çevir. Burada ağırlıklı doğrusal bir fonksiyon:
                      her 4'lü pencerede yalnızca bir oyuncunun taşları varsa
                      1 taş → 1, 2 taş → 10, 3 taş → 100 puan; ayrıca orta sütun bonusu.
  * HAMLE SIRALAMASI: önce ortadaki sütunları dene (genelde daha iyi).
  * TRANSPOZİSYON TABLOSU: aynı duruma farklı hamle sırasıyla gelinirse tekrar arama.

Çalıştırma:
    python dortlu_ab.py                 # düğüm sayısı karşılaştırması + ajan maçları
    python dortlu_ab.py --oyna          # bilgisayara karşı oyna (sen X'sin)
"""
from __future__ import annotations

import argparse
import math
import random

SATIR, SUTUN = 6, 7
BOS, X, O = ".", "X", "O"
MERKEZ_SIRA = [3, 2, 4, 1, 5, 0, 6]
KAZANC = 1_000_000

# Dört taşlık tüm pencereler (69 tane): (satır, sütun) listeleri
PENCERELER = []
for r in range(SATIR):
    for c in range(SUTUN):
        for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
            hucreler = [(r + i * dr, c + i * dc) for i in range(4)]
            if all(0 <= rr < SATIR and 0 <= cc < SUTUN for rr, cc in hucreler):
                PENCERELER.append(hucreler)


class Tahta:
    def __init__(self) -> None:
        self.h = [[BOS] * SUTUN for _ in range(SATIR)]  # satır 0 = en alt

    def kopya(self) -> "Tahta":
        t = Tahta()
        t.h = [r[:] for r in self.h]
        return t

    def gecerli(self) -> list[int]:
        return [c for c in range(SUTUN) if self.h[SATIR - 1][c] == BOS]

    def oyna(self, c: int, oyuncu: str) -> "Tahta":
        t = self.kopya()
        for r in range(SATIR):
            if t.h[r][c] == BOS:
                t.h[r][c] = oyuncu
                return t
        raise ValueError("sütun dolu")

    def kazanan(self) -> str | None:
        for p in PENCERELER:
            a = self.h[p[0][0]][p[0][1]]
            if a != BOS and all(self.h[r][c] == a for r, c in p[1:]):
                return a
        return None

    def anahtar(self) -> str:
        return "".join("".join(r) for r in self.h)

    def __str__(self) -> str:
        satirlar = ["  " + " ".join(self.h[r]) for r in reversed(range(SATIR))]
        return "\n".join(satirlar + ["  " + " ".join(map(str, range(SUTUN)))])


def degerlendir(t: Tahta, oyuncu: str) -> int:
    """Ağırlıklı doğrusal değerlendirme, `oyuncu` açısından."""
    puan_tablosu = {1: 1, 2: 10, 3: 100}
    rakip = O if oyuncu == X else X
    puan = 0
    for p in PENCERELER:
        degerler = [t.h[r][c] for r, c in p]
        benim, onun = degerler.count(oyuncu), degerler.count(rakip)
        if benim and not onun:
            puan += puan_tablosu.get(benim, 0)
        elif onun and not benim:
            puan -= puan_tablosu.get(onun, 0)
    merkez = [t.h[r][3] for r in range(SATIR)]
    puan += 3 * (merkez.count(oyuncu) - merkez.count(rakip))
    return puan


class Arama:
    """Derinlik sınırlı alfa-beta (negamax biçiminde) + isteğe bağlı sıralama ve TT."""

    def __init__(self, siralama: bool = True, tt: bool = True, degerlendirme=None) -> None:
        self.degerlendirme = degerlendirme or degerlendir
        self.siralama = siralama
        self.tt_acik = tt
        self.tt: dict = {}
        self.dugum = 0

    def negamax(self, t: Tahta, derinlik: int, alfa: float, beta: float, oyuncu: str) -> float:
        self.dugum += 1
        rakip = O if oyuncu == X else X
        k = t.kazanan()
        if k is not None:  # önceki hamle kazandırdı: sıra kimdeyse kaybetmiştir
            return -(KAZANC + derinlik)  # erken kaybı daha kötü say
        hamleler = t.gecerli()
        if not hamleler:
            return 0
        if derinlik == 0:  # KESME TESTİ
            return self.degerlendirme(t, oyuncu)
        anahtar = (t.anahtar(), oyuncu, derinlik)
        alfa0 = alfa
        if self.tt_acik and anahtar in self.tt:
            v, bayrak = self.tt[anahtar]
            if bayrak == "kesin":
                return v
            if bayrak == "alt":      # gerçek değer ≥ v
                alfa = max(alfa, v)
            else:                    # "üst": gerçek değer ≤ v
                beta = min(beta, v)
            if alfa >= beta:
                return v
        sira = [c for c in MERKEZ_SIRA if c in hamleler] if self.siralama else hamleler
        en_iyi = -math.inf
        for c in sira:
            v = -self.negamax(t.oyna(c, oyuncu), derinlik - 1, -beta, -alfa, rakip)
            en_iyi = max(en_iyi, v)
            alfa = max(alfa, v)
            if alfa >= beta:
                break  # budama
        if self.tt_acik:
            # Budama olduysa değer yalnızca bir SINIRDIR; bunu da not ederek sakla.
            if en_iyi <= alfa0:
                bayrak = "üst"
            elif en_iyi >= beta:
                bayrak = "alt"
            else:
                bayrak = "kesin"
            self.tt[anahtar] = (en_iyi, bayrak)
        return en_iyi

    def en_iyi_hamle(self, t: Tahta, oyuncu: str, derinlik: int) -> int:
        rakip = O if oyuncu == X else X
        hamleler = t.gecerli()
        sira = [c for c in MERKEZ_SIRA if c in hamleler] if self.siralama else hamleler
        en_iyi_c, en_iyi_v = sira[0], -math.inf
        for c in sira:
            v = -self.negamax(t.oyna(c, oyuncu), derinlik - 1, -math.inf, -en_iyi_v, rakip)
            if v > en_iyi_v:
                en_iyi_c, en_iyi_v = c, v
        return en_iyi_c


def mac(x_derinlik: int | None, o_derinlik: int | None, rng: random.Random) -> str:
    """None = rastgele oyuncu. Kazananı ('X', 'O') ya da 'berabere' döndür."""
    t, sira = Tahta(), X
    while t.kazanan() is None and t.gecerli():
        d = x_derinlik if sira == X else o_derinlik
        c = rng.choice(t.gecerli()) if d is None else Arama().en_iyi_hamle(t, sira, d)
        t = t.oyna(c, sira)
        sira = O if sira == X else X
    return t.kazanan() or "berabere"


def dugum_karsilastirmasi(derinlikler=(2, 4, 6, 8)) -> list[tuple[int, int, int, int]]:
    """Başlangıç konumundan: (derinlik, düz, +sıralama, +sıralama+TT) düğüm sayıları."""
    satirlar = []
    t = Tahta()
    for d in derinlikler:
        sayilar = []
        for sir, tt in ((False, False), (True, False), (True, True)):
            a = Arama(sir, tt)
            a.en_iyi_hamle(t, X, d)
            sayilar.append(a.dugum)
        satirlar.append((d, *sayilar))
    return satirlar


def oyna_insan(derinlik: int) -> None:
    t, sira = Tahta(), X
    ai = Arama()
    while t.kazanan() is None and t.gecerli():
        print(t)
        if sira == X:
            try:
                c = int(input(f"Sütun seç {t.gecerli()}: "))
            except (ValueError, EOFError):
                return
            if c not in t.gecerli():
                continue
        else:
            c = ai.en_iyi_hamle(t, O, derinlik)
            print(f"Bilgisayar: {c}")
        t = t.oyna(c, sira)
        sira = O if sira == X else X
    print(t)
    print(f"Sonuç: {t.kazanan() or 'berabere'}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Dört-Bir-Arada, sezgisel alfa-beta")
    ap.add_argument("--oyna", action="store_true")
    ap.add_argument("--derinlik", type=int, default=5)
    args = ap.parse_args()
    if args.oyna:
        oyna_insan(args.derinlik)
        return

    print("Boş tahtadan ilk hamle için üretilen düğüm sayısı:")
    print(f"{'derinlik':>9}{'düz alfa-beta':>15}{'+ sıralama':>12}{'+ sıralama + TT':>18}")
    for d, duz, sir, tt in dugum_karsilastirmasi():
        print(f"{d:>9}{duz:>15,}{sir:>12,}{tt:>18,}")

    rng = random.Random(0)
    print("\nMaçlar (5'er oyun, X başlar):")
    for x_d, o_d, ad in [(4, None, "derinlik 4 — rastgele"), (4, 1, "derinlik 4 — derinlik 1"),
                         (1, 4, "derinlik 1 — derinlik 4")]:
        s = [mac(x_d, o_d, rng) for _ in range(5)]
        print(f"  X {ad:<26} → X: {s.count('X')}, O: {s.count('O')}, berabere: {s.count('berabere')}")
    print("\nDaha derine bakan ajan genelde kazanır. Ama değerlendirme fonksiyonu kusurlu olduğu"
          "\niçin 'ufuk etkisi' ile kaçınılmaz bir tehdidi kesme derinliğinin ötesine itebilir.")


if __name__ == "__main__":
    main()
