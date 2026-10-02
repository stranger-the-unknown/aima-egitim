#!/usr/bin/env python3
"""Bölüm 6'nın CSP araçları: tek dosyada, okunaklı hâlde.

İçerik
  * CSP              : değişkenler, alanlar, komşular ve ikili kısıt fonksiyonu
  * ac3              : yay tutarlılığı (kitaptaki AC-3)
  * geri_izleme      : MRV / derece / LCV sezgiselleri; çıkarım yok / ileri kontrol / MAC
  * min_catisma      : yerel arama
  * agac_coz         : ağaç yapılı CSP'ler için O(n·d²) çözücü
  * kesme_kumesi_coz : döngü kesme kümesiyle koşullandırma

Yalnızca **ikili** kısıtlar desteklenir: kisit(A, a, B, b) → True ise A=a ile B=b uyumludur.
Çalıştırınca küçük bir kendi kendini sınama yapar:
    python kisit.py
"""
from __future__ import annotations

import random
from collections import deque
from dataclasses import dataclass, field
from typing import Callable, Hashable, Optional

Degisken = Hashable
Kisit = Callable[[Degisken, object, Degisken, object], bool]


def farkli(A, a, B, b) -> bool:
    """En yaygın ikili kısıt: komşular farklı değer almalı."""
    return a != b


class CSP:
    def __init__(self, degiskenler, alanlar: dict, komsular: dict, kisit: Kisit = farkli) -> None:
        self.degiskenler = list(degiskenler)
        self.alanlar = {v: list(alanlar[v]) for v in self.degiskenler}
        self.komsular = {v: list(komsular.get(v, [])) for v in self.degiskenler}
        self.kisit = kisit

    def catisma_sayisi(self, X, x, atama: dict) -> int:
        return sum(1 for Y in self.komsular[X] if Y in atama and not self.kisit(X, x, Y, atama[Y]))

    def tutarli(self, X, x, atama: dict) -> bool:
        return self.catisma_sayisi(X, x, atama) == 0

    def cozum_mu(self, atama: dict) -> bool:
        return len(atama) == len(self.degiskenler) and all(
            self.tutarli(X, atama[X], atama) for X in self.degiskenler)

    def yaylar(self):
        return [(X, Y) for X in self.degiskenler for Y in self.komsular[X]]


# ---------------------------------------------------------------------------
# Yay tutarlılığı
# ---------------------------------------------------------------------------

def _duzelt(csp: CSP, alanlar: dict, Xi, Xj, sayac: dict) -> bool:
    """Xi'nin alanından, Xj'de destekçisi olmayan değerleri sil. Silme olduysa True."""
    silindi = False
    for x in list(alanlar[Xi]):
        sayac["kontrol"] += len(alanlar[Xj])
        if not any(csp.kisit(Xi, x, Xj, y) for y in alanlar[Xj]):
            alanlar[Xi].remove(x)
            silindi = True
    return silindi


def ac3(csp: CSP, alanlar: Optional[dict] = None, kuyruk=None, sayac: Optional[dict] = None):
    """Kitaptaki AC-3. Döner: (tutarlı mı, yeni alanlar).

    `alanlar` verilmezse CSP'nin alanlarının bir kopyası kullanılır; orijinal değişmez.
    """
    alanlar = {v: list(d) for v, d in (alanlar or csp.alanlar).items()}
    sayac = sayac if sayac is not None else {"kontrol": 0}
    kuyruk = deque(kuyruk if kuyruk is not None else csp.yaylar())
    kuyrukta = set(kuyruk)
    while kuyruk:
        Xi, Xj = kuyruk.popleft()
        kuyrukta.discard((Xi, Xj))
        if _duzelt(csp, alanlar, Xi, Xj, sayac):
            if not alanlar[Xi]:
                return False, alanlar
            for Xk in csp.komsular[Xi]:
                if Xk != Xj and (Xk, Xi) not in kuyrukta:
                    kuyruk.append((Xk, Xi))
                    kuyrukta.add((Xk, Xi))
    return True, alanlar


# ---------------------------------------------------------------------------
# Geri izleme araması
# ---------------------------------------------------------------------------

