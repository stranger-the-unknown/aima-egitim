#!/usr/bin/env python3
"""Tekrarlı mahkûm ikilemi (kitaptaki 18.2.3).

* Sabit, sonlu ve herkesçe bilinen 100 tur: geriye tümevarımla her turda tanıklık → 500 yıl.
* Sonsuz tekrar: stratejiler sonlu durum makineleri (Şekil 18.3): ŞAHİN, GÜVERCİN, ACIMASIZ,
  KISASA KISAS. (Şekildeki TAT-FOR-TIT'in ne yaptığını kitap okura soru olarak bırakır.) Fayda: ortalamaların limiti (lim 1/T Σ U_t).
  Kitaptaki değerler: GÜVERCİN–GÜVERCİN −1/−1; ŞAHİN–GÜVERCİN 0/−10; ŞAHİN–ŞAHİN −5/−5;
  ŞAHİN–ACIMASIZ −5/−5; ACIMASIZ–ACIMASIZ −1/−1 (bir Nash dengesi: halk teoremleri).

Çalıştırma:
    python tekrarli_oyunlar.py
"""
from __future__ import annotations

from fractions import Fraction

T, S = "tanık", "sus"
ODUL = {(T, T): (-5, -5), (T, S): (0, -10), (S, T): (-10, 0), (S, S): (-1, -1)}


class Makine:
    """Çıktılı sonlu durum makinesi: durum → eylem; (durum, karşının eylemi) → yeni durum."""

    def __init__(self, ad: str, baslangic, eylem: dict, gecis: dict):
        self.ad, self.baslangic, self.eylem, self.gecis = ad, baslangic, eylem, gecis


SAHIN = Makine("ŞAHİN", "t", {"t": T}, {("t", T): "t", ("t", S): "t"})
GUVERCIN = Makine("GÜVERCİN", "s", {"s": S}, {("s", T): "s", ("s", S): "s"})
ACIMASIZ = Makine("ACIMASIZ", "s", {"s": S, "t": T}, {("s", S): "s", ("s", T): "t", ("t", S): "t", ("t", T): "t"})
KISAS = Makine("KISASA KISAS", "s", {"s": S, "t": T}, {("s", S): "s", ("s", T): "t", ("t", S): "s", ("t", T): "t"})
MAKINELER = [SAHIN, GUVERCIN, ACIMASIZ, KISAS]


def oyna(m1: Makine, m2: Makine) -> tuple[list, list, tuple]:
    """Durum çifti tekrar edene kadar oyna. (tekrarlanmayan önek, döngü, ortalamaların limiti)."""
    d1, d2, gorulen, gecmis = m1.baslangic, m2.baslangic, {}, []
    while (d1, d2) not in gorulen:
        gorulen[(d1, d2)] = len(gecmis)
        a1, a2 = m1.eylem[d1], m2.eylem[d2]
        gecmis.append((a1, a2))
        d1, d2 = m1.gecis[(d1, a2)], m2.gecis[(d2, a1)]
    bas = gorulen[(d1, d2)]
    dongu = gecmis[bas:]
    limit = tuple(Fraction(sum(ODUL[e][i] for e in dongu), len(dongu)) for i in (0, 1))
    return gecmis[:bas], dongu, limit


def sonlu_geriye_tumevarim(tur: int = 100) -> tuple[list, int]:
    """Son tur tek seferlik oyundur → tanık. Bir önceki tur sonrakini etkilemez → tanık, ..."""
    eylemler = [None] * tur
    for t in reversed(range(tur)):
        # t'den sonraki turlar zaten belirlendi ve t'deki eyleme bağlı değil: tek seferlik oyun.
        eylemler[t] = T if ODUL[(T, T)][0] > ODUL[(S, T)][0] and ODUL[(T, S)][0] > ODUL[(S, S)][0] else S
    return eylemler, sum(ODUL[(a, a)][0] for a in eylemler)


def nash_mi(m1: Makine, m2: Makine, adaylar=MAKINELER) -> bool:
    """Aday makineler arasında, hiçbir oyuncu tek başına sapınca daha iyi ortalama alamıyor mu?
    (Gerçek tanım bütün makineleri kapsar; burada yalnızca adaylar denenir.)"""
    _, _, (u1, u2) = oyna(m1, m2)
    return (all(oyna(d, m2)[2][0] <= u1 for d in adaylar)
            and all(oyna(m1, d)[2][1] <= u2 for d in adaylar))


def main() -> None:
    eylemler, toplam = sonlu_geriye_tumevarim()
    print(f"=== 100 turluk ikilem: geriye tümevarım ===\n  Her turda {set(eylemler)}; toplam {toplam} → {-toplam} yıl hapis")

    print("\n=== Sonsuz tekrar: ortalamaların limiti ===")
    print(f"  {'':<14}" + "".join(f"{m.ad:>15}" for m in MAKINELER))
    for m1 in MAKINELER:
        satir = "".join(f"{float(oyna(m1, m2)[2][0]):>7.1f} /{float(oyna(m1, m2)[2][1]):>5.1f}" for m2 in MAKINELER)
        print(f"  {m1.ad:<14}{satir}")
    print("  (Hücre: satır oyuncusunun / sütun oyuncusunun ortalama faydası)")

    print("\n=== Kitaptaki eşleşmeler ===")
    for m1, m2 in ((GUVERCIN, GUVERCIN), (SAHIN, GUVERCIN), (SAHIN, SAHIN), (SAHIN, ACIMASIZ), (ACIMASIZ, ACIMASIZ)):
        onek, dongu, limit = oyna(m1, m2)
        print(f"  {m1.ad:<9} – {m2.ad:<9}: önek {onek}, döngü {dongu}, fayda {limit[0]}/{limit[1]}, "
              f"Nash (adaylar arasında)? {nash_mi(m1, m2)}")
    print("  ACIMASIZ–ACIMASIZ işbirliğini sürdüren bir dengedir: Sapan, sonsuza dek cezalandırılır.")


if __name__ == "__main__":
    main()
