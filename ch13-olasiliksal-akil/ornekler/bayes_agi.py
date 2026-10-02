#!/usr/bin/env python3
"""Bayes ağı kütüphanesi (Bölüm 13): Boole değişkenli ağlar, kesin ve yaklaşık çıkarım.

Ağ tanımı:
    ag = BayesAgi()
    ag.ekle("Burglary", [], {(): 0.001})
    ag.ekle("Alarm", ["Burglary", "Earthquake"], {(True, True): 0.95, (True, False): 0.94, ...})
CPT anahtarı: ebeveyn değerleri demeti, değer: P(düğüm = true | ebeveynler).
Düğümler topolojik sırada eklenmelidir (ebeveynler önce).

Kesin çıkarım
  * numaralandirma(X, kanit)   : ENUMERATION-ASK (13.3.1)
  * degisken_eleme(X, kanit)   : faktörlerle değişken eleme (13.3.2); ilgisiz değişkenler budanır
Yaklaşık çıkarım (13.4)
  * onsel_ornek, ret_ornekleme, olabilirlik_agirliklandirma, gibbs
Diğer
  * ortak(olay)       : P(x1, ..., xn) = Π P(xi | ebeveynler(Xi))      (13.2)
  * markov_ortusu(X)  : ebeveynler, çocuklar, çocukların diğer ebeveynleri
  * mudahale(X, v)    : do(X = v); X'e gelen okları kesen "sakatlanmış" ağ (13.5)

Çalıştırma: python bayes_agi.py  (küçük bir kendi kendini sınama)
"""
from __future__ import annotations

import itertools
import random
from typing import Optional


def normalize(d: dict) -> dict:
    z = sum(d.values())
    if z == 0:
        raise ZeroDivisionError("Kanıtın olasılığı 0")
    return {k: v / z for k, v in d.items()}


