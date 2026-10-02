#!/usr/bin/env python3
"""Çözümleme ile kanıt: Kediyi Curiosity mi öldürdü? (kitaptaki örnek)

Doğal dilde:
    Tüm hayvanları seven herkes, biri tarafından sevilir.
    Bir hayvanı öldüren kimse sevilmez.
    Jack tüm hayvanları sever.
    Kediyi (adı Tuna) ya Jack ya da Curiosity öldürdü.
    Soru: Kediyi Curiosity mi öldürdü?

Kitaptaki CNF tümceleri (F ve G Skolem fonksiyonları):
    A1. Animal(F(x)) ∨ Loves(G(x), x)
    A2. ¬Loves(x, F(x)) ∨ Loves(G(x), x)
    B.  ¬Loves(y, x) ∨ ¬Animal(z) ∨ ¬Kills(x, z)
    C.  ¬Animal(x) ∨ Loves(Jack, x)
    D.  Kills(Jack, Tuna) ∨ Kills(Curiosity, Tuna)
    E.  Cat(Tuna)
    F.  ¬Cat(x) ∨ Animal(x)
    ¬G. ¬Kills(Curiosity, Tuna)

Çalıştırma:
    python kedi_cozumleme.py
"""
from __future__ import annotations

from fol_cikarim import cozumleme, tamamla, tumce, tumce_yaz, yaz

KB = {
    "A1": "Animal(F(x)) | Loves(G(x), x)",
    "A2": "~Loves(x, F(x)) | Loves(G(x), x)",
    "B": "~Loves(y, x) | ~Animal(z) | ~Kills(x, z)",
    "C": "~Animal(x) | Loves(Jack, x)",
    "D": "Kills(Jack, Tuna) | Kills(Curiosity, Tuna)",
    "E": "Cat(Tuna)",
    "F": "~Cat(x) | Animal(x)",
}


def kanit(hedef_degili: str, yanit: bool = False, tek: bool = False):
    return cozumleme([tumce(t) for t in KB.values()], [tumce(hedef_degili)],
                     yanit_yuklemi="Yanit" if yanit else None, tek_yanit=tek)


def kim_oldurdu(tek: bool) -> str:
    """∃w Kills(w, Tuna) sorgusunun değili ¬Kills(w, Tuna)'ya Yanit(w) literali eklenir.
    Yalnızca Yanit(…) kalan tümce, w'nin kanıtta hangi değeri aldığını gösterir."""
    bulundu, adimlar = kanit("~Kills(w, Tuna) | Yanit(w)", yanit=True, tek=tek)
    return tumce_yaz(adimlar[-1][2]) if bulundu else "bulunamadı"


def main() -> None:
    for ad, t in KB.items():
        print(f"  {ad:>3}. {t.replace('~', '¬').replace(' | ', ' ∨ ')}")
    print("  ¬G. ¬Kills(Curiosity, Tuna)\n")

    bulundu, adimlar = kanit("~Kills(Curiosity, Tuna)")
    print(f"Boş tümce türetildi mi? {bulundu}  ({len(adimlar)} çözümleme adımı)")
    for a, b, r, _ in adimlar:
        print(f"  ({tumce_yaz(a)})\n    + ({tumce_yaz(b)})\n    → {tumce_yaz(r)}")
    print("Kitaptaki kanıtta olduğu gibi Loves(G(Jack), Jack) gibi ara sonuçlar Skolem"
          "\nfonksiyonları (F, G) içerir; birleştirme bunları sıradan terimler gibi ele alır.")

    print("\n=== 'Kediyi kim öldürdü?': yanıt çıkarma ===")
    print(f"  Hedef: ∃w Kills(w, Tuna).  İlk bulunan yanıt tümcesi: {kim_oldurdu(False)}")
    print("  Bu YAPICI OLMAYAN bir yanıttır: Birinin öldürdüğü kanıtlandı ama kim olduğu belirsiz"
          "\n  (yalnızca D tümcesi kullanıldı). Tek yanıt literali kalana kadar aramayı sürdürünce:")
    print(f"  Yapıcı yanıt: {kim_oldurdu(True)}")

    print("\n=== Jack öldürmedi: KB ⊨ ¬Kills(Jack, Tuna) ===")
    bulundu, adimlar = kanit("Kills(Jack, Tuna)")
    print(f"  Boş tümce türetildi mi? {bulundu}  ({len(adimlar)} adım)")
    print("  Jack tüm hayvanları sever → biri Jack'i sever → hayvan öldüren kimse sevilmez"
          "\n  → Jack hiçbir hayvanı, dolayısıyla Tuna'yı öldüremez.")


if __name__ == "__main__":
    main()
