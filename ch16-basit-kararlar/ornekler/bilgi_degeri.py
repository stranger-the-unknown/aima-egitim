#!/usr/bin/env python3
"""Bilginin değeri (kitaptaki 16.6).

Genel formül (mükemmel bilgi, E_j gözlenirse):
    VPI_e(E_j) = Σ_k P(E_j = e_jk | e) · max_a EU(a | e, E_j = e_jk)  −  max_a EU(a | e)

Kitaptaki petrol örneği: n bloktan tam biri C $ kâr getiren petrol içeriyor; her blok C/n $.
Blok 3'ün araştırma sonucu (kesin) → VPI = C/n.

Özellikler (kitap): VPI ≥ 0; toplamsal değil; sıradan bağımsız.
Miyop bilgi toplayan ajan: VPI − maliyet en büyük olan gözlemi, pozitif oldukça yap.

Çalıştırma:
    python bilgi_degeri.py
"""
from __future__ import annotations

import itertools
import math
import random
from fractions import Fraction


class KararProblemi:
    """Ayrık durumlar, eylemler ve gözlemlerle basit bir karar problemi.
    durumlar : {s: P(s)}
    fayda    : fayda(a, s)
    testler  : {ad: fonksiyon(s) → {sonuç: P(sonuç | s)}}"""

    def __init__(self, durumlar: dict, eylemler: list, fayda, testler: dict):
        self.durumlar, self.eylemler, self.fayda, self.testler = durumlar, eylemler, fayda, testler

    def sonsal(self, gozlem: dict) -> dict:
        ham = {}
        for s, p in self.durumlar.items():
            for test, sonuc in gozlem.items():
                p *= self.testler[test](s).get(sonuc, 0)
            ham[s] = p
        z = sum(ham.values())
        return {s: v / z for s, v in ham.items()}

    def meu(self, gozlem: dict | None = None) -> tuple[object, float]:
        P = self.sonsal(gozlem or {})
        eu = {a: sum(P[s] * self.fayda(a, s) for s in P) for a in self.eylemler}
        a = max(eu, key=eu.get)
        return a, eu[a]

    def gozlem_olasiligi(self, gozlem: dict, yeni: dict) -> float:
        P = self.sonsal(gozlem)
        toplam = 0
        for s, p in P.items():
            for test, sonuc in yeni.items():
                p *= self.testler[test](s).get(sonuc, 0)
            toplam += p
        return toplam

    def vpi(self, testler: list[str], gozlem: dict | None = None):
        gozlem = gozlem or {}
        sonuclar = {t: sorted({o for s in self.durumlar for o in self.testler[t](s)}, key=str) for t in testler}
        toplam = 0
        for degerler in itertools.product(*(sonuclar[t] for t in testler)):
            yeni = dict(zip(testler, degerler))
            p = self.gozlem_olasiligi(gozlem, yeni)
            if p > 0:
                toplam += p * self.meu({**gozlem, **yeni})[1]
        return toplam - self.meu(gozlem)[1]


def petrol(n: int, C=Fraction(1)) -> KararProblemi:
    durumlar = {i: Fraction(1, n) for i in range(1, n + 1)}       # petrol hangi blokta?
    eylemler = ["hiçbiri"] + list(range(1, n + 1))

    def fayda(a, s):
        return 0 if a == "hiçbiri" else (C if a == s else 0) - C / n

    testler = {"araştırma(3)": lambda s: {"petrol": 1} if s == 3 else {"yok": 1}}
    return KararProblemi(durumlar, eylemler, fayda, testler)


def tibbi(p_hasta: float = 0.2) -> KararProblemi:
    """Özgün örnek: tedavi et / bekle; iki test (T1 ve onun aynısı T1b) ve farklı bir test T2."""
    U = {("tedavi", "hasta"): 80, ("tedavi", "sağlıklı"): 90, ("bekle", "hasta"): 20, ("bekle", "sağlıklı"): 100}

    def test(duyarlilik, ozgulluk):
        return lambda s: ({"+": duyarlilik, "−": 1 - duyarlilik} if s == "hasta"
                          else {"+": 1 - ozgulluk, "−": ozgulluk})

    return KararProblemi({"hasta": p_hasta, "sağlıklı": 1 - p_hasta}, ["tedavi", "bekle"],
                         lambda a, s: U[(a, s)],
                         {"T1": test(0.9, 0.85), "T1b": test(0.9, 0.85), "T2": test(0.7, 0.95)})


