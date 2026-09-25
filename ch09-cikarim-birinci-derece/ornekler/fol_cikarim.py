#!/usr/bin/env python3
"""Birinci derece mantıkta çıkarım (Bölüm 9): birleştirme, ileri/geri zincirleme, çözümleme.

Gösterim (kitaptaki gibi):
  * Değişken: küçük harfle başlar          x, y, z, x17
  * Sabit   : büyük harfle başlar          John, M1, Nono
  * Bileşik terim / atomik cümle: demet    ("Knows", "John", "x"),  ("Mother", "y")
  * Literal : (işaret, atom)               (True, atom) ya da (False, atom) = ¬atom
  * Tümce   : literallerin frozenset'i

Metinden okumak için: terim("Knows(John, Mother(y))"), tumce("~Loves(y,x) | ~Animal(z)")

Çalıştırınca kitaptaki birleştirme örneklerini yazdırır:
    python fol_cikarim.py
"""
from __future__ import annotations

import itertools
import re
from typing import Iterator, Optional, Union

Terim = Union[str, tuple]
Yerine = dict  # yerine koyma: {değişken: terim}


# ---------------------------------------------------------------------------
# Ayrıştırma ve yazdırma
# ---------------------------------------------------------------------------

def degisken_mi(t) -> bool:
    return isinstance(t, str) and t[:1].islower()


def terim(metin: str) -> Terim:
    jetonlar = re.findall(r"[A-Za-z_][A-Za-z0-9_]*|[(),]", metin)
    i = 0

    def oku() -> Terim:
        nonlocal i
        ad = jetonlar[i]
        i += 1
        if i < len(jetonlar) and jetonlar[i] == "(":
            i += 1
            args = [oku()]
            while jetonlar[i] == ",":
                i += 1
                args.append(oku())
            i += 1  # ")"
            return (ad, *args)
        return ad

    return oku()


def literal(metin: str):
    metin = metin.strip()
    if metin.startswith("~") or metin.startswith("¬"):
        return (False, terim(metin[1:]))
    return (True, terim(metin))


def tumce(metin: str) -> frozenset:
    return frozenset(literal(p) for p in re.split(r"\s*[|∨]\s*", metin.strip()))


def yaz(t) -> str:
    if isinstance(t, tuple) and len(t) == 2 and isinstance(t[0], bool):  # literal
        return ("" if t[0] else "¬") + yaz(t[1])
    if isinstance(t, tuple):
        return f"{t[0]}({', '.join(yaz(a) for a in t[1:])})"
    return t


def tumce_yaz(c) -> str:
    return " ∨ ".join(sorted(yaz(l) for l in c)) if c else "□"


def yerine_yaz(teta: Optional[Yerine]) -> str:
    if teta is None:
        return "başarısız"
    return "{" + ", ".join(f"{v}/{yaz(t)}" for v, t in tamamla(teta).items()) + "}"


def tamamla(teta: Yerine) -> Yerine:
    """Üçgen biçimdeki yerine koymayı tamamen uygula: {y/John, x/Mother(y)} → {y/John, x/Mother(John)}."""
    return {v: yerine_koy(teta, t) for v, t in teta.items()}


# ---------------------------------------------------------------------------
# Birleştirme
# ---------------------------------------------------------------------------

def yerine_koy(teta: Yerine, t: Terim) -> Terim:
    if degisken_mi(t):
        return yerine_koy(teta, teta[t]) if t in teta else t
    if isinstance(t, tuple):
        return tuple([t[0]] + [yerine_koy(teta, a) for a in t[1:]])
    return t


def _gecer_mi(v: str, t: Terim, teta: Yerine) -> bool:
    """Occurs check: v, t'nin içinde geçiyor mu?"""
    if v == t:
        return True
    if degisken_mi(t) and t in teta:
        return _gecer_mi(v, teta[t], teta)
    if isinstance(t, tuple):
        return any(_gecer_mi(v, a, teta) for a in t[1:])
    return False


def birlestir(x: Terim, y: Terim, teta: Optional[Yerine] = None) -> Optional[Yerine]:
    """Kitaptaki UNIFY: en genel birleştiriciyi (MGU) döndür, yoksa None."""
    if teta is None:
        teta = {}
    if x == y:
        return teta
    if degisken_mi(x):
        return _degisken_birlestir(x, y, teta)
    if degisken_mi(y):
        return _degisken_birlestir(y, x, teta)
    if isinstance(x, tuple) and isinstance(y, tuple) and len(x) == len(y) and x[0] == y[0]:
        for a, b in zip(x[1:], y[1:]):
            teta = birlestir(a, b, teta)
            if teta is None:
                return None
        return teta
    return None


