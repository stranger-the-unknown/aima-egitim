#!/usr/bin/env python3
"""Normal biçimli oyunlar için küçük bir kütüphane (kitaptaki 18.2.1–18.2.2).

Bir oyun: oyuncu adları, her oyuncunun eylemleri ve her eylem profili için fayda demeti.
    oyun.fayda[(a1, a2)] = (u1, u2)

Kitaptaki örnekler (testlerle doğrulanır):
  * Mahkûm ikilemi: tanıklık et baskın strateji; (tanık, tanık) tek Nash dengesi ve
    Pareto en iyi olmayan tek sonuç.
  * Koordinasyon oyunu: (t, l) ve (b, r) iki Nash dengesi; baskın strateji yok.
  * Yazı-tura eşleştirme: saf Nash dengesi yok; karma denge (½, ½).
  * İki parmaklı Morra (sıfır toplamlı): saf stratejilerle −3 ≤ U ≤ 2; karma maksimin dengesi
    [7/12: bir; 5/12: iki], oyunun değeri E için −1/12.

Sıfır toplamlı oyunların maksimin çözümü doğrusal programlamadır; burada küçük bir simpleks
(Bland kuralı) kullanılır.

Çalıştırma:
    python oyun_kurami.py
"""
from __future__ import annotations

import itertools
from dataclasses import dataclass
from fractions import Fraction

import numpy as np


@dataclass
class Oyun:
    oyuncular: tuple
    eylemler: tuple                 # her oyuncu için eylem listesi
    fayda: dict                     # eylem profili → fayda demeti

    def profiller(self):
        return itertools.product(*self.eylemler)

    def u(self, i: int, profil) -> float:
        return self.fayda[tuple(profil)][i]

    def degistir(self, profil, i: int, a):
        p = list(profil)
        p[i] = a
        return tuple(p)


def iki_oyunculu(oyuncular, satir, sutun, tablo) -> Oyun:
    """tablo[(satır eylemi, sütun eylemi)] = (satır oyuncusunun faydası, sütun oyuncusunun faydası)."""
    return Oyun(tuple(oyuncular), (tuple(satir), tuple(sutun)), dict(tablo))


# --- Çözüm kavramları ------------------------------------------------------------
def baskin_mi(oyun: Oyun, i: int, s, s2, guclu: bool = True) -> bool:
    """i oyuncusu için s, s2'yi (güçlü / zayıf) baskılıyor mu?"""
    digerleri = [e for j, e in enumerate(oyun.eylemler) if j != i]
    farklar = []
    for diger in itertools.product(*digerleri):
        p = list(diger)
        p.insert(i, s)
        q = list(diger)
        q.insert(i, s2)
        farklar.append(oyun.u(i, p) - oyun.u(i, q))
    return all(f > 0 for f in farklar) if guclu else (all(f >= 0 for f in farklar) and any(f > 0 for f in farklar))


def baskin_strateji(oyun: Oyun, i: int):
    """Diğer bütün stratejileri güçlü biçimde baskılayan strateji (yoksa None)."""
    for s in oyun.eylemler[i]:
        if all(baskin_mi(oyun, i, s, s2) for s2 in oyun.eylemler[i] if s2 != s):
            return s
    return None


def en_iyi_tepkiler(oyun: Oyun, i: int, profil) -> list:
    degerler = {a: oyun.u(i, oyun.degistir(profil, i, a)) for a in oyun.eylemler[i]}
    en = max(degerler.values())
    return [a for a, v in degerler.items() if v == en]


def saf_nash(oyun: Oyun) -> list:
    """Hiçbir oyuncunun tek başına sapmakla kazanamadığı profiller."""
    return [p for p in oyun.profiller()
            if all(p[i] in en_iyi_tepkiler(oyun, i, p) for i in range(len(oyun.oyuncular)))]


def pareto_en_iyi(oyun: Oyun) -> list:
    sonuc = []
    for p in oyun.profiller():
        u = oyun.fayda[p]
        baskilaniyor = any(all(v[k] >= u[k] for k in range(len(u))) and any(v[k] > u[k] for k in range(len(u)))
                           for v in oyun.fayda.values())
        if not baskilaniyor:
            sonuc.append(p)
    return sonuc


