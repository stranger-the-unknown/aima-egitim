#!/usr/bin/env python3
"""Varsayılan (default) / nonmonotonic oyuncak akıl yürütme.

Kural sezgisi:
  - Kuşlar (varsayılan olarak) uçar.
  - Penguenler kuştur ama uçmaz (istisna, varsayımdan önce gelir).

Özgün eğitim demosu; kitap metni değildir.

Resmi referans: https://aima.cs.berkeley.edu/ · https://github.com/aimacode
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set


@dataclass
class DefaultKB:
    """Basit olgu + istisna + varsayılan kural motoru."""

    kuslar: Set[str] = field(default_factory=set)
    penguenler: Set[str] = field(default_factory=set)
    # açıkça uçmaz denilenler (deve kuşu vb.)
    ucmaz_istisna: Set[str] = field(default_factory=set)
    # açıkça uçar denilenler (nadir override)
    ucar_kesin: Set[str] = field(default_factory=set)

    def tell_kus(self, ad: str) -> None:
        self.kuslar.add(ad)

    def tell_penguen(self, ad: str) -> None:
        self.penguenler.add(ad)
        self.kuslar.add(ad)  # penguen de kuş
        self.ucmaz_istisna.add(ad)

    def tell_ucmaz(self, ad: str) -> None:
        self.ucmaz_istisna.add(ad)

    def tell_ucar_kesin(self, ad: str) -> None:
        self.ucar_kesin.add(ad)

    def ucar_mi(self, ad: str) -> tuple[Optional[bool], str]:
        """(sonuç, gerekçe). Sonuç None = bilinmiyor."""
        if ad in self.ucar_kesin:
            return True, "kesin olgu: uçar"
        if ad in self.ucmaz_istisna or ad in self.penguenler:
            return False, "istisna: uçmaz (penguen veya açık istisna)"
        if ad in self.kuslar:
            return True, "varsayılan: kuş ⇒ uçar (aksi kanıt yok)"
        return None, "bilgi yok: kuş olduğu bilinmiyor"

    def ozet(self) -> None:
        herkes = sorted(self.kuslar | self.ucar_kesin | self.ucmaz_istisna)
        print("=== Varsayılan akıl demosu: kuşlar / penguenler ===")
        print(f"Kuşlar     : {sorted(self.kuslar)}")
        print(f"Penguenler : {sorted(self.penguenler)}")
        print(f"Uçmaz ist. : {sorted(self.ucmaz_istisna)}")
        print()
        for ad in herkes:
            sonuc, gerekce = self.ucar_mi(ad)
            if sonuc is True:
                etiket = "UÇAR"
            elif sonuc is False:
                etiket = "UÇMAZ"
            else:
                etiket = "?"
            print(f"  {ad:16} → {etiket:6}  ({gerekce})")


def demo() -> None:
    kb = DefaultKB()
    kb.tell_kus("serce")
    kb.tell_kus("kartal")
    kb.tell_penguen("pingu")
    kb.tell_kus("deve_kusu")
    kb.tell_ucmaz("deve_kusu")  # kuş ama uçmaz

    kb.ozet()

    print("\n--- Yeni bilgi: 'uçan_penguen_robot' kesin uçar ---")
    kb.tell_penguen("ucan_penguen_robot")
    # istisna listesinde; kesin uçar ile ezmek için:
    kb.ucar_kesin.add("ucan_penguen_robot")
    kb.ucmaz_istisna.discard("ucan_penguen_robot")
    sonuc, g = kb.ucar_mi("ucan_penguen_robot")
    print(f"  ucan_penguen_robot → {'UÇAR' if sonuc else 'UÇMAZ'} ({g})")

    print("\nNot: Yeni istisna eski varsayılan sonucu geri alabilir → nonmonotonic sezgi.")


if __name__ == "__main__":
    demo()