def _degisken_birlestir(v: str, x: Terim, teta: Yerine) -> Optional[Yerine]:
    if v in teta:
        return birlestir(teta[v], x, teta)
    if degisken_mi(x) and x in teta:
        return birlestir(v, teta[x], teta)
    if _gecer_mi(v, x, teta):
        return None
    return {**teta, v: x}


def degiskenler(t) -> set[str]:
    if degisken_mi(t):
        return {t}
    if isinstance(t, tuple):
        if len(t) == 2 and isinstance(t[0], bool):
            return degiskenler(t[1])
        return set().union(*(degiskenler(a) for a in t[1:])) if len(t) > 1 else set()
    return set()


_sayac = itertools.count(1)


def ayir(ifade, onek: str = "v"):
    """Değişkenleri standartlaştır (yeniden adlandır): x → x_17."""
    n = next(_sayac)
    teta = {v: f"{v}_{n}" for v in degiskenler(ifade)}
    if isinstance(ifade, frozenset):
        return frozenset((s, yerine_koy(teta, a)) for s, a in ifade)
    return yerine_koy(teta, ifade)


# ---------------------------------------------------------------------------
# Kesin tümceler: ileri ve geri zincirleme
# ---------------------------------------------------------------------------

Kural = tuple  # (öncüller listesi, sonuç)


def _kural_ayir(oncul, sonuc):
    """Bir kuralın TÜM değişkenlerini birlikte yeniden adlandır (öncüller + sonuç)."""
    t = ayir(("⊢", sonuc, *oncul))
    return list(t[2:]), t[1]


def ileri_zincirleme(kurallar: list[Kural], olgular: list, sorgu=None):
    """FOL-FC-ASK. Döner: (sorguyu karşılayan yerine koyma ya da None, tur başına yeni olgular)."""
    bilinen = list(olgular)
    turlar = []
    while True:
        yeni = []
        for oncul, sonuc in kurallar:
            oncul, sonuc = _kural_ayir(oncul, sonuc)
            for teta in _eslestir(oncul, bilinen, {}):
                q = yerine_koy(teta, sonuc)
                if not any(birlestir(q, f) is not None and _yeniden_adlandirma_mi(q, f) for f in bilinen + yeni):
                    yeni.append(q)
                    if sorgu is not None:
                        phi = birlestir(q, sorgu)
                        if phi is not None:
                            turlar.append(yeni)
                            return phi, turlar
        if not yeni:
            return None, turlar
        turlar.append(yeni)
        bilinen += yeni


def _yeniden_adlandirma_mi(a, b) -> bool:
    return a == b or (degiskenler(a) and birlestir(a, b) is not None and len(degiskenler(a)) == len(degiskenler(b)))


def _eslestir(onculler: list, olgular: list, teta: Yerine) -> Iterator[Yerine]:
    """Öncüllerin hepsini olgularla eşleyen tüm yerine koymalar."""
    if not onculler:
        yield teta
        return
    ilk, geri = onculler[0], onculler[1:]
    for f in olgular:
        t2 = birlestir(yerine_koy(teta, ilk), f, dict(teta))
        if t2 is not None:
            yield from _eslestir(geri, olgular, t2)


def geri_zincirleme(kurallar: list[Kural], olgular: list, hedef, teta: Optional[Yerine] = None,
                    derinlik: int = 0, iz: Optional[list] = None, sinir: int = 30) -> Iterator[Yerine]:
    """FOL-BC-ASK (üreteç): hedefi karşılayan her yerine koymayı sırayla üretir."""
    teta = teta or {}
    if derinlik > sinir:
        return
    hedef_s = yerine_koy(teta, hedef)
    if iz is not None:
        iz.append("  " * derinlik + yaz(hedef_s))
    for f in olgular:
        t2 = birlestir(hedef_s, f, dict(teta))
        if t2 is not None:
            yield t2
    for oncul, sonuc in kurallar:
        oncul, sonuc = _kural_ayir(oncul, sonuc)
        t2 = birlestir(sonuc, hedef_s, dict(teta))
        if t2 is not None:
            yield from _ve_geri(kurallar, olgular, oncul, t2, derinlik + 1, iz, sinir)


def _ve_geri(kurallar, olgular, hedefler, teta, derinlik, iz, sinir):
    if not hedefler:
        yield teta
        return
    for t2 in geri_zincirleme(kurallar, olgular, hedefler[0], teta, derinlik, iz, sinir):
        yield from _ve_geri(kurallar, olgular, hedefler[1:], t2, derinlik, iz, sinir)


