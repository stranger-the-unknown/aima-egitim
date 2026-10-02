#!/usr/bin/env python3
"""Bölüm 18 alıştırmaları: kodlu çözümler (A1, A3–A10).

Çalıştırma (bölüm klasöründen):
    python cozumler/alistirma_kod.py
"""
from __future__ import annotations

import itertools
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "ornekler"))

import isbirlikci_oyunlar as io  # noqa: E402
import mekanizma_tasarimi as mt  # noqa: E402
import oyun_kurami as ok  # noqa: E402
import tekrarli_oyunlar as to  # noqa: E402
import uzun_bicim as ub  # noqa: E402


# --- A1: tavuk oyunu --------------------------------------------------------------
TAVUK = ok.iki_oyunculu(("Ayşe", "Can"), ("kaç", "dümdüz"), ("kaç", "dümdüz"), {
    ("kaç", "kaç"): (0, 0), ("kaç", "dümdüz"): (-1, 1),
    ("dümdüz", "kaç"): (1, -1), ("dümdüz", "dümdüz"): (-10, -10)})


def iki_kere_iki_karma_nash(oyun: ok.Oyun) -> tuple[Fraction, Fraction]:
    """2 × 2 genel toplamlı oyunda tam karma denge: Her oyuncu karşısını kayıtsız bırakır.
    (satır oyuncusunun 1. eylem olasılığı, sütun oyuncusunun 1. eylem olasılığı)."""
    (r1, r2), (c1, c2) = oyun.eylemler
    u = lambda i, a, b: Fraction(oyun.fayda[(a, b)][i])
    # p: satırın r1 olasılığı; sütunun c1 ve c2 faydaları eşit olsun
    p = (u(1, r2, c2) - u(1, r2, c1)) / (u(1, r1, c1) - u(1, r2, c1) - u(1, r1, c2) + u(1, r2, c2))
    q = (u(0, r2, c2) - u(0, r1, c2)) / (u(0, r1, c1) - u(0, r1, c2) - u(0, r2, c1) + u(0, r2, c2))
    return p, q


def a1() -> dict:
    p, q = iki_kere_iki_karma_nash(TAVUK)
    return {"baskın": [ok.baskin_strateji(TAVUK, i) for i in (0, 1)], "saf Nash": ok.saf_nash(TAVUK),
            "Pareto": ok.pareto_en_iyi(TAVUK), "karma: P(kaç)": (p, q),
            "karma: çarpışma olasılığı": (1 - p) * (1 - q)}


# --- A3: üç parmaklı Morra ------------------------------------------------------------
def morra3() -> np.ndarray:
    """E ve O 1–3 parmak gösterir; toplam çiftse E, tekse O toplam kadar kazanır. E için matris."""
    return np.array([[(e + o) if (e + o) % 2 == 0 else -(e + o) for o in (1, 2, 3)] for e in (1, 2, 3)], dtype=float)


def a3() -> dict:
    v, p, q = ok.maksimin(morra3())
    return {"matris": morra3(), "değer": v, "E": p, "O": q}


# --- A4: bilinmeyen sayıda tur ------------------------------------------------------------
def a4(delta: float) -> dict:
    """Her turdan sonra oyun δ olasılıkla sürer. ACIMASIZ'a karşı: hep sus → −1/(1 − δ);
    bir kez tanıklık et → 0 + δ(−5)/(1 − δ). Susmak en az onun kadar iyi ⇔ δ ≥ 0.2."""
    isbirligi = -1 / (1 - delta)
    sapma = 0 + delta * (-5) / (1 - delta)
    return {"işbirliği": isbirligi, "sapma": sapma, "ACIMASIZ–ACIMASIZ denge mi": isbirligi >= sapma}


# --- A5: poker ---------------------------------------------------------------------------
def a5() -> dict:
    A = ub.poker_matrisi()
    hucre = ub.poker_fayda("kr", "fc")
    # Oyuncu 1 hep artırmak zorunda olsaydı (yalnızca rr satırı): oyuncu 2'nin en iyi tepkisi
    zorunlu = dict(zip(ub.P2_STRATEJILER, A[0]))
    return {"kr–fc": hucre, "denge": ub.saf_eyer_noktalari(A), "hep artırmak zorunda": zorunlu,
            "oyuncu 2'nin tepkisi": min(zorunlu, key=zorunlu.get)}


# --- A6: ataş oyununda farklı seçenekler ---------------------------------------------------
def a6(orta: int = 40) -> dict:
    """Robbie'nin orta seçeneği orta + orta olsun. Harriet 1 + 1 yapıp Robbie orta + orta ile cevap verirse
    Harriet'in toplamı 1 + orta; 2 ataş yapıp 90 ataş gelirse 92θ. 1 + 1 ⇔ 92θ ≤ 1 + orta ve 92(1 − θ) ≤ 1 + orta."""
    eski = dict(ub.ROBBIE)
    try:
        ub.ROBBIE.clear()
        ub.ROBBIE.update({"90 ataş": (90, 0), f"{orta} + {orta}": (orta, orta), "90 zımba": (0, 90)})
        robbie, aralik = ub.atas_dengesi()
    finally:
        ub.ROBBIE.clear()
        ub.ROBBIE.update(eski)
    esik = Fraction(1 + orta, 92)
    return {"Robbie": robbie, "1+1 aralığı (benzetim)": aralik,
            "1+1 aralığı (kesin)": (1 - esik, esik) if esik > Fraction(1, 2) else None}


