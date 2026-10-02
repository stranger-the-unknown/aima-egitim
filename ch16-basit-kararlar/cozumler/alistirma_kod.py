#!/usr/bin/env python3
"""Bölüm 16 alıştırmaları: kodlu çözümler (A4, A5, A6, A7, A9, A10).

Çalıştırma (bölüm klasöründen):
    python cozumler/alistirma_kod.py
"""
from __future__ import annotations

import itertools
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "ornekler"))

import bilinmeyen_tercihler as bt  # noqa: E402
import fayda_kurami as fk  # noqa: E402
import karar_agi as ka  # noqa: E402


# --- A4: paranın faydası ve mikromort ----------------------------------------
def a4() -> dict:
    piyango = [(0.5, 0), (0.5, 800_000)]
    ke = fk.kesinlik_esdegeri(piyango, fk.beard, fk.beard_ters)
    # Arabanın ömrü 92 000 mil, 230 milde 1 mikromort → 400 mikromort; daha güvenli araba riski yarıya indirir.
    mikromort = 92_000 / 230
    return {"EMV": fk.beklenen(piyango), "kesinlik eşdeğeri": ke, "sigorta primi": fk.beklenen(piyango) - ke,
            "araba mikromortu": mikromort, "$/mikromort": 12_000 / (mikromort / 2)}


# --- A5: Allais ve pişmanlık -------------------------------------------------
def allais_araligi(r: float) -> tuple[float, float] | None:
    """U($0) = 0, U($4000) = 1, U($3000) = u. A'yı seçip kaybedersen ek pişmanlık −r.
    (C ve D'de kesin bir şey bırakılmadığı için pişmanlık terimi yok.)
    B ≻ A ⇔ u > 0.8 − 0.2r;  C ≻ D ⇔ u < 0.8.  İkisini sağlayan u aralığı (yoksa None)."""
    alt, ust = 0.8 - 0.2 * r, 0.8
    return (round(alt, 6), ust) if alt < ust else None


def a5() -> dict:
    return {"EMV(A) − EMV(B)": 0.8 * 4000 - 3000, "pişmanlıksız tutarlı mı": fk.allais_tutarli_mi(),
            **{f"r = {r}: u aralığı": allais_araligi(r) for r in (0.0, 0.05, 0.25, 1.0)}}


