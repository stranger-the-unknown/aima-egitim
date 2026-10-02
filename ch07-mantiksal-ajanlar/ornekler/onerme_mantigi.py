#!/usr/bin/env python3
"""Bilgi tabanı: TELL ve ASK; geçerlilik, karşılanabilirlik, eşdeğerlik.

Bilgi tabanlı ajanın iki temel işlemi:
    TELL(KB, cümle)  — bilgi tabanına yeni bir cümle ekle
    ASK(KB, α)       — KB ⊨ α mı? (α, KB'nin doğru olduğu HER modelde doğru mu?)

ASK'in üç olası yanıtı vardır: "evet" (KB ⊨ α), "hayır" (KB ⊨ ¬α) ve
"bilinmiyor" (ikisi de değil). Mantık, bilinmeyeni uydurmaz.

Çalıştırma:
    python onerme_mantigi.py
"""
from __future__ import annotations

from itertools import product

from onerme import ayristir, dogru_mu, semboller, tt_gerektirir, ve, yaz


class BilgiTabani:
    def __init__(self) -> None:
        self.cumleler: list = []

    def tell(self, metin: str) -> None:
        self.cumleler.append(ayristir(metin))

    def ask(self, metin: str) -> str:
        alfa = ayristir(metin)
        kb = ve(*self.cumleler)
        if tt_gerektirir(kb, alfa)[0]:
            return "evet"
        if tt_gerektirir(kb, ("~", alfa))[0]:
            return "hayır"
        return "bilinmiyor"


def gecerli_mi(metin: str) -> bool:
    """Her modelde doğru (totoloji) mu?"""
    e = ayristir(metin)
    semb = sorted(semboller(e))
    return all(dogru_mu(e, dict(zip(semb, d))) for d in product([False, True], repeat=len(semb)))


def karsilanabilir_mi(metin: str) -> bool:
    """En az bir modelde doğru mu? (¬α geçerli değilse)"""
    return not gecerli_mi(f"~({metin})")


def esdeger_mi(a: str, b: str) -> bool:
    return gecerli_mi(f"({a}) <=> ({b})")


def main() -> None:
    kb = BilgiTabani()
    print("=== TELL ===")
    for c in ["Yagmur => IslakZemin", "Bulut | Yagmur", "Yagmur"]:
        kb.tell(c)
        print(f"  TELL: {yaz(ayristir(c))}")

    print("\n=== ASK ===")
    for soru in ["IslakZemin", "Bulut", "~Bulut", "Bulut | IslakZemin", "~IslakZemin"]:
        print(f"  ASK: {yaz(ayristir(soru)):<24} → {kb.ask(soru)}")
    print("  'Bulut' için cevap 'bilinmiyor': Yağmur yağıyor olsa da bulut hakkında bilgimiz yok.")
    print("  KB'nin doğru olduğu modellerin bazısında Bulut doğru, bazısında yanlış.")

    print("\n=== Geçerlilik, karşılanabilirlik, eşdeğerlik ===")
    for c in ["P | ~P", "P & ~P", "(P => Q) & P => Q", "P => Q"]:
        print(f"  {yaz(ayristir(c)):<28} geçerli: {str(gecerli_mi(c)):<5}  karşılanabilir: {karsilanabilir_mi(c)}")
    ciftler = [("P => Q", "~Q => ~P"), ("P => Q", "Q => P"), ("~(P & Q)", "~P | ~Q"), ("P <=> Q", "(P => Q) & (Q => P)")]
    for a, b in ciftler:
        print(f"  {yaz(ayristir(a)):<14} ≡ {yaz(ayristir(b)):<22}? {esdeger_mi(a, b)}")
    print("\n  Karşıt ters (contrapositive) eşdeğerdir; ters (converse) değildir.")
    print("  Tümdengelim teoremi: KB ⊨ α ⟺ (KB ⇒ α) geçerlidir.")
    print("  Çelişki ile kanıt   : KB ⊨ α ⟺ (KB ∧ ¬α) karşılanamaz.")


if __name__ == "__main__":
    main()
