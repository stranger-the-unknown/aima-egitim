#!/usr/bin/env python3
"""Horn tümceleriyle ileri ve geri zincirleme (kitaptaki örnek).

Bilgi tabanı (kesin tümceler):
    P ⇒ Q        L ∧ M ⇒ P      B ∧ L ⇒ M
    A ∧ P ⇒ L    A ∧ B ⇒ L      A      B
Sorgu: Q

İleri zincirleme veri güdümlüdür: bilinen gerçeklerden başlar, öncülleri tamamlanan
her kuralı "ateşler". Geri zincirleme hedef güdümlüdür: Q'dan başlar ve Q'yu
kanıtlamak için gereken alt hedeflere iner. İkisi de Horn tümcelerinde tam ve
doğrusal zamanlıdır.

Çalıştırma:
    python ileri_geri_zincirleme.py
"""
from __future__ import annotations

from onerme import ayristir, cnf, geri_zincirleme, ileri_zincirleme, sat_gerektirir

KURALLAR = [
    (["P"], "Q"),
    (["L", "M"], "P"),
    (["B", "L"], "M"),
    (["A", "P"], "L"),
    (["A", "B"], "L"),
]
GERCEKLER = ["A", "B"]


def kurali_yaz(onc: list[str], sonuc: str) -> str:
    return " ∧ ".join(onc) + " ⇒ " + sonuc


def main() -> None:
    print("Bilgi tabanı:")
    for onc, s in KURALLAR:
        print(f"  {kurali_yaz(onc, s)}")
    print(f"  gerçekler: {', '.join(GERCEKLER)}")

    sonuc, sira = ileri_zincirleme(KURALLAR, GERCEKLER, "Q")
    print(f"\nİleri zincirleme: Q çıkarıldı mı? {sonuc}")
    print(f"  Çıkarım sırası: {' → '.join(sira)}")
    print("  (A ∧ B ⇒ L ateşlenir; ardından B ∧ L ⇒ M, L ∧ M ⇒ P, P ⇒ Q.)")

    iz: list[str] = []
    sonuc_g = geri_zincirleme(KURALLAR, GERCEKLER, "Q", iz=iz)
    print(f"\nGeri zincirleme: Q kanıtlandı mı? {sonuc_g}")
    print("  Alt hedef ağacı (girinti = derinlik):")
    for satir in iz:
        print("   " + satir)
    print("  A ∧ P ⇒ L kuralı P'yi yeniden sorar; döngü denetimi bu dalı keser ve")
    print("  A ∧ B ⇒ L kuralı ile devam edilir.")

    kb = []
    for onc, s in KURALLAR:
        kb += cnf(ayristir(" & ".join(onc) + " => " + s))
    kb += cnf(ayristir("A & B"))
    print(f"\nGenel doğrulama (DPLL ile KB ⊨ Q): {sat_gerektirir(kb, 'Q')}")
    print(f"Bir de KB ⊨ ¬Q denetimi: {sat_gerektirir(kb, ayristir('~Q'))} (beklenen: False)")


if __name__ == "__main__":
    main()
