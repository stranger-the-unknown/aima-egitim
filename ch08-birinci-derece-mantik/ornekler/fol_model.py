#!/usr/bin/env python3
"""Birinci derece mantığın anlamı: bir modelde cümleleri değerlendirmek.

Kitaptaki modele benzer bir model: beş nesne (Richard, John, ikisinin sol bacakları
ve bir taç), ikili ilişkiler Kardeş ve BaşınınÜstünde, tekli ilişkiler Kişi, Kral, Taç
ve SolBacak fonksiyonu.

Gösterilenler
  1. Niceleyicili cümleleri modelde değerlendirmek.
  2. Kitapta vurgulanan iki klasik hata:
       ∀x Kral(x) ∧ Kişi(x)   (yanlış: "herkes kral ve kişidir" der)
       ∃x Taç(x) ⇒ Başında(x, John)   (neredeyse her zaman doğru: taç olmayan
                                       herhangi bir nesne ⇒'yi doğru yapar)
  3. Niceleyici sırası: ∀x ∃y ile ∃y ∀x farklıdır.
  4. Standart anlam ile veritabanı anlamı: 2 sabit ve 1 ikili ilişkiyle
     veritabanı anlamında 2⁴ = 16 model vardır (standart anlamda sonsuz).

Çalıştırma:
    python fol_model.py
"""
from __future__ import annotations

from itertools import product

NESNELER = ["Richard", "John", "RichardınBacağı", "JohnunBacağı", "Taç"]
ILISKILER = {
    "Kardeş": {("Richard", "John"), ("John", "Richard")},
    "Başında": {("Taç", "John")},
    "Kişi": {("Richard",), ("John",)},
    "Kral": {("John",)},
    "Taç": {("Taç",)},
}
SOL_BACAK = {"Richard": "RichardınBacağı", "John": "JohnunBacağı"}


# Cümleler Python lambdaları olarak yazılır; niceleyiciler model üzerinde döngüdür.
def her(yuklem) -> bool:
    return all(yuklem(x) for x in NESNELER)


def bazi(yuklem) -> bool:
    return any(yuklem(x) for x in NESNELER)


def R(ad: str, *args) -> bool:
    return tuple(args) in ILISKILER[ad]


CUMLELER = [
    ("Kral(John)", lambda: R("Kral", "John")),
    ("Kardeş(Richard, John)", lambda: R("Kardeş", "Richard", "John")),
    ("∀x Kral(x) ⇒ Kişi(x)", lambda: her(lambda x: (not R("Kral", x)) or R("Kişi", x))),
    ("∀x Kral(x) ∧ Kişi(x)          [HATA]", lambda: her(lambda x: R("Kral", x) and R("Kişi", x))),
    ("∃x Taç(x) ∧ Başında(x, John)", lambda: bazi(lambda x: R("Taç", x) and R("Başında", x, "John"))),
    ("∃x Taç(x) ⇒ Başında(x, John)  [HATA]", lambda: bazi(lambda x: (not R("Taç", x)) or R("Başında", x, "John"))),
    ("∀x Kişi(x) ⇒ Kişi(SolBacak(x))  (bacak kişi değil)",
     lambda: her(lambda x: (not R("Kişi", x)) or R("Kişi", SOL_BACAK[x]))),
]


def niceleyici_sirasi() -> list[tuple[str, bool, bool]]:
    """İki ayrı 'sevgi' modelinde ∀x∃y ve ∃y∀x cümleleri."""
    kisiler = ["Ali", "Ayşe", "Can"]
    modeller = {
        "herkes başka birini seviyor": {("Ali", "Ayşe"), ("Ayşe", "Can"), ("Can", "Ali")},
        "herkes Ayşe'yi seviyor": {("Ali", "Ayşe"), ("Ayşe", "Ayşe"), ("Can", "Ayşe")},
    }
    sonuc = []
    for ad, sever in modeller.items():
        herkes_birini = all(any((x, y) in sever for y in kisiler) for x in kisiler)   # ∀x ∃y
        biri_herkesce = any(all((x, y) in sever for x in kisiler) for y in kisiler)   # ∃y ∀x
        sonuc.append((ad, herkes_birini, biri_herkesce))
    return sonuc


def veritabani_modelleri() -> int:
    """2 sabit (R, J), 1 ikili ilişki; benzersiz isimler + kapalı dünya + alan kapanışı."""
    nesneler = ["R", "J"]
    ciftler = [(a, b) for a in nesneler for b in nesneler]
    return sum(1 for _ in product([False, True], repeat=len(ciftler)))


def standart_anlam_ornegi() -> list[str]:
    """Kardeş(John, Richard) ∧ Kardeş(Geoffrey, Richard): 'Richard'ın iki kardeşi var' mı?"""
    aciklama = []
    # Standart anlam: John ve Geoffrey aynı nesneyi gösterebilir.
    yorum = {"John": "o1", "Geoffrey": "o1", "Richard": "o2"}
    kardes = {("o1", "o2")}
    dogru = (yorum["John"], yorum["Richard"]) in kardes and (yorum["Geoffrey"], yorum["Richard"]) in kardes
    aciklama.append(f"John ve Geoffrey aynı nesneyse cümle yine doğru: {dogru}  → yalnızca 1 kardeş!")
    aciklama.append("Doğru ifade: Kardeş(John,R) ∧ Kardeş(Geoffrey,R) ∧ John ≠ Geoffrey ∧ "
                    "∀x Kardeş(x,R) ⇒ (x = John ∨ x = Geoffrey)")
    return aciklama


def main() -> None:
    print("=== Model ===")
    print(f"  Nesneler: {', '.join(NESNELER)}")
    for ad, demetler in ILISKILER.items():
        print(f"  {ad}: {sorted(demetler)}")
    print(f"  SolBacak: {SOL_BACAK}  (kişi olmayanlar için tanımsız bırakıldı)\n")

    print("=== Cümleler bu modelde doğru mu? ===")
    for metin, f in CUMLELER:
        try:
            deger = f()
        except KeyError:
            deger = "tanımsız (SolBacak kişi olmayanlar için tanımlı değil)"
        print(f"  {metin:<46} → {deger}")
    print("\n  ∀ ile ⇒, ∃ ile ∧ doğal eşlerdir. Tersini kullanmak yukarıdaki iki hataya yol açar.")

    print("\n=== Niceleyici sırası ===")
    for ad, a, b in niceleyici_sirasi():
        print(f"  Model '{ad}': ∀x ∃y Sever(x,y) = {a},  ∃y ∀x Sever(x,y) = {b}")

    print("\n=== Standart anlam ve veritabanı anlamı ===")
    for satir in standart_anlam_ornegi():
        print(f"  {satir}")
    print(f"  Veritabanı anlamında 2 sabit + 1 ikili ilişki için model sayısı: {veritabani_modelleri()}"
          "  (standart anlamda sonsuz)")


if __name__ == "__main__":
    main()
