#!/usr/bin/env python3
"""Bölüm 13 alıştırmaları: kodlu çözümler (A4, A5, A6, A7, A8, A9, A10).

Çalıştırma (bölüm klasöründen):
    python cozumler/alistirma_kod.py
"""
from __future__ import annotations

import itertools
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "ornekler"))

from bayes_agi import BayesAgi, gurultulu_or  # noqa: E402
from hirsiz_alarmi import hirsiz_agi, minimal_ebeveynler  # noqa: E402
from ornekleme import yagmurlama_agi  # noqa: E402

T, F = True, False


# --- A4: P(Burglary | alarm) elle ------------------------------------------
def a4() -> dict:
    p_b_a = 0.001 * (0.002 * 0.95 + 0.998 * 0.94)
    p_nb_a = 0.999 * (0.002 * 0.29 + 0.998 * 0.001)
    return {"P(b, a)": p_b_a, "P(¬b, a)": p_nb_a, "elle": p_b_a / (p_b_a + p_nb_a),
            "kod": hirsiz_agi().degisken_eleme("Burglary", {"Alarm": T})[T]}


# --- A5: yağmurlama ağında bağımsızlıklar -----------------------------------
def bagimsiz_mi(ag: BayesAgi, X: str, Y: str, Z: list[str]) -> bool:
    """Tam ortak dağılımdan sayısal kontrol: P(X, Y | z) = P(X | z) P(Y | z) her z için."""
    ortak = ag.tam_ortak_tablo()
    idx = {v: i for i, v in enumerate(ag.degiskenler)}

    def P(kosul):
        return sum(p for k, p in ortak.items() if all(k[idx[v]] == d for v, d in kosul.items()))

    for zdeg in itertools.product((T, F), repeat=len(Z)):
        z = dict(zip(Z, zdeg))
        pz = P(z)
        if pz == 0:
            continue
        for x, y in itertools.product((T, F), repeat=2):
            if abs(P({**z, X: x, Y: y}) / pz - (P({**z, X: x}) / pz) * (P({**z, Y: y}) / pz)) > 1e-12:
                return False
    return True


def a5() -> dict:
    ag = yagmurlama_agi()
    return {
        "Markov örtüsü(Sprinkler)": sorted(ag.markov_ortusu("Sprinkler")),
        "S ⊥ R": bagimsiz_mi(ag, "Sprinkler", "Rain", []),
        "S ⊥ R | C": bagimsiz_mi(ag, "Sprinkler", "Rain", ["Cloudy"]),
        "S ⊥ R | C, W": bagimsiz_mi(ag, "Sprinkler", "Rain", ["Cloudy", "WetGrass"]),
        "C ⊥ W | S, R": bagimsiz_mi(ag, "Cloudy", "WetGrass", ["Sprinkler", "Rain"]),
    }


# --- A6: yağmurlama ağında ters düğüm sırası --------------------------------
def a6() -> dict:
    ag = yagmurlama_agi()
    sonuc = {}
    for sira in (["Cloudy", "Sprinkler", "Rain", "WetGrass"], ["WetGrass", "Sprinkler", "Rain", "Cloudy"]):
        eb = minimal_ebeveynler(ag, sira)
        sonuc[" → ".join(sira)] = (sum(2 ** len(v) for v in eb.values()), eb)
    return sonuc


# --- A7: gürültülü-VEYA öksürük ---------------------------------------------
Q_OKSURUK = {"Soğuk": 0.5, "Grip": 0.3, "Alerji": 0.4}


def a7() -> dict:
    cpt = gurultulu_or(Q_OKSURUK)
    sizintili = gurultulu_or(Q_OKSURUK, sizinti=0.1)
    return {"P(öksürük | ¬soğuk, grip, alerji)": cpt[(F, T, T)],
            "P(öksürük | hiçbiri)": cpt[(F, F, F)],
            "sızıntıyla, grip + alerji": sizintili[(F, T, T)],
            "sızıntıyla, hiçbiri": sizintili[(F, F, F)]}


