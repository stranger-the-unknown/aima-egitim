#!/usr/bin/env python3
"""Pasif pekiştirmeli öğrenme: sabit politikanın faydalarını öğrenmek (kitaptaki 22.2).

Ortam: Bölüm 17'deki 4 × 3 dünya (ödül geçişe ait, r = −0.04, γ = 1); ajan geçiş modelini bilmez.
Kitaptaki üç deneme (sayfa 792) ile:
  * Doğrudan fayda kestirimi: 1. denemede (1,1) için 0.76; (1,2) için 0.80 ve 0.88; (1,3) için 0.84 ve 0.92.
  * ADP: (3,3)'te Sağ dört kez yapılmış; ikisinde (4,3), ikisinde (3,2) → P̂ = 1/2.
  * TD: U(1,3) = 0.84, U(2,3) = 0.96 iken (1,3) → (2,3) geçişi U(1,3)'ü 0.92'ye doğru çeker.
Çok denemeli benzetimde üç yöntem de Şekil 17.3'teki faydalara yakınsar; ADP en hızlı, doğrudan kestirim
en yavaştır. TD öğrenme hızı α(n) = 60/(59 + n) (kitap).

Çalıştırma:
    python pasif_ogrenme.py
"""
from __future__ import annotations

import random
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "ch17-karmasik-kararlar" / "ornekler"))

import mdp  # noqa: E402  (Bölüm 17'nin MDP kütüphanesi)

R = -0.04
DUNYA = mdp.dort_uc(r=R)
GERCEK_U, _ = mdp.deger_yineleme(DUNYA, eps=1e-10)
POLITIKA = DUNYA.acgozlu(GERCEK_U)                   # Şekil 17.2(a)'daki en iyi politika

# Kitaptaki üç deneme: [(durum, eylem, ödül, sonraki durum), ...]
_YON = {"U": "Yukarı", "R": "Sağ"}


def _deneme(yol: list, eylemler: str, son_odul: float):
    adimlar = []
    for i, (s, a) in enumerate(zip(yol[:-1], eylemler)):
        odul = son_odul if i == len(yol) - 2 else R
        adimlar.append((s, _YON[a], odul, yol[i + 1]))
    return adimlar


KITAP_DENEMELERI = [
    _deneme([(1, 1), (1, 2), (1, 3), (1, 2), (1, 3), (2, 3), (3, 3), (4, 3)], "UURURRR", 1.0),
    _deneme([(1, 1), (1, 2), (1, 3), (2, 3), (3, 3), (3, 2), (3, 3), (4, 3)], "UURRRUR", 1.0),
    _deneme([(1, 1), (1, 2), (1, 3), (2, 3), (3, 3), (3, 2), (4, 2)], "UURRRU", -1.0),
]


def deneme_uret(rng: random.Random, politika=POLITIKA, dunya=DUNYA, en_cok: int = 200):
    s, adimlar = (1, 1), []
    while s not in dunya.uclar and len(adimlar) < en_cok:
        a = politika[s]
        sonuclar = dunya.gecis[(s, a)]
        s2 = rng.choices([x for _, x in sonuclar], weights=[p for p, _ in sonuclar])[0]
        adimlar.append((s, a, dunya.odul(s, a, s2), s2))
        s = s2
    return adimlar


# --- Doğrudan fayda kestirimi ---------------------------------------------------------
def odul_kalan(deneme) -> list[tuple]:
    """Her ziyaret için (durum, o noktadan sonraki toplam ödül)."""
    toplam, sonuc = 0.0, []
    for s, _, r, _ in reversed(deneme):
        toplam += r
        sonuc.append((s, toplam))
    return list(reversed(sonuc))


class DogrudanKestirim:
    def __init__(self):
        self.toplam, self.sayi = defaultdict(float), defaultdict(int)

    def ogren(self, deneme):
        for s, g in odul_kalan(deneme):
            self.toplam[s] += g
            self.sayi[s] += 1

    def U(self, s) -> float:
        return self.toplam[s] / self.sayi[s] if self.sayi[s] else 0.0


# --- Uyarlamalı dinamik programlama (ADP) -------------------------------------------------
class PasifADP:
    def __init__(self, gama: float = 1.0):
        self.N_sa = defaultdict(int)
        self.N_s2_sa = defaultdict(int)
        self.odul = {}
        self.gama = gama
        self.Ud = defaultdict(float)

    def P(self, s2, s, a) -> float:
        return self.N_s2_sa[(s2, s, a)] / self.N_sa[(s, a)] if self.N_sa[(s, a)] else 0.0

    def ogren(self, deneme, politika=POLITIKA, yineleme: int = 50):
        for s, a, r, s2 in deneme:
            self.N_sa[(s, a)] += 1
            self.N_s2_sa[(s2, s, a)] += 1
            self.odul[(s, a, s2)] = r
        # Değiştirilmiş politika yinelemesi: öğrenilen modelle basit Bellman güncellemeleri
        durumlar = {s for (s, a) in self.N_sa}
        for _ in range(yineleme):
            for s in durumlar:
                a = politika[s]
                self.Ud[s] = sum(self.P(s2, s, a) * (self.odul[(s, a, s2)] + self.gama * self.Ud[s2])
                                 for (s2, s_, a_) in list(self.N_s2_sa) if s_ == s and a_ == a)

    def U(self, s) -> float:
        return self.Ud[s]


