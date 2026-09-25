#!/usr/bin/env python3
"""Varsayılan akıl yürütme: sınırlandırma (circumscription) ve varsayılan mantık.

Klasik mantık monotondur: KB ⊨ α ise KB ∧ β ⊨ α. Günlük akıl yürütme değildir:
"Kuşlar uçar" deriz, penguen olduğunu öğrenince sonucu geri alırız.

1. Sınırlandırma = model tercihi. Anormal(x) yüklemleri "olabildiğince yanlış" tutulur:
   KB'nin modelleri arasından, anormal atomları (küme olarak) EN AZ olanlar tercih edilir.
   Sonuç, TÜM tercih edilen modellerde doğruysa (varsayılan olarak) gerektirilir.

       Kuş(x) ∧ ¬Anormal1(x) ⇒ Uçar(x)          Tweety: kuş → uçar; penguen olduğunu öğrenince → ?

2. Nixon elması (kitaptaki klasik örnek):
       Cumhuriyetçi(Nixon) ∧ Quaker(Nixon)
       Cumhuriyetçi(x) ∧ ¬Anormal2(x) ⇒ ¬Pasifist(x)
       Quaker(x)       ∧ ¬Anormal3(x) ⇒  Pasifist(x)
   Anormal2 ve Anormal3 sınırlandırılınca İKİ tercih edilen model vardır; biri Pasifist,
   biri değil. Akıl yürütücü "bilinmiyor" der. Öncelikli sınırlandırma (önce Anormal3'ü
   en aza indir: "dinî inanç siyasi görüşten önce gelir") ise Pasifist sonucunu verir.

3. Varsayılan mantık: Cumhuriyetçi(x) : ¬Pasifist(x) / ¬Pasifist(x) gibi kurallar.
   Nixon için iki GENİŞLEME (tutarlı inanç kümesi) vardır.

Çalıştırma:
    python varsayilan_akil.py
"""
from __future__ import annotations

from itertools import product
from typing import Callable

Model = dict


def modeller(atomlar: list[str], kb: Callable[[Model], bool]) -> list[Model]:
    return [m for m in (dict(zip(atomlar, d)) for d in product([False, True], repeat=len(atomlar))) if kb(m)]


def tercih_edilen(kb_modelleri: list[Model], anormaller: list[str]) -> list[Model]:
    """Anormal atom kümesi ⊆-minimal olan modeller (sınırlandırma)."""
    def ab(m):
        return {a for a in anormaller if m[a]}
    return [m for m in kb_modelleri if not any(ab(n) < ab(m) for n in kb_modelleri)]


def oncelikli(kb_modelleri: list[Model], oncelik: list[list[str]]) -> list[Model]:
    """Öncelikli sınırlandırma: önce ilk gruptaki anormalleri en aza indir, sonra sıradakileri."""
    kalan = kb_modelleri
    for grup in oncelik:
        kalan = tercih_edilen(kalan, grup)
    return kalan


def sonuc(tercihler: list[Model], atom: str) -> str:
    degerler = {m[atom] for m in tercihler}
    if degerler == {True}:
        return "EVET (varsayılan olarak gerektirilir)"
    if degerler == {False}:
        return "HAYIR (değili gerektirilir)"
    return "bilinmiyor (tercih edilen modeller ayrışıyor)"


# ----------------------------------------------------------------------------
# Tweety
# ----------------------------------------------------------------------------

def tweety_kb(penguen_bilgisi: bool):
    atomlar = ["Kus", "Penguen", "Ucar", "Ab1"]

    def kb(m):
        kurallar = (not (m["Kus"] and not m["Ab1"]) or m["Ucar"])       # Kuş ∧ ¬Ab1 ⇒ Uçar
        kurallar &= (not m["Penguen"] or (m["Kus"] and not m["Ucar"]))  # Penguen ⇒ Kuş ∧ ¬Uçar
        kurallar &= m["Kus"]                                            # Kuş(Tweety)
        if penguen_bilgisi:
            kurallar &= m["Penguen"]
        return kurallar

    return atomlar, kb


# ----------------------------------------------------------------------------
# Nixon elması
# ----------------------------------------------------------------------------

NIXON_ATOMLAR = ["Pasifist", "Ab2", "Ab3"]


def nixon_kb(m: Model) -> bool:
    # Cumhuriyetçi(Nixon) ve Quaker(Nixon) doğru kabul edildi
    return ((m["Ab2"] or not m["Pasifist"])       # Cumhuriyetçi ∧ ¬Ab2 ⇒ ¬Pasifist
            and (m["Ab3"] or m["Pasifist"]))      # Quaker ∧ ¬Ab3 ⇒ Pasifist


def nixon_genislemeleri() -> list[set[str]]:
    """Varsayılan mantık: kuralları farklı sıralarla uygula; tutarlı kalan inanç kümeleri."""
    kurallar = [("Cumhuriyetçi", "¬Pasifist"), ("Quaker", "Pasifist")]
    genislemeler = []
    for sira in (kurallar, kurallar[::-1]):
        inanc = {"Cumhuriyetçi", "Quaker"}
        for onkosul, sonuc_ in sira:
            zit = sonuc_[1:] if sonuc_.startswith("¬") else "¬" + sonuc_
            if onkosul in inanc and zit not in inanc:  # gerekçe tutarlıysa uygula
                inanc.add(sonuc_)
        if inanc not in genislemeler:
            genislemeler.append(inanc)
    return genislemeler


def yaz(m: Model) -> str:
    return "{" + ", ".join(f"{k}={'D' if v else 'Y'}" for k, v in m.items()) + "}"


def main() -> None:
    print("=== Tweety ===")
    for bilgi in (False, True):
        atomlar, kb = tweety_kb(bilgi)
        tum = modeller(atomlar, kb)
        tercih = tercih_edilen(tum, ["Ab1"])
        etiket = "Kuş(Tweety)" + (" + Penguen(Tweety)" if bilgi else "")
        print(f"  KB = {etiket}: {len(tum)} model, {len(tercih)} tercih edilen → Uçar(Tweety)? "
              f"{sonuc(tercih, 'Ucar')}")
    print("  Yeni bilgi eski sonucu geri aldı: akıl yürütme monoton DEĞİL.")

    print("\n=== Nixon elması: sınırlandırma ===")
    tum = modeller(NIXON_ATOMLAR, nixon_kb)
    tercih = tercih_edilen(tum, ["Ab2", "Ab3"])
    print(f"  KB'nin {len(tum)} modeli var; tercih edilenler:")
    for m in tercih:
        print(f"    {yaz(m)}")
    print(f"  Pasifist(Nixon)? {sonuc(tercih, 'Pasifist')}")
    onc = oncelikli(tum, [["Ab3"], ["Ab2"]])
    print(f"  Öncelikli sınırlandırma (önce Ab3): {[yaz(m) for m in onc]} → Pasifist? {sonuc(onc, 'Pasifist')}")

    print("\n=== Nixon elması: varsayılan mantık genişlemeleri ===")
    for g in nixon_genislemeleri():
        print(f"    {sorted(g)}")
    print("  İki genişleme var. 'Temkinli' akıl yürütme yalnızca tüm genişlemelerde ortak olana,"
          "\n  'cesur' akıl yürütme ise herhangi birine inanır.")


if __name__ == "__main__":
    main()
