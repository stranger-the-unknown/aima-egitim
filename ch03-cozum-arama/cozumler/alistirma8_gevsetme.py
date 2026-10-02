#!/usr/bin/env python3
"""Alıştırma 8 çözümü: "komşu olma" koşulu atılmış 8-bulmaca sezgiseli.

Gevşetilmiş kural: Bir taş, hedef kare BOŞ ise herhangi bir kareden oraya geçebilir.
Bu problemin optimal çözümü, "boşluğu bir değiş-tokuş aracı gibi kullanarak"
permütasyonu sıralamaktır:

    boşluk hedefteki kendi yerinde değilse → orada olması gereken taşı boşluğa taşı
    boşluk yerindeyse ama iş bitmediyse    → yanlış yerdeki herhangi bir taşı boşluğa taşı

Bu sezgisel literatürde Gaschnig sezgiseli olarak bilinir.
"""
from __future__ import annotations

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ornekler"))

from sekiz_bulmaca import HEDEF, KITAP_BASLANGIC, SekizBulmaca, rastgele_bulmaca  # noqa: E402


def h_gevsek(durum, hedef=HEDEF) -> int:
    d = list(durum)
    hedef_yer = {tas: i for i, tas in enumerate(hedef)}
    hamle = 0
    while d != list(hedef):
        bos = d.index(0)
        if bos != hedef_yer[0]:
            # Boşluğun şu anki yerinde olması gereken taşı bul ve boşluğa taşı
            gereken = hedef[bos]
            j = d.index(gereken)
        else:
            # Boşluk yerinde: yanlış yerdeki ilk taşı boşluğa taşı
            j = next(i for i, t in enumerate(d) if t != 0 and t != hedef[i])
        d[bos], d[j] = d[j], d[bos]
        hamle += 1
    return hamle


def main() -> None:
    p = SekizBulmaca(KITAP_BASLANGIC)
    s = KITAP_BASLANGIC
    print("Kitap örneği: 7 2 4 / 5 _ 6 / 8 3 1")
    print(f"  h1 = {p.h1(s)},  h_gevşek = {h_gevsek(s)},  h2 = {p.h2(s)},  gerçek = 26\n")

    rng = random.Random(0)
    h1_bask = hg_ustun = h2_ustun = 0
    ornek = None
    n = 2000
    for _ in range(n):
        s = rastgele_bulmaca(rng.randint(5, 60), rng)
        hg, h1, h2 = h_gevsek(s), p.h1(s), p.h2(s)
        h1_bask += hg >= h1
        h2_ustun += h2 > hg
        if hg > h2:
            hg_ustun += 1
            ornek = ornek or s
    print(f"{n} rastgele durumda:")
    print(f"  h_gevşek ≥ h1 : {h1_bask}/{n}  → h1'i baskılar (her yanlış taş en az bir kez taşınır)")
    print(f"  h2 > h_gevşek : {h2_ustun}/{n}")
    print(f"  h_gevşek > h2 : {hg_ustun}/{n}  (ör. {ornek}: h_gevşek = {h_gevsek(ornek)}, h2 = {p.h2(ornek)})")
    print("  → İki sezgisel birbirini baskılamaz; çoğu durumda h2 daha bilgilendiricidir.")
    print("\nİkisi de kabul edilebilir olduğu için max(h2, h_gevşek) de kabul edilebilir ve ikisini de baskılar.")


if __name__ == "__main__":
    main()