# --- Zamansal fark (TD) öğrenmesi --------------------------------------------------------------
class PasifTD:
    def __init__(self, alfa=lambda n: 60 / (59 + n), gama: float = 1.0):
        self.Ud, self.N = defaultdict(float), defaultdict(int)
        self.alfa, self.gama = alfa, gama

    def guncelle(self, s, r, s2):
        """U(s) ← U(s) + α(N_s) [r + γ U(s′) − U(s)]  (22.3). Uç durumların faydası 0."""
        self.N[s] += 1
        self.Ud[s] += self.alfa(self.N[s]) * (r + self.gama * self.Ud[s2] - self.Ud[s])

    def ogren(self, deneme):
        for s, _, r, s2 in deneme:
            self.guncelle(s, r, s2)

    def U(self, s) -> float:
        return self.Ud[s]


def rms_hata(ajan, durumlar=None) -> float:
    durumlar = durumlar or [s for s in DUNYA.durumlar if s not in DUNYA.uclar]
    return float(np.sqrt(np.mean([(ajan.U(s) - GERCEK_U[s]) ** 2 for s in durumlar])))


def karsilastir(deneme_sayilari=(10, 50, 200, 1000), tohum: int = 0) -> dict:
    rng = random.Random(tohum)
    ajanlar = {"doğrudan": DogrudanKestirim(), "ADP": PasifADP(), "TD": PasifTD()}
    sonuc, n = {}, 0
    for hedef in deneme_sayilari:
        while n < hedef:
            d = deneme_uret(rng)
            for ad, ajan in ajanlar.items():
                ajan.ogren(d) if ad != "ADP" else ajan.ogren(d, yineleme=10)   # önceki U'dan başlar
            n += 1
        gorulen = [s for s in DUNYA.durumlar if ajanlar["doğrudan"].sayi[s] > 0]
        sonuc[hedef] = {ad: rms_hata(a, gorulen) for ad, a in ajanlar.items()}
    return sonuc, ajanlar


def main() -> None:
    print("=== Kitaptaki üç deneme ===")
    for s, g in odul_kalan(KITAP_DENEMELERI[0]):
        print(f"  1. deneme: {s} için ödül-kalan {g:.2f}")
    adp = PasifADP()
    for d in KITAP_DENEMELERI:
        adp.ogren(d)
    print(f"  ADP: (3,3)'te Sağ {adp.N_sa[((3, 3), 'Sağ')]} kez; P̂((4,3) | (3,3), Sağ) = {adp.P((4, 3), (3, 3), 'Sağ'):.2f},"
          f" P̂((3,2) | (3,3), Sağ) = {adp.P((3, 2), (3, 3), 'Sağ'):.2f}")
    td = PasifTD(alfa=lambda n: 0.5)
    td.Ud[(1, 3)], td.Ud[(2, 3)] = 0.84, 0.96
    td.guncelle((1, 3), -0.04, (2, 3))
    print(f"  TD (α = 0.5): U(1,3) 0.84 → {td.U((1, 3)):.2f}  (hedef −0.04 + 0.96 = 0.92)")

    print("\n=== Benzetim: en iyi politikayla denemeler, ziyaret edilen durumlarda RMS hata ===")
    print("  (Politika (3,1) ve (4,1)'e hiç gitmez; pasif ajan bu durumların faydasını öğrenemez.)")
    sonuc, ajanlar = karsilastir()
    print("  deneme   doğrudan      ADP       TD")
    for n, h in sonuc.items():
        print(f"  {n:>6}   {h['doğrudan']:8.4f}  {h['ADP']:7.4f}  {h['TD']:7.4f}")
    print("\n  1000 denemeden sonra:   durum   ziyaret   gerçek   doğrudan     ADP      TD")
    for s in DUNYA.durumlar:
        if s not in DUNYA.uclar:
            print(f"                         {s}  {ajanlar['doğrudan'].sayi[s]:>7}   {GERCEK_U[s]:.4f}   "
                  + "   ".join(f"{ajanlar[k].U(s):.4f}" for k in ("doğrudan", "ADP", "TD")))
    print("  Az ziyaret edilen durumlarda (ör. (3,2)) bütün yöntemlerin hatası büyük; TD en gürültülüsü.")


if __name__ == "__main__":
    main()
