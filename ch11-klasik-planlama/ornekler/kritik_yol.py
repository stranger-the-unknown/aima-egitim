#!/usr/bin/env python3
"""Zaman, çizelgeler ve kaynaklar: kitaptaki iki arabalık montaj problemi.

İki iş, her biri [MotorTak, TekerTak, Denetle] sırasıyla:
    Araba 1: MotorTak1 30 dk, TekerTak1 30 dk, Denetle1 10 dk
    Araba 2: MotorTak2 60 dk, TekerTak2 15 dk, Denetle2 10 dk
Kaynaklar: 1 motor vinci, 1 teker istasyonu, 2 denetçi.

Kitaptaki sonuçlar (testlerle doğrulanır):
  * Kaynak kısıtı yokken kritik yol yöntemi (CPM): toplam 85 dk.
    [ES, LS] değerleri: MotorTak1 [0,15], TekerTak1 [30,45], Denetle1 [60,75],
    MotorTak2 [0,0], TekerTak2 [60,60], Denetle2 [75,75]. Üstteki işin bolluğu 15 dk.
  * Kaynak kısıtlarıyla en kısa çizelge 115 dk (30 dk daha uzun).

    ES(Başla) = 0,   ES(B) = max_{A≺B} ES(A) + Süre(A)
    LS(Bitir) = ES(Bitir),   LS(A) = min_{B≻A} LS(B) − Süre(A)

Çalıştırma:
    python kritik_yol.py
"""
from __future__ import annotations

from itertools import permutations, product

SURE = {"MotorTak1": 30, "TekerTak1": 30, "Denetle1": 10,
        "MotorTak2": 60, "TekerTak2": 15, "Denetle2": 10}
ONCELIK = [("MotorTak1", "TekerTak1"), ("TekerTak1", "Denetle1"),
           ("MotorTak2", "TekerTak2"), ("TekerTak2", "Denetle2")]
KAYNAK = {"MotorTak1": "vinç", "MotorTak2": "vinç", "TekerTak1": "istasyon", "TekerTak2": "istasyon",
          "Denetle1": "denetçi", "Denetle2": "denetçi"}
KAPASITE = {"vinç": 1, "istasyon": 1, "denetçi": 2}


def kritik_yol(sure=SURE, oncelik=ONCELIK) -> tuple[dict, dict, int]:
    """Döner: (ES, LS, toplam süre). Eylemler topolojik sırada işlenir."""
    onceki = {a: [x for x, y in oncelik if y == a] for a in sure}
    sonraki = {a: [y for x, y in oncelik if x == a] for a in sure}
    ES: dict[str, int] = {}
    while len(ES) < len(sure):
        onceki_sayi = len(ES)
        for a in sure:
            if a not in ES and all(p in ES for p in onceki[a]):
                ES[a] = max((ES[p] + sure[p] for p in onceki[a]), default=0)
        if len(ES) == onceki_sayi:
            raise ValueError("Öncelik kısıtlarında döngü var")
    bitis = max(ES[a] + sure[a] for a in sure)
    LS: dict[str, int] = {}
    while len(LS) < len(sure):
        for a in sure:
            if a not in LS and all(s in LS for s in sonraki[a]):
                LS[a] = min((LS[s] for s in sonraki[a]), default=bitis) - sure[a]
    return ES, LS, bitis


def kaynakli_cizelge(sure=SURE, oncelik=ONCELIK, kaynak=KAYNAK, kapasite=KAPASITE) -> tuple[int, dict]:
    """Kapasitesi 1 olan her kaynağın kullanıcılarını olası tüm sıralarla dene (kim önce?).
    Kaynak kısıtları "A önce mi B önce mi?" ayrılmaları getirir; bu problemi NP-zor yapar.
    Kapasitesi kullanıcı sayısına yeten kaynaklar kısıt getirmez."""
    secenekler = []
    for k, kap in kapasite.items():
        kullananlar = [a for a in sure if kaynak.get(a) == k]
        if len(kullananlar) <= kap:
            continue
        if kap != 1:
            raise NotImplementedError("Yalnızca kapasitesi 1 olan kaynaklar sıralanır")
        secenekler.append([list(zip(sira, sira[1:])) for sira in permutations(kullananlar)])
    en_iyi = (float("inf"), None)
    for secim in product(*secenekler):
        ek = list(oncelik) + [kisit for sira in secim for kisit in sira]  # aynı kaynak: sırayla
        ES, _, bitis = kritik_yol(sure, ek)
        if bitis < en_iyi[0]:
            en_iyi = (bitis, ES)
    return en_iyi


def zaman_cizelgesi(ES: dict, sure=SURE, olcek: int = 5) -> str:
    satirlar = []
    for a in sure:
        bas = ES[a] // olcek
        uzun = sure[a] // olcek
        satirlar.append(f"  {a:<10} {' ' * bas}{'█' * max(1, uzun)}  [{ES[a]}–{ES[a] + sure[a]}]")
    return "\n".join(satirlar)


def main() -> None:
    ES, LS, bitis = kritik_yol()
    print("=== Kritik yol yöntemi (kaynak kısıtı yok) ===")
    print(f"  {'eylem':<10} {'süre':>5} {'[ES, LS]':>10} {'bolluk':>7}")
    for a in SURE:
        print(f"  {a:<10} {SURE[a]:>5} {f'[{ES[a]}, {LS[a]}]':>10} {LS[a] - ES[a]:>7}{'   ← kritik' if LS[a] == ES[a] else ''}")
    print(f"  Toplam süre: {bitis} dk (kitap: 85)")
    print(zaman_cizelgesi(ES))

    sure, ES2 = kaynakli_cizelge()
    print(f"\n=== Kaynak kısıtlarıyla (1 vinç, 1 istasyon) en kısa çizelge: {sure} dk (kitap: 115) ===")
    print(zaman_cizelgesi(ES2))
    print("  İki motor aynı vinci kullandığı için üst üste binemez. Kısa işi (MotorTak1) önce yapmak"
          "\n  en iyisidir. İki denetim hiçbir anda çakışmıyor: ikinci denetçiye aslında gerek yok.")


if __name__ == "__main__":
    main()
