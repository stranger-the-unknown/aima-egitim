#!/usr/bin/env python3
"""Klasik planlama araçları (Bölüm 11): PDDL tarzı eylem şemaları ve planlayıcılar.

Durum: temel atomların kümesi (frozenset), veritabanı anlamıyla: listede olmayan yanlıştır.
Atom: "At(C1,SFO)" gibi boşluksuz metin.

Eylem şeması örneği (hava kargo):
    Sema("Load", ["c", "p", "a"],
         on=["At(c,a)", "At(p,a)", "Cargo(c)", "Plane(p)", "Airport(a)"],
         ekle=["In(c,p)"], sil=["At(c,a)"])
Şemalar tüm nesne kombinasyonlarıyla temellendirilir (grounding); statik önkoşullar
(Cargo, Plane gibi hiç değişmeyen atomlar) başlangıçta sağlanmayan eylemleri eler.

Planlayıcılar
  * ileri_ara     : ileri (progression) arama; BFS ya da A* (sezgiselle)
  * h_hedef_sayisi: sağlanmamış hedef sayısı (önkoşulları yok sayma sezgiselinin kaba hâli)
  * h_max, h_add  : silme listelerini yok say (gevşetilmiş problem) + maliyet yayılımı
  * planlama_grafigi_seviyeleri: her atomun ilk göründüğü seviye (seviye toplamı, en büyük seviye)
  * geri_ilgili   : geri (regression) arama için ilgili eylemler

Çalıştırınca küçük bir kendi kendini sınama yapar:
    python planlama.py
"""
from __future__ import annotations

import heapq
import itertools
import re
from collections import deque
from dataclasses import dataclass
from typing import Callable, Iterable, Optional

Durum = frozenset


@dataclass(frozen=True)
class Eylem:
    ad: str
    on: frozenset          # pozitif önkoşullar
    on_degil: frozenset    # negatif önkoşullar (¬At(Flat,Axle) gibi)
    ekle: frozenset
    sil: frozenset

    def uygulanabilir(self, s: Durum) -> bool:
        return self.on <= s and not (self.on_degil & s)

    def uygula(self, s: Durum) -> Durum:
        return (s - self.sil) | self.ekle

    def __str__(self) -> str:
        return self.ad


@dataclass
class Sema:
    ad: str
    parametreler: list[str]
    on: list[str]
    ekle: list[str]
    sil: list[str]
    on_degil: tuple = ()
    farkli: tuple = ()  # birbirinden farklı olması gereken parametre çiftleri


def _yerlestir(atom: str, baglama: dict) -> str:
    ad, _, args = atom.partition("(")
    if not args:
        return atom
    argumanlar = [baglama.get(a.strip(), a.strip()) for a in args.rstrip(")").split(",")]
    return f"{ad}({','.join(argumanlar)})"


def temellendir(semalar: list[Sema], nesneler: list[str], baslangic: Iterable[str],
                statik: Iterable[str] = ()) -> list[Eylem]:
    """Şemaları tüm nesne atamalarıyla somutlaştır. `statik` yüklemler hiç değişmez;
    başlangıçta sağlanmayan statik önkoşullu eylemler hemen elenir."""
    bas = set(baslangic)
    statik = set(statik)
    eylemler = []
    for sema in semalar:
        for degerler in itertools.product(nesneler, repeat=len(sema.parametreler)):
            b = dict(zip(sema.parametreler, degerler))
            if any(b.get(x, x) == b.get(y, y) for x, y in sema.farkli):  # parametre ya da sabit
                continue
            on = [_yerlestir(a, b) for a in sema.on]
            if any(a.split("(")[0] in statik and a not in bas for a in on):
                continue
            ad = f"{sema.ad}({','.join(degerler)})" if degerler else sema.ad
            eylemler.append(Eylem(ad, frozenset(on), frozenset(_yerlestir(a, b) for a in sema.on_degil),
                                  frozenset(_yerlestir(a, b) for a in sema.ekle),
                                  frozenset(_yerlestir(a, b) for a in sema.sil)))
    return eylemler


@dataclass
class Planlama:
    baslangic: Durum
    hedef: frozenset
    eylemler: list[Eylem]

    def hedef_mi(self, s: Durum) -> bool:
        return self.hedef <= s


# ---------------------------------------------------------------------------
# Sezgiseller
# ---------------------------------------------------------------------------

def h_hedef_sayisi(p: Planlama, s: Durum) -> float:
    """Sağlanmamış hedef atomu sayısı. Her eylem en fazla bir hedef sağlıyorsa kabul edilebilir."""
    return len(p.hedef - s)


def _gevsetilmis_maliyet(p: Planlama, s: Durum, birlestir: Callable) -> dict:
    """Silme listelerini yok sayarak her atomun maliyetini yay (h_max: max, h_add: toplam)."""
    maliyet = {a: 0 for a in s}
    degisti = True
    while degisti:
        degisti = False
        for e in p.eylemler:
            if e.on <= maliyet.keys():
                c = 1 + (birlestir(maliyet[a] for a in e.on) if e.on else 0)
                for a in e.ekle:
                    if c < maliyet.get(a, float("inf")):
                        maliyet[a] = c
                        degisti = True
    return maliyet


