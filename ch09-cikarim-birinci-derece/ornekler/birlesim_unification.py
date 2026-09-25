#!/usr/bin/env python3
"""Birleştirme (unification): kitaptaki örnekler ve yaygın durumlar.

UNIFY(p, q), p ve q'yu özdeş yapan bir yerine koyma θ bulur: SUBST(θ, p) = SUBST(θ, q).
Birden çok birleştirici varsa **en genel** olanı (MGU) döndürülür.

Kitaptaki örnekler (testlerle doğrulanır):
    UNIFY(Knows(John, x), Knows(John, Jane))       = {x/Jane}
    UNIFY(Knows(John, x), Knows(y, Bill))          = {x/Bill, y/John}
    UNIFY(Knows(John, x), Knows(y, Mother(y)))     = {y/John, x/Mother(John)}
    UNIFY(Knows(John, x), Knows(x, Elizabeth))     = başarısız
    … ama değişkenler ayrılınca (x → x17):         = {x/Elizabeth, x17/John}

Çalıştırma:
    python birlesim_unification.py
"""
from __future__ import annotations

from fol_cikarim import KITAP_BIRLESTIRME, birlestir, tamamla, terim, yaz, yerine_koy, yerine_yaz

EK_ORNEKLER = [
    ("Knows(John, x)", "Knows(y, z)", "MGU: {y/John, x/z}; {y/John, x/John, z/John} de birleştirir ama daha özeldir"),
    ("f(x)", "f(Ankara)", "değişken ↔ sabit"),
    ("f(x)", "g(Ankara)", "farklı fonksiyon sembolü"),
    ("x", "f(x)", "occurs check: x, f(x)'in içinde geçiyor"),
    ("p(f(x), x)", "p(f(Ankara), Bursa)", "x hem Ankara hem Bursa olamaz"),
    ("P(x, g(x), g(f(a)))", "P(f(u), v, v)", "zincirleme bağlama"),
]


def goster(a: str, b: str, aciklama: str = "") -> None:
    teta = birlestir(terim(a), terim(b))
    satir = f"  UNIFY({a}, {b}) = {yerine_yaz(teta)}"
    if teta is not None:
        satir += f"   → {yaz(yerine_koy(tamamla(teta), terim(a)))}"
    print(satir)
    if aciklama:
        print(f"      ({aciklama})")


def main() -> None:
    print("=== Kitaptaki örnekler ===")
    for a, b in KITAP_BIRLESTIRME:
        goster(a, b)
    print("  Son örnek başarısız, çünkü iki cümlede de 'x' adı geçiyor. Oysa ikisi farklı")
    print("  ∀-cümlelerinden gelir ve x'ler aslında ilgisizdir. Değişkenleri ayırınca:")
    goster("Knows(John, x)", "Knows(x17, Elizabeth)")

    print("\n=== Diğer durumlar ===")
    for a, b, aciklama in EK_ORNEKLER:
        goster(a, b, aciklama)


if __name__ == "__main__":
    main()