# ---------------------------------------------------------------------------
# Çözümleme (resolution)
# ---------------------------------------------------------------------------

def _uygula(teta: Yerine, c: frozenset) -> frozenset:
    return frozenset((s, yerine_koy(teta, a)) for s, a in c)


def cozumleyiciler(c1: frozenset, c2: frozenset) -> list[tuple[frozenset, Yerine]]:
    """İki tümcenin (değişkenleri ayrılmış) ikili çözümleyicileri."""
    c2 = ayir(c2)
    sonuc = []
    for s1, a1 in c1:
        for s2, a2 in c2:
            if s1 != s2:
                teta = birlestir(a1, a2)
                if teta is not None:
                    r = _uygula(teta, (c1 - {(s1, a1)}) | (c2 - {(s2, a2)}))
                    sonuc.append((r, teta))
    return sonuc


def carpanla(c: frozenset) -> list[frozenset]:
    """Aynı işaretli iki literal birleşiyorsa tek literale indir (çarpanlama)."""
    sonuc = []
    for (s1, a1), (s2, a2) in itertools.combinations(c, 2):
        if s1 == s2:
            teta = birlestir(a1, a2)
            if teta is not None:
                sonuc.append(_uygula(teta, c))
    return sonuc


def _derinlik(t) -> int:
    if isinstance(t, tuple):
        if len(t) == 2 and isinstance(t[0], bool):
            return _derinlik(t[1])
        return 1 + max((_derinlik(a) for a in t[1:]), default=0)
    return 0


def cozumleme(kb: list[frozenset], olumsuz_hedef: list[frozenset], max_adim: int = 5000,
              max_derinlik: int = 4, yanit_yuklemi: Optional[str] = None,
              tek_yanit: bool = False):
    """Destek kümesi stratejili çözümleme: her adımda en az bir ebeveyn hedeften türemiş olmalı.

    yanit_yuklemi verilirse (ör. "Yanit"), yalnızca bu yüklemin literallerinden oluşan bir
    tümce de "başarı" sayılır: ∃w sorgularında yanıtı çıkarmanın kitaptaki yöntemi.
    tek_yanit=True ise yalnızca TEK yanıt literali kalan tümce başarı sayılır (yapıcı yanıt).
    Döner: (bulundu mu, kanıt adımları [(t1, t2, çözümleyici, yerine koyma)]).
    """
    tumceler = list(kb) + list(olumsuz_hedef)
    destek = list(olumsuz_hedef)
    ebeveyn: dict = {}
    gorulen = set(tumceler)
    adim = 0
    while destek and adim < max_adim:
        destek.sort(key=len)  # birim tercihi: kısa tümceler önce
        c = destek.pop(0)
        for d in list(tumceler):
            for r, teta in cozumleyiciler(c, d):
                adim += 1
                adaylar = [r] + carpanla(r)
                for r2 in adaylar:
                    if r2 in gorulen or any(_derinlik(l) > max_derinlik for l in r2):
                        continue
                    gorulen.add(r2)
                    ebeveyn[r2] = (c, d, teta)
                    yanit_tumcesi = yanit_yuklemi and all(a[0] == yanit_yuklemi for _, a in r2)
                    if not r2 or (yanit_tumcesi and (len(r2) == 1 or not tek_yanit)):
                        return True, _kanit_izi(ebeveyn, r2)
                    tumceler.append(r2)
                    destek.append(r2)
    return False, []


def _kanit_izi(ebeveyn: dict, son: frozenset) -> list:
    """Kanıt adımlarını, her tümce kullanılmadan önce türetilecek sırayla döndür."""
    adimlar, gorulen = [], set()

    def gez(t):
        if t in gorulen or t not in ebeveyn:
            return
        gorulen.add(t)
        a, b, teta = ebeveyn[t]
        gez(a)
        gez(b)
        adimlar.append((a, b, t, teta))

    gez(son)
    return adimlar


KITAP_BIRLESTIRME = [
    ("Knows(John, x)", "Knows(John, Jane)"),
    ("Knows(John, x)", "Knows(y, Bill)"),
    ("Knows(John, x)", "Knows(y, Mother(y))"),
    ("Knows(John, x)", "Knows(x, Elizabeth)"),
]

if __name__ == "__main__":
    for a, b in KITAP_BIRLESTIRME:
        print(f"UNIFY({a}, {b}) = {yerine_yaz(birlestir(terim(a), terim(b)))}")
    print("Değişkenler ayrılınca:",
          yerine_yaz(birlestir(terim("Knows(John, x)"), terim("Knows(x17, Elizabeth)"))))