def faydaci_refah(oyun: Oyun, p) -> float:
    return sum(oyun.fayda[p])


def esitlikci_refah(oyun: Oyun, p) -> float:
    return min(oyun.fayda[p])


def miyop_en_iyi_tepki(oyun: Oyun, baslangic, en_cok: int = 100) -> tuple:
    """Bir oyuncu en iyi tepkiyi oynamıyorsa onu değiştir; Nash dengesinde durur (ya da döngüye girer)."""
    p, yol = tuple(baslangic), [tuple(baslangic)]
    for _ in range(en_cok):
        for i in range(len(oyun.oyuncular)):
            tepkiler = en_iyi_tepkiler(oyun, i, p)
            if p[i] not in tepkiler:
                p = oyun.degistir(p, i, tepkiler[0])
                yol.append(p)
                break
        else:
            return p, yol
    return None, yol


# --- Sıfır toplamlı oyunlar: maksimin (doğrusal programlama) ------------------------
def simpleks(B: np.ndarray, eps: float = 1e-12):
    """max Σz  öyle ki  B z ≤ 1, z ≥ 0  (B > 0). (z, ikil y, amaç) döndürür. Bland kuralı."""
    m, n = B.shape
    T = np.zeros((m + 1, n + m + 1))
    T[:m, :n], T[:m, n:n + m], T[:m, -1], T[m, :n] = B, np.eye(m), 1.0, -1.0
    taban = [n + i for i in range(m)]
    while True:
        giren = next((j for j in range(n + m) if T[m, j] < -eps), None)
        if giren is None:
            break
        oranlar = [(T[i, -1] / T[i, giren], taban[i], i) for i in range(m) if T[i, giren] > eps]
        _, _, satir = min(oranlar)
        T[satir] /= T[satir, giren]
        for i in range(m + 1):
            if i != satir:
                T[i] -= T[i, giren] * T[satir]
        taban[satir] = giren
    z = np.zeros(n)
    for i, j in enumerate(taban):
        if j < n:
            z[j] = T[i, -1]
    return z, T[m, n:n + m].copy(), T[m, -1]


def maksimin(A) -> tuple[float, np.ndarray, np.ndarray]:
    """A: satır oyuncusunun (en büyükleyen) fayda matrisi. (oyun değeri, satır stratejisi, sütun stratejisi)."""
    A = np.asarray(A, dtype=float)
    kaydir = 1.0 - A.min()
    z, y, amac = simpleks(A + kaydir)
    v = 1.0 / amac
    return v - kaydir, y * v, z * v


def morra() -> Oyun:
    """İki parmaklı Morra: toplam f tekse O, çiftse E f dolar kazanır. E satır oyuncusu."""
    tablo = {}
    for e, o in itertools.product((1, 2), repeat=2):
        f = e + o
        tablo[("bir" if e == 1 else "iki", "bir" if o == 1 else "iki")] = (f, -f) if f % 2 == 0 else (-f, f)
    return iki_oyunculu(("E", "O"), ("bir", "iki"), ("bir", "iki"), tablo)


def sirali_saf_minimaks(A) -> tuple[float, float]:
    """Saf stratejilerle: önce satır oyuncusu açıklarsa değer U_{E,O}, önce sütun oyuncusu açıklarsa U_{O,E}."""
    A = np.asarray(A, dtype=float)
    return float(A.min(axis=1).max()), float(A.max(axis=0).min())


def iki_kere_iki_karma(A) -> tuple[Fraction, Fraction]:
    """2 × 2 sıfır toplamlı oyunda (saf eyer noktası yoksa) satır oyuncusunun 1. eylem olasılığı ve değer.
    Kitaptaki yöntem: iki doğrunun kesişimi, p a + (1 − p) c = p b + (1 − p) d."""
    (a, b), (c, d) = [[Fraction(x) for x in satir] for satir in A]
    p = (d - c) / (a - b - c + d)
    return p, p * a + (1 - p) * c


