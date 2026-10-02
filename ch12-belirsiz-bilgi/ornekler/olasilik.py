#!/usr/bin/env python3
"""Olasılık araçları (Bölüm 12): tam ortak dağılım ile çıkarım.

Bir olasılık modeli = olası dünyalar + her dünyanın olasılığı.
    OrtakDagilim(["Zar1", "Zar2"], {(1, 1): 1/36, (1, 2): 1/36, ...})

Önerme (olay): {değişken: değer} sözlüğü ya da dünya → bool fonksiyonu.
    P(olay)              : olayın doğru olduğu dünyaların olasılıkları toplamı  (12.2)
    kosullu(X, kanit)    : P(X | kanıt) = α Σ_y P(X, kanıt, y)                    (12.9)
    marjinal([X, Y])     : P(X, Y) = Σ_z P(X, Y, z)
    bagimsiz_mi(X, Y, Z) : P(X, Y | Z) = P(X | Z) P(Y | Z) her değer için mi?

Çalıştırınca kitaptaki zar örneklerini hesaplar:
    python olasilik.py
"""
from __future__ import annotations

import itertools
from fractions import Fraction
from typing import Callable, Union

Olay = Union[dict, Callable[[dict], bool]]


def normalize(dagilim: dict) -> dict:
    """α ile çarp: değerlerin toplamı 1 olsun."""
    toplam = sum(dagilim.values())
    if toplam == 0:
        raise ZeroDivisionError("Kanıtın olasılığı 0: bu kanıt modelde imkânsız")
    return {k: v / toplam for k, v in dagilim.items()}


class OrtakDagilim:
    def __init__(self, degiskenler: list[str], tablo: dict[tuple, float]):
        self.degiskenler = list(degiskenler)
        self.tablo = dict(tablo)

    def dunyalar(self):
        for degerler, p in self.tablo.items():
            yield dict(zip(self.degiskenler, degerler)), p

    def degerler(self, degisken: str) -> list:
        """Değişkenin değerleri, tabloda ilk görüldükleri sırayla."""
        i = self.degiskenler.index(degisken)
        return list(dict.fromkeys(d[i] for d in self.tablo))

    @staticmethod
    def _sagliyor(dunya: dict, olay: Olay) -> bool:
        if callable(olay):
            return olay(dunya)
        return all(dunya[k] == v for k, v in olay.items())

    def P(self, olay: Olay, kanit: Olay = None) -> float:
        """P(olay) ya da P(olay | kanıt) = P(olay ∧ kanıt) / P(kanıt)."""
        if kanit is None:
            return sum(p for d, p in self.dunyalar() if self._sagliyor(d, olay))
        pay = sum(p for d, p in self.dunyalar() if self._sagliyor(d, olay) and self._sagliyor(d, kanit))
        return pay / self.P(kanit)

    def kosullu(self, sorgu: Union[str, list[str]], kanit: dict = None) -> dict:
        """P(Sorgu | kanıt) dağılımı: kanıtla tutarlı dünyaları topla, sonra normalize et."""
        sorgu = [sorgu] if isinstance(sorgu, str) else list(sorgu)
        kanit = kanit or {}
        ham: dict = {}
        for d, p in self.dunyalar():
            if self._sagliyor(d, kanit):
                anahtar = tuple(d[x] for x in sorgu)
                anahtar = anahtar[0] if len(sorgu) == 1 else anahtar
                ham[anahtar] = ham.get(anahtar, 0) + p
        return normalize(ham)

    def marjinal(self, degiskenler: list[str]) -> "OrtakDagilim":
        tablo: dict = {}
        for d, p in self.dunyalar():
            k = tuple(d[x] for x in degiskenler)
            tablo[k] = tablo.get(k, 0) + p
        return OrtakDagilim(degiskenler, tablo)

    def bagimsiz_mi(self, X: str, Y: str, Z: str = None, tol: float = 1e-9) -> bool:
        """Z verilmezse mutlak, verilirse koşullu bağımsızlık."""
        z_degerleri = self.degerler(Z) if Z else [None]
        for z in z_degerleri:
            kanit = {Z: z} if Z else {}
            if self.P(kanit or (lambda d: True)) == 0:
                continue
            for x in self.degerler(X):
                for y in self.degerler(Y):
                    ortak = self.P({X: x, Y: y, **kanit}, kanit or None)
                    carpim = self.P({X: x, **kanit}, kanit or None) * self.P({Y: y, **kanit}, kanit or None)
                    if abs(ortak - carpim) > tol:
                        return False
        return True

    def carp(self, diger: "OrtakDagilim") -> "OrtakDagilim":
        """Bağımsız iki dağılımdan ortak dağılım: P(X, Y) = P(X) P(Y)."""
        tablo = {a + b: pa * pb for a, pa in self.tablo.items() for b, pb in diger.tablo.items()}
        return OrtakDagilim(self.degiskenler + diger.degiskenler, tablo)


def iki_zar() -> OrtakDagilim:
    """Adil iki zar: 36 olası dünya, her biri 1/36 (kesirlerle, yuvarlama yok)."""
    return OrtakDagilim(["Zar1", "Zar2"],
                        {(a, b): Fraction(1, 36) for a, b in itertools.product(range(1, 7), repeat=2)})


if __name__ == "__main__":
    z = iki_zar()
    print("=== İki adil zar: olası dünyalar ve olaylar ===")
    print(f"  P(Toplam = 11)       = {z.P(lambda d: d['Zar1'] + d['Zar2'] == 11)}   (kitap: 1/18)")
    print(f"  P(çift)              = {z.P(lambda d: d['Zar1'] == d['Zar2'])}")
    print(f"  P(çift | Zar1 = 5)   = {z.P(lambda d: d['Zar1'] == d['Zar2'], {'Zar1': 5})}")
    print(f"  P(Toplam=11 | Zar1=5)= {z.P(lambda d: d['Zar1'] + d['Zar2'] == 11, {'Zar1': 5})}")
    print(f"  Zar1 ve Zar2 bağımsız mı? {z.bagimsiz_mi('Zar1', 'Zar2')}")
    toplam = {s: z.P(lambda d, s=s: d['Zar1'] + d['Zar2'] == s) for s in range(2, 13)}
    print("  Toplamın dağılımı: " + ", ".join(f"{s}:{p}" for s, p in toplam.items()))