def h_max(p: Planlama, s: Durum) -> float:
    m = _gevsetilmis_maliyet(p, s, max)
    return max((m.get(g, float("inf")) for g in p.hedef), default=0)


def h_add(p: Planlama, s: Durum) -> float:
    m = _gevsetilmis_maliyet(p, s, sum)
    return sum(m.get(g, float("inf")) for g in p.hedef)


def planlama_grafigi_seviyeleri(p: Planlama, s: Optional[Durum] = None) -> dict[str, int]:
    """Karşılıklı dışlama (mutex) olmadan planlama grafiği: her atomun ilk göründüğü seviye."""
    s = s if s is not None else p.baslangic
    seviye = {a: 0 for a in s}
    k = 0
    while True:
        k += 1
        yeni = {}
        for e in p.eylemler:
            if e.on <= seviye.keys():
                for a in e.ekle:
                    if a not in seviye:
                        yeni[a] = k
        if not yeni:
            return seviye
        seviye.update(yeni)


def h_seviye_toplami(p: Planlama, s: Durum) -> float:
    sv = planlama_grafigi_seviyeleri(p, s)
    return sum(sv.get(g, float("inf")) for g in p.hedef)


# ---------------------------------------------------------------------------
# Arama
# ---------------------------------------------------------------------------

@dataclass
class Sonuc:
    plan: Optional[list[str]]
    genisletilen: int


def ileri_ara(p: Planlama, h: Optional[Callable[[Planlama, Durum], float]] = None) -> Sonuc:
    """h verilmezse BFS (en kısa plan), verilirse A*."""
    if h is None:
        sinir = deque([(p.baslangic, [])])
        gorulen = {p.baslangic}
        genis = 0
        while sinir:
            s, plan = sinir.popleft()
            if p.hedef_mi(s):
                return Sonuc(plan, genis)
            genis += 1
            for e in p.eylemler:
                if e.uygulanabilir(s):
                    s2 = e.uygula(s)
                    if s2 not in gorulen:
                        gorulen.add(s2)
                        sinir.append((s2, plan + [e.ad]))
        return Sonuc(None, genis)
    sayac = itertools.count()
    sinir = [(h(p, p.baslangic), next(sayac), p.baslangic, [])]
    en_iyi = {p.baslangic: 0}
    genis = 0
    while sinir:
        _, _, s, plan = heapq.heappop(sinir)
        if len(plan) > en_iyi.get(s, float("inf")):
            continue
        if p.hedef_mi(s):
            return Sonuc(plan, genis)
        genis += 1
        for e in p.eylemler:
            if e.uygulanabilir(s):
                s2 = e.uygula(s)
                g = len(plan) + 1
                if g < en_iyi.get(s2, float("inf")):
                    en_iyi[s2] = g
                    heapq.heappush(sinir, (g + h(p, s2), next(sayac), s2, plan + [e.ad]))
    return Sonuc(None, genis)


def plani_uygula(p: Planlama, plan: list[str]) -> Durum:
    adlar = {e.ad: e for e in p.eylemler}
    s = p.baslangic
    for ad in plan:
        e = adlar[ad]
        assert e.uygulanabilir(s), f"{ad} uygulanamaz"
        s = e.uygula(s)
    return s


def geri_ilgili(p: Planlama, hedef: frozenset) -> list[tuple[str, frozenset]]:
    """Geri (regression) arama: hedefin bir atomunu ekleyen ve hiçbir hedef atomunu
    silmeyen eylemler ile onların gerilemiş hedefleri: g' = (g − EKLE(a)) ∪ ÖN(a)."""
    sonuc = []
    for e in p.eylemler:
        if e.ekle & hedef and not (e.sil & hedef):
            sonuc.append((e.ad, (hedef - e.ekle) | e.on))
    return sonuc


def atomlar(metin: str) -> frozenset:
    return frozenset(a for a in re.split(r"\s*,\s*(?![^()]*\))", metin.replace(" ", "")) if a)


if __name__ == "__main__":
    # İki odalı süpürge dünyası PDDL ile: iki oda da temiz olsun, ajan A'ya dönsün.
    semalar = [
        Sema("Süpür", ["r"], ["İçinde(r)", "Kirli(r)"], ["Temiz(r)"], ["Kirli(r)"]),
        Sema("Git", ["a", "b"], ["İçinde(a)", "Oda(a)", "Oda(b)"], ["İçinde(b)"], ["İçinde(a)"],
             farkli=(("a", "b"),)),
    ]
    bas = atomlar("Oda(A),Oda(B),İçinde(A),Kirli(A),Kirli(B)")
    p = Planlama(bas, atomlar("Temiz(A),Temiz(B),İçinde(A)"),
                 temellendir(semalar, ["A", "B"], bas, statik=["Oda"]))
    print("Temellendirilen eylemler:", [e.ad for e in p.eylemler])
    for ad, h in [("BFS", None), ("A* h_max", h_max), ("A* h_add", h_add)]:
        s = ileri_ara(p, h)
        print(f"{ad:<9}: {s.plan}  (genişletilen: {s.genisletilen})")
