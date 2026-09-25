#!/usr/bin/env python3
"""8-bulmaca (8-puzzle): sezgisel fonksiyonların gücü.

3×3 tahtada 8 numaralı taş ve bir boşluk (0). Eylemler boşluğu hareket ettirir:
Yukarı, Aşağı, Sol, Sağ. Hedef:

    _ 1 2
    3 4 5
    6 7 8

Kitaptaki örnek başlangıç durumu:

    7 2 4
    5 _ 6
    8 3 1

Bu durum için kitaptaki değerler (testlerle doğrulanır):
    h1 (yanlış yerdeki taş sayısı)       = 8
    h2 (Manhattan uzaklıkları toplamı)   = 18
    optimal çözüm uzunluğu               = 26 hamle

Script ayrıca h1 ile h2'yi rastgele bulmacalarda karşılaştırır ve
**etkin dallanma faktörünü** (b*) hesaplar: iyi sezgisel = küçük b*.

Çalıştırma:
    python sekiz_bulmaca.py                 # kitap örneği + küçük karşılaştırma
    python sekiz_bulmaca.py --deneme 30     # karşılaştırmada daha çok bulmaca
"""
from __future__ import annotations

import argparse
import random
import time
from collections import defaultdict

from arama import (Problem, a_yildiz, etkin_dallanma, genislik_oncelikli,
                   ida_yildiz)

HEDEF = (0, 1, 2, 3, 4, 5, 6, 7, 8)
KITAP_BASLANGIC = (7, 2, 4, 5, 0, 6, 8, 3, 1)

# Boşluğun hareketi: indeks değişimi ve geçerlilik koşulu
HAREKETLER = {
    "Yukarı": -3,
    "Aşağı": +3,
    "Sol": -1,
    "Sağ": +1,
}


class SekizBulmaca(Problem):
    """Durum: 9 elemanlı demet; 0 = boşluk. (Ayrışık temsil: her kare bir değişken.)"""

    def __init__(self, baslangic, hedef=HEDEF, sezgisel: str = "h2"):
        super().__init__(baslangic, hedef)
        self.sezgisel = sezgisel
        # Her taşın hedefteki (satır, sütun) konumu
        self._hedef_konum = {tas: divmod(i, 3) for i, tas in enumerate(hedef)}

    def eylemler(self, durum):
        i = durum.index(0)
        satir, sutun = divmod(i, 3)
        if satir > 0:
            yield "Yukarı"
        if satir < 2:
            yield "Aşağı"
        if sutun > 0:
            yield "Sol"
        if sutun < 2:
            yield "Sağ"

    def sonuc(self, durum, eylem):
        i = durum.index(0)
        j = i + HAREKETLER[eylem]
        yeni = list(durum)
        yeni[i], yeni[j] = yeni[j], yeni[i]
        return tuple(yeni)

    # --- Sezgiseller ---------------------------------------------------------
    def h1(self, durum) -> int:
        """Yanlış yerdeki taş sayısı (boşluk sayılmaz)."""
        return sum(1 for i, tas in enumerate(durum) if tas != 0 and tas != self.hedef[i])

    def h2(self, durum) -> int:
        """Her taşın hedef konumuna Manhattan uzaklığı toplamı (boşluk sayılmaz)."""
        toplam = 0
        for i, tas in enumerate(durum):
            if tas == 0:
                continue
            satir, sutun = divmod(i, 3)
            hs, hc = self._hedef_konum[tas]
            toplam += abs(satir - hs) + abs(sutun - hc)
        return toplam

    def h(self, dugum):
        if self.sezgisel == "h1":
            return self.h1(dugum.durum)
        if self.sezgisel == "h2":
            return self.h2(dugum.durum)
        return 0


def cozulebilir_mi(durum, hedef=HEDEF) -> bool:
    """3×3 bulmacada iki durum arasında geçiş, taşların (boşluk hariç) ters
    çevrim sayılarının paritesi aynıysa mümkündür. Durum uzayı bu yüzden
    9!/2 = 181.440 durumluk iki ayrık parçaya bölünür."""

    def ters_cevrim(d):
        t = [x for x in d if x != 0]
        return sum(1 for i in range(len(t)) for j in range(i + 1, len(t)) if t[i] > t[j])

    return ters_cevrim(durum) % 2 == ters_cevrim(hedef) % 2


def tahta(durum) -> str:
    return "\n".join(
        "    " + " ".join("_" if x == 0 else str(x) for x in durum[r * 3:(r + 1) * 3])
        for r in range(3)
    )


def rastgele_bulmaca(adim: int, rng: random.Random) -> tuple:
    """Hedeften başlayıp rastgele yürüyerek (geri adım atmadan) bulmaca üret."""
    p = SekizBulmaca(HEDEF)
    durum, onceki = HEDEF, None
    for _ in range(adim):
        secenekler = [p.sonuc(durum, e) for e in p.eylemler(durum)]
        secenekler = [s for s in secenekler if s != onceki] or secenekler
        onceki, durum = durum, rng.choice(secenekler)
    return durum