# --- A7: eldiven oyunu ----------------------------------------------------------------------
def eldiven(C) -> int:
    """1'de sol eldiven, 2 ve 3'te sağ eldiven var; bir çift 1 değerinde."""
    return 1 if 1 in C and (2 in C or 3 in C) else 0


def a7() -> dict:
    N = [1, 2, 3]
    izgara = [Fraction(i, 20) for i in range(21)]
    cekirdek = [(a, b, 1 - a - b) for a in izgara for b in izgara
                if a + b <= 1 and io.cekirdekte_mi(N, eldiven, {1: a, 2: b, 3: 1 - a - b})]
    return {"Shapley": io.shapley(N, eldiven), "çekirdek (ızgarada)": cekirdek}


# --- A8: VCG ve dürüstlük ----------------------------------------------------------------------
def a8() -> dict:
    gercek = [30, 25, 10, 5]
    kazananlar, vergi = mt.vcg(gercek, 2)
    # Her ajan için: dürüst teklifin net faydası, herhangi bir sapmanınkinden küçük değil mi?
    def net(i, teklif_i):
        t = list(gercek)
        t[i] = teklif_i
        k, v = mt.vcg(t, 2)
        return gercek[i] - v[i] if i in k else 0

    durust_en_iyi = all(net(i, gercek[i]) >= net(i, b) for i in range(4) for b in range(0, 41))
    return {"kazananlar": [gercek[i] for i in kazananlar], "vergiler": list(vergi.values()),
            "dürüstlük her ajan için en iyi": durust_en_iyi}


# --- A9: stratejik oy ------------------------------------------------------------------------
def a9() -> dict:
    gercek = [["A", "C", "B"]] * 4 + [["B", "C", "A"]] * 3 + [["C", "B", "A"]] * 2
    stratejik = [["A", "C", "B"]] * 4 + [["B", "C", "A"]] * 3 + [["B", "C", "A"]] * 2
    return {"dürüst çoğunluk": mt.cogunluk(gercek), "C'ciler B'ye oy verirse": mt.cogunluk(stratejik),
            "dürüst Borda": mt.borda(gercek), "Condorcet": mt.condorcet_kazanani(gercek)}


# --- A10: eşit sabır --------------------------------------------------------------------------
def a10() -> dict:
    return {g: mt.rubinstein(g, g) for g in (0.5, 0.9, 0.99, 0.999)}


def yaz(x):
    """Kesirleri ve numpy sayılarını okunur yaz."""
    if isinstance(x, dict):
        return "{" + ", ".join(f"{k}: {yaz(v)}" for k, v in x.items()) + "}"
    if isinstance(x, (list, tuple)):
        return "(" + ", ".join(yaz(v) for v in x) + ")"
    if isinstance(x, float):
        return f"{x:.3f}"
    return str(x)


def main() -> None:
    print("=== A1: tavuk oyunu ===")
    for k, v in a1().items():
        print(f"  {k}: {yaz(v)}")

    print("\n=== A3: üç parmaklı Morra ===")
    s = a3()
    print(f"  Matris (E için):\n{s['matris']}")
    print(f"  Değer {s['değer']:+.4f}; E {np.round(s['E'], 4)}; O {np.round(s['O'], 4)}")

    print("\n=== A4: devam olasılığı δ ile ACIMASIZ ===")
    for d in (0.1, 0.2, 0.5, 0.9):
        s = a4(d)
        print(f"  δ = {d}: işbirliği {s['işbirliği']:.3f}, sapma {s['sapma']:.3f}, denge? {s['ACIMASIZ–ACIMASIZ denge mi']}")

    print("\n=== A5: poker ===")
    for k, v in a5().items():
        print(f"  {k}: {yaz(v)}")

    print("\n=== A6: ataş oyununda Robbie'nin orta seçeneği ===")
    for orta in (50, 45, 40):
        print(f"  {orta} + {orta}: {yaz(a6(orta))}")

    print("\n=== A7: eldiven oyunu ===")
    s = a7()
    print(f"  Shapley: {', '.join(f'{i}: {v}' for i, v in s['Shapley'].items())}")
    print(f"  Çekirdek (1/20 ızgarasında): {[tuple(str(x) for x in c) for c in s['çekirdek (ızgarada)']]}")

    print("\n=== A8: VCG, 2 mal, teklifler 30, 25, 10, 5 ===")
    for k, v in a8().items():
        print(f"  {k}: {v}")

    print("\n=== A9: stratejik oy ===")
    for k, v in a9().items():
        print(f"  {k}: {v}")

    print("\n=== A10: eşit sabırlı oyuncular, Rubinstein payı ===")
    for g, v in a10().items():
        print(f"  γ = {g}: A1 {v:.4f}, A2 {1 - v:.4f}")


if __name__ == "__main__":
    main()
