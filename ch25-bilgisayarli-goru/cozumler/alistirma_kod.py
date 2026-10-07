#!/usr/bin/env python3
"""Bölüm 25 alıştırmaları: kodlu çözümler (A2, A5, A6, A7, A8, A9, A10).

Çalıştırma (bölüm klasöründen):
    python cozumler/alistirma_kod.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "ornekler"))

import goruntu_olusumu as go  # noqa: E402
import ozellikler as oz  # noqa: E402
import tespit as ts  # noqa: E402


# --- A2: kaybolma noktaları ve ufuk -------------------------------------------------------------
def a2() -> dict:
    sonuc = {}
    for yon in ((0, 0, 1), (1, 0, 1), (-1, 0, 1), (1, 0, 3), (0, 1, 1)):
        sonuc[yon] = go.kaybolma_noktasi(yon)
    yakin = go.perspektif(go.dogru_uzerinde((0, -1.5, 2), (1, 0, 1), 1e6), ters=False)
    return {"kaybolma": sonuc, "λ = 10⁶ için (1, 0, 1) doğrusu": yakin}


# --- A5: düzeltme ölçeği -----------------------------------------------------------------------
def dar_serit(n: int = 100, bas: int = 49, son: int = 51, gurultu: float = 0.05, tohum: int = 0) -> np.ndarray:
    rng = np.random.default_rng(tohum)
    x = np.arange(n)
    return ((x >= bas) & (x < son)).astype(float) + rng.normal(0, gurultu, n)


def a5() -> dict:
    I = oz.basamak()
    serit = dar_serit()
    return {
        "basamak": {s: oz.kenar_1b(I, s) for s in (None, 1, 2, 4)},
        "2 piksellik şerit": {s: oz.kenar_1b(serit, s) for s in (1, 2, 4)},
    }


# --- A6: doku histogramları -------------------------------------------------------------------
def capraz_cizgiler(n: int = 36, periyot: int = 8) -> np.ndarray:
    y, x = np.mgrid[0:n, 0:n]
    return (((x + y) // (periyot // 2)) % 2).astype(float)


def a6() -> dict:
    D = oz.cizgiler()
    return {
        "dikey": oz.yon_histogrami(D),
        "dikey, 90° döndürülmüş": oz.yon_histogrami(np.rot90(D)),
        "çapraz": oz.yon_histogrami(capraz_cizgiler()),
        "benekler": oz.yon_histogrami(oz.benekler()),
        "dikey, 0.3 kat + 0.5": oz.yon_histogrami(0.3 * D + 0.5),
    }


# --- A7: optik akış ve açıklık sorunu --------------------------------------------------------------
def a7() -> dict:
    rng = np.random.default_rng(2)
    doku = rng.random((40, 40))
    bulunan, _ = oz.ssd_akis(doku, oz.kaydir(doku, 2, 1), (20, 20))
    D = oz.cizgiler(40)
    _, tablo = oz.ssd_akis(D, oz.kaydir(D, 0, 3), (20, 20))
    sifir = sorted(k for k, v in tablo.items() if v == 0)
    return {"dokulu (2, 1) kaydırma": bulunan, "dikey çizgiler, SSD = 0 olan adaylar": sifir,
            "çarpışma zamanı (Z = 0.5 m, Tz = 0.25 m/s)": 0.5 / 0.25}


# --- A8: normalleştirilmiş kesme ve tek eşik ----------------------------------------------------------
def a8(tohumlar=range(5)) -> dict:
    sonuc = {}
    for egim in (0.0, 0.4, 0.8):
        ncut, esik = [], []
        for t in tohumlar:
            I, g = oz.iki_bolgeli(egim=egim, tohum=t)
            ncut.append(oz.dogruluk(oz.normallestirilmis_kesme(I), g))
            esik.append(oz.en_iyi_esik(I, g))
        sonuc[egim] = (np.round(ncut, 2).tolist(), np.round(esik, 2).tolist())
    return sonuc


# --- A9: artıyı köşeden ayırmak ------------------------------------------------------------------------
def kol(satir: slice, sutun: slice) -> np.ndarray:
    K = np.zeros((5, 5))
    K[satir, sutun] = 1
    return K


def arti_katmani(H: np.ndarray, V: np.ndarray, sapma: float = 32.0) -> np.ndarray:
    """Üçüncü katman: Merkezin solunda VE sağında yatay, üstünde VE altında dikey yanıt ister.
    Artıda dört kol da dolu (toplam 40); köşede ya da tek çubukta yalnızca iki kol (24). Sapma 32 ayırır."""
    sol, sag = kol(slice(2, 3), slice(0, 2)), kol(slice(2, 3), slice(3, 5))
    ust, alt = kol(slice(0, 2), slice(2, 3)), kol(slice(3, 5), slice(2, 3))
    toplam = ts.konv2(H, sol) + ts.konv2(H, sag) + ts.konv2(V, ust) + ts.konv2(V, alt)
    return ts.relu(toplam - sapma)


def a9() -> dict:
    sonuc = {"alıcı alanlar": [ts.alici_alan(L) for L in range(1, 6)]}
    for ad, I in ts.sekiller().items():
        k1 = ts.birinci_katman(I)
        sonuc[ad] = (float(ts.bulusma_katmani(k1["yatay"], k1["dikey"]).max()),
                     float(arti_katmani(k1["yatay"], k1["dikey"]).max()))
    return sonuc


# --- A10: IoU, NMS, kesinlik/duyarlılık ---------------------------------------------------------------
def a10() -> dict:
    A, B = (0, 0, 4, 4), (2, 2, 6, 6)
    kutular = [(0, 0, 10, 10), (1, 1, 11, 11), (20, 20, 30, 30), (21, 19, 31, 29), (50, 50, 60, 60)]
    puanlar = [0.95, 0.9, 0.8, 0.85, 0.4]
    gercek = [(0, 0, 10, 10), (20, 20, 30, 30), (70, 70, 80, 80)]
    kabul = nms(kutular, puanlar)
    return {
        "IoU(A, B)": ts.iou(A, B),
        "NMS kabul": kabul,
        "kesinlik, duyarlılık": ts.degerlendir([kutular[i] for i in kabul], gercek),
        "kesinlik, duyarlılık (puan > 0.5)": ts.degerlendir([kutular[i] for i in nms(kutular, puanlar, en_az=0.5)], gercek),
        "200 × 200 dikdörtgen sayısı": ts.dikdortgen_sayisi(200),
        "1280 × 720 çapa kutusu": ts.capa_kutusu_sayisi(1280, 720),
    }


def nms(kutular, puanlar, en_az: float = 0.0):
    return ts.nms(kutular, puanlar, esik=0.5, en_az=en_az)


def main() -> None:
    print("=== A2: kaybolma noktaları (f = 1) ===")
    r = a2()
    for yon, p in r["kaybolma"].items():
        print(f"  yön {yon}: {p}")
    print(f"  (1, 0, 1) doğrusunda çok uzak bir nokta: {tuple(round(v, 4) for v in r['λ = 10⁶ için (1, 0, 1) doğrusu'])}")

    print("\n=== A5: düzeltme ölçeği ===")
    for ad, d in a5().items():
        for s, p in d.items():
            print(f"  {ad:<17} σ = {str(s):<4}: tepeler {p}")

    print("\n=== A6: yön histogramları (0°, 45°, …, 315°) ===")
    for ad, h in a6().items():
        print(f"  {ad:<24}: {np.round(h, 2)}")

    print("\n=== A7: optik akış ===")
    for k, v in a7().items():
        print(f"  {k}: {v}")

    print("\n=== A8: Ncut ve en iyi tek eşik (5 tohum) ===")
    for egim, (n, e) in a8().items():
        print(f"  eğim {egim}: Ncut {n}  |  tek eşik {e}")

    print("\n=== A9: desenlerin deseni ===")
    for k, v in a9().items():
        print(f"  {k}: {v}")

    print("\n=== A10: tespit ===")
    for k, v in a10().items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
