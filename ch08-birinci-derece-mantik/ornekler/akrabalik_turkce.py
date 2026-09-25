#!/usr/bin/env python3
"""Akrabalık alanı: Türkçe akrabalık terimlerini birinci derece mantıkla tanımlamak.

Kitaptaki akrabalık örneği "anne, baba, kardeş, büyükanne…" gibi kavramları temel
ilişkilerden tanımlar. Türkçe burada ilginç bir fark gösterir: İngilizcedeki tek bir
"uncle" kelimesinin karşılığı iki ayrı kavramdır (amca ve dayı), "aunt" için de
hala ve teyze vardır. Hangi kavramların sözcük dağarcığına gireceği bir **ontoloji**
kararıdır; dil ve kültür bu kararı etkiler.

Temel ilişkiler (yalnızca bunlar olgu olarak verilir):
    Ebeveyn(p, c)   Erkek(x)   Kadın(x)
Tanımlar (aksiyomlar):
    ∀p,c  Anne(p, c) ⇔ Ebeveyn(p, c) ∧ Kadın(p)
    ∀p,c  Baba(p, c) ⇔ Ebeveyn(p, c) ∧ Erkek(p)
    ∀x,y  Kardeş(x, y) ⇔ x ≠ y ∧ ∃p Ebeveyn(p, x) ∧ Ebeveyn(p, y)
    ∀x,y  Amca(x, y)  ⇔ Erkek(x) ∧ ∃b Baba(b, y) ∧ Kardeş(x, b)
    ∀x,y  Dayı(x, y)  ⇔ Erkek(x) ∧ ∃a Anne(a, y) ∧ Kardeş(x, a)
    ∀x,y  Hala(x, y)  ⇔ Kadın(x) ∧ ∃b Baba(b, y) ∧ Kardeş(x, b)
    ∀x,y  Teyze(x, y) ⇔ Kadın(x) ∧ ∃a Anne(a, y) ∧ Kardeş(x, a)
    ∀x,y  Kuzen(x, y) ⇔ ∃p,q Ebeveyn(p, x) ∧ Ebeveyn(q, y) ∧ Kardeş(p, q)
    ∀x,y  Dede(x, y)  ⇔ Erkek(x) ∧ ∃p Ebeveyn(x, p) ∧ Ebeveyn(p, y)

Çalıştırma:
    python akrabalik_turkce.py
"""
from __future__ import annotations

KISILER = ["Hasan", "Fatma", "Ahmet", "Zeynep", "Mehmet", "Elif", "Ayşe", "Ali",
           "Deniz", "Can", "Ece", "Selin"]
ERKEK = {"Hasan", "Ahmet", "Mehmet", "Ali", "Can"}
KADIN = set(KISILER) - ERKEK
EBEVEYN = {
    # Hasan ve Fatma'nın çocukları: Ahmet, Zeynep, Mehmet
    ("Hasan", "Ahmet"), ("Fatma", "Ahmet"),
    ("Hasan", "Zeynep"), ("Fatma", "Zeynep"),
    ("Hasan", "Mehmet"), ("Fatma", "Mehmet"),
    # Ahmet + Elif → Deniz, Can
    ("Ahmet", "Deniz"), ("Elif", "Deniz"), ("Ahmet", "Can"), ("Elif", "Can"),
    # Zeynep + Ali → Ece
    ("Zeynep", "Ece"), ("Ali", "Ece"),
    # Elif'in kız kardeşi Ayşe (Elif ile Ayşe'nin ortak ebeveyni: Selin)
    ("Selin", "Elif"), ("Selin", "Ayşe"),
}


def ebeveyn(p, c): return (p, c) in EBEVEYN  # noqa: E704
def anne(p, c): return ebeveyn(p, c) and p in KADIN  # noqa: E704
def baba(p, c): return ebeveyn(p, c) and p in ERKEK  # noqa: E704


def kardes(x, y) -> bool:
    return x != y and any(ebeveyn(p, x) and ebeveyn(p, y) for p in KISILER)


def amca(x, y): return x in ERKEK and any(baba(b, y) and kardes(x, b) for b in KISILER)  # noqa: E704
def dayi(x, y): return x in ERKEK and any(anne(a, y) and kardes(x, a) for a in KISILER)  # noqa: E704
def hala(x, y): return x in KADIN and any(baba(b, y) and kardes(x, b) for b in KISILER)  # noqa: E704
def teyze(x, y): return x in KADIN and any(anne(a, y) and kardes(x, a) for a in KISILER)  # noqa: E704


def kuzen(x, y) -> bool:
    return any(ebeveyn(p, x) and ebeveyn(q, y) and kardes(p, q) for p in KISILER for q in KISILER)


def dede(x, y) -> bool:
    return x in ERKEK and any(ebeveyn(x, p) and ebeveyn(p, y) for p in KISILER)


def uncle(x, y) -> bool:
    """İngilizce 'uncle': amca ya da dayı (bu ayrımı yapmaz)."""
    return amca(x, y) or dayi(x, y)


ILISKILER = {"amca": amca, "dayı": dayi, "hala": hala, "teyze": teyze, "kuzen": kuzen, "dede": dede}


def hepsi(iliski) -> list[tuple[str, str]]:
    return [(x, y) for x in KISILER for y in KISILER if iliski(x, y)]


def teoremler() -> dict[str, bool]:
    """Tanımlardan çıkan ve modelde doğrulanabilen genel özellikler."""
    return {
        "Kardeş simetriktir": all(kardes(x, y) == kardes(y, x) for x in KISILER for y in KISILER),
        "Kimse kendinin kardeşi değildir": not any(kardes(x, x) for x in KISILER),
        "Kuzen simetriktir": all(kuzen(x, y) == kuzen(y, x) for x in KISILER for y in KISILER),
        "Amca ve dayı aynı kişi-çift için ikisi birden olamaz (bu ailede)":
            not any(amca(x, y) and dayi(x, y) for x in KISILER for y in KISILER),
    }


def main() -> None:
    print("Aile (Ebeveyn olguları):")
    for p, c in sorted(EBEVEYN):
        print(f"  Ebeveyn({p}, {c})")
    print("\nTanımlardan türetilen ilişkiler:")
    for ad, f in ILISKILER.items():
        ciftler = hepsi(f)
        print(f"  {ad:<6}: " + (", ".join(f"{ad.capitalize()}({x}, {y})" for x, y in ciftler) or "—"))
    print("\nİngilizce 'uncle' tek kavramla: " + ", ".join(f"Uncle({x}, {y})" for x, y in hepsi(uncle)))
    print("  → Türkçe, aynı olguları iki ayrı kavrama (amca, dayı) bölüyor.")
    print("\nModelde doğrulanan genel özellikler:")
    for ad, dogru in teoremler().items():
        print(f"  {ad}: {dogru}")


if __name__ == "__main__":
    main()
