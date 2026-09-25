#!/usr/bin/env python3
"""Küçük kategori hiyerarşisi ve is_a kalıtım sorguları.

Özgün eğitim örneği (kitap metni değil): Hayvan → Memeli → Kedi vb.

Resmi referans: https://aima.cs.berkeley.edu/ · https://github.com/aimacode
"""
from __future__ import annotations

from typing import Dict, Iterable, List, Optional, Set


class MiniOntoloji:
    """Üst kategori haritası + örnek üyelikleri."""

    def __init__(self) -> None:
        # alt_kategori -> doğrudan üst
        self.ust: Dict[str, Optional[str]] = {}
        # nesne -> ait olduğu kategori
        self.uye: Dict[str, str] = {}
        # kategori -> kısa Türkçe özellikler (kalıtım için)
        self.ozellik: Dict[str, List[str]] = {}

    def kategori(self, ad: str, ust: Optional[str] = None, *ozellikler: str) -> None:
        if ust is not None and ust not in self.ust and ust not in self.ozellik:
            # Üst henüz yoksa boş kaydet
            self.ust.setdefault(ust, None)
            self.ozellik.setdefault(ust, [])
        self.ust[ad] = ust
        self.ozellik[ad] = list(ozellikler)

    def ornek_ekle(self, nesne: str, kategori: str) -> None:
        if kategori not in self.ust:
            raise KeyError(f"Bilinmeyen kategori: {kategori}")
        self.uye[nesne] = kategori

    def is_a(self, alt: str, ust: str) -> bool:
        """alt, ust ile aynı mı veya ust'un altında mı?"""
        if alt == ust:
            return True
        gorulen: Set[str] = set()
        cur: Optional[str] = alt
        while cur is not None:
            if cur in gorulen:
                break
            gorulen.add(cur)
            if cur == ust:
                return True
            cur = self.ust.get(cur)
        return False

    def atalar(self, kategori: str) -> List[str]:
        zincir: List[str] = []
        cur: Optional[str] = kategori
        gorulen: Set[str] = set()
        while cur is not None and cur not in gorulen:
            zincir.append(cur)
            gorulen.add(cur)
            cur = self.ust.get(cur)
        return zincir

    def miras_ozellikler(self, kategori: str) -> List[str]:
        """Alttan üste: kendi + ataların özellikleri (tekrarsız, sıra korunur)."""
        sonuc: List[str] = []
        gorulen: Set[str] = set()
        for kat in self.atalar(kategori):
            for o in self.ozellik.get(kat, []):
                if o not in gorulen:
                    gorulen.add(o)
                    sonuc.append(o)
        return sonuc

    def nesne_kategorileri(self, nesne: str) -> List[str]:
        if nesne not in self.uye:
            return []
        return self.atalar(self.uye[nesne])

    def yazdir_agac(self, kok: str, girinti: int = 0) -> None:
        print("  " * girinti + f"- {kok}")
        cocuklar = sorted(k for k, u in self.ust.items() if u == kok)
        for c in cocuklar:
            self.yazdir_agac(c, girinti + 1)


def demo() -> None:
    o = MiniOntoloji()
    o.kategori("Hayvan", None, "canlı", "hareket_edebilir")
    o.kategori("Memeli", "Hayvan", "sıcakkanlı", "süt_emer")
    o.kategori("Kedi", "Memeli", "miyavlar")
    o.kategori("Kopek", "Memeli", "havlar")
    o.kategori("Kus", "Hayvan", "tüylü")
    o.kategori("Penguen", "Kus", "yüzer")

    o.ornek_ekle("minnos", "Kedi")
    o.ornek_ekle("karabas", "Kopek")
    o.ornek_ekle("pingu", "Penguen")

    print("=== Mini ontoloji ağacı (Hayvan kökü) ===")
    o.yazdir_agac("Hayvan")

    print("\n=== is_a sorguları ===")
    sorgular = [
        ("Kedi", "Memeli"),
        ("Kedi", "Hayvan"),
        ("Kopek", "Kedi"),
        ("Penguen", "Hayvan"),
        ("Memeli", "Kedi"),
    ]
    for alt, ust in sorgular:
        sonuc = "EVET" if o.is_a(alt, ust) else "HAYIR"
        print(f"  is_a({alt}, {ust}) → {sonuc}")

    print("\n=== Örnek üyelik + kalıtım ===")
    for nesne in ("minnos", "karabas", "pingu"):
        cats = o.nesne_kategorileri(nesne)
        oz = o.miras_ozellikler(o.uye[nesne])
        print(f"  {nesne}: kategoriler={cats}")
        print(f"           miras özellikler={oz}")

    print("\n=== Tekir alt kategorisi (kalıtım kontrolü) ===")
    o.kategori("Tekir", "Kedi", "çizgili")
    o.ornek_ekle("pamuk", "Tekir")
    print(f"  is_a(Tekir, Memeli) → {'EVET' if o.is_a('Tekir', 'Memeli') else 'HAYIR'}")
    print(f"  pamuk miras → {o.miras_ozellikler('Tekir')}")


if __name__ == "__main__":
    demo()