# --- A6: iyileştiricinin laneti ve büzme --------------------------------------
def a6(k: int = 20, deneme: int = 20_000, tohum: int = 0) -> dict:
    """Gerçek değerler V ~ N(0, 1). Seçeneklerin yarısı gürültülü (σe = 3), yarısı az gürültülü (σe = 0.5).
    Saf seçici en büyük tahmini seçer; Bayesçi seçici E[V | tahmin] = tahmin / (1 + σe²) ile seçer."""
    rng = np.random.default_rng(tohum)
    sigma = np.array([3.0] * (k // 2) + [0.5] * (k - k // 2))
    V = rng.normal(size=(deneme, k))
    tahmin = V + rng.normal(size=(deneme, k)) * sigma
    bayes = tahmin / (1 + sigma ** 2)
    satir = np.arange(deneme)
    saf, by = tahmin.argmax(axis=1), bayes.argmax(axis=1)
    return {
        "saf: seçilenin tahmini": float(tahmin[satir, saf].mean()),
        "saf: seçilenin gerçek değeri": float(V[satir, saf].mean()),
        "saf: gürültülü seçenek seçme oranı": float((saf < k // 2).mean()),
        "Bayes: seçilenin tahmini": float(bayes[satir, by].mean()),
        "Bayes: seçilenin gerçek değeri": float(V[satir, by].mean()),
        "Bayes: gürültülü seçenek seçme oranı": float((by < k // 2).mean()),
    }


# --- A7: karar ağında bilgi değeri, duyarlılık, sağlam karar ------------------
def eu_trafik(yer: str, p_trafik: float) -> float:
    return (p_trafik * ka.beklenen_fayda(yer, trafik_bilgisi=True)
            + (1 - p_trafik) * ka.beklenen_fayda(yer, trafik_bilgisi=False))


def a7() -> dict:
    p = ka.P_TRAFIK_YOGUN
    meu = max(ka.beklenen_fayda(y) for y in ka.YERLER)
    bilgili = sum(pt * max(ka.beklenen_fayda(y, trafik_bilgisi=t) for y in ka.YERLER)
                  for t, pt in ((True, p), (False, 1 - p)))
    # Ölüm ağırlığı hangi değerden sonra karar S1'den S3'e döner?
    esik = next(w for w in np.arange(5.0, 30.0, 0.01)
                if ka.en_iyi_yer({**ka.AGIRLIK, "olum": float(w)})[0] != "S1")
    # Sağlam karar: P(trafik yoğun) ∈ [0, 1] ise en kötü durumda en iyi yer.
    izgara = np.linspace(0, 1, 101)
    en_kotu = {y: min(eu_trafik(y, t) for t in izgara) for y in ka.YERLER}
    return {"VPI(HavaTrafiği)": bilgili - meu, "ölüm ağırlığı eşiği": round(float(esik), 2),
            "en kötü durumda EU": en_kotu, "sağlam karar": max(en_kotu, key=en_kotu.get)}


# --- A9: hazine avı (kitaptaki 16.6.5) ---------------------------------------
HAZINE_P = [0.3, 0.6, 0.15, 0.4]   # her yerde hazine olma olasılığı (bağımsız)
HAZINE_C = [3.0, 10.0, 1.0, 2.0]   # bakma maliyeti


def beklenen_maliyet(sira, P=HAZINE_P, C=HAZINE_C) -> float:
    """C(xy) = C(x) + F(x) C(y): hazine bulununca durulur."""
    toplam, basarisiz = 0.0, 1.0
    for i in sira:
        toplam += basarisiz * C[i]
        basarisiz *= 1 - P[i]
    return toplam


def a9() -> dict:
    n = len(HAZINE_P)
    sirala = {
        "P/C büyükten küçüğe": sorted(range(n), key=lambda i: -HAZINE_P[i] / HAZINE_C[i]),
        "en olası önce": sorted(range(n), key=lambda i: -HAZINE_P[i]),
        "en ucuz önce": sorted(range(n), key=lambda i: HAZINE_C[i]),
    }
    en_iyi = min(itertools.permutations(range(n)), key=beklenen_maliyet)
    sonuc = {ad: ([i + 1 for i in s], round(beklenen_maliyet(s), 4)) for ad, s in sirala.items()}
    sonuc["kaba kuvvet en iyisi"] = ([i + 1 for i in en_iyi], round(beklenen_maliyet(en_iyi), 4))
    return sonuc


# --- A10: hata yapan Harriet --------------------------------------------------
def hatali_harriet(a: float, b: float, eps: float) -> dict:
    """u ~ U[a, b]. Harriet ε olasılıkla yanlış karar verir (iyi eylemi durdurur, kötüsüne izin verir)."""
    d = bt.tekduze_oyun(a, b)
    e_maks = d["bekle"]                      # E[max(u, 0)]
    e_min = (a + b) / 2 - e_maks             # E[min(u, 0)] = E[u] − E[max(u, 0)]
    return {"hemen yap": d["hemen yap"], "kendini kapat": 0.0, "bekle": (1 - eps) * e_maks + eps * e_min}


def a10() -> dict:
    tablo = {eps: hatali_harriet(-40, 60, eps)["bekle"] for eps in (0.0, 0.1, 0.2, 0.3, 0.4)}
    # bekle = 18 − 26ε > 10  ⇔  ε < 8/26
    return {"bekle(ε)": tablo, "eşik ε": 8 / 26}


def main() -> None:
    print("=== A4: Bay Beard ve mikromort ===")
    for k, v in a4().items():
        print(f"  {k}: {v:,.2f}")

    print("\n=== A5: Allais paradoksu ve pişmanlık ===")
    for k, v in a5().items():
        print(f"  {k}: {v}")

    print("\n=== A6: iyileştiricinin laneti, saf seçim vs Bayesçi büzme (k = 20) ===")
    for k, v in a6().items():
        print(f"  {k}: {v:.3f}")

    print("\n=== A7: havalimanı karar ağı ===")
    for k, v in a7().items():
        if isinstance(v, dict):
            v = ", ".join(f"{y}: {e:.2f}" for y, e in v.items())
        elif isinstance(v, float):
            v = f"{v:.4f}"
        print(f"  {k}: {v}")

    print("\n=== A9: hazine avı ===")
    print(f"  P = {HAZINE_P}, C = {HAZINE_C}")
    for k, (sira, m) in a9().items():
        print(f"  {k:<22} sıra {sira}  beklenen maliyet {m}")

    print("\n=== A10: hata yapan Harriet, u ~ U[−40, 60] ===")
    s = a10()
    for eps, v in s["bekle(ε)"].items():
        print(f"  ε = {eps:.1f}: bekle {v:+.1f}  (hemen yap +10.0)")
    print(f"  Robbie ε < {s['eşik ε']:.3f} olduğu sürece Harriet'e danışır.")


if __name__ == "__main__":
    main()