def vpi_gauss(mu: float, sigma: float, c: float) -> float:
    """U1 ~ N(μ, σ²) belirsiz, U2 = c kesin. U1'i tam öğrenmenin değeri: E[max(U1, c)] − max(μ, c)."""
    z = (mu - c) / sigma
    phi = math.exp(-z * z / 2) / math.sqrt(2 * math.pi)
    Phi = 0.5 * (1 + math.erf(z / math.sqrt(2)))
    return c + sigma * (phi + z * Phi) - max(mu, c)


def miyop_ajan(p: KararProblemi, maliyet: dict, gercek: str, rng: random.Random) -> list:
    gozlem, adimlar = {}, []
    while True:
        adaylar = [(float(p.vpi([t], gozlem)) - maliyet[t], t) for t in p.testler if t not in gozlem]
        if not adaylar:
            break
        net, t = max(adaylar, key=lambda x: x[0])  # eşitlikte ilk test
        if net <= 0:
            break
        dagilim = p.testler[t](gercek)
        sonuc = rng.choices(list(dagilim), weights=list(dagilim.values()))[0]
        gozlem[t] = sonuc
        adimlar.append((t, round(net, 3), sonuc))
    return adimlar + [("karar", p.meu(gozlem)[0])]


def main() -> None:
    print("=== Petrol blokları (kitap): VPI = C/n ===")
    for n in (3, 4, 5, 10):
        v = petrol(n).vpi(["araştırma(3)"])
        print(f"  n = {n:>2}: VPI(araştırma) = {v} × C")

    print("\n=== Tıbbi karar (özgün): VPI özellikleri ===")
    t = tibbi()
    a, eu = t.meu()
    print(f"  Testsiz karar: {a} (EU = {eu:.2f})")
    v1, v1b, v2 = t.vpi(["T1"]), t.vpi(["T1b"]), t.vpi(["T2"])
    print(f"  VPI(T1) = {v1:.3f}, VPI(T2) = {v2:.3f}")
    print(f"  VPI(T1, T1b) = {t.vpi(['T1', 'T1b']):.3f}  ≠  VPI(T1) + VPI(T1b) = {v1 + v1b:.3f}   (toplamsal değil)")
    sira1 = v1 + sum(t.gozlem_olasiligi({}, {'T1': o}) * t.vpi(['T2'], {'T1': o}) for o in '+−')
    sira2 = v2 + sum(t.gozlem_olasiligi({}, {'T2': o}) * t.vpi(['T1'], {'T2': o}) for o in '+−')
    print(f"  Önce T1 sonra T2: {sira1:.3f};  önce T2 sonra T1: {sira2:.3f};  birlikte: {t.vpi(['T1', 'T2']):.3f}"
          "   (sıradan bağımsız)")

    print("\n=== Bilgi ne zaman değerli? (U1 ~ N(μ, σ²), U2 = 0 kesin) ===")
    for ad, mu, sigma in (("(a) seçim açık: μ = 5, σ = 1", 5, 1), ("(b) eşit, belirsizlik az: μ = 0.1, σ = 0.2", 0.1, 0.2),
                          ("(c) eşit, belirsizlik çok: μ = 0.1, σ = 3", 0.1, 3)):
        print(f"  {ad:<44} VPI = {vpi_gauss(mu, sigma, 0.0):.3f}")
    print("  Bilgi, eylemler birbirine yakın VE sonuç belirsizken değerlidir: kararı değiştirebilir.")

    print("\n=== Miyop bilgi toplayan ajan (test maliyeti T1 = 1, T2 = 0.5, T1b = 1) ===")
    for gercek in ("hasta", "sağlıklı"):
        adimlar = miyop_ajan(t, {"T1": 1.0, "T1b": 1.0, "T2": 0.5}, gercek, random.Random(4))
        print(f"  Gerçek durum {gercek}: {adimlar}")


if __name__ == "__main__":
    main()
