#!/usr/bin/env python3
"""Küçük Horn KB üzerinde geriye zincirleme (backward chaining).

Özgün oyuncak senaryo: kampüs kayıp eşya / tanık zinciri (kitap metni değil).
Birleştirme çok basit (yalnız sabit + ?değişken atomları).

Resmi referans: https://aima.cs.berkeley.edu/ · https://github.com/aimacode
"""
from __future__ import annotations

from typing import Dict, Iterable, List, Optional, Set, Tuple

Atom = Tuple[str, ...]
Subst = Dict[str, str]
Rule = Tuple[List[Atom], Atom]  # oncesuller ⇒ sonuc


def degisken_mi(s: str) -> bool:
    return s.startswith("?")


def yaz_atom(a: Atom) -> str:
    if len(a) == 1:
        return a[0]
    return f"{a[0]}({', '.join(a[1:])})"


def coz(s: str, theta: Subst) -> str:
    """Değişkeni atamada son değere kadar takip et (döngü korumalı)."""
    gorulen: Set[str] = set()
    while degisken_mi(s) and s in theta:
        if s in gorulen:
            break
        gorulen.add(s)
        s = theta[s]
    return s


def birlestir(oruntu: Atom, olgu: Atom, theta: Subst) -> Optional[Subst]:
    if len(oruntu) != len(olgu) or oruntu[0] != olgu[0]:
        return None
    theta = dict(theta)
    for x, y in zip(oruntu[1:], olgu[1:]):
        x = coz(x, theta)
        y = coz(y, theta)
        if x == y:
            continue
        if degisken_mi(x):
            theta[x] = y
        elif degisken_mi(y):
            theta[y] = x
        else:
            return None
    return theta


def uygula(atom: Atom, theta: Subst) -> Atom:
    return (atom[0], *(coz(a, theta) for a in atom[1:]))


def temiz_cevap(theta: Subst, sorgu: Atom) -> Subst:
    """Sorgudaki değişkenlerin somut bağlarını döndür."""
    out: Subst = {}
    for a in sorgu[1:]:
        if degisken_mi(a):
            v = coz(a, theta)
            if not degisken_mi(v):
                out[a] = v
    return out


class GeriyeZincirKB:
    def __init__(self) -> None:
        self.olgular: List[Atom] = []
        self.kurallar: List[Rule] = []

    def tell_olgu(self, atom: Atom) -> None:
        self.olgular.append(atom)

    def tell_kural(self, oncesuller: List[Atom], sonuc: Atom) -> None:
        self.kurallar.append((oncesuller, sonuc))

    def ask(self, hedef: Atom, iz: bool = True) -> List[Subst]:
        self._derinlik = 0
        self._iz = iz
        self._max_derinlik = 30
        GeriyeZincirKB._kural_sayac = 0
        ham = list(self._bc([hedef], {}))
        # sorgu değişkenlerine göre sadeleştir; tekrarları at
        uniq: List[Subst] = []
        seen: Set[Tuple[Tuple[str, str], ...]] = set()
        for th in ham:
            c = temiz_cevap(th, hedef)
            key = tuple(sorted(c.items()))
            if key not in seen:
                seen.add(key)
                uniq.append(c)
        return uniq

    def _bc(self, hedefler: List[Atom], theta: Subst) -> Iterable[Subst]:
        if self._derinlik > self._max_derinlik:
            return
        if not hedefler:
            yield dict(theta)
            return
        ilk = uygula(hedefler[0], theta)
        kalan = hedefler[1:]
        girinti = "  " * self._derinlik

        if self._iz:
            print(f"{girinti}? {yaz_atom(ilk)}")

        for olgu in self.olgular:
            t2 = birlestir(ilk, olgu, theta)
            if t2 is not None:
                if self._iz:
                    print(f"{girinti}  ✓ olgu {yaz_atom(olgu)}")
                self._derinlik += 1
                yield from self._bc(kalan, t2)
                self._derinlik -= 1

        for oncesuller, sonuc in self.kurallar:
            # Kural değişkenlerini tazeleyelim (ad çakışması olmasın)
            taze = self._yeniden_adlandir(oncesuller, sonuc)
            oncesuller_t, sonuc_t = taze
            t2 = birlestir(ilk, sonuc_t, theta)
            if t2 is not None:
                if self._iz:
                    print(f"{girinti}  → kural {yaz_atom(sonuc)} ← …")
                self._derinlik += 1
                yield from self._bc(oncesuller_t + kalan, t2)
                self._derinlik -= 1

    _kural_sayac = 0

    def _yeniden_adlandir(
        self, oncesuller: List[Atom], sonuc: Atom
    ) -> Tuple[List[Atom], Atom]:
        GeriyeZincirKB._kural_sayac += 1
        tag = f"_{self._kural_sayac}"

        def rename_atom(a: Atom) -> Atom:
            return (a[0], *(f"{x}{tag}" if degisken_mi(x) else x for x in a[1:]))

        return [rename_atom(p) for p in oncesuller], rename_atom(sonuc)


def kur_kampus_kb() -> GeriyeZincirKB:
    """Özgün senaryo: kayıp USB kimde / tanık zinciri."""
    kb = GeriyeZincirKB()
    kb.tell_olgu(("Sahip", "USB", "Selin"))
    kb.tell_olgu(("Gordu", "Emre", "Selin", "Lab3"))
    kb.tell_olgu(("Gordu", "Ayla", "Emre", "Koridor"))
    kb.tell_olgu(("Guvenilir", "Ayla"))
    kb.tell_olgu(("Guvenilir", "Emre"))
    # Guvenilir(t) ∧ Gordu(t, k, yer) ∧ Sahip(esy, k) ⇒ SonGorulen(esy, yer)
    kb.tell_kural(
        [("Guvenilir", "?t"), ("Gordu", "?t", "?k", "?yer"), ("Sahip", "?esy", "?k")],
        ("SonGorulen", "?esy", "?yer"),
    )
    # Dolaylı tanık: A, B'yi gördü ve B eşyayı taşıyanı gördü ⇒ IzSur(esy, A)
    kb.tell_kural(
        [
            ("Guvenilir", "?t"),
            ("Gordu", "?t", "?k", "?yer"),
            ("Gordu", "?k", "?tasivan", "?yer2"),
            ("Sahip", "?esy", "?tasivan"),
        ],
        ("IzSur", "?esy", "?t"),
    )
    kb.tell_kural([("Sahip", "?esy", "?k")], ("Ilgili", "?esy", "?k"))
    return kb


def demo() -> None:
    print("=== Geriye zincirleme demosu (kampüs kayıp USB) ===\n")
    kb = kur_kampus_kb()
    print("Olgular:")
    for o in kb.olgular:
        print(f"  {yaz_atom(o)}")
    print("\nKurallar: SonGorulen / IzSur / Ilgili (Horn)\n")

    sorgular = [
        ("Ilgili", "USB", "Selin"),
        ("SonGorulen", "USB", "?yer"),
        ("IzSur", "USB", "?kim"),
        ("SonGorulen", "USB", "Kantin"),
    ]
    for s in sorgular:
        print(f"--- Ask {yaz_atom(s)} ---")
        cevaplar = kb.ask(s, iz=True)
        if cevaplar:
            for th in cevaplar:
                if th:
                    bag = ", ".join(f"{k}={v}" for k, v in sorted(th.items()))
                    print(f"SONUÇ: EVET ({bag})\n")
                else:
                    print("SONUÇ: EVET\n")
        else:
            print("SONUÇ: HAYIR\n")


if __name__ == "__main__":
    demo()
