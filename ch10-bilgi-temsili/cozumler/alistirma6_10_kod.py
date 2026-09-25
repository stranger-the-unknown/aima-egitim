#!/usr/bin/env python3
"""Alıştırma 6, 8, 9, 10 çözümleri."""
from __future__ import annotations

import sys
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ornekler"))

import olay_hesabi as oh  # noqa: E402
import varsayilan_akil as va  # noqa: E402


# --- A6: olay hesabı ---------------------------------------------------------
def a6():
    olaylar = sorted(oh.OLAYLAR + [("KapıyıAç", 5), ("EvdenÇık(Ali)", 6), ("EveGir(Ali)", 8)], key=lambda x: x[1])
    cizelge = {f: [t for t in range(14) if oh.T(f, t, olaylar)] for f in ("İçeride(Ali)", "Açık(Kapı)")}
    return olaylar, cizelge


# --- A8: olası dünyalar ------------------------------------------------------
GERCEK = ("Mayıs", 14)


def ayse_dunyalari(ipucu: bool = False) -> list[tuple[str, int]]:
    gunler = range(1, 16) if ipucu else range(1, 32)
    return [("Mayıs", g) for g in gunler]


def a8(ipucu: bool = False) -> dict[str, bool]:
    W = ayse_dunyalari(ipucu)
    return {
        "K(Ay = Mayıs)": all(ay == "Mayıs" for ay, _ in W),
        "K(Gün = 14)": all(g == 14 for _, g in W),
        "K(Gün ≤ 31)": all(g <= 31 for _, g in W),
        "∃g K(Gün = g)": any(all(gun == g for _, gun in W) for g in range(1, 32)),
        "K(Gün ≤ 15)": all(g <= 15 for _, g in W),
    }


# --- A9: özgüllük -----------------------------------------------------------
A9_ATOMLAR = ["Yetiskin", "Ab1", "Ab2"]  # Ab1: öğrenci-anormali, Ab2: lise öğrencisi-anormali


def a9_kb(m) -> bool:
    # Ali lise öğrencisi ve dolayısıyla öğrenci.
    return ((m["Ab1"] or m["Yetiskin"])            # Öğrenci ∧ ¬Ab1 ⇒ Yetişkin
            and (m["Ab2"] or not m["Yetiskin"]))   # LiseÖğr ∧ ¬Ab2 ⇒ ¬Yetişkin


def a9():
    tum = va.modeller(A9_ATOMLAR, a9_kb)
    duz = va.tercih_edilen(tum, ["Ab1", "Ab2"])
    ozgul = va.oncelikli(tum, [["Ab2"], ["Ab1"]])  # daha özel varsayılanın anormali önce en aza
    return duz, ozgul


# --- A10: ATMS etiketleri ---------------------------------------------------
VARSAYIMLAR = ["Yağmur", "Sulama", "Güneş"]
KURALLAR = [
    ({"Yağmur"}, "IslakÇim"), ({"Sulama"}, "IslakÇim"),
    ({"Yağmur"}, "KayganYol"), ({"Yağmur"}, "Şemsiye"),
    ({"IslakÇim", "Güneş"}, "Gökkuşağı"),
]


def ture(varsayimlar: set[str]) -> set[str]:
    inanc = set(varsayimlar)
    degisti = True
    while degisti:
        degisti = False
        for onc, s in KURALLAR:
            if onc <= inanc and s not in inanc:
                inanc.add(s)
                degisti = True
    return inanc


def etiket(inanc: str) -> list[set[str]]:
    """İnancı türeten en küçük varsayım kümeleri (ATMS etiketi)."""
    bulunan: list[set[str]] = []
    for k in range(len(VARSAYIMLAR) + 1):
        for kume in combinations(VARSAYIMLAR, k):
            s = set(kume)
            if inanc in ture(s) and not any(b <= s for b in bulunan):
                bulunan.append(s)
    return bulunan


def main() -> None:
    olaylar, cizelge = a6()
    print("A6:", ", ".join(f"{e}@{t}" for e, t in olaylar))
    for f, anlar in cizelge.items():
        print(f"    {f}: doğru olduğu anlar {anlar}")

    print("\nA8: Ayşe'nin bilgisi (yalnızca Mayıs olduğunu biliyor)")
    for k, v in a8().items():
        print(f"    {k:<16} {v}")
    print("    'Ayın ilk yarısında' ipucundan sonra:")
    for k, v in a8(ipucu=True).items():
        print(f"    {k:<16} {v}")

    duz, ozgul = a9()
    print(f"\nA9: sınırlandırma → {len(duz)} tercih edilen model: {[va.yaz(m) for m in duz]}"
          f" → Yetişkin(Ali)? {va.sonuc(duz, 'Yetiskin')}")
    print(f"    özgüllük önceliğiyle → {[va.yaz(m) for m in ozgul]} → Yetişkin(Ali)? {va.sonuc(ozgul, 'Yetiskin')}")

    print("\nA10: ATMS etiketleri")
    for inanc in ("IslakÇim", "KayganYol", "Şemsiye", "Gökkuşağı"):
        print(f"    {inanc:<10}: {[sorted(k) for k in etiket(inanc)]}")


if __name__ == "__main__":
    main()
