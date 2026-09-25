#!/usr/bin/env python3
"""Bölüm 12 alıştırmaları: kodlu çözümler (A4, A5, A6, A7, A8, A9, A10).

Çalıştırma (bölüm klasöründen):
    python cozumler/alistirma_kod.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "ornekler"))

import bayes_kurali as bk  # noqa: E402
import dis_hekimi as dh  # noqa: E402
import hollanda_kitabi as hk  # noqa: E402
import wumpus_olasilik as wo  # noqa: E402
from olasilik import OrtakDagilim, normalize  # noqa: E402


# --- A4: diş hekimi tablosundan sorgular -----------------------------------
def a4() -> dict:
    d = dh.dis_dagilimi()
    return {
        "P(toothache)": d.P({"Toothache": True}),
        "P(Cavity | catch)": d.kosullu("Cavity", {"Catch": True}),
        "P(toothache | cavity)": d.P({"Toothache": True}, {"Cavity": True}),
        "P(cavity | toothache ∨ catch)": d.P({"Cavity": True}, lambda w: w["Toothache"] or w["Catch"]),
    }


# --- A5: yeni bir Hollanda kitabı -------------------------------------------
def a5() -> dict:
    """P(a)=0.5, P(b)=0.5, P(a∧b)=0.4, P(a∨b)=0.5 (0.6 olmalıydı).
    Birim bilet mantığı: fiyatı p olan bilet, önerme doğruysa 1$ öder.
    Ajan 2: a∨b biletini alır (0.5), a ve b biletlerini satar (0.5'er), a∧b biletini alır (0.4).
    1[a∨b] − 1[a] − 1[b] + 1[a∧b] = 0 her sonuçta; fiyat farkı 0.1 hep Ajan 2'ye kalır."""
    inanclar = {"a": 0.5, "b": 0.5, "a∧b": 0.4, "a∨b": 0.5}
    # (önerme, Ajan 2 lehine mi, Ajan 2'nin yatırımı): lehine p, aleyhine 1 − p yatırmak bir birim bilettir
    bahisler = [("a∨b", True, 0.5), ("a", False, 0.5), ("b", False, 0.5), ("a∧b", True, 0.4)]
    return hk.kazanc_tablosu(inanclar, bahisler)


# --- A6: salgın -------------------------------------------------------------
def a6() -> dict:
    return {"P(s|¬m)": bk.P_S_DEGIL_M, "normal": bk.menenjit_salgin(1), "10 kat": bk.menenjit_salgin(10),
            "P(s) salgında": bk.P_S_M * 10 * bk.P_M + bk.P_S_DEGIL_M * (1 - 10 * bk.P_M)}


# --- A7: naif Bayes ile metin sınıflandırma ---------------------------------
ONSEL = {"spor": 0.4, "ekonomi": 0.6}
KELIME = {  # P(HasWord = true | Kategori)
    "gol": {"spor": 0.5, "ekonomi": 0.02},
    "maç": {"spor": 0.6, "ekonomi": 0.05},
    "borsa": {"spor": 0.01, "ekonomi": 0.4},
}


def naif_bayes(gozlem: dict, onsel=ONSEL, kelime=KELIME) -> dict:
    """gozlem: {kelime: True/False}; gözlenmeyen kelimeler hesaba girmez."""
    ham = {}
    for c, p in onsel.items():
        for w, var in gozlem.items():
            p *= kelime[w][c] if var else 1 - kelime[w][c]
        ham[c] = p
    return normalize(ham)


# --- A8: havalimanı, en yüksek beklenen fayda -------------------------------
PLANLAR = {"A60": (60, 0.70), "A90": (90, 0.97), "A120": (120, 0.99), "A180": (180, 0.999), "A1440": (1440, 0.9999)}
YOL = 55  # ortalama yol süresi (dk): bekleme ≈ çıkış öncesi süre − yol


def beklenen_fayda(ucak_degeri: float, dakika_maliyeti: float = 1.0) -> dict:
    return {ad: p * ucak_degeri - dakika_maliyeti * max(0, sure - YOL) for ad, (sure, p) in PLANLAR.items()}


# --- A9: Wumpus'ta önselin etkisi -------------------------------------------
def a9() -> dict:
    return {p: (wo.sinir_toplami((1, 3), p=p), wo.sinir_toplami((2, 2), p=p)) for p in (0.01, 0.2, 0.5)}


# --- A10: koşullu bağımsızlık bozulunca naif Bayes --------------------------
def a10() -> dict:
    tablo = dict(dh.TABLO)
    # cavity satırını değiştir: ağrı ve sonda, çürük verildiğinde artık birlikte görülüyor
    tablo.update({(True, True, True): 0.14, (True, False, True): 0.0,
                  (False, True, True): 0.04, (False, False, True): 0.02})
    d = OrtakDagilim(dh.DEGISKENLER, tablo)
    kesin = d.kosullu("Cavity", {"Toothache": True, "Catch": True})[True]
    ham = {cav: d.P({"Toothache": True}, {"Cavity": cav}) * d.P({"Catch": True}, {"Cavity": cav})
           * d.P({"Cavity": cav}) for cav in (True, False)}
    naif = normalize(ham)[True]
    return {"koşullu bağımsız mı": d.bagimsiz_mi("Toothache", "Catch", "Cavity"), "kesin": kesin, "naif": naif}


def main() -> None:
    print("=== A4 ===")
    for k, v in a4().items():
        v = {kk: round(vv, 4) for kk, vv in v.items()} if isinstance(v, dict) else round(v, 4)
        print(f"  {k:<30} = {v}")

    print("\n=== A5: Hollanda kitabı ===")
    for (a, b), k in a5().items():
        print(f"  a={a!s:<5} b={b!s:<5} → Ajan 1'in kazancı {k:+.2f}$")

    print("\n=== A6: salgın ===")
    for k, v in a6().items():
        print(f"  {k:<14} {v:.6f}")

    print("\n=== A7: naif Bayes ===")
    for gozlem in ({"gol": True, "maç": True, "borsa": False}, {"gol": True, "maç": True},
                   {"gol": False, "maç": False, "borsa": True}):
        print(f"  {gozlem} → { {c: round(p, 4) for c, p in naif_bayes(gozlem).items()} }")
    sifirli = {**KELIME, "gol": {"spor": 0.5, "ekonomi": 0.0}}
    print(f"  P(gol | ekonomi) = 0 iken 'gol' ve 'borsa' geçen belge: "
          f"{ {c: round(p, 4) for c, p in naif_bayes({'gol': True, 'borsa': True}, kelime=sifirli).items()} }")

    print("\n=== A8: havalimanı ===")
    for deger in (1000, 10000):
        eu = beklenen_fayda(deger)
        en_iyi = max(eu, key=eu.get)
        print(f"  Uçağı yakalamanın değeri {deger}: " + ", ".join(f"{k}={v:.1f}" for k, v in eu.items())
              + f"  → en iyisi {en_iyi}")

    print("\n=== A9: çukur önseli ===")
    for p, (p13, p22) in a9().items():
        print(f"  p = {p:<4}: P(P13) = {p13:.3f}, P(P22) = {p22:.3f}")

    print("\n=== A10: koşullu bağımsızlık bozulunca ===")
    for k, v in a10().items():
        print(f"  {k:<20} {v if isinstance(v, bool) else round(v, 4)}")


if __name__ == "__main__":
    main()
