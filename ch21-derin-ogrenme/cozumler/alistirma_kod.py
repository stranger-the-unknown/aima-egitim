#!/usr/bin/env python3
"""Bölüm 21 alıştırmaları: kodlu çözümler (A2–A10).

Çalıştırma (bölüm klasöründen):
    python cozumler/alistirma_kod.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "ornekler"))

import cnn  # noqa: E402
import hesap_grafigi as hg  # noqa: E402
import mlp_egitim as me  # noqa: E402
import otokodlayici as ok  # noqa: E402

A2_AGIRLIK = {"w03": 0.0, "w13": 1.0, "w23": 1.0, "w04": 0.0, "w14": -1.0, "w24": 1.0,
              "w05": 0.0, "w35": 1.0, "w45": 1.0}


# --- A2: Şekil 21.3'ü elle --------------------------------------------------------------
def a2() -> dict:
    a = hg.ileri(A2_AGIRLIK, 1.0, 1.0)
    g = hg.geri_yayilim(A2_AGIRLIK, 1.0, 1.0, 1.0)
    return {**{k: float(v) for k, v in a.items()}, "∂L/∂w35": g["w35"], "∂L/∂w13": g["w13"]}


# --- A3: softmax özellikleri ------------------------------------------------------------
def a3() -> dict:
    z = np.array([5.0, 2.0, 0.0, -2.0])
    return {"softmax": hg.softmax(z), "sabit eklenince": hg.softmax(z + 100),
            "T = 0.5": hg.softmax(z / 0.5), "T = 5": hg.softmax(z / 5)}


# --- A4: evrişim ve alıcı alan ---------------------------------------------------------------
def a4() -> dict:
    x, k = [5, 6, 6, 2, 5, 6, 5], [1, -1, 1]
    return {"adım 1, dolgu yok": cnn.evrisim_1b(x, k, 1), "adım 1, dolgu 1": cnn.evrisim_1b(x, k, 1, 1),
            "alıcı alanlar": [cnn.alici_alan(n, 3, 1) for n in (1, 2, 3, 4)]}


# --- A5: çıktı boyutu ve parametre sayısı -----------------------------------------------------
def cikti_boyutu(n: int, l: int, s: int, p: int) -> int:
    return (n + 2 * p - l) // s + 1


def a5() -> dict:
    return {"224, l=7, s=2, p=3": cikti_boyutu(224, 7, 2, 3), "32, l=5, s=1, p=0": cikti_boyutu(32, 5, 1, 0),
            "32, l=3, s=1, p=1": cikti_boyutu(32, 3, 1, 1),
            "parametreler (32×32×3 → 32×32×16, 3×3)": (32 * 32 * 3 * 32 * 32 * 16, 3 * 3 * 3 * 16 + 16)}


# --- A6: sigmoid ve ReLU derinlikte -----------------------------------------------------------------
def gradyan_normu(derinlik: int, akt: str, genislik: int = 64, tohum: int = 0) -> float:
    """Rastgele girdide, her katmanda tam bağlı + aktivasyon; ilk katmana geri yayılan gradyanın normu.
    ReLU için He (√(2/n)), sigmoid için Xavier (√(1/n)) başlangıcı."""
    rng = np.random.default_rng(tohum)
    olcek = np.sqrt(2 / genislik) if akt == "relu" else np.sqrt(1 / genislik)
    W = [rng.normal(0, olcek, (genislik, genislik)) for _ in range(derinlik)]
    a, turevler = rng.normal(size=genislik), []
    for Wi in W:
        z = a @ Wi
        if akt == "relu":
            a, d = np.maximum(0, z), (z > 0).astype(float)
        else:
            a = 1 / (1 + np.exp(-z))
            d = a * (1 - a)
        turevler.append(d)
    g = np.ones(genislik)
    for Wi, d in zip(reversed(W), reversed(turevler)):
        g = (g * d) @ Wi.T
    return float(np.linalg.norm(g))


def a6() -> dict:
    return {n: (gradyan_normu(n, "sigmoid"), gradyan_normu(n, "relu")) for n in (2, 10, 20, 50)}


# --- A7: iki gizli birimle XOR ------------------------------------------------------------------------
def a7() -> dict:
    """Basamak aktivasyonlu ağ: h1 = [x1 + x2 ≥ 0.5] (VEYA), h2 = [x1 + x2 ≥ 1.5] (VE), y = [h1 − h2 ≥ 0.5]."""
    basamak = lambda z: (z >= 0).astype(int)
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    h1 = basamak(X @ np.array([1, 1]) - 0.5)
    h2 = basamak(X @ np.array([1, 1]) - 1.5)
    y = basamak(h1 - h2 - 0.5)
    return {"girdi": X.tolist(), "h1 (VEYA)": h1.tolist(), "h2 (VE)": h2.tolist(), "çıktı": y.tolist()}


# --- A8: dropout'ta beklenen değer ----------------------------------------------------------------------
def a8(p: float = 0.5, deneme: int = 200_000, tohum: int = 0) -> dict:
    rng = np.random.default_rng(tohum)
    h = np.array([0.3, 1.2, 2.0])
    maske = (rng.random((deneme, 3)) < p) / p             # ters ölçeklemeli dropout
    return {"ortalama çıktı": (h * maske).mean(axis=0), "gerçek": h, "alt ağ sayısı (n = 100)": 2 ** 100}


# --- A9: toplu normalleştirme ölçeğe duyarsızdır --------------------------------------------------------
def a9(tohum: int = 0) -> dict:
    rng = np.random.default_rng(tohum)
    X = rng.normal(size=(32, 5))
    W = rng.normal(size=(5, 4))
    once = me.toplu_normallestir(X @ W)
    sonra = me.toplu_normallestir(X @ (10 * W))
    return {"aynı mı": bool(np.allclose(once, sonra, atol=1e-4)), "en büyük fark": float(np.abs(once - sonra).max())}


# --- A10: otokodlayıcının hatası = atılan özdeğerlerin toplamı ------------------------------------------------
def a10(tohum: int = 0) -> dict:
    rng = np.random.default_rng(tohum)
    W_gercek = rng.normal(size=(10, 2)) * np.array([3.0, 1.5])
    X = ok.ppca_ornekle(1000, W_gercek, 0.3, rng)
    deger, _ = ok.pca(X, 10)
    N = len(X)
    sonuc = {}
    for m in (1, 2, 3):
        W = ok.dogrusal_otokodlayici(X, m, adim=4000)
        sonuc[m] = (ok.yeniden_kurma_hatasi(X, W.T), float(deger[m:].sum()) * (N - 1) / N)
    return sonuc


def main() -> None:
    print("=== A2: Şekil 21.3, x = (1, 1), y = 1 ===")
    for k, v in a2().items():
        print(f"  {k}: {v:.4f}")

    print("\n=== A3: softmax ===")
    for k, v in a3().items():
        print(f"  {k}: {np.round(v, 4)}")

    print("\n=== A4: evrişim ===")
    for k, v in a4().items():
        print(f"  {k}: {np.asarray(v).astype(int).tolist()}")

    print("\n=== A5: çıktı boyutu ⌊(n + 2p − l)/s⌋ + 1 ve parametreler ===")
    for k, v in a5().items():
        print(f"  {k}: {v}")

    print("\n=== A6: ilk katmana ulaşan gradyanın normu ===")
    for n, (s, r) in a6().items():
        print(f"  {n:>2} katman: sigmoid {s:.2e}, ReLU {r:.2e}")

    print("\n=== A7: XOR, iki gizli birim ===")
    for k, v in a7().items():
        print(f"  {k}: {v}")

    print("\n=== A8: ters ölçeklemeli dropout ===")
    s = a8()
    print(f"  ortalama çıktı {np.round(s['ortalama çıktı'], 3)}, gerçek {s['gerçek']}; 100 birimde 2^100 ≈ {float(s['alt ağ sayısı (n = 100)']):.2e} alt ağ")

    print("\n=== A9: toplu normalleştirme ===")
    print(f"  ağırlıklar 10 ile çarpılınca çıktı aynı mı? {a9()['aynı mı']} (fark {a9()['en büyük fark']:.1e})")

    print("\n=== A10: doğrusal otokodlayıcının hatası ve atılan özdeğerler ===")
    for m, (h, d) in a10().items():
        print(f"  m = {m}: yeniden kurma hatası {h:.3f}, atılan özdeğerlerin toplamı {d:.3f}")


if __name__ == "__main__":
    main()
