#!/usr/bin/env python3
"""Alıştırma 4, 6, 7, 8, 9 çözümleri (kodla doğrulanabilen kısımlar)."""
from __future__ import annotations

import random
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ornekler"))

import ileri_geri_zincirleme as igz  # noqa: E402
import wumpus_mantik as wm  # noqa: E402
from onerme import (ayristir, cnf, cozumleme, dpll, geri_zincirleme,  # noqa: E402
                    ileri_zincirleme, rastgele_3cnf, tumce_yaz, walksat)


def a4() -> list:
    return cnf(ayristir("(A | B) => (C & ~D)"))


def a6():
    kb = []
    for c in wm.KITAP_KB:
        kb += cnf(ayristir(c))
    return cozumleme(kb, ayristir("P22 | P31"))


def a7():
    ek = [(["A"], "X1")] + [([f"X{i}"], f"X{i + 1}") for i in range(1, 10)]
    sonuc = {}
    for ad, kurallar in (("özgün", igz.KURALLAR), ("+10 ilgisiz kural", igz.KURALLAR + ek)):
        _, sira = ileri_zincirleme(kurallar, igz.GERCEKLER, "Q")
        iz: list = []
        geri_zincirleme(kurallar, igz.GERCEKLER, "Q", iz=iz)
        sonuc[ad] = (len(sira), len(iz))
    return sonuc


def a8():
    ajan = wm.MantiksalAjan()
    for konum in ((1, 1), (2, 1), (1, 2)):
        ajan.kb += cnf(wm.B(*konum) if wm.algi(konum)["esinti"] else ("~", wm.B(*konum)))
        ajan.kb += cnf(wm.S(*konum) if wm.algi(konum)["koku"] else ("~", wm.S(*konum)))
    semboller = {lit.lstrip("~") for t in ajan.kb for lit in t}
    sonuc = {"sembol": len(semboller)}
    for ad, sezgisel in (("sezgiselli", True), ("sezgiselsiz", False)):
        ist: dict = {}
        model = dpll(ajan.kb + cnf(("~", "W13")), ist=ist, bilgi_sezgiseli=sezgisel)
        sonuc[ad] = (model is None, ist["cagri"])
    return sonuc


def a9():
    rng = random.Random(7)
    cumleler = []
    while len(cumleler) < 20:
        t = rastgele_3cnf(30, 120, rng)
        if dpll(t) is not None:
            cumleler.append(t)
    sonuc = {}
    for p in (0.0, 0.2, 0.5, 0.8, 1.0):
        cevirme = []
        basari = 0
        for i, t in enumerate(cumleler):
            model, n = walksat(t, p=p, max_cevirme=5000, rng=random.Random(i))
            basari += model is not None
            cevirme.append(n)
        sonuc[p] = (basari, statistics.median(cevirme))
    return sonuc


def main() -> None:
    print("A4: (A ∨ B) ⇒ (C ∧ ¬D) CNF'si:")
    print("   " + " ∧ ".join(f"({tumce_yaz(t)})" for t in a4()))

    sonuc, ist, adimlar = a6()
    print(f"\nA6: R1–R5 ⊨ P22 ∨ P31 ? {sonuc}  ({ist['uretilen']} çözümleyici üretildi)")
    for a, b, r in adimlar:
        print(f"   ({tumce_yaz(a)})  +  ({tumce_yaz(b)})  →  {tumce_yaz(r)}")

    print("\nA7: (ileri zincirlemede çıkarılan sembol, geri zincirlemede bakılan alt hedef)")
    for ad, (fc, bc) in a7().items():
        print(f"   {ad:<18}: ileri {fc:>2}, geri {bc:>2}")

    d = a8()
    print(f"\nA8: sembol sayısı {d['sembol']} → doğruluk tablosu 2^{d['sembol']} ≈ {2 ** d['sembol']:.1e} model")
    for ad in ("sezgiselli", "sezgiselsiz"):
        gerektirir, cagri = d[ad]
        print(f"   DPLL {ad:<11}: KB ⊨ W13 = {gerektirir}, {cagri:,} çağrı")

    print("\nA9: WalkSAT, 20 karşılanabilir cümle (n=30, m/n=4), en fazla 5000 çevirme")
    for p, (b, med) in a9().items():
        print(f"   p = {p:<4}: başarı {b:>2}/20, medyan çevirme {med:,.0f}")


if __name__ == "__main__":
    main()