@dataclass
class Istatistik:
    atama: int = 0        # denenen (değişken, değer) atamaları
    geri_donus: int = 0   # başarısız olup geri alınan atamalar
    izler: list = field(default_factory=list)


def geri_izleme(csp: CSP, degisken_sec: str = "sirali", deger_sirala: str = "sirali",
                cikarim: str = "yok", tum_cozumler: bool = False,
                iz: bool = False) -> tuple[list[dict], Istatistik]:
    """Kitaptaki BACKTRACKING-SEARCH.

    degisken_sec : "sirali" | "mrv" (en az kalan değer; eşitlikte derece) | "derece"
    deger_sirala : "sirali" | "lcv" (komşulara en az kısıt koyan değer önce)
    cikarim      : "yok" | "ileri" (ileri kontrol) | "mac" (yay tutarlılığını koru)
    Döner: (bulunan çözümler, istatistik). tum_cozumler=False ise en fazla bir çözüm.
    """
    ist = Istatistik()
    cozumler: list[dict] = []

    def yasal(X, atama, alanlar):
        return [x for x in alanlar[X] if csp.tutarli(X, x, atama)]

    def sec(atama, alanlar):
        kalan = [v for v in csp.degiskenler if v not in atama]
        derece = lambda v: sum(1 for Y in csp.komsular[v] if Y not in atama)  # noqa: E731
        if degisken_sec == "mrv":
            return min(kalan, key=lambda v: (len(yasal(v, atama, alanlar)), -derece(v)))
        if degisken_sec == "derece":
            return max(kalan, key=derece)
        return kalan[0]

    def sirala(X, atama, alanlar):
        degerler = yasal(X, atama, alanlar) if cikarim == "yok" else list(alanlar[X])
        if deger_sirala == "lcv":
            def elenen(x):
                return sum(1 for Y in csp.komsular[X] if Y not in atama
                           for y in alanlar[Y] if not csp.kisit(X, x, Y, y))
            degerler.sort(key=elenen)
        return degerler

    def cikar(X, x, atama, alanlar):
        """Çıkarım yap; yeni alanlar ya da başarısızlık için None döndür."""
        yeni = {v: list(d) for v, d in alanlar.items()}
        yeni[X] = [x]
        if cikarim == "ileri":
            for Y in csp.komsular[X]:
                if Y not in atama:
                    yeni[Y] = [y for y in yeni[Y] if csp.kisit(X, x, Y, y)]
                    if not yeni[Y]:
                        return None
            return yeni
        if cikarim == "mac":
            kuyruk = [(Y, X) for Y in csp.komsular[X] if Y not in atama]
            tamam, yeni = ac3(csp, yeni, kuyruk)
            return yeni if tamam else None
        return yeni

    def ara(atama, alanlar) -> bool:
        if len(atama) == len(csp.degiskenler):
            cozumler.append(dict(atama))
            return not tum_cozumler
        X = sec(atama, alanlar)
        for x in sirala(X, atama, alanlar):
            if not csp.tutarli(X, x, atama):
                continue
            ist.atama += 1
            atama[X] = x
            yeni = cikar(X, x, atama, alanlar)
            if iz:
                ist.izler.append((X, x, None if yeni is None else {v: list(d) for v, d in yeni.items()}))
            if yeni is not None and ara(atama, yeni):
                return True
            del atama[X]
            ist.geri_donus += 1
        return False

    ara({}, {v: list(d) for v, d in csp.alanlar.items()})
    return cozumler, ist


# ---------------------------------------------------------------------------
# Min-çatışma (yerel arama)
# ---------------------------------------------------------------------------

def min_catisma(csp: CSP, max_adim: int = 100_000, rng: Optional[random.Random] = None):
    """Döner: (çözüm ya da None, adım sayısı)."""
    rng = rng or random.Random(0)
    atama = {}
    for X in csp.degiskenler:  # açgözlü başlangıç: her değişkene en az çatışan değer
        atama[X] = min(csp.alanlar[X], key=lambda x: (csp.catisma_sayisi(X, x, atama), rng.random()))
    for adim in range(max_adim):
        catisanlar = [X for X in csp.degiskenler if csp.catisma_sayisi(X, atama[X], atama)]
        if not catisanlar:
            return atama, adim
        X = rng.choice(catisanlar)
        atama[X] = min(csp.alanlar[X], key=lambda x: (csp.catisma_sayisi(X, x, atama), rng.random()))
    return None, max_adim