# --- Kitaptaki oyunlar --------------------------------------------------------------
MAHKUM = iki_oyunculu(("Ali", "Bo"), ("tanık", "sus"), ("tanık", "sus"), {
    ("tanık", "tanık"): (-5, -5), ("tanık", "sus"): (0, -10),
    ("sus", "tanık"): (-10, 0), ("sus", "sus"): (-1, -1)})
KOORDINASYON = iki_oyunculu(("Bo", "Ali"), ("t", "b"), ("l", "r"), {
    ("t", "l"): (10, 10), ("t", "r"): (0, 0), ("b", "l"): (0, 0), ("b", "r"): (1, 1)})
YAZI_TURA = iki_oyunculu(("Ali", "Bo"), ("yazı", "tura"), ("yazı", "tura"), {
    ("yazı", "yazı"): (1, -1), ("yazı", "tura"): (-1, 1), ("tura", "yazı"): (-1, 1), ("tura", "tura"): (1, -1)})


def matris(oyun: Oyun, oyuncu: int = 0) -> np.ndarray:
    return np.array([[oyun.fayda[(a, b)][oyuncu] for b in oyun.eylemler[1]] for a in oyun.eylemler[0]], dtype=float)


def main() -> None:
    print("=== Mahkûm ikilemi ===")
    for i, ad in enumerate(MAHKUM.oyuncular):
        print(f"  {ad} için baskın strateji: {baskin_strateji(MAHKUM, i)}")
    print(f"  Saf Nash dengeleri: {saf_nash(MAHKUM)}")
    print(f"  Pareto en iyi sonuçlar: {pareto_en_iyi(MAHKUM)}")
    for p in MAHKUM.profiller():
        print(f"    {p}: faydacı refah {faydaci_refah(MAHKUM, p):>4}, eşitlikçi refah {esitlikci_refah(MAHKUM, p):>4}")
    print("  İkilem: Baskın strateji dengesi, Pareto en iyi olmayan tek sonuçtur.")

    print("\n=== Koordinasyon oyunu ===")
    print(f"  Baskın strateji: Bo {baskin_strateji(KOORDINASYON, 0)}, Ali {baskin_strateji(KOORDINASYON, 1)}")
    print(f"  Saf Nash dengeleri: {saf_nash(KOORDINASYON)}  (odak noktası: (t, l))")
    denge, yol = miyop_en_iyi_tepki(KOORDINASYON, ("b", "l"))
    print(f"  Miyop en iyi tepki (b, l)'den: {' → '.join(map(str, yol))}")

    print("\n=== Yazı-tura eşleştirme ===")
    print(f"  Saf Nash dengesi: {saf_nash(YAZI_TURA) or 'yok'}")
    _, yol = miyop_en_iyi_tepki(YAZI_TURA, ("yazı", "yazı"), en_cok=6)
    print(f"  Miyop en iyi tepki döngüye girer: {' → '.join(map(str, yol[:6]))} …")
    v, p, q = maksimin(matris(YAZI_TURA))
    print(f"  Karma denge: Ali {np.round(p, 3)}, Bo {np.round(q, 3)}, değer {v:+.3f}")

    print("\n=== İki parmaklı Morra (E satır, en büyükleyen) ===")
    A = matris(morra())
    print(f"  Fayda matrisi (E için):\n{A}")
    alt, ust = sirali_saf_minimaks(A)
    print(f"  Saf stratejilerle: U_E,O = {alt:+.0f} ≤ U ≤ U_O,E = {ust:+.0f}")
    p, deger = iki_kere_iki_karma(A)
    print(f"  Kesişim yöntemi: p = {p}, değer = {deger}")
    v, p, q = maksimin(A)
    print(f"  LP (simpleks): değer {v:+.5f}, E {np.round(p, 4)}, O {np.round(q, 4)}")
    print("  Denge stratejisi [7/12: bir; 5/12: iki]; oyun E'nin aleyhine (−1/12).")


if __name__ == "__main__":
    main()