def kitap_ornegi() -> None:
    p = SekizBulmaca(KITAP_BASLANGIC)
    print("Kitaptaki başlangıç durumu:")
    print(tahta(KITAP_BASLANGIC))
    print(f"\n  h1 = {p.h1(KITAP_BASLANGIC)}   (kitap: 8)")
    print(f"  h2 = {p.h2(KITAP_BASLANGIC)}  (kitap: 18)")
    print(f"  çözülebilir mi? {cozulebilir_mi(KITAP_BASLANGIC)}\n")

    print(f"{'Algoritma':<12}{'hamle':>7}{'genişletilen':>14}{'üretilen':>11}{'b*':>7}{'süre (sn)':>11}")
    for ad, fonk in [
        ("BFS", lambda: genislik_oncelikli(SekizBulmaca(KITAP_BASLANGIC))),
        ("A* (h1)", lambda: a_yildiz(SekizBulmaca(KITAP_BASLANGIC, sezgisel="h1"))),
        ("A* (h2)", lambda: a_yildiz(SekizBulmaca(KITAP_BASLANGIC, sezgisel="h2"))),
        ("IDA* (h2)", lambda: ida_yildiz(SekizBulmaca(KITAP_BASLANGIC, sezgisel="h2"))),
    ]:
        t0 = time.perf_counter()
        s = fonk()
        sure = time.perf_counter() - t0
        d = len(s.eylemler)
        print(f"{ad:<12}{d:>7}{s.genisletilen:>14,}{s.uretilen:>11,}"
              f"{etkin_dallanma(s.uretilen, d):>7.2f}{sure:>11.2f}")
    print("(b*, kitaptaki gibi *üretilen* düğüm sayısından hesaplanır.)")
    s = a_yildiz(SekizBulmaca(KITAP_BASLANGIC))
    print(f"\nOptimal çözüm ({len(s.eylemler)} hamle, boşluğun hareketi):")
    print("  " + " ".join(e[:2] for e in s.eylemler))


def karsilastirma(deneme: int, tohum: int = 1) -> None:
    """Farklı derinliklerde rastgele bulmacalarda h1 ve h2'yi karşılaştır."""
    rng = random.Random(tohum)
    kayit: dict[int, dict[str, list[int]]] = defaultdict(lambda: {"h1": [], "h2": []})
    for _ in range(deneme):
        baslangic = rastgele_bulmaca(rng.randint(8, 40), rng)
        s2 = a_yildiz(SekizBulmaca(baslangic, sezgisel="h2"))
        d = len(s2.eylemler)
        if d < 2:
            continue
        s1 = a_yildiz(SekizBulmaca(baslangic, sezgisel="h1"))
        assert len(s1.eylemler) == d, "iki sezgisel de kabul edilebilir: aynı optimal uzunluk"
        kayit[d]["h1"].append(s1.uretilen)
        kayit[d]["h2"].append(s2.uretilen)

    print(f"\nRastgele {deneme} bulmacada A*(h1) ve A*(h2): ortalama üretilen düğüm ve b*")
    print(f"{'d':>4}{'adet':>6}{'A*(h1)':>12}{'A*(h2)':>12}{'b*(h1)':>9}{'b*(h2)':>9}")
    for d in sorted(kayit):
        n1 = sum(kayit[d]["h1"]) / len(kayit[d]["h1"])
        n2 = sum(kayit[d]["h2"]) / len(kayit[d]["h2"])
        print(f"{d:>4}{len(kayit[d]['h1']):>6}{n1:>12,.0f}{n2:>12,.0f}"
              f"{etkin_dallanma(round(n1), d):>9.2f}{etkin_dallanma(round(n2), d):>9.2f}")
    print("\nKarşılaştır: kitaptaki deneyde (her d için 100 bulmaca) b* yaklaşık"
          "\nh1 için 1,42–1,50, h2 için 1,27–1,36 çıkıyor.")
    print("\nh2 her durumda h1'den büyük ya da eşittir (h2, h1'i *baskılar*). İkisi de"
          "\ntutarlı olduğu için A*(h2)'nin genişlettiği her düğümü A*(h1) de genişletir"
          "\n(eşit f değerli düğümler hariç). Farkın derinlikle nasıl açıldığına dikkat et.")


def main() -> None:
    ap = argparse.ArgumentParser(description="8-bulmaca: h1 ve h2 sezgiselleri")
    ap.add_argument("--deneme", type=int, default=12, help="karşılaştırmadaki rastgele bulmaca sayısı")
    args = ap.parse_args()
    kitap_ornegi()
    karsilastirma(args.deneme)


if __name__ == "__main__":
    main()