# ---------------------------------------------------------------------------
# Problemin yapısı: ağaçlar ve kesme kümeleri
# ---------------------------------------------------------------------------

def agac_coz(csp: CSP, kok=None, alanlar: Optional[dict] = None) -> Optional[dict]:
    """Kitaptaki TREE-CSP-SOLVER. Kısıt grafı bir ormansa O(n·d²) sürede çözer."""
    alanlar = {v: list(d) for v, d in (alanlar or csp.alanlar).items()}
    atama: dict = {}
    ziyaret: set = set()
    for baslangic in ([kok] if kok is not None else []) + csp.degiskenler:
        if baslangic in ziyaret:
            continue
        # 1. Topolojik sıra (BFS) ve ebeveynler
        sira, ebeveyn = [baslangic], {baslangic: None}
        ziyaret.add(baslangic)
        i = 0
        while i < len(sira):
            for Y in csp.komsular[sira[i]]:
                if Y not in ziyaret:
                    ziyaret.add(Y)
                    ebeveyn[Y] = sira[i]
                    sira.append(Y)
                elif Y != ebeveyn[sira[i]] and ebeveyn.get(Y) != sira[i]:
                    raise ValueError("kısıt grafı ağaç değil (döngü var)")
            i += 1
        # 2. Yapraklardan köke yönlü yay tutarlılığı
        sayac = {"kontrol": 0}
        for Xj in reversed(sira[1:]):
            _duzelt(csp, alanlar, ebeveyn[Xj], Xj, sayac)
            if not alanlar[ebeveyn[Xj]]:
                return None
        # 3. Kökten yapraklara atama (geri izleme gerekmez)
        for X in sira:
            uygun = [x for x in alanlar[X]
                     if ebeveyn[X] is None or csp.kisit(X, x, ebeveyn[X], atama[ebeveyn[X]])]
            if not uygun:
                return None
            atama[X] = uygun[0]
    return atama


def kesme_kumesi_coz(csp: CSP, kesme: list) -> Optional[dict]:
    """Döngü kesme kümesiyle koşullandırma: kesme değişkenlerinin her tutarlı ataması
    için kalan (ağaç) CSP'yi çöz."""
    from itertools import product

    kalan = [v for v in csp.degiskenler if v not in kesme]
    alt = CSP(kalan, csp.alanlar, {v: [Y for Y in csp.komsular[v] if Y in kalan] for v in kalan}, csp.kisit)
    for degerler in product(*(csp.alanlar[v] for v in kesme)):
        atama = dict(zip(kesme, degerler))
        if not all(csp.tutarli(v, atama[v], atama) for v in kesme):
            continue
        alanlar = {v: [x for x in csp.alanlar[v] if csp.tutarli(v, x, atama)] for v in kalan}
        if any(not d for d in alanlar.values()):
            continue
        cozum = agac_coz(alt, alanlar=alanlar)
        if cozum is not None:
            return {**atama, **cozum}
    return None


if __name__ == "__main__":
    # Üçgen + bir kuyruk: A-B-C üçgen, C-D
    komsu = {"A": ["B", "C"], "B": ["A", "C"], "C": ["A", "B", "D"], "D": ["C"]}
    csp = CSP("ABCD", {v: ["k", "y", "m"] for v in "ABCD"}, komsu)
    for ayar in [("sirali", "sirali", "yok"), ("mrv", "lcv", "mac")]:
        c, ist = geri_izleme(csp, *ayar)
        print(f"{ayar}: {c[0]}  atama={ist.atama}")
    print("AC-3 (tutarlı mı):", ac3(csp)[0])
    print("min-çatışma:", min_catisma(csp))
    print("kesme kümesi {C}:", kesme_kumesi_coz(csp, ["C"]))