# --- A8: ilgisiz değişkenler ve çarpma sayısı -------------------------------
def a8() -> dict:
    ag = hirsiz_agi()
    ag.carpma_sayisi = 0
    s1 = ag.numaralandirma("Burglary", {"JohnCalls": T})
    n1 = ag.carpma_sayisi
    ag.carpma_sayisi = 0
    s2 = ag.degisken_eleme("Burglary", {"JohnCalls": T})
    n2 = ag.carpma_sayisi
    return {"ilgili": sorted(ag.atalar(["Burglary", "JohnCalls"])), "numaralandırma": (s1[T], n1),
            "eleme": (s2[T], n2)}


# --- A9: 3-SAT'ı Bayes ağına indirgemek -------------------------------------
# (A ∨ B ∨ ¬C) ∧ (¬A ∨ C ∨ D) ∧ (B ∨ ¬C ∨ ¬D) ∧ (¬B ∨ ¬D ∨ A)
CUMLELER = [[("A", T), ("B", T), ("C", F)], [("A", F), ("C", T), ("D", T)],
            [("B", T), ("C", F), ("D", F)], [("B", F), ("D", F), ("A", T)]]


def sat_agi(cumleler=CUMLELER) -> BayesAgi:
    ag = BayesAgi()
    degiskenler = sorted({v for c in cumleler for v, _ in c})
    for v in degiskenler:
        ag.ekle(v, [], {(): 0.5})
    for i, cumle in enumerate(cumleler, 1):
        ebeveyn = [v for v, _ in cumle]
        cpt = {deg: (1.0 if any(d == isaret for d, (_, isaret) in zip(deg, cumle)) else 0.0)
               for deg in itertools.product((T, F), repeat=len(cumle))}
        ag.ekle(f"C{i}", ebeveyn, cpt)
    cler = [f"C{i}" for i in range(1, len(cumleler) + 1)]
    ag.ekle("S", cler, {deg: (1.0 if all(deg) else 0.0) for deg in itertools.product((T, F), repeat=len(cler))})
    return ag


def a9() -> dict:
    ag = sat_agi()
    n = len({v for c in CUMLELER for v, _ in c})
    # P(S = true): S'yi sorgula, kanıt yok. Normalizasyon öncesi değeri almak için numaralandırma.
    p_s = ag.numaralandirma("S", {}, ham=True)[T]
    kaba = sum(all(any(atama[v] == isaret for v, isaret in c) for c in CUMLELER)
               for atama in (dict(zip("ABCD", d)) for d in itertools.product((T, F), repeat=n)))
    return {"P(S = true)": p_s, "karşılayan atama (P·2ⁿ)": p_s * 2 ** n, "kaba kuvvet": kaba}


# --- A10: hırsız ağında örnekleme -------------------------------------------
def a10(tohum: int = 7) -> dict:
    ag, rng = hirsiz_agi(), random.Random(tohum)
    kanit = {"JohnCalls": T, "MaryCalls": T}
    kesin = ag.numaralandirma("Burglary", kanit)[T]
    sonuc = {"kesin": kesin}
    for N in (10_000, 100_000):
        ret, kabul = ag.ret_ornekleme("Burglary", kanit, N, rng)
        ow = ag.olabilirlik_agirliklandirma("Burglary", kanit, N, rng)
        sonuc[N] = {"ret": (ret[T], kabul), "ağırlıklandırma": ow[T]}
    sonuc["gibbs"] = ag.gibbs("Burglary", kanit, 100_000, rng, isinma=1000)[T]
    return sonuc


def main() -> None:
    print("=== A4 ===")
    for k, v in a4().items():
        print(f"  {k:<10} {v:.6f}")
    print("\n=== A5 ===")
    for k, v in a5().items():
        print(f"  {k:<26} {v}")
    print("\n=== A6 ===")
    for sira, (n, eb) in a6().items():
        print(f"  {sira}: {n} parametre  " + "; ".join(f"{x}←{','.join(p) or '∅'}" for x, p in eb.items()))
    print("\n=== A7 ===")
    for k, v in a7().items():
        print(f"  {k:<36} {v:.3f}")
    print("\n=== A8 ===")
    for k, v in a8().items():
        print(f"  {k:<15} {v}")
    print("\n=== A9 ===")
    for k, v in a9().items():
        print(f"  {k:<25} {v}")
    print("\n=== A10 ===")
    for k, v in a10().items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