class BayesAgi:
    def __init__(self):
        self.degiskenler: list[str] = []
        self.ebeveynler: dict[str, list[str]] = {}
        self.cpt: dict[str, dict[tuple, float]] = {}
        self.carpma_sayisi = 0  # numaralandırma / eleme karşılaştırması için

    def ekle(self, ad: str, ebeveynler: list[str], cpt: dict) -> "BayesAgi":
        for e in ebeveynler:
            if e not in self.ebeveynler:
                raise ValueError(f"{ad} eklenmeden önce ebeveyni {e} eklenmeli (topolojik sıra)")
        self.degiskenler.append(ad)
        self.ebeveynler[ad] = list(ebeveynler)
        self.cpt[ad] = dict(cpt)
        return self

    def cocuklar(self, ad: str) -> list[str]:
        return [x for x in self.degiskenler if ad in self.ebeveynler[x]]

    def p(self, ad: str, deger: bool, olay: dict) -> float:
        """P(ad = deger | ebeveynlerin olaydaki değerleri)."""
        p_dogru = self.cpt[ad][tuple(olay[e] for e in self.ebeveynler[ad])]
        return p_dogru if deger else 1 - p_dogru

    def ortak(self, olay: dict) -> float:
        sonuc = 1.0
        for x in self.degiskenler:
            sonuc *= self.p(x, olay[x], olay)
        return sonuc

    def parametre_sayisi(self) -> int:
        return sum(2 ** len(self.ebeveynler[x]) for x in self.degiskenler)

    def markov_ortusu(self, ad: str) -> set:
        ortu = set(self.ebeveynler[ad])
        for c in self.cocuklar(ad):
            ortu.add(c)
            ortu.update(self.ebeveynler[c])
        ortu.discard(ad)
        return ortu

    # ------------------------------------------------------------------
    # Kesin çıkarım
    # ------------------------------------------------------------------
    def numaralandirma(self, X: str, kanit: dict, ham: bool = False) -> dict:
        """ENUMERATION-ASK: derinlik öncelikli, soldan sağa toplam–çarpım ağacı."""
        Q = {}
        for x in (True, False):
            Q[x] = self._hepsini_say(self.degiskenler, {**kanit, X: x})
        return Q if ham else normalize(Q)

    def _hepsini_say(self, degiskenler: list[str], e: dict) -> float:
        if not degiskenler:
            return 1.0
        V, geri = degiskenler[0], degiskenler[1:]
        if V in e:
            self.carpma_sayisi += 1
            return self.p(V, e[V], e) * self._hepsini_say(geri, e)
        toplam = 0.0
        for v in (True, False):
            self.carpma_sayisi += 1
            toplam += self.p(V, v, e) * self._hepsini_say(geri, {**e, V: v})
        return toplam

    def atalar(self, dugumler) -> set:
        sonuc, yigin = set(), list(dugumler)
        while yigin:
            x = yigin.pop()
            if x not in sonuc:
                sonuc.add(x)
                yigin.extend(self.ebeveynler[x])
        return sonuc

    def degisken_eleme(self, X: str, kanit: dict, sira: Optional[list[str]] = None) -> dict:
        """Faktörlerle değişken eleme. Sorgu ya da kanıtın atası olmayan değişkenler ilgisizdir
        ve hiç faktör oluşturmaz (kitaptaki budama)."""
        ilgili = self.atalar([X, *kanit])
        faktorler = [Faktor.cpt_den(self, x, kanit) for x in self.degiskenler if x in ilgili]
        gizli = [x for x in (sira or list(reversed(self.degiskenler))) if x in ilgili and x != X and x not in kanit]
        for h in gizli:
            icinde = [f for f in faktorler if h in f.degiskenler]
            disinda = [f for f in faktorler if h not in f.degiskenler]
            carpim = icinde[0]
            for f in icinde[1:]:
                carpim = carpim.carp(f, self)
            faktorler = disinda + [carpim.topla(h)]
        sonuc = faktorler[0]
        for f in faktorler[1:]:
            sonuc = sonuc.carp(f, self)
        return normalize({x: sonuc.tablo[(x,)] for x in (True, False)})

    def tam_ortak_tablo(self) -> dict:
        return {deg: self.ortak(dict(zip(self.degiskenler, deg)))
                for deg in itertools.product((True, False), repeat=len(self.degiskenler))}

    # ------------------------------------------------------------------
    # Yaklaşık çıkarım
    # ------------------------------------------------------------------
    def onsel_ornek(self, rng: random.Random) -> dict:
        olay = {}
        for x in self.degiskenler:
            olay[x] = rng.random() < self.p(x, True, olay)
        return olay

    def ret_ornekleme(self, X: str, kanit: dict, N: int, rng: random.Random) -> tuple[dict, int]:
        """Döner: (tahmin, kabul edilen örnek sayısı)."""
        sayim = {True: 0, False: 0}
        for _ in range(N):
            o = self.onsel_ornek(rng)
            if all(o[k] == v for k, v in kanit.items()):
                sayim[o[X]] += 1
        kabul = sayim[True] + sayim[False]
        return (normalize(sayim) if kabul else {True: float("nan"), False: float("nan")}), kabul

    def agirlikli_ornek(self, kanit: dict, rng: random.Random) -> tuple[dict, float]:
        w, olay = 1.0, {}
        for x in self.degiskenler:
            if x in kanit:
                olay[x] = kanit[x]
                w *= self.p(x, kanit[x], olay)
            else:
                olay[x] = rng.random() < self.p(x, True, olay)
        return olay, w

    def olabilirlik_agirliklandirma(self, X: str, kanit: dict, N: int, rng: random.Random) -> dict:
        W = {True: 0.0, False: 0.0}
        for _ in range(N):
            o, w = self.agirlikli_ornek(kanit, rng)
            W[o[X]] += w
        return normalize(W)

    def markov_ortusu_dagilimi(self, ad: str, durum: dict) -> float:
        """P(ad = true | Markov örtüsü) ∝ P(ad | ebeveynler) Π P(çocuk | ebeveynleri)."""
        ham = {}
        for v in (True, False):
            d = {**durum, ad: v}
            p = self.p(ad, v, d)
            for c in self.cocuklar(ad):
                p *= self.p(c, d[c], d)
            ham[v] = p
        return normalize(ham)[True]

    def gibbs(self, X: str, kanit: dict, N: int, rng: random.Random, isinma: int = 0) -> dict:
        durum = {x: kanit.get(x, rng.random() < 0.5) for x in self.degiskenler}
        gizli = [x for x in self.degiskenler if x not in kanit]
        sayim = {True: 0, False: 0}
        for t in range(N + isinma):
            z = rng.choice(gizli)
            durum[z] = rng.random() < self.markov_ortusu_dagilimi(z, durum)
            if t >= isinma:
                sayim[durum[X]] += 1
        return normalize(sayim)

    # ------------------------------------------------------------------
    # Nedensel ağlar
    # ------------------------------------------------------------------
    def mudahale(self, ad: str, deger: bool) -> "BayesAgi":
        """do(ad = deger): ad'ın ebeveyn bağlarını kes, değerini sabitle."""
        yeni = BayesAgi()
        for x in self.degiskenler:
            if x == ad:
                yeni.ekle(x, [], {(): 1.0 if deger else 0.0})
            else:
                yeni.ekle(x, self.ebeveynler[x], self.cpt[x])
        return yeni


