#!/usr/bin/env python3
"""Küçük eğitim amaçlı FOL-benzeri KB — olgular + evrensel örnekleme / örüntü eşleme.

Tam teorem kanıtlayıcı DEĞİLDİR. Parent/Ancestor tarzı olgularla
∀-kurallarının somut sabitlere uygulanmasını gösterir.

Resmi referans: https://aima.cs.berkeley.edu/ · https://github.com/aimacode
"""
from __future__ import annotations

from typing import Dict, Iterable, List, Optional, Set, Tuple

# Atom: ("Yuklem", arg1, arg2, ...) — arg sabit (str) veya değişken (?x)
Atom = Tuple[str, ...]
Subst = Dict[str, str]


def degisken_mi(s: str) -> bool:
    return s.startswith("?")


def birlestir_arg(a: str, b: str, theta: Subst) -> Optional[Subst]:
    """İki argümanı birleştir; başarısızsa None."""
    theta = dict(theta)
    if degisken_mi(a):
        if a in theta:
            return birlestir_arg(theta[a], b, theta)
        if degisken_mi(b) and b in theta:
            return birlestir_arg(a, theta[b], theta)
        theta[a] = b if not degisken_mi(b) else theta.get(b, b)
        return theta
    if degisken_mi(b):
        return birlestir_arg(b, a, theta)
    return theta if a == b else None


def birlestir_atom(oruntu: Atom, olgu: Atom, theta: Optional[Subst] = None) -> Optional[Subst]:
    """Basit örüntü eşleme (sabit + değişken). Fonksiyon terimi yok."""
    if theta is None:
        theta = {}
    if len(oruntu) != len(olgu) or oruntu[0] != olgu[0]:
        return None
    for x, y in zip(oruntu[1:], olgu[1:]):
        theta = birlestir_arg(x, y, theta)
        if theta is None:
            return None
    return theta


def uygula(atom: Atom, theta: Subst) -> Atom:
    args = []
    for a in atom[1:]:
        while degisken_mi(a) and a in theta:
            a = theta[a]
        args.append(a)
    return (atom[0], *args)


class FolSozlukKB:
    """Olgular kümesi + Horn-benzeri kurallar (gövde ⇒ baş)."""

    def __init__(self) -> None:
        self.olgular: Set[Atom] = set()
        # kural: (oncesuller_listesi, sonuc)
        self.kurallar: List[Tuple[List[Atom], Atom]] = []

    def tell_olgu(self, atom: Atom) -> None:
        self.olgular.add(atom)

    def tell_kural(self, oncesuller: List[Atom], sonuc: Atom) -> None:
        self.kurallar.append((oncesuller, sonuc))

    def ask_olgu(self, sorgu: Atom) -> List[Subst]:
        """Doğrudan olgu eşlemesi — tüm birleştirmeler."""
        sonuclar: List[Subst] = []
        for olgu in self.olgular:
            theta = birlestir_atom(sorgu, olgu)
            if theta is not None:
                sonuclar.append(theta)
        return sonuclar

    def ileri_zincir_adim(self) -> int:
        """Tek tur: kuralları olgulara uygula (eğitim UI + eşleme). Yeni olgu sayısı."""
        yeni = 0
        mevcut = list(self.olgular)
        for oncesuller, sonuc in self.kurallar:
            for theta in self._eslestir_hepsi(oncesuller, mevcut):
                turetilen = uygula(sonuc, theta)
                if any(degisken_mi(a) for a in turetilen[1:]):
                    continue  # tamamen somut olmalı
                if turetilen not in self.olgular:
                    self.olgular.add(turetilen)
                    yeni += 1
        return yeni

    def doyur(self, max_tur: int = 20) -> int:
        toplam = 0
        for _ in range(max_tur):
            n = self.ileri_zincir_adim()
            toplam += n
            if n == 0:
                break
        return toplam

    def _eslestir_hepsi(
        self, oruntuler: List[Atom], olgular: List[Atom], theta: Optional[Subst] = None
    ) -> Iterable[Subst]:
        if theta is None:
            theta = {}
        if not oruntuler:
            yield dict(theta)
            return
        ilk, *kalan = oruntuler
        hedef = uygula(ilk, theta)
        for olgu in olgular:
            t2 = birlestir_atom(hedef, olgu, dict(theta))
            if t2 is not None:
                yield from self._eslestir_hepsi(kalan, olgular, t2)


def atom_yaz(a: Atom) -> str:
    if len(a) == 1:
        return a[0]
    return f"{a[0]}({', '.join(a[1:])})"


def demo() -> None:
    print("=== FOL sözlük KB demosu (Parent / Ancestor) ===\n")
    kb = FolSozlukKB()

    # Özgün mini aile — kitap metni değil
    olgular = [
        ("Ebeveyn", "Leyla", "Deniz"),
        ("Ebeveyn", "Mert", "Deniz"),
        ("Ebeveyn", "Deniz", "Ece"),
        ("Ebeveyn", "Deniz", "Kaan"),
    ]
    for o in olgular:
        kb.tell_olgu(o)
        print(f"  Tell olgu: {atom_yaz(o)}")

    # ∀x∀y Ebeveyn(x,y) ⇒ Ata(x,y)
    kb.tell_kural([("Ebeveyn", "?x", "?y")], ("Ata", "?x", "?y"))
    # ∀x∀y∀z Ebeveyn(x,z) ∧ Ata(z,y) ⇒ Ata(x,y)
    kb.tell_kural(
        [("Ebeveyn", "?x", "?z"), ("Ata", "?z", "?y")],
        ("Ata", "?x", "?y"),
    )
    print("\n  Tell kurallar: Ebeveyn ⇒ Ata ; Ebeveyn+Ata ⇒ Ata (geçişli)")

    n = kb.doyur()
    print(f"\n  İleri zincir: {n} yeni olgu türetildi.\n")

    print("--- Tüm Ata olguları ---")
    for o in sorted(a for a in kb.olgular if a[0] == "Ata"):
        print(f"  {atom_yaz(o)}")

    print("\n--- Sorgular (örüntü eşleme) ---")
    sorgular = [
        ("Ebeveyn", "Deniz", "?cocuk"),
        ("Ata", "Leyla", "Ece"),
        ("Ata", "Mert", "?torun"),
        ("Ata", "Ece", "Leyla"),  # beklenen: eşleşme yok
    ]
    for s in sorgular:
        cevaplar = kb.ask_olgu(s)
        if cevaplar:
            for th in cevaplar:
                if th:
                    bag = ", ".join(f"{k}={v}" for k, v in sorted(th.items()))
                    print(f"  Ask {atom_yaz(s)} → EVET ({bag})")
                else:
                    print(f"  Ask {atom_yaz(s)} → EVET")
        else:
            print(f"  Ask {atom_yaz(s)} → HAYIR")

    print("\nNot: Bu motor eğitim içindir; genel FOL ispatı yapmaz.")


if __name__ == "__main__":
    demo()
