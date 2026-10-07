#!/usr/bin/env python3
"""Bölüm 26 alıştırmaları: kodlu çözümler (A3, A4, A5, A7, A8, A9, A10).

Çalıştırma (bölüm klasöründen):
    python cozumler/alistirma_kod.py
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "ornekler"))

import insan_robot as ir  # noqa: E402
import kontrol as kn  # noqa: E402
import lokalizasyon as lk  # noqa: E402
import planlama as pl  # noqa: E402


# --- A3: MCL'de parçacık sayısı ve tepe kaybı ----------------------------------------------------------
def a3(tohumlar=range(8)) -> dict:
    sonuc = {}
    for N, koridor in ((1000, True), (5000, True), (5000, False)):
        iki_tepe, dogru = 0, 0
        for t in tohumlar:
            s = lk.mcl_deneyi(N=N, tohum=t, koridor_yonu=koridor)
            g8, a8 = s[8][1], s[8][2]
            iki_tepe += (g8 > 0.05 and a8 > 0.05)
            dogru += s[-1][1] > 0.5
        sonuc[(N, "θ ∈ {0, π}" if koridor else "θ düzgün")] = (iki_tepe, dogru, len(tohumlar))
    return sonuc


# --- A4: EKF ve doğrusallaştırma --------------------------------------------------------------------
def a4() -> dict:
    gorunur = [round(s, 3) for _, _, s in lk.ekf_deneyi()]
    hic = [round(s, 3) for _, _, s in lk.ekf_deneyi(gorus=0.0)]
    dogrusal = {s: lk.dogrusallastirma(sigma=s) for s in (0.1, 0.5, 1.0)}
    return {"işaretle": gorunur, "işaretsiz": hic, "doğrusallaştırma": dogrusal}


# --- A5: C-uzayı -------------------------------------------------------------------------------------------
def a5() -> dict:
    kare = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
    K_ucgen = pl.c_engeli()
    K_kare = pl.c_engeli(kare)
    return {"üçgen C_obs": K_ucgen, "üçgen alan": pl.cokgen_alani(K_ucgen),
            "kare C_obs": K_kare, "kare alan": pl.cokgen_alani(K_kare)}


# --- A7: planlayıcıları karşılaştır ---------------------------------------------------------------------
def izgara_planlayici(cozunurluk: float = 0.25):
    """Düzenli ızgara hücre ayrıştırması: yalnızca tamamen serbest hücreler; 8 komşulu Dijkstra."""
    nx, ny = int(pl.DUNYA[0] / cozunurluk), int(pl.DUNYA[1] / cozunurluk)
    C = np.zeros((nx, ny), dtype=bool)
    for i in range(nx):
        for j in range(ny):
            x1, y1 = i * cozunurluk, j * cozunurluk
            kose = [(x1 + a * cozunurluk, y1 + b * cozunurluk) for a in (0, 0.5, 1) for b in (0, 0.5, 1)]
            C[i, j] = not all(pl.serbest_nokta(k) for k in kose)
    hucre = lambda p: (min(int(p[0] / cozunurluk), nx - 1), min(int(p[1] / cozunurluk), ny - 1))  # noqa: E731
    V, yol = pl.izgara_en_kisa(C, hucre(pl.BASLA), hucre(pl.HEDEF))
    merkez = [((i + 0.5) * cozunurluk, (j + 0.5) * cozunurluk) for i, j in yol]
    return [pl.BASLA] + merkez + [pl.HEDEF]


def a7() -> dict:
    _, en_iyi = pl.gorunurluk_cizgesi()
    izgara = izgara_planlayici()
    prm = [pl.prm(30, tohum=t)[1] for t in range(10)]
    rrt = [pl.rrt_cift_yonlu(tohum=t) for t in range(10)]
    return {
        "görünürlük çizgesi": en_iyi,
        "ızgara (0.25 m)": pl.yol_uzunlugu(izgara),
        "ızgara + kısaltma": pl.yol_uzunlugu(pl.kisalt(izgara, deneme=500)),
        "k-PRM ort.": float(np.mean(prm)),
        "RRT ort.": float(np.mean([pl.yol_uzunlugu(r) for r in rrt])),
        "RRT + kısaltma ort.": float(np.mean([pl.yol_uzunlugu(pl.kisalt(r, tohum=t)) for t, r in enumerate(rrt)])),
    }


# --- A8: yörünge optimizasyonu ---------------------------------------------------------------------------
def a8() -> dict:
    sonuc = {}
    for lam in (20, 200, 1000, 3000):
        T = pl.yorunge_optimizasyonu(lam=lam)
        sonuc[f"λ = {lam}"] = (round(pl.en_kucuk_aciklik(T), 2), round(pl.yol_uzunlugu(T), 2))
    ust = np.linspace((0, 0), (10, 0), 51)
    ust[1:-1, 1] = 3 * np.sin(np.linspace(0, np.pi, 51))[1:-1]          # iki engelin de üstünden başlat
    T = pl.yorunge_optimizasyonu(baslangic=ust)
    sonuc["üstten başlangıç"] = (round(pl.en_kucuk_aciklik(T), 2), round(pl.yol_uzunlugu(T), 2))
    return sonuc


# --- A9: denetçi kazançları ve LQR ------------------------------------------------------------------------
def oturma_suresi(t, Q, hedef: float = 1.0, bant: float = 0.02) -> float:
    disarida = np.nonzero(np.abs(Q - hedef) > bant)[0]
    return float(t[disarida[-1]]) if len(disarida) else 0.0


def a9() -> dict:
    sonuc = {}
    for KD in (0.1, 0.8, 3.0):
        t, Q = kn.benzet(0.3, KD)
        sonuc[f"K_P = 0.3, K_D = {KD}"] = (round(kn.ozet(t, Q)["aşım"], 3), round(oturma_suresi(t, Q), 1))
    for R in (0.1, 1.0, 10.0):
        K = kn.lqr_ayrik(*kn.cift_integrator(0.01), np.diag([1.0, 0.0]), np.array([[R]]))
        sonuc[f"LQR R = {R}"] = tuple(round(float(k), 2) for k in K.ravel())
    return sonuc


# --- A10: insan modeli ve gürültülü gösterimler -----------------------------------------------------------
def a10() -> dict:
    sonuc = {}
    for beta in (0.1, 1.0, 5.0):
        b = ir.amac_cikarimi(beta=beta)[2]
        sonuc[f"β = {beta}, 2 adım sonra P(pencere)"] = round(b["pencere"], 3)
    rng = np.random.default_rng(0)
    gosterim = []
    for _ in range(5):                                   # uzman gürültülü bir ortamda sürüyor
        durumlar, _ = ir.surus(ir.uzman, 50, rng, gurultu=0.05)
        gosterim.extend(durumlar)
    Y = np.array(gosterim)
    pi, (a, b) = ir.dogrusal_politika(Y, ir.uzman(Y))
    sonuc["gürültülü gösterimden klonlama"] = (round(a, 2), round(b, 2), ir.cikma_orani(pi, rng))
    return sonuc


def main() -> None:
    print("=== A3: MCL, 8 tohum ===")
    for (N, onsel), (iki, dogru, n) in a3().items():
        print(f"  N = {N}, {onsel}: 8. adımda iki tepe de yaşıyor {iki}/{n}, sonda doğru konum {dogru}/{n}")

    print("\n=== A4: EKF ===")
    r = a4()
    print(f"  işaretle  : {r['işaretle']}")
    print(f"  işaretsiz : {r['işaretsiz']}")
    for s, d in r["doğrusallaştırma"].items():
        print(f"  σ = {s}: " + ", ".join(f"{k} {v:.3f}" for k, v in d.items()))

    print("\n=== A5: C-uzayı engelleri ===")
    for k, v in a5().items():
        print(f"  {k}: {v}")

    print("\n=== A7: yol uzunlukları ===")
    for k, v in a7().items():
        print(f"  {k:<22}: {v:.2f}")

    print("\n=== A8: yörünge optimizasyonu (en küçük uzaklık, uzunluk) ===")
    for k, v in a8().items():
        print(f"  {k:<17}: {v}")

    print("\n=== A9: kazançlar (aşım, %2 bandına oturma süresi) ve LQR K ===")
    for k, v in a9().items():
        print(f"  {k:<22}: {v}")

    print("\n=== A10 ===")
    for k, v in a10().items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