class Faktor:
    """Boole değişkenler üzerinde bir tablo: f(degiskenler) → sayı."""

    def __init__(self, degiskenler: list[str], tablo: dict[tuple, float]):
        self.degiskenler = degiskenler
        self.tablo = tablo

    @classmethod
    def cpt_den(cls, ag: BayesAgi, ad: str, kanit: dict) -> "Faktor":
        degiskenler = [x for x in [ad] + ag.ebeveynler[ad] if x not in kanit]
        tablo = {}
        for degerler in itertools.product((True, False), repeat=len(degiskenler)):
            olay = {**kanit, **dict(zip(degiskenler, degerler))}
            tablo[degerler] = ag.p(ad, olay[ad], olay)
        return cls(degiskenler, tablo)

    def carp(self, diger: "Faktor", ag: Optional[BayesAgi] = None) -> "Faktor":
        degiskenler = self.degiskenler + [x for x in diger.degiskenler if x not in self.degiskenler]
        tablo = {}
        for degerler in itertools.product((True, False), repeat=len(degiskenler)):
            d = dict(zip(degiskenler, degerler))
            tablo[degerler] = (self.tablo[tuple(d[x] for x in self.degiskenler)]
                               * diger.tablo[tuple(d[x] for x in diger.degiskenler)])
            if ag is not None:
                ag.carpma_sayisi += 1
        return Faktor(degiskenler, tablo)

    def topla(self, degisken: str) -> "Faktor":
        i = self.degiskenler.index(degisken)
        kalan = self.degiskenler[:i] + self.degiskenler[i + 1:]
        tablo: dict = {}
        for degerler, p in self.tablo.items():
            k = degerler[:i] + degerler[i + 1:]
            tablo[k] = tablo.get(k, 0.0) + p
        return Faktor(kalan, tablo)


def gurultulu_or(q: dict[str, float], sizinti: float = 0.0) -> dict[tuple, float]:
    """Gürültülü-VEYA CPT'si. q[neden] = o neden tek başına varken etkinin OLMAMA olasılığı.
    P(¬etki | nedenler) = (1 − sızıntı) × Π_{doğru nedenler} q."""
    nedenler = list(q)
    cpt = {}
    for degerler in itertools.product((True, False), repeat=len(nedenler)):
        p_yok = 1 - sizinti
        for n, v in zip(nedenler, degerler):
            if v:
                p_yok *= q[n]
        cpt[degerler] = 1 - p_yok
    return cpt


if __name__ == "__main__":
    # Kitaptaki Toothache–Catch–Cavity ağı (Bölüm 12'deki tablodan): aynı sonuçlar çıkmalı
    ag = BayesAgi()
    ag.ekle("Cavity", [], {(): 0.2})
    ag.ekle("Toothache", ["Cavity"], {(True,): 0.6, (False,): 0.1})
    ag.ekle("Catch", ["Cavity"], {(True,): 0.9, (False,): 0.2})
    print("P(Cavity | toothache, catch):")
    print("  numaralandırma :", {k: round(v, 3) for k, v in ag.numaralandirma("Cavity", {"Toothache": True, "Catch": True}).items()})
    print("  değişken eleme :", {k: round(v, 3) for k, v in ag.degisken_eleme("Cavity", {"Toothache": True, "Catch": True}).items()})
    print(f"  Parametre sayısı: {ag.parametre_sayisi()} (tam tablo 7)")
    print(f"  P(toothache, catch, cavity) = {ag.ortak({'Cavity': True, 'Toothache': True, 'Catch': True}):.3f} (tablo: 0.108)")
