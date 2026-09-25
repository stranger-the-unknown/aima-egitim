#!/usr/bin/env python3
"""Deterministik olmayan eylemler: kararsız süpürge dünyasında AND-OR araması.

Kararsız (erratic) süpürge:
  * Kirli karede Süpür: kareyi temizler, **bazen** yandaki kareyi de temizler.
  * Temiz karede Süpür: **bazen** halıya kir döker.
  * Sağ / Sol: deterministik.

Artık bir eylemin sonucu tek bir durum değil, bir durum **kümesidir**. Çözüm de
bir eylem dizisi değil, **koşullu plandır**: "eğer şu durumdaysan şunu yap".

Durum numaraları kitaptakiyle aynıdır (tek sayılar: ajan solda):
    1: ajan sol, iki kare kirli      2: ajan sağ, iki kare kirli
    3: ajan sol, yalnız sol kirli     4: ajan sağ, yalnız sol kirli
    5: ajan sol, yalnız sağ kirli     6: ajan sağ, yalnız sağ kirli
    7: ajan sol, her yer temiz        8: ajan sağ, her yer temiz   (7, 8 = hedef)

Kitaptaki sonuç (testlerle doğrulanır):
    SONUÇLAR(1, Süpür) = {5, 7}
    plan = [Süpür, eğer durum = 5 ise [Sağ, Süpür] değilse []]

Çalıştırma:
    python and_or_supurge.py
"""
from __future__ import annotations

from typing import Union

# Durum = (ajan konumu, sol kirli mi, sağ kirli mi)
NUMARA = {
    ("L", True, True): 1, ("R", True, True): 2,
    ("L", True, False): 3, ("R", True, False): 4,
    ("L", False, True): 5, ("R", False, True): 6,
    ("L", False, False): 7, ("R", False, False): 8,
}
DURUM = {n: d for d, n in NUMARA.items()}
HEDEFLER = {7, 8}
EYLEMLER = ["Süpür", "Sağ", "Sol"]  # kitaptaki planı bulmak için Süpür önce denenir


def sonuclar(s: int, eylem: str) -> set[int]:
    """Kararsız süpürge için olası sonuç durumları."""
    konum, sol, sag = DURUM[s]
    if eylem == "Sağ":
        return {NUMARA[("R", sol, sag)]}
    if eylem == "Sol":
        return {NUMARA[("L", sol, sag)]}
    # Süpür
    burasi_kirli = sol if konum == "L" else sag
    if burasi_kirli:
        # Bulunduğu kare temizlenir; yandaki de temizlenebilir
        yalniz_burasi = ("L", False, sag) if konum == "L" else ("R", sol, False)
        ikisi = (konum, False, False)
        return {NUMARA[yalniz_burasi], NUMARA[ikisi]}
    # Temiz karede süpürmek bazen kir döker
    kirlenmis = ("L", True, sag) if konum == "L" else ("R", sol, True)
    return {s, NUMARA[kirlenmis]}


# Plan: eylemlerin ve koşullu dalların listesi.
# Koşullu dal: {"eger": {durum: alt_plan, ...}}
Plan = list[Union[str, dict]]
BASARISIZ = None


def or_arama(s: int, yol: list[int]) -> Plan | None:
    """VEYA düğümü: Ajan seçer. Eylemlerden *biri* işe yarasın yeter."""
    if s in HEDEFLER:
        return []
    if s in yol:
        return BASARISIZ  # döngü: bu dal çözüm üretmez
    for eylem in EYLEMLER:
        plan = and_arama(sonuclar(s, eylem), [s] + yol)
        if plan is not BASARISIZ:
            return [eylem] + plan
    return BASARISIZ


def and_arama(durumlar: set[int], yol: list[int]) -> Plan | None:
    """VE düğümü: Ortam seçer. Olası *her* sonuç için bir plan gerekir."""
    alt_planlar = {}
    for s in sorted(durumlar):
        plan = or_arama(s, yol)
        if plan is BASARISIZ:
            return BASARISIZ
        alt_planlar[s] = plan
    if len(alt_planlar) == 1:
        return next(iter(alt_planlar.values()))
    return [{"eger": alt_planlar}]


def and_or_arama(baslangic: int) -> Plan | None:
    return or_arama(baslangic, [])


def plan_metni(plan: Plan) -> str:
    """Planı kitaptaki gösterime benzer biçimde yaz."""
    parcalar = []
    for adim in plan:
        if isinstance(adim, str):
            parcalar.append(adim)
        else:
            dallar = list(adim["eger"].items())
            metin = ""
            for i, (s, alt) in enumerate(dallar):
                if i < len(dallar) - 1:
                    metin += f"eğer durum = {s} ise {plan_metni(alt)} değilse "
                else:
                    metin += plan_metni(alt)
            parcalar.append(metin)
    return "[" + ", ".join(parcalar) + "]"


def calistir(plan: Plan, s: int, secici) -> list[int]:
    """Planı bir 'ortam' ile uygula. secici(olası_kümesi) → gerçekleşen durum."""
    iz = [s]
    for adim in plan:
        if isinstance(adim, str):
            s = secici(sonuclar(s, adim))
            iz.append(s)
        else:
            iz += calistir(adim["eger"][s], s, secici)[1:]
            s = iz[-1]
    return iz


def main() -> None:
    print("Kararsız süpürge dünyası: SONUÇLAR(s, Süpür)")
    for s in range(1, 9):
        print(f"  {s}: {DURUM[s]} → {sorted(sonuclar(s, 'Süpür'))}")

    plan = and_or_arama(1)
    print(f"\nDurum 1'den koşullu plan:\n  {plan_metni(plan)}")

    print("\nPlanı iki farklı 'şans' ile uygula:")
    print(f"  ortam hep küçük numaralı sonucu seçerse: {calistir(plan, 1, min)}")
    print(f"  ortam hep büyük numaralı sonucu seçerse: {calistir(plan, 1, max)}")
    print("\nİki durumda da hedefe (7 veya 8) ulaşıldı: plan *her* olası sonuç için çalışır.")

    print("\nTüm başlangıç durumları için planlar:")
    for s in range(1, 9):
        print(f"  {s}: {plan_metni(and_or_arama(s))}")


if __name__ == "__main__":
    main()
