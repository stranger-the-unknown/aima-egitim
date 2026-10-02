#!/usr/bin/env python3
"""Kriptaritmetik: TWO + TWO = FOUR (kitaptaki örnek).

Her harf farklı bir rakam; baştaki harfler (T, F) sıfır olamaz. Kısıtlar ikili değil:
  * Alldiff(F, T, U, W, R, O)                    — küresel kısıt
  * O + O = R + 10·C1                             — birler basamağı
  * C1 + W + W = U + 10·C2                        — onlar
  * C2 + T + T = O + 10·C3                        — yüzler
  * C3 = F                                        — binler
C1, C2, C3 elde (taşıma) değişkenleridir. Bu yapı kitaptaki "kısıt hiper grafiği"dir.

Arama, sütunları sağdan sola doldurur ve her sütunu dolar dolmaz kontrol eder.
Böylece kısıtlar, bütün harfler atanmayı beklemeden erken budama yapar.

Çalıştırma:
    python kriptaritmetik.py
    python kriptaritmetik.py --bulmaca "SEND+MORE=MONEY"
"""
from __future__ import annotations

import argparse
from itertools import permutations


def ayristir(bulmaca: str) -> tuple[list[str], str]:
    sol, sag = bulmaca.replace(" ", "").upper().split("=")
    return sol.split("+"), sag


def coz(bulmaca: str, tumu: bool = True) -> tuple[list[dict], int]:
    """Sütun sütun geri izleme. Döner: (çözümler, denenen kısmi atama sayısı)."""
    terimler, toplam = ayristir(bulmaca)
    uzunluk = len(toplam)
    sutunlar = []  # her sütun: (terimlerdeki harfler, sonuç harfi)
    for i in range(1, uzunluk + 1):
        sutunlar.append(([t[-i] for t in terimler if len(t) >= i], toplam[-i]))
    bas_harfler = {t[0] for t in terimler + [toplam]}
    cozumler: list[dict] = []
    sayac = 0

    def ata(harfler, atama, kullanilan):
        """Verilen harflere, henüz atanmamışsa farklı rakamlar ver (üreteç)."""
        yeni = [h for h in dict.fromkeys(harfler) if h not in atama]
        bos = [d for d in range(10) if d not in kullanilan]
        for rakamlar in permutations(bos, len(yeni)):
            if any(h in bas_harfler and d == 0 for h, d in zip(yeni, rakamlar)):
                continue
            yield dict(zip(yeni, rakamlar))

    def ara(i: int, elde: int, atama: dict) -> bool:
        nonlocal sayac
        if i == uzunluk:
            if elde == 0:
                cozumler.append(dict(atama))
                return not tumu
            return False
        harfler, sonuc_harfi = sutunlar[i]
        for ek in ata(harfler + [sonuc_harfi], atama, set(atama.values())):
            sayac += 1
            a = {**atama, **ek}
            s = elde + sum(a[h] for h in harfler)
            if s % 10 == a[sonuc_harfi] and ara(i + 1, s // 10, a):
                return True
        return False

    ara(0, 0, {})
    return cozumler, sayac


def kaba_kuvvet(bulmaca: str) -> list[dict]:
    """Doğrulama için: tüm rakam permütasyonlarını dene."""
    terimler, toplam = ayristir(bulmaca)
    harfler = sorted(set("".join(terimler) + toplam))
    bas = {t[0] for t in terimler + [toplam]}
    sonuc = []
    for rakamlar in permutations(range(10), len(harfler)):
        a = dict(zip(harfler, rakamlar))
        if any(a[h] == 0 for h in bas):
            continue
        sayi = lambda k: int("".join(str(a[h]) for h in k))  # noqa: E731
        if sum(map(sayi, terimler)) == sayi(toplam):
            sonuc.append(a)
    return sonuc


def goster(bulmaca: str, a: dict) -> str:
    terimler, toplam = ayristir(bulmaca)
    sayi = lambda k: "".join(str(a[h]) for h in k)  # noqa: E731
    return " + ".join(map(sayi, terimler)) + " = " + sayi(toplam)


def main() -> None:
    ap = argparse.ArgumentParser(description="Kriptaritmetik CSP")
    ap.add_argument("--bulmaca", default="TWO+TWO=FOUR")
    args = ap.parse_args()
    cozumler, sayac = coz(args.bulmaca)
    print(f"{args.bulmaca}: {len(cozumler)} çözüm ({sayac:,} kısmi atama denendi)")
    for a in cozumler:
        print(f"  {goster(args.bulmaca, a)}")
    harf_sayisi = len(set(args.bulmaca.replace('+', '').replace('=', '')))
    tam = 1
    for k in range(harf_sayisi):
        tam *= 10 - k
    print(f"\nKarşılaştırma: kaba kuvvet {tam:,} permütasyonu tek tek dener.")


if __name__ == "__main__":
    main()
